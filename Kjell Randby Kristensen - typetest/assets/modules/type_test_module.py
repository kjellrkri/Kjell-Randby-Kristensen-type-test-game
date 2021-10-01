"""Module contains type test functions."""
import statistics


def get_word_list():
    """
    Get list of 236736 english words.
    :return: list.
    """
    w_list = []
    with open('assets\\lists\\words.txt', 'r') as f:
        for line in f:
            word = line[:-1]  # remove linebreak which is the last character of the string
            w_list.append(word)  # add item to the list
    return w_list


def get_pb_score(hs_list, keyword, min_max=max):
    """
    Return personal best score based on the given keyword in a high score list.

    :param hs_list: takes any high score list containing dictionaries
    :param keyword: takes a string that represents a keyword in a dictionary within the hs_list
    :param min_max: takes either min or max, denotes if we want highest or lowest score
    :return: personal best high score
    """
    pb_score_list = []
    for score in hs_list:
        pb_score_list.append(score[keyword])
    pb = round(min_max(pb_score_list), 1)
    return pb


def get_mean_score(hs_list, keyword):
    """
        Return personal best score based on the given keyword in a high score list.

        :param hs_list: takes any high score list containing dictionaries
        :param keyword: takes a string that represents a keyword in a dictionary within the hs_list
        :return: personal mean high score
    """
    mean_score_list = []
    for score in hs_list:
        mean_score_list.append(score[keyword])
    mean = round(statistics.mean(mean_score_list), 1)
    return mean

