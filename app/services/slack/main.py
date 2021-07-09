"""
This lambda requires 2 environment variables:
    1. SLACK_HOOK_URL - example: https://hooks.slack.com/services/T0G7N0L18/B1J49EPCV/4fTwvHvtlRiRx8q8VV9m
    2. SLACK_CHANNEL  - example: #alerts

Follow these steps to create a webhook in Slack:
    1. Navigate to https://<your-team-domain>.slack.com/services/new
    2. Search for and select "Incoming WebHooks".
    3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".
    4. Copy the webhook URL from the setup instructions and use it in the next section.
"""

import json

from aws_lambda_powertools.utilities.typing import LambdaContext
from requests import Response
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import event_source, SNSEvent

from model import CloudWatchAlarmEvent
from logic import cloudwatch, slack

tracer = Tracer()
logger = Logger()


@tracer.capture_lambda_handler
@event_source(data_class=SNSEvent)
def lambda_handler(event: SNSEvent, context: LambdaContext):

    for record in event.records:
        subject = record.sns.subject
        message = record.sns.message

        event_body = message
        # CloudWatch alarms are represented as a json string
        if is_json(message):
            event_body = json.loads(message)

        if 'AlarmName' in event_body:
            event: CloudWatchAlarmEvent = cloudwatch.parse_alarm(event_body=event_body)
            slack_response: Response = slack.send(alarm_event=event)
            logger.info(f"CloudWatch alarm event, new state value: {event.new_state_value} sent to slack. "
                        f"Status: {slack_response.status_code}")
            slack_response.raise_for_status()
        else:
            logger.error(f"Unsupported subject: {subject}")


def is_json(string):
    try:
        json.loads(string)
    except ValueError:
        return False
    return True
