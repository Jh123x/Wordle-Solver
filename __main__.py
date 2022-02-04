from Guesser.Guesser import Guesser
from Tree.WordTree import WordTree


def read_word_list(filename: str) -> list:
    with open(filename, 'r') as f:
        data = f.readlines()
    return [word.strip() for word in data]


if __name__ == '__main__':

    word_list = read_word_list('wordle-answers-alphabetical.txt')
    word_tree = WordTree(word_list)
    # print(word_tree)

    # Create word tree
    guesser = Guesser(word_list)

    # 5 tries total
    recommended_guess = "slate"
    for _ in range(5):
        print(recommended_guess)
        print("Small letter for correct position and letter")
        print("Capital letter for correct letter wrong position")
        print("'_' for wrong letter not in word")
        guess = input("Enter the results: ")
        recommended_guess = guesser.get_best_guess(guess, recommended_guess)
