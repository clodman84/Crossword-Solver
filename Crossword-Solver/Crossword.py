import json
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

with open('dictionary.json') as file:
    dictionary = json.load(file)


class Crossword:
    def __init__(self, board):
        self.board = board
        self.nodes = []
        self.find_nodes()

    def find_nodes(self):
        for row_index in range(len(self.board)):
            for column_index in range(len(self.board[0])):

                # if it is a vertical node
                if self.vertical_node(row_index, column_index):
                    char = self.board[row_index][column_index]
                    pos = (row_index, column_index)
                    length = self.get_length(pos, 'v')
                    node = Node(
                        pos,
                        'v',
                        length
                    )
                    node.get_word_list(char)
                    self.nodes.append(node)
                # if it is a horizontal node
                if self.horizontal_node(row_index, column_index):
                    char = self.board[row_index][column_index]
                    pos = (row_index, column_index)
                    length = self.get_length(pos, 'h')
                    node = Node(
                        pos,
                        'h',
                        length
                    )
                    node.get_word_list(char)
                    self.nodes.append(node)

    def vertical_node(self, row, column):
        # checking for cell above and below to decide if this is vertical node
        aboveBlocked = False
        bottomBlocked = False
        if self.board[row][column] == ' ':
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
        print(' ', *[i for i in range(len(self.board[0]))])
        for i, row in enumerate(self.board):
            print(i, end=' ')
            for char in row:
                if char == ' ':
                    print('|', end=' ')
                else:
                    print(char, end=' ')
            print()

    def get_length(self, pos, orientation):
        length = 1
        row, column = pos
        if orientation == 'v':
            while True:
                if row == len(self.board) - 1:
                    return length
                if self.board[row + 1][column] != ' ':
                    length += 1
                    row += 1
                else:
                    return length
        elif orientation == 'h':
            while True:
                if column == len(self.board[0]) - 1:
                    return length
                if self.board[row][column + 1] != ' ':
                    length += 1
                    column += 1
                else:
                    return length

    def check_word(self, node, word):
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
            row, column = node.position
            if node.orientation == 'v':
                if self.board[row + 1][column] == '_':
                    return node

            if node.orientation == 'h':
                if self.board[row][column + 1] == '_':
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

    def erase(self, node):
        row, column = node.position
        if node.orientation == 'v':
            for i in range(node.length):
                self.board[row][column] = '_'
                row += 1
        if node.orientation == 'h':
            for i in range(node.length):
                self.board[row][column] = '_'
                column += 1

    def solve(self):
        node = self.get_empty_node()
        if not node:
            return True

        # making the word list shorter and more specific if the node is not a fixed node
        if node.is_var:
            row, column = node.position
            char = self.board[row][column]
            if char.isalpha():
                word_list = dictionary[char][str(node.length)]
            else:
                word_list = node.word_list
        else:
            word_list = node.word_list

        for word in word_list:
            if self.check_word(node, word):
                self.write(node, word)
                if self.solve():
                    return True
                self.erase(node)

        return False

    def show_nodes(self):
        for node in self.nodes:
            print(node, end='\n\n')


class Node:
    def __init__(self, position, orientation, length):
        self.position = position
        self.orientation = orientation
        self.length = length
        self.word_list = []
        self.is_var = False

    def get_word_list(self, char):
        if char.isalpha():
            self.word_list = dictionary[char][str(self.length)]
        else:
            for alpha in dictionary:
                self.word_list.extend(dictionary[alpha][str(self.length)])
            self.is_var = True

    def __str__(self):
        return f"Orientation:{self.orientation}\nPosition:{self.position}" \
               f"\nWorldList:{self.word_list}"


if __name__ == '__main__':
    cross = Crossword(puzzle)
    cross.display_board()
    a = time.perf_counter()
    cross.solve()
    print('\nIt took ', time.perf_counter()-a, ' seconds to solve this!\n')
    cross.display_board()
