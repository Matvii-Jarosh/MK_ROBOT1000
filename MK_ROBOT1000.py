# Copyright (c) 2025 Matvii Jarosh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import re
from itertools import product

CHAR_REPLACEMENTS = {
    '0': ['о', 'o'],
    '1': ['l', 'i', 'і', 'ї'],
    '2': ['z'],
    '3': ['е', 'e', 'з'],
    '4': ['ч', 'a'],
    '5': ['s'],
    '6': ['б', 'b'],
    '7': ['т', 't'],
    '8': ['в', 'b'],
    '9': ['g'],

    '@': [
        'а', 'е', 'є', 'и', 'і', 'ї', 'о', 'у', 'ю', 'я',
        'ё', 'ы', 'э',
        'a', 'e', 'i', 'o', 'u', 'y',
    ],
    '*': [
        'а', 'е', 'є', 'и', 'і', 'ї', 'о', 'у', 'ю', 'я',
        'ё', 'ы', 'э',
        'a', 'e', 'i', 'o', 'u', 'y',
    ],

    '$': ['s'],
    '!': ['i', 'l', 'і'],
    '#': ['н', 'n'],
    '%': ['оо', 'oo'],
    '&': ['і', 'i'],
    '?': ['ї', 'і'],
    '^': ['ш', 'щ'],

    'a': ['а'],
    'b': ['б'],
    'c': ['с'],
    'd': ['д'],
    'e': ['е', 'є'],
    'f': ['ф'],
    'g': ['г', 'ґ'],
    'h': ['х'],
    'i': ['і', 'ї'],
    'j': ['й'],
    'k': ['к'],
    'l': ['л'],
    'm': ['м'],
    'n': ['н'],
    'o': ['о'],
    'p': ['п', 'р'],
    'q': ['я'],
    'r': ['р'],
    's': ['с'],
    't': ['т'],
    'u': ['у'],
    'v': ['в'],
    'w': ['ш', 'щ'],
    'x': ['х'],
    'y': ['у', 'й'],
    'z': ['з'],
    'а': ['a'],
    'в': ['v'],
    'е': ['e'],
    'з': ['z'],
    'и': ['u', 'y'],
    'і': ['i'],
    'к': ['k'],
    'м': ['m'],
    'о': ['o'],
    'п': ['n'],
    'р': ['p'],
    'с': ['s', 'c'],
    'т': ['t'],
    'у': ['u', 'y'],
    'х': ['h', 'x'],
}

BAD_WORDS = {
    'дебіл': 1,
    'дур': 1,
    'лох': 1,
    'лошара': 1,
    'лошок': 1,
    'туп': 1,
    'чмо': 1,
    'чмарити': 1,
    'кретин': 1,
    'крейзі': 1,
    'крейзи': 1,
    'ідіот': 1,
    'идиот': 1,
    'stupid': 1,
    'параш': 1,
    'dumb': 1,
    'loser': 1,
    'sucker': 1,
    'jerk': 1,

    'бля': 2,
    'гів': 2,
    'говно': 2,
    'говнюк': 2,
    'гавно': 2,
    'муд': 2,
    'пізд': 2,
    'срат': 2,
    'жоп': 2,
    'залупа': 2,
    'залупка': 2,
    'шльондра': 2,
    'падла': 2,
    'падлюка': 2,
    'сучка': 2,
    'сука': 2,
    'сучара': 2,
    'курва': 2,
    'курвин': 2,
    'fuck': 2,
    'shit': 2,
    'bullshit': 2,
    'shitty': 2,
    'shitter': 2,
    'ass': 2,
    'bitch': 2,
    'cock': 2,
    'dick': 2,
    'pussy': 2,
    'whore': 2,
    'slut': 2,
    'bastard': 2,
    'damn': 2,
    'cunt': 2,
    'retard': 2,
    'idiot': 2,
    'moron': 2,

    'хер': 3,
    'хуй': 3,
    'хуесос': 3,
    'підорас': 3,
    'пидорас': 3,
    'підар': 3,
    'пидар': 3,
    'ублюдок': 3,
    'виродок': 3,
    'motherfucker': 3,
    'nigger': 3,
    'nigga': 3,
}

EXCLUSION = [
    "тупик",
    "тупік",
    "тупок",
    "дуршл",
    "дурниц",
    "дурост",
    "лохн",
    "пізн",
    "жопк",
    "залупл",
    "херув",
    "херсон",
    "хулиг",
    "хутор",
    "срачк",
    "підаркув",
    "лохин",
    "блядк",
]

bad_words_regex = re.compile("|".join(sorted(map(re.escape, BAD_WORDS.keys()), key=len, reverse=True)))
exclusion_regex = re.compile("|".join(map(re.escape, EXCLUSION)))
min_bad_len = min(len(bw) for bw in BAD_WORDS) if BAD_WORDS else 0
min_excl_len = min(len(ew) for ew in EXCLUSION) if EXCLUSION else 0

def contains_bad_word(word: str) -> tuple[bool, str | None, int | None]:
    """
    Перевіряє на погані слова
    :param word: слово на перевірку
    :return: Чи є слово поганим, і за чого воно погане, ступінь поганості слова
    """
    word_lower = word.lower()
    word_len = len(word_lower)

    if word_lower in BAD_WORDS:
        return True, word_lower, BAD_WORDS[word_lower]

    if word_len < min(min_bad_len, min_excl_len):
        return False, None, None

    def generate_variants(word_prefix, target_words):
        variants = {word_prefix}
        for i, char in enumerate(word_prefix):
            if char not in CHAR_REPLACEMENTS:
                continue
            new_variants = set()
            for variant in variants:
                for replacement in CHAR_REPLACEMENTS[char]:
                    new_variant = variant[:i] + replacement + variant[i + 1:]
                    if new_variant in target_words:
                        return new_variant
                    new_variants.add(new_variant)
            variants.update(new_variants)
        return None

    for exclusion_word in EXCLUSION:
        excl_len = len(exclusion_word)
        if word_len < excl_len:
            continue

        prefix = word_lower[:excl_len]
        if prefix == exclusion_word:
            return False, None, None

        match = generate_variants(prefix, {exclusion_word})
        if match is not None:
            return False, None, None

    for bad_word in BAD_WORDS:
        bad_len = len(bad_word)
        if word_len < bad_len:
            continue

        prefix = word_lower[:bad_len]
        if prefix == bad_word:
            return True, bad_word, BAD_WORDS[bad_word]

        match = generate_variants(prefix, {bad_word})
        if match is not None:
            return True, bad_word, BAD_WORDS[bad_word]

    return False, None, None


def check_sentence_for_bad_words(sentence: str) -> list[tuple[str, str, int]]:
    """
    Перевіряє речення на погані слова
    :param sentence: речення яке перевіряємо
    :return: список усіх поганих слів де на початку саме слова, аналог в словарі та ступінь поганості слова
    """
    bad_found = []
    words = re.findall(r"[a-zA-Zа-яА-ЯіїєґІЇЄҐ0-9@*$#&\^]+|[!?.,:]", sentence)
    seen = set()

    for word in words:
        if word in seen:
            continue
        seen.add(word)

        is_bad, found_word, severity = contains_bad_word(word)
        if is_bad:
            bad_found.append((word, found_word, severity))

    return bad_found


def replace_bad_words(sentence: str) -> str:
    """
    Замінює усі погані слова в реченні на зірочки
    :param sentence: рядок з поганими словами
    :return: рядок з заміненими поганими словами
    """
    bad_words = check_sentence_for_bad_words(sentence)
    for bad_word in bad_words:
        sentence = sentence.replace(bad_word[0], "*" * len(bad_word[0]))

    return sentence
