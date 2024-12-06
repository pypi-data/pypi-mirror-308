from enum import Enum


class BaseEnum(str, Enum):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __str__(self):
        return self.value

class WorkRequestStatus(BaseEnum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'


class TaskType(BaseEnum):
    CODING = 'CODING'
    LABELING = 'LABELING'
    DESIGN = 'DESIGN'


