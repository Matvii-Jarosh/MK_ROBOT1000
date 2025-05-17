# MK_ROBOT1000 

**MK_ROBOT1000** — це інструмент для автоматичного виявлення та фільтрації образливих слів у тексті з підтримкою замін символів (наприклад, "7уп0" → "тупо").

## Встановлення

1. Клонуйте репозиторій:
```commandline
   git clone https://github.com/Matvii-Jarosh/MK_ROBOT1000.git
   cd MK_ROBOT1000
```

2. Встановіть залежності (якщо потрібно):
```commandline
   pip install -r requirements.txt
 ```

## Використання

### Основна функція
```python
from mk_robot1000 import contains_bad_word, check_sentence_for_bad_words

result, matched_word, severity = contains_bad_word("п@р@ша")
print(result)

bad_words = check_sentence_for_bad_words("Ти 7упий, та ти l0$3r")

if bad_words:
    reply_lines = [" Знайдено погані слова!"]

    for original_word, bad_word_matched, severity in bad_words:
        line = f"* `{original_word}` -> схоже на `{bad_word_matched}` (!!! рівень {severity})"
        print(line)
```

## Ліцензія
MIT License