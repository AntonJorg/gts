import time

from dataclasses import dataclass
from typing import Callable

from gts.node import Node, get_children, get_parent, single_expand, set_values
from gts.state import State


type SearchFunction[T] = Callable[[State[T]], T]

type NodeValue = dict[str, float]

type Frontier[T] = list[Node[T]]
type ShouldTerminateFunction[T] = Callable[[Node[T], Frontier[T]], bool]
type ShouldEvaluateFunction = Callable[[], bool]
type EvaluateFunction[T] = Callable[[Node[T]], NodeValue]
type ActionValueFunction[T] = Callable[[Node[T]], NodeValue]

type UseFrontierFunction = Callable[[], bool]
type ShouldSelectFunction[T] = Callable[[Node[T]], bool]
type SelectFunction[T] = Callable[[list[Node[T]]], Node[T]]

type BackdownFunction[T] = Callable[[Node[T]], NodeValue]

type ShouldBackupFunction[T] = Callable[[Node[T]], bool]
type BackupFunction[T] = Callable[[Node[T], Node[T], list[Node[T]]], NodeValue]


class _SearchTimer:
    def __init__(self):
        self.timeout = 0.0
        self.start_time = 0

    def start(self, timeout: float) -> None:
        self.timeout = timeout
        self.start_time = time.thread_time_ns()

    def is_timeout(self) -> bool:
        return time.thread_time_ns() - self.start_time > self.timeout * 1e9

search_timer = _SearchTimer()


@dataclass
class SearchFunctionDefinition[T]:
    # main algorithm
    frontier: Frontier[T]
    should_terminate: Callable[[Node[T], Frontier[T]], bool]
    should_evaluate: Callable[[], bool]
    evaluate: EvaluateFunction
    action_value: Callable[[Node[T]], NodeValue]
    # selection step
    use_frontier: Callable[[Node[T]], bool]
    should_select: Callable[[Node[T]], bool]
    select: SelectFunction
    # expansion step
    backdown: BackdownFunction
    # backpropagation step
    should_backup: Callable[[Node[T]], bool]
    backup: BackupFunction


def create_search_function[T](sfd: SearchFunctionDefinition[T]) -> SearchFunction[T]:
    """ """

    def select(root: Node[T], frontier: Frontier[T]) -> Node[T]:
        # frontier selection
        if sfd.use_frontier():
            return frontier.peek()

        # tree selection
        node = root
        while sfd.should_select(node):
            children = get_children(node)
            node = sfd.select(children)

        return node

    def expand(node: Node[T], frontier: Frontier[T]) -> Node[T]:
        child = single_expand(node)

        frontier.push(child)

        if node.is_fully_expanded:
            frontier.remove(node)

        return child

    def backpropagate(node: Node[T], values) -> None:
        set_values(node, values)
        node = get_parent(node)
        while sfd.should_backup(node):
            children = get_children(node)
            values = sfd.backup(children)
            set_values(node, values)
            node = get_parent(node)

    def treesearch(state: State[T]) -> T:
        root = Node[T](state)

        frontier = sfd.frontier()
        frontier.push(root)

        search_timer.start(1.0)

        print(root)
        while not sfd.should_terminate(root, frontier):
            node = select(root, frontier)
            child = expand(node, frontier)

            if sfd.should_evaluate():
                value = sfd.evaluate(child.state)
                backpropagate(child, value)

        children = get_children(root)

        best_child = max(children, key=sfd.action_value)

        return best_child[0]

    return treesearch
