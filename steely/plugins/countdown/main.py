import heapq
import random
import threading
import time

from collections import Counter, defaultdict

from plugin import create_plugin
from message import SteelyMessage
from .solver import CountdownSolver

WORDLIST_URL = 'https://raw.githubusercontent.com/jesstess/Scrabble/5d4a1e69ad2267126fa8d82bbc34ca936d1f878a/scrabble/sowpods.txt'
WORDS = set()
GAME_MANAGER = None
SOLVER = None

plugin = create_plugin(name='countdown', author='iandioch', help='TODO')


class CountdownGame:

    def __init__(self, letters, word_checker):
        # `letters` must be a string of available letters.
        # `word_checker` must be a function which takes one string argument, and
        # returns True or False if it is a real word.
        self.letters = letters
        self.letter_counts = Counter(self.letters)
        # Maps author_id to their best word
        self.best_word = defaultdict(str)
        self.all_words = set()

        self.check_word = word_checker

    def submit_word(self, author_id, word):
        # Try to add the given word for the given author.
        # Will fail silently if the word is invalid (not a real word or not
        # possible with the available letters), if the word was already
        # submitted, or the word is worse than the best word this author has
        # already submitted.
        word = word.upper()
        if not self._is_valid(word):
            return
        if word in self.all_words:
            return
        self.all_words.add(word)
        if len(self.best_word[author_id]) >= len(word):
            return
        self.best_word[author_id] = word

    def get_winners(self):
        # Returns a list containing (author_id, word) tuples of winning users.
        # If no such user was found, returns an empty list.
        # There can be multiple winners if several people submit different valid
        # words of the same maximal length.
        print('Winners of countdown game: ', self.best_word)
        if not len(self.best_word):
            return []
        best_score = max(len(self.best_word[w]) for w in self.best_word)
        return [
            (user, word) for _, (user, word) in enumerate(self.best_word.items()) if len(word) == best_score]

    def _is_valid(self, word):
        used_letters = Counter(word)
        if not all(
            (letter in self.letter_counts and
                self.letter_counts[letter] >= used_letters[letter])
                for letter in used_letters):
            return False
        is_valid = self.check_word(word)
        print('Countdown word {} is createable with letters {}, is it in the dictionary? {}'.format(
            word, self.letters, is_valid))
        return is_valid


class CountdownGameManager:

    def __init__(self, word_checker):
        # Maps from thread_id to CountdownGame instance.
        self.word_checker = word_checker

        # .games maps thread_id to a CountdownGame instance.
        self.games = {}
        # .finish_time is a heapq containing (finish_time_millis, thread_id) tuples.
        self.finish_times = []
        self.message_senders = {}
        self.user_name_getters = {}
        # A mutex to protect .games, .finish_time, .message_senders,
        # .user_name_getters  from being modified by different threads (the
        # game creation thread, and the thread listening for finished games) at
        # the same time.
        self.game_lock = threading.Lock()

        polling_thread = threading.Thread(target=self._poll_for_finished_games)
        polling_thread.start()

    def create_game(self, thread_id, letters, message_sender, user_name_getter):
        # Create a game with for the given thread, with the given letters.
        # message_sender must be a function which takes a single string argument
        # and sends it as a message to the relevant thread.
        # user_name_getter must be a function which takes a single author_id
        # argument, and returns a human-readable name for that user.
        self.game_lock.acquire()
        if thread_id in self.games:
            message_sender('There is already an active game in this chat!')
        message_sender("Your letters are {}. Let's countdown!".format(letters))
        self.games[thread_id] = CountdownGame(letters, self.word_checker)
        self.message_senders[thread_id] = message_sender
        self.user_name_getters[thread_id] = user_name_getter
        # TODO(iandioch): Allow user to define game length.
        end_time = time.time() * 1000 + 60 * 1000
        heapq.heappush(self.finish_times, (end_time, thread_id))
        self.game_lock.release()

    def add_word(self, thread_id, author_id, word):
        # Try to add the given word to a game in that thread. If there is no
        # such game, no problemo!
        self.game_lock.acquire()
        if thread_id in self.games:
            self.games[thread_id].submit_word(author_id, word)
        self.game_lock.release()

    def _poll_for_finished_games(self):
        # This method should be called in a new thread, as it will loop
        # indefinitely triggering the end of finished games. "finished" here
        # means that the time has run out.
        while True:
            self.game_lock.acquire()
            # Iterate the active games, and finish any of which the end time
            # has passed.
            while True:
                if not len(self.finish_times):
                    break
                next_time = self.finish_times[0][0]
                if (time.time() * 1000) < next_time:
                    break
                _, thread_id = heapq.heappop(self.finish_times)
                self._finish_game(thread_id)
            self.game_lock.release()
            time.sleep(1)

    def _finish_game(self, thread_id):
        # Finish the game for the given thread. The .game_lock mutex should
        # already be held before calling this method!
        if thread_id not in self.games:
            print('Requested to end game for thread {}, but no such game was found!'.format(
                thread_id))
            return
        if thread_id not in self.message_senders:
            print('Could not find message sender for thread {} when trying to finish game!'.format(
                thread_id))
            return
        if thread_id not in self.user_name_getters:
            print('Could not find user name getter for thread {} when trying to finish game!'.format(
                thread_id))
        send_message = self.message_senders[thread_id]
        game = self.games[thread_id]
        winners = game.get_winners()
        if not len(winners):
            send_message(
                "Countdown game finished! But there were no winners...")
        else:
            message = ['Countdown game finished! Winning words:']
            for winner in winners:
                name = self.user_name_getters[thread_id](winner[0])
                word = winner[1]
                message.append('*{}* by _{}_'.format(word, name))
            send_message('\n'.join(message))

        best_words = SOLVER.all_best_words(self.games[thread_id].letters)
        send_message(f'Best words: {", ".join("*" + word + "*" for word in best_words)}')

        del self.user_name_getters[thread_id]
        del self.message_senders[thread_id]
        del self.games[thread_id]


def get_letter_distribution():
    return ({
        'A': 15, 'E': 21, 'I': 13, 'O': 13, 'U': 5
    }, {
        'B': 2,
        'C': 3,
        'D': 6,
        'F': 2,
        'G': 3,
        'H': 2,
        'J': 1,
        'K': 1,
        'L': 5,
        'M': 4,
        'N': 8,
        'P': 4,
        'Q': 1,
        'R': 9,
        'S': 9,
        'T': 9,
        'V': 1,
        'W': 1,
        'X': 1,
        'Y': 1,
        'Z': 1
    })


def generate_letters(schema):
    num_consonant = 0
    num_vowel = 0
    for letter in schema:
        if letter in 'cCkK':
            num_consonant += 1
        elif letter in 'vV':
            num_vowel += 1

    vowels, consonants = get_letter_distribution()
    vowel_distribution = ''.join(v * vowels[v] for v in vowels)
    consonant_distribution = ''.join(c * consonants[c] for c in consonants)
    letters = random.sample(vowel_distribution, num_vowel)
    letters += random.sample(consonant_distribution, num_consonant)
    return ''.join(letters)


@plugin.setup()
def load_wordlist():
    import urllib.request as request
    global WORDS
    with request.urlopen(WORDLIST_URL) as resp:
        if resp.status != 200:
            return False
        contents = resp.read().decode('utf-8')
        WORDS = set(w.upper() for w in contents.split('\n'))
        print('Loaded {} words into the Countdown wordlist.'.format(len(WORDS)))

    global GAME_MANAGER
    GAME_MANAGER = CountdownGameManager(
        word_checker=lambda word: word in WORDS)

    global SOLVER
    SOLVER = CountdownSolver(WORDS)


@plugin.listen(command='countdown [schema]')
def create_game(bot, message: SteelyMessage, **kwargs):
    schema = 'cccccvvvv'
    if 'schema' in kwargs:
        # TODO(iandioch): Check given distribution is valid
        schema = kwargs['schema']

    letters = generate_letters(schema)

    def send_message(text):
        bot.sendMessage(text, thread_id=message.thread_id,
                        thread_type=message.thread_type)

    def get_user_name(user_id):
        return bot.fetchUserInfo(user_id)[0]['username']

    GAME_MANAGER.create_game(thread_id=message.thread_id,
                             letters=letters,
                             message_sender=send_message,
                             user_name_getter=get_user_name)


@plugin.listen()
def listen_for_words(bot, message: SteelyMessage, **kwargs):
    GAME_MANAGER.add_word(
        message.thread_id, message.author_id, message.text.strip())
