from dataclasses import dataclass
from enum import Enum


class CloudWatchAlarmState(Enum):
    OK = 'OK'
    ALARM = 'ALARM'
    INSUFFICIENT_DATA = 'INSUFFICIENT_DATA'


@dataclass
class CloudWatchAlarmEvent:
    new_state_value: CloudWatchAlarmState
    message: str
    alarm_name: str
    new_state_reason: str
