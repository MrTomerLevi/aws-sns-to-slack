from typing import Dict

from model import CloudWatchAlarmEvent, CloudWatchAlarmState


def parse_alarm(event_body: Dict) -> CloudWatchAlarmEvent:
    message = get_alarm_message(event_body)
    state = CloudWatchAlarmState[event_body['NewStateValue']]
    return CloudWatchAlarmEvent(new_state_value=state,
                                message=message,
                                alarm_name=event_body['AlarmName'],
                                new_state_reason=event_body['NewStateReason'])


def get_alarm_message(event_body):
    alarm_name = event_body['AlarmName']
    alarm_description = event_body.get('AlarmDescription', '')
    return "Incident - {}\n {}\n".format(alarm_name, alarm_description)