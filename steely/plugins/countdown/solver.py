from collections import deque

class TrieNode:
    def __init__(self, key=None):
        self.key = key
        self.children = {}
        self.is_word_end = False

    def add_descendant(self, word):
        if not len(word):
            self.is_word_end = True
            return

        k = word[0]
        if k not in self.children:
            self.children[k] = TrieNode(key=k)
        self.children[k].add_descendant(word[1:])

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        self.root.add_descendant(word)

    def get_words_for_letters(self, letters):
        words = set()
        n = len(letters)
        q = deque([(self.root, '', [False for _ in range(n)])])
        while len(q):
            node, path, used_letters = q.popleft()
            if node.is_word_end:
                words.add(path)
            for i in range(n):
                # TODO(iandioch): There's an optimisation available here if
                # there are some duplicate letters in `letters`. If letters[3]
                # is the same letter as letters[5], this loop will start a
                # subsearch from both of those letters, even though the subtree
                # they are searching will be identical.
                if used_letters[i]:
                    continue
                if letters[i] in node.children:
                    used = used_letters[:]
                    used[i] = True
                    q.append((node.children[letters[i]], path + letters[i], used))
        return words

class CountdownSolver:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.trie = Trie()
        for word in self.dictionary:
            self.trie.add_word(word)

    # Figures out the longest length of word it is possible to create with the 
    # letters in the sequence `available_letters`, and returns all such words of
    # that length.
    def all_best_words(self, available_letters):
        all_words = self.trie.get_words_for_letters(available_letters)
        best_len = max(len(word) for word in all_words)
        return [word for word in all_words if len(word) == best_len]

def main():
    c = CountdownSolver(['a', 'aa', 'ab', 'aab', 'abc'])
    print(c.all_best_words('a')) # Expected: ['a']
    print(c.all_best_words('ab')) # Expected: ['ab']
    print(c.all_best_words('aab')) # Expected: ['aab']
    print(c.all_best_words('ac')) # Expected: ['a']
    print(c.all_best_words('abc')) # Expected: ['abc']
    print(c.all_best_words('aabc')) # Expected: ['abc', 'aab']

if __name__ == '__main__':
    main()
