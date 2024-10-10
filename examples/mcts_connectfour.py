from gts.games.connectfour import ConnectFourState

from gts.search import SearchFunctionDefinition, create_search_function

if __name__ == "__main__":

    search_function_definition = SearchFunctionDefinition(
        frontier=[],
        should_terminate=None,
        should_evaluate=None,
        evaluate=None,
        action_value=None,
        use_frontier=None,
        should_select=None,
        select=None,
        backdown=None,
        should_backup=None,
        backup=None
    )

    search_function = create_search_function(search_function_definition)

    state = ConnectFourState()
    print(state)
    print(state.applicable_actions)

    print(search_function(state))