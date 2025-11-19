import re
import pandas as pd
from collections import Counter


def __readfiles() -> list:
    """ Reads the Wordle word lists (full and used) from bdwalker1's github
        repository and returns them as lists.
    """
    srvr = "https://raw.githubusercontent.com/"
    repopath = "bdwalker1/WordleHelper/main/"
    raw_df = pd.read_csv(srvr + repopath + "wordle_valid_words.txt")
    valid_words = list(raw_df['valid_word'])
    del raw_df
    raw_df = pd.read_csv(srvr + repopath + "wordle_used_words.txt")
    used_words = list(raw_df['used_word'])
    del raw_df
    return [valid_words, used_words]


def compare_word_files() -> list:
    """ Reads the Wordle word lists (full and used) from bdwalker1's github
        repository and returns them as lists.
    """
    srvr = "https://raw.githubusercontent.com/"
    repopath = "bdwalker1/WordleHelper/main/"
    raw_df = pd.read_csv(srvr + repopath + "wordle_used_words_old.txt")
    oldstyle_words = list(raw_df['used_word'])
    del raw_df
    raw_df = pd.read_csv(srvr + repopath + "wordle_used_words.txt")
    used_words = list(raw_df['used_word'])
    del raw_df
    return [[word for word in used_words if word not in oldstyle_words], [word for word in oldstyle_words if word not in used_words]]

def novel_words() -> list:
    """ Reads the Wordle word lists (full and used) from bdwalker1's github
        repository and returns them as lists.
    """
    srvr = "https://raw.githubusercontent.com/"
    repopath = "bdwalker1/WordleHelper/main/"
    raw_df = pd.read_csv(srvr + repopath + "wordle_valid_words.txt")
    valid_words = list(raw_df['valid_word'])
    del raw_df
    raw_df = pd.read_csv(srvr + repopath + "wordle_used_words.txt")
    used_words = list(raw_df['used_word'])
    del raw_df
    return sorted([word for word in used_words if word not in valid_words])
    
def unused_words() -> list:
    """ Reads the Wordle word lists (full and used) from bdwalker1's github
        repository and returns them as lists.
    """
    srvr = "https://raw.githubusercontent.com/"
    repopath = "bdwalker1/WordleHelper/main/"
    raw_df = pd.read_csv(srvr + repopath + "wordle_valid_words.txt")
    valid_words = list(raw_df['valid_word'])
    del raw_df
    raw_df = pd.read_csv(srvr + repopath + "wordle_used_words.txt")
    used_words = list(raw_df['used_word'])
    del raw_df
    return sorted([word for word in valid_words if word not in used_words])

def __validateparams(pattern: str, keep_ltrs: str,
                     elim_ltrs: str, elim_pattern: list) -> tuple:
    """ Converts all parameters to lowercase and performs some basic validation
        on them then returns them.
    """
    ptrn = pattern.lower()
    in_ltrs = keep_ltrs.lower()
    ex_ltrs = elim_ltrs.lower()
    excl_pattern = [p.lower() for p in elim_pattern]

    if len(pattern) != 5:
        raise ValueError("The RegEx pattern must be 5 characters long")

    for c in pattern:
        if c not in '.abcdefghijklmnopqrstuvwxyz':
            errmsg: str = "Your pattern contains characters other than . or a-z"
            raise ValueError(errmsg)

    try:
        re.compile(pattern)
    except re.error:
        raise ValueError("Your match pattern is not a valid regex pattern")

    for test_pattern in excl_pattern:
        try:
            re.compile(test_pattern)
        except re.error:
            errmsg: str = "One of your elimination pattern(s) is "
            errmsg += "not a valid regex pattern"
            raise ValueError(errmsg)

    for c in ex_ltrs:
        if c in pattern:
            msg: str = "Your pattern contains one of the elimination characters: "
            msg += f"{pattern} --> {str().join(sorted(ex_ltrs))}"
            raise ValueError(msg)
        if c in in_ltrs:
            msg: str = "Your keep letter(s) contain one of the elimination "
            msg += "characters: "
            msg += f"{str().join(sorted(in_ltrs))} --> {str().join(sorted(ex_ltrs))}"
            raise ValueError(msg)
    return ptrn, in_ltrs, ex_ltrs, excl_pattern


def _findmatchingwords(wordlist: list, keep_ltrs: str, elim_ltrs: str) -> list:
    """ Checks a word list for words that contain the specified keep letters
        and not the specified elimination letters then returns the filtered list.
    """
    matches = list()
    for word in wordlist:
        word_good: bool = True
        for c in elim_ltrs:
            if c in word:
                word_good = False
                break
        for c in keep_ltrs:
            if c not in word:
                word_good = False
                break
        if word_good:
            matches.append(word)
    return matches


def matchunusedwords(pattern: str, keep_ltrs: str = '',
                     elim_ltrs: str = '', elim_pattern: list = ['zzzzz']
                     ) -> tuple:
    """ Given a RegEx pattern and a string of eliminated letters,
        return matching words from the valid Wordle word list
        that have not yet been used.
    """

    possible_words, most_common_ltrs = (
        matchwords(pattern, keep_ltrs, elim_ltrs, elim_pattern, unused=True)
        )

    return possible_words, most_common_ltrs


def matchwords(pattern: str, keep_ltrs: str = '', elim_ltrs: str = '',
               elim_pattern: list = ['zzzzz'], unused: bool = False) -> tuple:
    """ Given a RegEx pattern and a string of eliminated letters,
        return matching words from the valid Wordle word list
    """

    ptrn, in_ltrs, ex_ltrs, elim_ptrn = __validateparams(pattern, keep_ltrs,
                                                         elim_ltrs, elim_pattern)
    word_lists = __readfiles()
    valid_words, used_words = word_lists[0], word_lists[1]
    if unused == True:
        valid_words = [word for word in valid_words if word not in used_words]
    match_words = [word for word in valid_words if (re.search(ptrn, word)
                                                    is not None)]
    for excl_pattern in elim_pattern:
        drop_words =  [word for word in match_words
                       if (re.search(excl_pattern, word) is not None)]
        match_words = [word for word in match_words if (word not in drop_words)]

    matching_words = _findmatchingwords(match_words, in_ltrs, ex_ltrs)

    counts = Counter()
    for word in matching_words:
        counts.update(word)

    return matching_words, counts.most_common(5)


if __name__ == '__main__':
    # These statements make it easy to use the module
    # in Pythonista on iPhone or iPad
    from wordleHelper import matchunusedwords as muw
    from wordleHelper import matchwords as mw

    print('')
    print("w, c = mw('.....', '', '', ['zzzzz']); print(w); print(len(w)); print(c)")
    print("w, c = muw('.....', '', '', ['zzzzz']); print(w); print(len(w)); print(c)")

    print(compare_word_files())
 