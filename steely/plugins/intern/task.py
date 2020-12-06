import datetime

from enum import IntEnum, unique

@unique
class TaskType(IntEnum):
    # Likelier if focus is low.
    DOSSING = 1
    # Likelier if focus is high.
    STUDYING = 2
    # Likelier if focus is high. More intelligence = better at INVESTING.
    INVESTING = 3


class Task:
    start_time: datetime.datetime
    end_time: datetime.datetime
    type_: TaskType

    @staticmethod
    def encode_datetime(obj: datetime.datetime) -> str:
        return obj.strftime('%Y-%m-%d-%H-%M-%S-%z')

    @staticmethod
    def decode_datetime(s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, '%Y-%m-%d-%H-%M-%S-%z')

    @staticmethod
    def serialize(task):
        d = {
            'start_time': Task.encode_datetime(task.start_time),
            'end_time': Task.encode_datetime(task.end_time),
            'type': int(task.type_)
        }
        return d

    @staticmethod
    def deserialize(obj):
        t = Task()
        t.start_time = Task.decode_datetime(obj['start_time'])
        t.end_time = Task.decode_datetime(obj['end_time'])
        t.type_ = TaskType(obj['type'])
        return t

