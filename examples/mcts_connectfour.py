import random

from gts.games.connectfour import ConnectFourState

from gts.search import SearchFunctionDefinition, create_search_function, search_timer
from gts.frontier import FrontierNone
from gts.state import State

def should_terminate(node, frontier):
    return search_timer.is_timeout()

def should_select(node):
    return node.is_fully_expanded

def uct_select(children):
    return children

def backup_max(children):
    evaluation = max(child._values["evaluation"] for child in children)
    return {"evaluation": evaluation}

def evaluate(state: State):

    while not state.is_terminal:
        action = random.choice(state.applicable_actions)
        state = state.result(action)

    return {"utility": state.utility}



if __name__ == "__main__":

    search_function_definition = SearchFunctionDefinition(
        frontier=FrontierNone,
        should_terminate=should_terminate,
        should_evaluate=lambda *_: True,
        evaluate=lambda node: {"evaluation": 0.5},
        action_value=None,
        use_frontier=lambda *_: False,
        should_select=should_select,
        select=uct_select,
        backdown=None,
        should_backup=lambda node: node._parent is not None,
        backup=backup_max
    )

    search_function = create_search_function(search_function_definition)

    state = ConnectFourState()
    print(state)
    print(state.applicable_actions)

    print(search_function(state))