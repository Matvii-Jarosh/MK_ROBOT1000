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
import unittest
from MK_ROBOT1000 import *


class TestBadWordDetection(unittest.TestCase):

    def test_clear_sentence(self):
        sentence = "Привіт, як твої справи сьогодні?"
        self.assertEqual(check_sentence_for_bad_words(sentence), [])

    def test_level_1_words(self):
        sentence = "Ти дурень і л*х!"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('дурень', 'дур', 1), result)
        self.assertIn(('л*х', 'лох', 1), result)

    def test_level_2_words(self):
        sentence = "Це блядь і сука!"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('блядь', 'бля', 2), result)
        self.assertIn(('сука', 'сука', 2), result)

    def test_level_3_words(self):
        sentence = "Ти хуйло і підорас!"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('хуйло', 'хуй', 3), result)
        self.assertIn(('підорас', 'підорас', 3), result)

    def test_mixed_level_words(self):
        sentence = "Дебіл, мудак і хуйло"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('Дебіл', 'дебіл', 1), result)
        self.assertIn(('мудак', 'муд', 2), result)
        self.assertIn(('хуйло', 'хуй', 3), result)

    def test_leetspeak_words(self):
        sentence = "Ти л0х, муд@к і х@йло!"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('л0х', 'лох', 1), result)
        self.assertIn(('муд@к', 'муд', 2), result)
        self.assertIn(('х@йло', 'хуй', 3), result)

    def test_english_words(self):
        sentence = "You are idiot and motherfucker!"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('idiot', 'idiot', 2), result)
        self.assertIn(('motherfucker', 'motherfucker', 3), result)

    def test_disguised_english(self):
        sentence = "Y0u 4re 4ssh0le and n1gg3r!"
        result = check_sentence_for_bad_words(sentence)
        self.assertTrue(any(bad == 'ass' and level == 2 for _, bad, level in result))
        self.assertTrue(any(bad == 'nigger' and level == 3 for _, bad, level in result))

    def test_case_insensitivity(self):
        sentence = "Ти ЛоХ, СУКА і ХуЙлО!"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('ЛоХ', 'лох', 1), result)
        self.assertIn(('СУКА', 'сука', 2), result)
        self.assertIn(('ХуЙлО', 'хуй', 3), result)

    def test_max_severity(self):
        sentence = "Це дебіл, мудак і хуйло"
        result = check_sentence_for_bad_words(sentence)
        max_severity = max(level for _, _, level in result)
        self.assertEqual(max_severity, 3)

    def test_exclusion_words(self):
        """Тестуємо слова, які мають бути виключені з перевірки"""
        sentence = "Херсон - гарне місто, а тупик - це кінець вулиці"
        result = check_sentence_for_bad_words(sentence)
        self.assertEqual(result, [])

    def test_exclusion_prefixes(self):
        """Тестуємо слова, які починаються з виключень"""
        sentence = "тупиковий херувим залуплистий"
        result = check_sentence_for_bad_words(sentence)
        self.assertEqual(result, [])

    def test_exclusion_with_bad_words(self):
        """Тестуємо речення з виключеннями та поганими словами разом"""
        sentence = "Херсон - гарне місто, але мешканці - мудаки"
        result = check_sentence_for_bad_words(sentence)
        self.assertIn(('мудаки', 'муд', 2), result)
        self.assertEqual(len(result), 1)

    def test_exclusion_edge_cases(self):
        """Тестуємо граничні випадки з виключеннями"""
        cases = [
            ("тупик", False),
            ("тупиковий", False),
            ("тупік", False),
            ("тупіковий", False),
            ("херсон", False),
            ("херувим", False),
            ("херувими", False),
            ("тупой", True),  # Має бути виявлено
            ("дурень", True),  # Має бути виявлено
            ("херня", True),  # Має бути виявлено
        ]

        for word, should_detect in cases:
            with self.subTest(word=word):
                result = contains_bad_word(word)
                if should_detect:
                    self.assertTrue(result[0], f"Слово '{word}' має бути виявлено")
                else:
                    self.assertFalse(result[0], f"Слово '{word}' не має бути виявлено")

    def test_exclusion_with_leetspeak(self):
        """Тестуємо виключення з leetspeak"""
        sentence = "Х3рсон - гарне місто, т0пік - тема для обговорення"
        result = check_sentence_for_bad_words(sentence)
        self.assertEqual(result, [])

    def test_replace_clean_sentence(self):
        sentence = "Привіт, друже!"
        expected = "Привіт, друже!"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_replace_simple_bad_words(self):
        sentence = "Ти лох і дурень!"
        expected = "Ти *** і ******!"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_replace_with_leetspeak(self):
        sentence = "Ти л0х і х@йло!"
        expected = "Ти *** і *****!"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_case_insensitive_replacement(self):
        sentence = "Ти ЛоХ, СУКА і ХуЙлО!"
        expected = "Ти ***, **** і *****!"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_replace_only_detected(self):
        sentence = "Херсон — чудове місто, але мудаки скрізь"
        expected = "Херсон — чудове місто, але ****** скрізь"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_partial_word_not_replaced(self):
        sentence = "У тупиковому районі жив херувим"
        expected = "У тупиковому районі жив херувим"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_replace_multiple_same_bad_words(self):
        sentence = "Лох! Лох! Лох!"
        expected = "***! ***! ***!"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_punctuation_attached_to_bad_words(self):
        sentence = "Ти лох! Ідіот?"
        expected = "Ти ***! *****?"
        self.assertEqual(replace_bad_words(sentence), expected)

    def test_english_replacement(self):
        sentence = "You are idiot and motherfucker."
        expected = "You are ***** and ************."
        self.assertEqual(replace_bad_words(sentence), expected)


if __name__ == '__main__':
    unittest.main()
