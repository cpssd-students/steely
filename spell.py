#!/usr/bin/env python3


WORDS = []


def correction(word):
    "most probable spelling correction for word"
    return list(candidates(word))


def candidates(word):
    "generate possible spelling corrections for word"
    return known([word]) or known(edits1(word)) or known(edits2(word))


def known(words):
    "the subset of `words` that appear in the dictionary of WORDS"
    return set(w for w in words if w in WORDS)


def edits1(word):
    "all edits that are one edit away from `word`"
    letters    = '.abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "all edits that are two edits away from `word`"
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


if __name__ == '__main__':
    print(correction('heo'))
