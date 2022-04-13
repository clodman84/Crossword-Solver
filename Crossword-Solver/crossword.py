import json
from itertools import chain

with open('dictionary.json') as file:
    dictionary = json.load(file)

"""
    This holds the basic Crossword and Node classes that the algorithms will use.
"""


class Crossword:
    """
    Takes in a 2D list of letters, then automatically detects the across and down "nodes".
    Also has methods for erasing and writing from each one of these nodes, checking if a word fits, etc.
    """

    def __init__(self, board):
        self.board = board
        self.nodes = []
        self.find_nodes()

    def find_nodes(self):
        for row_index in range(len(self.board)):
            for column_index in range(len(self.board[0])):

                # if it is a vertical node
                if self.vertical_node(row_index, column_index):
                    pos = (row_index, column_index)
                    dim = self.getNodeDimensions(pos, 'v')
                    node = Node(
                        pos,
                        orientation='v',
                        length=dim[0],
                        fixed_char=dim[1]
                    )
                    self.nodes.append(node)

                # if it is a horizontal node
                if self.horizontal_node(row_index, column_index):
                    pos = (row_index, column_index)
                    dim = self.getNodeDimensions(pos, 'h')
                    node = Node(
                        pos,
                        orientation='h',
                        length=dim[0],
                        fixed_char=dim[1]
                    )
                    self.nodes.append(node)

    def vertical_node(self, row, column):
        # checking for cell above and below to decide if this is vertical node
        aboveBlocked = False
        bottomBlocked = False
        if self.board[row][column] == ' ':  # in case the cell cannot store a character, a ' ' cell
            return False
        if row == 0 or self.board[row - 1][column] == ' ':
            aboveBlocked = True
        if row == len(self.board) - 1 or self.board[row + 1][column] == ' ':
            bottomBlocked = True
        return aboveBlocked and not bottomBlocked

    def horizontal_node(self, row, column):
        # checking for cell left and right to decide if this is horizontal node
        leftBlocked = False
        rightBlocked = False
        if self.board[row][column] == ' ':
            return False
        if column == 0 or self.board[row][column - 1] == ' ':
            leftBlocked = True
        if column == len(self.board[0]) - 1 or self.board[row][column + 1] == ' ':
            rightBlocked = True
        return leftBlocked and not rightBlocked

    def display_board(self):
        board = '  ' + ' '.join([str(i) for i in range(len(self.board[0]))]) + '\n'
        for i, row in enumerate(self.board):
            board += f'{i} '
            for char in row:
                if char == ' ':
                    board += '| '
                else:
                    board += f"{char} "
            board += '\n'
        print(board)

    def getNodeDimensions(self, pos, orientation):
        """
        Returns the length and fixed characters of a node given the position and the orientation, does not take node
        as parameter.

        :param pos: Tuple with (row, column) position, with origin at top left corner
        :param orientation: Orientation the node, 'v' for vertical 'h' for horizontal
        :return: (tuple): length (int), fixed_chars (tuple)
        """
        length = 0
        row, column = pos
        fixed_char = []
        if orientation == 'v':
            while True:
                if row == len(self.board) - 1:
                    return length, fixed_char
                try:
                    char = self.board[row + length][column]
                except IndexError:
                    break

                if char != ' ':  # if the character in that position is not a blocked out cell
                    if char.isalpha():
                        fixed_char.append(row+length)
                    length += 1
                else:
                    break

        elif orientation == 'h':
            while True:
                if column == len(self.board[0]) - 1:
                    return length, fixed_char
                try:
                    char = self.board[row][column + length]
                except IndexError:
                    break

                if char != ' ':
                    if char.isalpha():
                        fixed_char.append(column+length)
                    length += 1
                else:
                    break

        return length, tuple(fixed_char)

    def check_word(self, node, word):
        """
        Checks if a word fits in a node or not.

        :param node: Node
        :param word: The word
        :return: Boolean: True if it fits in the node.
        """
        row, column = node.position
        if node.orientation == 'v':
            for i in word:
                char = self.board[row][column]
                if char.isalpha() and char != i:
                    return False
                else:
                    row += 1
            return True

        if node.orientation == 'h':
            for i in word:
                char = self.board[row][column]
                if char.isalpha() and char != i:
                    return False
                else:
                    column += 1
            return True

    def get_empty_node(self):
        for node in self.nodes:
            if node.is_empty:
                return node
        return None

    def write(self, node, word):
        row, column = node.position
        if node.orientation == 'v':
            for i in word:
                self.board[row][column] = i
                row += 1
        if node.orientation == 'h':
            for i in word:
                self.board[row][column] = i
                column += 1
        node.is_empty = False

    def erase(self, node):
        row, column = node.position

        if node.orientation == 'v':
            for i in range(len(node)):
                if row not in node.fixed_char:
                    self.board[row][column] = '_'
                row += 1

        if node.orientation == 'h':
            for i in range(len(node)):
                if column not in node.fixed_char:
                    self.board[row][column] = '_'
                column += 1
        node.is_empty = True

    def show_nodes(self):
        for node in self.nodes:
            print(node, end='\n\n')


class Node:
    def __init__(self, position, orientation, length, fixed_char):
        self.position = position
        self.orientation = orientation
        self.length = length
        self.is_empty = True

        # a list of column or row indexes (depending on orientation) which should not be erased.
        self.fixed_char = fixed_char

    def get_word_list(self, char):
        if char.isalpha():
            return dictionary[char][str(len(self))]
        else:
            return list(chain.from_iterable([dictionary[alpha][str(len(self))] for alpha in dictionary.keys()]))

    def __str__(self):
        return f"Orientation:{self.orientation} Position:{self.position} Length: {len(self)} Fixed: {self.fixed_char}"

    def __len__(self):
        return self.length
