from life import next_board_state

def unit_test(function, input_args, expected_result, passed_message="PASSED", failed_message="FAILED"):
    actual_result = function(*(input_args))
    if expected_result == actual_result:
        print(passed_message)
    else:
        print(failed_message)
        print("Expected:")
        print(expected_result)
        print("Actual:")
        print(actual_result)

if __name__ == "__main__":
    # TEST 1: dead cells with no live neighbors
    # should stay dead.
    init_state1 = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    born = "3"
    survive = "23"
    expected_next_state1 = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    unit_test(next_board_state, (init_state1, born, survive), expected_next_state1)

    # TEST 2: dead cells with exactly 3 neighbors
    # should come alive.
    init_state2 = [
        [0,0,1],
        [0,1,1],
        [0,0,0]
    ]
    born = "3"
    survive = "23"
    expected_next_state2 = [
        [0,1,1],
        [0,1,1],
        [0,0,0]
    ]
    unit_test(next_board_state, (init_state2, born, survive), expected_next_state2)