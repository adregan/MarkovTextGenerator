from collections import defaultdict
import random

class MarkovInputError(Exception):
    pass

class Markov(object):
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.text = file.read()
        self.words = self.text.split()

    def generate_text(self, finished_length, word_key_count=2):
        corpus = self._construct_corpus(self.words, word_key_count)
        seed_index = random.randint(0, len(self.words))
        seed_word = self.words[seed_index]

        seed_words = [
            self.words[seed_index + i]
            for i in range(0, word_key_count)
        ]

        generated = []
        for _ in range(finished_length):
            next_word = random.choice(corpus[tuple(seed_words)])
            seed_words.append(next_word)
            generated.append(seed_words.pop(0))

        generated_text = ' '.join(generated)

        print(generated_text)

    def _construct_corpus(self, words, word_key_count):
        def generate_word_group(current_word, index):
            additional_keys = [
                words[index + (i + 1)] 
                for i in range(word_key_count)
            ]
            return [current_word] + additional_keys

        final_words_indexes = [
            len(words) - (i + 1)
            for i in range(0, word_key_count)
        ]

        word_groups = [
            generate_word_group(word, i)
            for i, word in enumerate(words)
            if i not in final_words_indexes
        ]

        corpus = defaultdict(list)
        for word_group in word_groups:
            word_group_value = word_group.pop()
            corpus[tuple(word_group)].append(word_group_value)

        return corpus
