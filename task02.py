import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests

import matplotlib.pyplot as plt


def visualize_top_words(word_counts, top_n=10):
    # Сортуємо слова за частотою використання
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    # Вибираємо топ N слів
    top_words = sorted_words[:top_n]

    # Розділяємо слова та їх частоти для графіка
    words, counts = zip(*top_words)

    # Створення графіка
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="blue")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.title(f"Топ {top_n} слів у тексті")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None


# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


if __name__ == "__main__":
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        # search_words = ['war', 'peace', 'love']
        search_words = []
        result = map_reduce(text, search_words)

        print("Результат підрахунку слів:", result)
        # Візуалізація топ слів
        visualize_top_words(result, top_n=10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
