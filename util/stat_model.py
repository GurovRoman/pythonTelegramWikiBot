from ngram import Model
from collections import Counter
from numpy import std, average
from wordcloud import WordCloud
from io import BytesIO


class StatisticsModel(Model):
    def describe_word(self, word):
        indexed_block_start = self._word_index.get_index('_')
        indexed_empty_word = self._word_index.get_index('')
        padding = (indexed_empty_word,) * (self._n - 1)
        words = self._indexed_word_data[padding].copy()
        words.pop(self._word_index.get_index('_'), None)

        indexed_word = self._word_index.add_word(word)
        if indexed_word not in words:
            return None

        count = words[indexed_word]

        place = words.most_common().index((indexed_word, count)) + 1

        next = [self._word_index.get_word(i[0]) for i in
                self._indexed_word_data[padding[:-1] + (indexed_word,)].most_common(4)]

        prev_counter = Counter()
        over_one_counter = Counter()
        for key in self._indexed_word_data:
            if key[:-1] == padding[:-1] and key[-1] not in (indexed_empty_word, indexed_block_start):
                candidates = self._indexed_word_data[key]
                if indexed_word in candidates:
                    prev_counter[key[-1]] += candidates[indexed_word]
            if key[:-2] == padding[:-2] and key[-2] == indexed_word:
                over_one_counter.update(self._indexed_word_data[key])

        prev = [self._word_index.get_word(i[0]) for i in prev_counter.most_common(4)]
        over_one = [self._word_index.get_word(i[0]) for i in over_one_counter.most_common(4)]

        return count, place, next, prev, over_one

    def get_single_words(self):
        indexed_empty_word = self._word_index.get_index('')
        padding = (indexed_empty_word,) * (self._n - 1)
        words = self._indexed_word_data[padding].copy()
        words.pop(self._word_index.get_index('_'), None)
        return words

    def get_stop_words(self, indexed=False):
        words = self.get_single_words()

        values = list(words.values())
        deviation = std(values)
        avg = average(values)

        stops = set()

        for word in words:
            if abs(words[word] - avg) > deviation * 3:
                if indexed:
                    stops.add(word)
                else:
                    stops.add(self._word_index.get_word(word))

        return stops

    def get_top(self, count, order_desc=True):
        stops = self.get_stop_words(True)
        words = self.get_single_words()

        for stop in stops:
            words.pop(stop, None)

        words = sorted(words.items(), key=lambda x: x[1], reverse=not order_desc)
        words = [self._word_index.get_word(i[0]) for i in words]

        return list(words[0:count])

    def describe_all(self):
        words = self.get_single_words()

        freq_dist = sorted(Counter(words.values()).most_common(14))

        word_lengths = [len(self._word_index.get_word(i)) for i in words.keys()]
        len_dist = sorted(Counter(word_lengths).most_common(14))

        return freq_dist, len_dist

    def word_cloud(self, color):
        wc = WordCloud(stopwords=self.get_stop_words(), width=1280, height=720)

        words = self.get_single_words()
        for index in list(words.keys()):
            words[self._word_index.get_word(index)] = words.pop(index)

        wc.generate_from_frequencies(words)
        byte_image = BytesIO()
        wc.to_image().save(byte_image, 'PNG')
        byte_image.seek(0)
        return byte_image
