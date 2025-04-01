from src import source_repository, destination_repository, services
from src.utils.logs import default_module_logger
from src.utils.gcp_clients import create_bigquery_client, create_storage_client

logger = default_module_logger(__file__)


def function_entry_point(event, context):
    """
    Entry point function for ingesting ECB exchange rates into raw layer of the DW in BigQuery.
    This function initializes a BigQueryRepository and an EcbApiCaller, then calls a service to fetch and load ECB
    rates into BigQuery.

    Args:
         event: The dictionary with data specific to this type of event. The `@type` field maps to
                `type.googleapis.com/google.pubsub.v1.PubsubMessage`. The `data` field maps to the PubsubMessage data
                in a base64-encoded string. The `attributes` field maps to the PubsubMessage attributes
                if any is present.
         context: Metadata of triggering event including `event_id` which maps to the PubsubMessage
                  messageId, `timestamp` which maps to the PubsubMessage publishTime, `event_type` which maps to
                  `google.pubsub.topic.publish`, and `resource` which is a dictionary that describes the service
                  API endpoint pubsub.googleapis.com, the triggering topic's name, and the triggering event type
                  `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    Returns:
        None
    """
    bucket_name = event["bucket"]
    file_path = event["name"]
    logger.info(f"Working on file: '{file_path}' found on Bucket: '{bucket_name}'")
    file = source_repository.GcpBucketFileSource(
        file_path, bucket_name, create_storage_client()
    )
    bigquery = destination_repository.BiqQueryDestinationRepository(
        bigquery_client=create_bigquery_client()
    )

    services.asset_valuation_pipeline(file, bigquery)
