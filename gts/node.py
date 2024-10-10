"""
search tree nodes

getters etc. are defined as functions and not methods,
to emphasize that a caller with a Node instance can not access 
the Node's internals directly
"""
from gts.state import State


type Edge[ActionT] = tuple[ActionT, Node[State[ActionT]]]


class Node[ActionT]:
    # unique identifier for each node to facilitate efficient removal from the frontier
    _IDX_POINTER = 0
    
    def __init__(self, state: State[ActionT], parent: Edge[ActionT] | None = None) -> None:
        self._idx = Node._IDX_POINTER
        Node._IDX_POINTER += 1
        self.state = state
        self._values = {}
        self._parent: Edge[ActionT] | None = parent
        self._children: list[Edge[ActionT]] = []
        self._unexpanded_actions = state.applicable_actions


def set_values[ActionT](node: Node[ActionT], values: dict[str, float]) -> None:
    node._values.update(values)


def get_parent[ActionT](node: Node[ActionT]) -> Edge[ActionT] | None:
    return node._parent


def get_children[ActionT](node: Node[ActionT]) -> list[Edge[ActionT]]:
    return node._children


def single_expand[ActionT](node: Node[ActionT]) -> Edge[ActionT]:
    action = node._unexpanded_actions.pop()
    successor_state = node.state.result(action)
    edge = (action, Node(successor_state, (action, node)))
    node._children.append(edge)
    return edge
