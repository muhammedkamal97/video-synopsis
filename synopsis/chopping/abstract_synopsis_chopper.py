from abc import ABC, abstractmethod

from object.activity.activity_aggreagator import ActivityAggregator


class AbstractSynopsisChopper(ABC):
    # TODO: add return type hints for methods

    @abstractmethod
    def to_chop(self, activity_aggregator: ActivityAggregator) -> bool:
        pass
