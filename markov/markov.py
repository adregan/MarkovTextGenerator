from collections import defaultdict
import random

class MarkovInputError(Exception):
    pass

class Markov(object):
    def __init__(self, text='', files=[]):
        if not text and not files:
            raise MarkovInputError('Please supply input text or a file path.')
        if files:
            if not isinstance(files, (list)):
                files = [files]
            file_text = [
                self._open_files(file_path)
                for file_path in files
            ]
            text = ' '.join(file_text)

        self.words = text.split()

    def generate_text(self, output_length=50, word_grouping_length=2):
        corpus = self._construct_corpus(self.words, word_grouping_length)
        seed_index = random.randint(0, len(self.words))
        seed_word = self.words[seed_index]

        seed_words = [
            self.words[seed_index + i]
            for i in range(0, word_grouping_length)
        ]

        generated = []
        for _ in range(output_length):
            next_word = random.choice(corpus[tuple(seed_words)])
            seed_words.append(next_word)
            generated.append(seed_words.pop(0))

        generated_text = ' '.join(generated)

        return generated_text

    def _construct_corpus(self, words, word_grouping_length):
        def generate_word_group(current_word, index):
            additional_keys = [
                words[index + (i + 1)] 
                for i in range(word_grouping_length)
            ]
            return [current_word] + additional_keys

        final_words_indexes = [
            len(words) - (i + 1)
            for i in range(0, word_grouping_length)
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

    def _open_files(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
        except FileNotFoundError:
            raise MarkovInputError(
                'Couldn\'t find the file {}'.format(file_path)
            )
        else:
            return file_contents
