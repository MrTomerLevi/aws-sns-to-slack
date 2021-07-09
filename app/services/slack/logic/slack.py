import json
import os

import requests
from aws_lambda_powertools import Logger, Tracer
from requests import Response

from model import CloudWatchAlarmState, CloudWatchAlarmEvent

logger = Logger()
tracer = Tracer()

SLACK_HOOK_URL = os.environ['SLACK_HOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

state_data = {
    CloudWatchAlarmState.OK: {
        'icon': ':beer:',
        'color': 'good'
    },
    CloudWatchAlarmState.INSUFFICIENT_DATA: {
        'color': 'warning',
        'icon': ':interrobang:'
    },
    CloudWatchAlarmState.ALARM: {
        'color': 'danger',
        'icon': ':fire:'
    }
}


@tracer.capture_method
def send(alarm_event: CloudWatchAlarmEvent) -> Response:
    state_info = state_data[alarm_event.new_state_value]

    attachments = [{
        'fallback': alarm_event.message,
        'message': alarm_event.message,
        'color': state_info['color'],
        "fields": [{
            "title": "Alarm",
            "value": alarm_event.alarm_name,
            "short": True
        }, {
            "title": "Status",
            "value": alarm_event.new_state_value.value,
            "short": True
        }, {
            "title": "Reason",
            "value": alarm_event.new_state_reason,
            "short": False
        }]
    }]

    slack_message = dict(channel=SLACK_CHANNEL,
                         username='AWS Monitoring',
                         icon_emoji=state_info['icon'],
                         text=alarm_event.message + "\n<!here>",
                         attachments=attachments)

    response = requests.post(SLACK_HOOK_URL, data=json.dumps(slack_message))
    status_code = response.status_code
    logger.debug(f"Response from Slack to channel: {slack_message['channel']} "
                 f"is: {str(status_code)} response: {str(response.raw)}")
    return response
