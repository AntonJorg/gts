"""

"""
from typing import Protocol
from enum import Enum


class State[ActionType](Protocol):
    utility: float
    applicable_actions: list[ActionType]
    is_terminal: bool
    players: Enum

    def result(self, action: ActionType) -> "State[ActionType]":
        ...
