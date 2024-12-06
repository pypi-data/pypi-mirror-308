import json
from datetime import datetime

from confluent_kafka import (
    OFFSET_INVALID,
    Consumer,
    IsolationLevel,
    KafkaException,
    TopicPartition,
)
from confluent_kafka.admin import AdminClient, OffsetSpec
from tabulate import tabulate


class KafkaConsumer:
    def __init__(self, config_file, topic, group_id, auto_offset="earliest"):
        # Load Kafka configuration from a JSON file
        with open(config_file, "r") as file:
            self.config = json.load(file)

        if not self.config.get("bootstrap.servers") or not isinstance(
            self.config["bootstrap.servers"], str
        ):
            raise ValueError(
                "Configuration error: 'bootstrap.servers' must be defined as a non-empty string with brokers separated by commas."
            )

        self.admin_client = AdminClient(self.config)
        # Set the group ID in the configuration
        self.config["group.id"] = group_id
        self.config["auto.offset.reset"] = auto_offset

        # Initialize the Kafka consumer
        self.consumer = Consumer(self.config)
        self.topic = topic
        self.display_partition_offsets_and_lag()

    def display_partition_offsets_and_lag(self):
        topic = self.topic
        metadata = self.consumer.list_topics(topic, timeout=10)
        if metadata.topics[topic].error is not None:
            raise KafkaException(metadata.topics[topic].error)

        # Construct TopicPartition list of partitions to query
        partitions = [
            TopicPartition(topic, p) for p in metadata.topics[topic].partitions
        ]

        topic_partition_offsets = {}
        for each_partitions in partitions:
            topic_partition_offsets[each_partitions] = OffsetSpec.max_timestamp()

        futmap = self.admin_client.list_offsets(
            topic_partition_offsets,
            isolation_level=IsolationLevel.READ_COMMITTED,
            request_timeout=30,
        )

        topic_latest_offset = {}
        for partition, fut in futmap.items():
            try:
                result = fut.result()
                human_readable_timestamp = (
                    datetime.fromtimestamp(result.timestamp / 1000).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if result.timestamp != -1
                    else "N/A"
                )
                topic_latest_offset[partition.partition] = [
                    result.offset + 1,
                    human_readable_timestamp,
                ]
            except KafkaException as e:
                print(
                    f"Error retrieving offsets for {partition.topic} partition {partition.partition}: {e}"
                )

        # Query committed offsets for this group and the given partitions
        committed = self.consumer.committed(partitions, timeout=10)

        table_data = []
        for partition in committed:
            # Get the partitions low and high watermark offsets.
            (lo, hi) = self.consumer.get_watermark_offsets(
                partition, timeout=10, cached=False
            )

            if partition.offset == OFFSET_INVALID:
                offset = "-"
            else:
                offset = "%d" % (partition.offset)

            if hi < 0:
                lag = "no hwmark"  # Unlikely
            elif partition.offset < 0:
                # No committed offset, show total message count as lag.
                # The actual message count may be lower due to compaction
                # and record deletions.
                lag = "%d" % (hi - lo)
            else:
                lag = "%d" % (hi - partition.offset)

            table_data.append(
                [
                    partition.topic,
                    partition.partition,
                    offset,
                    lag,
                    topic_latest_offset[partition.partition][0],
                    topic_latest_offset[partition.partition][1],
                ]
            )

        print(
            tabulate(
                table_data,
                headers=[
                    "Topic",
                    "Partition",
                    "Consumer Offset",
                    "Lag",
                    "Topic Offset",
                    "Timestamp",
                ],
                tablefmt="grid",
            )
        )

    def get_partitions(self):
        # Get metadata for the topic to retrieve partition information
        metadata = self.consumer.list_topics(self.topic)
        return list(metadata.topics[self.topic].partitions.keys())

    def start_consuming_message(self, timeout=1.0):
        print("\nStarting to consume messages...")
        try:
            while True:
                msg = self.consumer.poll(timeout)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        print(f"Reached end of partition {msg.partition()}")
                    else:
                        print(f"Error: {msg.error()}")
                    continue

                # Display message details
                _, timestamp = msg.timestamp()
                human_readable_timestamp = datetime.fromtimestamp(
                    timestamp / 1000
                ).strftime("%Y-%m-%d %H:%M:%S")
                print(f"Received message: {msg.value().decode('utf-8')}")
                print(
                    f"Topic: {msg.topic()}, Partition: {msg.partition()}, Offset: {msg.offset()}, Timestamp: {human_readable_timestamp}"
                )

        except KeyboardInterrupt:
            print("Stopped consuming.")
            self.display_partition_offsets_and_lag()
        finally:
            # Close the consumer to release resources
            self.consumer.close()

    def consume_messages(self, timeout=1.0):
        # Subscribe to the specified topic
        self.consumer.subscribe([self.topic])
        self.start_consuming_message(timeout)

    def consume_from_offset(self, offset, partition=None, timeout=1.0):
        # Assign a specific partition and offset to start consuming from
        if partition is not None:
            # Assign a specific partition and offset
            tp = TopicPartition(self.topic, partition, offset)
            self.consumer.assign([tp])
            print(
                f"Starting to consume messages from {self.topic} partition: [{partition}] at offset: {offset}..."
            )
        else:
            # Assign all partitions with the specified offset
            tp_list = [
                TopicPartition(self.topic, p, offset) for p in self.get_partitions()
            ]
            self.consumer.assign(tp_list)
            print(
                f"Starting to consume messages from {self.topic} across all partitions at offset {offset}..."
            )
        self.start_consuming_message(timeout)

    def consume_from_timestamp(self, timestamp, partition=None, timeout=1.0):
        print(f"Consume messages from the specified timestamp {timestamp}...\n")
        # Convert string to datetime object
        from_timestamp = None
        try:
            # Try to parse the date string with the expected format
            from_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            # Raise an error if the format does not match
            raise ValueError(
                "Date string does not match the format '%Y-%m-%dT%H:%M:%S.%fZ'"
            )

        # Convert timestamp to milliseconds for Kafka
        timestamp_ms = int(from_timestamp.timestamp() * 1000)

        # # Get metadata for partitions
        if partition is not None:
            # Assign a specific partition and offset
            partitions = [TopicPartition(self.topic, partition)]
        else:
            partitions = [TopicPartition(self.topic, p) for p in self.get_partitions()]

        # Create OffsetSpec based on the provided timestamp
        topic_partition_offsets = {
            partition: OffsetSpec(timestamp_ms) for partition in partitions
        }

        # Retrieve the offsets corresponding to the timestamp
        futmap = self.admin_client.list_offsets(
            topic_partition_offsets, isolation_level=IsolationLevel.READ_COMMITTED
        )
        assigned_partitions = []

        print("*" * 200)
        for partition, fut in futmap.items():
            try:
                result = fut.result()
                # Assign the consumer to the retrieved offset
                if result.offset != OFFSET_INVALID:
                    tp = TopicPartition(
                        partition.topic, partition.partition, result.offset
                    )
                    assigned_partitions.append(tp)
                    print(
                        f"Assigned to {partition.topic} partition: [{partition.partition}] starting at offset: {result.offset} with timestamp: {datetime.fromtimestamp(result.timestamp / 1000)}"
                    )
                else:
                    print(
                        f"No messages found for {partition.topic} partition: [{partition.partition}] at the given timestamp."
                    )
            except KafkaException as e:
                print(
                    f"Error retrieving offsets for {partition.topic} partition {partition.partition}: {e}"
                )
        print("*" * 200)
        # Assign the consumer to start consuming from the calculated offsets
        self.consumer.assign(assigned_partitions)
        self.start_consuming_message(timeout)


# Usage example
if __name__ == "__main__":
    # Initialize consumer with the configuration file, topic name, and group ID
    config_file = "config.json"
    topic = "topic-1"
    group_id = "group-1"

    auto_offset = "earliest"  # Start from the beginning if no previous offset exists
    consumer = KafkaConsumer(config_file, topic, group_id, auto_offset)

    # Press enter to start the consuming message
    input("Press Enter to start consuming messages...")
    # Start consuming messages
    consumer.consume_messages()
    # consumer.consume_from_offset(partition=1, offset=2350)
