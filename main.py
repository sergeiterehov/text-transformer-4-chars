import os
from transformer import Transformer

# Температура (больше - точней)
t = 0.995

# Создаем модель
trans = Transformer()

# Читаем корпус текста
corpus = open("samples/corpus_pushkin.txt", "r", encoding="utf-8").read()

# Далее обучаем и сохраняем, или читаем сохраненную модель
model_file = "prob_4.pickle"

if os.path.isfile(model_file):
    trans.load(model_file)
else:
    trans.train(corpus)
    trans.save(model_file)

# Начинаем генерацию
while True:
    text = input(">> ")

    if len(text) < 4:
        text = "".join(trans.chars[: 4 - len(text)]) + text

    for i in range(1024):
        text += trans.transform(text, temp=t)

    print(text)
