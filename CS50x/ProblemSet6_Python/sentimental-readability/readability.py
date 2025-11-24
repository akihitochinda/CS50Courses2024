from cs50 import get_string
import re

sentence = get_string("Text: ")
sentence = sentence.split()

words = 0
letters = 0
sentences = 0

for word in sentence:
    # Count words
    words += 1

    # Count letters
    result = re.sub('[^A-Za-z0-9]+', '', word)
    letters += len(result)

    # Count sentences
    delimiters = ['!', '?', '.']
    # if any(delimiter in word for delimiter in delimiters):
    for delimiter in delimiters:
        if delimiter in word:
            sentences += 1

AVERAGE = 100 / words
index = (0.0588 * letters * AVERAGE) - (0.296 * sentences * AVERAGE) - 15.8

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
