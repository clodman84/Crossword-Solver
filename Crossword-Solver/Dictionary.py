import json


def make_dictionary():
    dictionary = {}
    # this part will make a dictionary with keys as letters and values as a list of words
    with open("words.txt") as file:
        for word in file:
            word = word.lower().strip()
            if word.isalpha():
                if word[0] not in dictionary:
                    dictionary[word[0]] = [word]
                else:
                    dictionary[word[0]].append(word)
    # this part will make the values of each letter a dictionary with the key as the length of the word and the values
    # as words of that length. dictionary['a'][6] will return list of words with starting letter a and length 6.
    for alpha in dictionary:
        sorted_by_length = {}
        words = dictionary[alpha]
        for word in words:
            if len(word) not in sorted_by_length:
                sorted_by_length[len(word)] = [word]
            else:
                sorted_by_length[len(word)].append(word)
        dictionary[alpha] = sorted_by_length

    return dictionary


if __name__ == "__main__":
    with open("dictionary.json", "w") as f:
        json.dump(make_dictionary(), f)
