from crossword import Crossword, Node
import time

puzzle = [
    ['a', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' '],
    ['_', ' ', ' ', ' ', ' ', ' ', '_', ' ', ' '],
    ['_', ' ', ' ', ' ', ' ', ' ', '_', ' ', ' '],
    ['_', '_', 'n', '_', '_', '_', '_', '_', '_'],
    ['_', ' ', '_', ' ', ' ', ' ', '_', ' ', ' '],
    ['_', ' ', '_', ' ', 't', ' ', '_', ' ', ' '],
    ['_', ' ', '_', '_', '_', '_', '_', '_', ' '],
    [' ', ' ', '_', ' ', '_', ' ', ' ', ' ', ' '],
    [' ', ' ', '_', ' ', '_', ' ', ' ', ' ', ' '],
]


def backTracking(crossword: Crossword):
    """
    Implements the backtracking algorithm
    :param crossword: The crossword
    :return: True if it solves the puzzle, alters the crossword.
    """

    node: Node = crossword.get_empty_node()
    if not node:
        return True
    # print(node, end='\n')

    row, column = node.position
    char = crossword.board[row][column]
    word_list = node.get_word_list(char)

    for word in word_list:
        # print(word, end='\r')
        if crossword.check_word(node, word):
            crossword.write(node, word)
            # crossword.display_board()
            if backTracking(crossword):
                return True
            crossword.erase(node)
    return False


if __name__ == '__main__':
    cross = Crossword(puzzle)
    cross.display_board()
    print("Nodes: \n")
    for n in cross.nodes:
        print(n)
    a = time.perf_counter()
    backTracking(crossword=cross)
    print('\nIt took ', time.perf_counter() - a, ' seconds to solve this!\n')
    cross.display_board()
