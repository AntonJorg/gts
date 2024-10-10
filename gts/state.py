"""

"""
from typing import Protocol


class State[ActionType](Protocol):
    utility: float
    applicable_actions: list[ActionType]
    is_terminal: bool

    def result(self, action: ActionType) -> "State[ActionType]":
        ...
