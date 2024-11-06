import random
import pickle


class Transformer:
    """
    Глупый трансформер, который работает на чистой статистике.
    Контекст - 4 символа.
    """

    tokens: list[str] = []
    weights: list[float] = None

    def save(self, file: str):
        print("Сохраняем модель")

        with open(file, "wb") as f:
            obj = {"prob_4": self.weights, "tokens": self.tokens}
            pickle.dump(obj, f)

        print("Готово")

    def load(self, file: str):
        print("Загружаем модель")

        with open(file, "rb") as f:
            obj = pickle.load(f)
            self.weights = obj["prob_4"]
            self.tokens = obj["tokens"]

        print("Готово")

    def train(self, corpus: str):
        print("Собираем уникальные токены")

        tokens = []

        for i in range(len(corpus)):
            a = corpus[i]

            if not a in tokens:
                tokens.append(a)

        self.tokens = tokens

        print("Инициализируем модель")

        weights = [0 for _ in range(len(tokens) ** 4)]

        print("Считаем частоту групп")

        for i in range(len(corpus) - 3):
            a = corpus[i]
            b = corpus[i + 1]
            c = corpus[i + 2]
            d = corpus[i + 3]

            ca = tokens.index(a)
            cb = tokens.index(b)
            cc = tokens.index(c)
            cd = tokens.index(d)

            weights[
                ca * len(tokens) ** 3 + cb * len(tokens) ** 2 + cc * len(tokens) + cd
            ] += 1

        print("Вычисляем вероятности")

        for c in range(0, len(tokens) ** 4, len(tokens)):
            print(f"\r{int(100 * c / len(tokens) ** 4)}%", end="")

            total = 0

            for i in range(len(tokens)):
                total += weights[c + i]

            if total == 0:
                continue

            for i in range(len(tokens)):
                weights[c + i] /= total

        print("\rОбучен!")

        self.weights = weights

        return self

    def transform(self, text: str, temp=1.0):
        if self.weights is None:
            raise "Трансформер не обучен"

        tokens = self.tokens
        weights = self.weights

        ca = tokens.index(text[-3])
        cb = tokens.index(text[-2])
        cc = tokens.index(text[-1])

        pointer = ca * len(tokens) ** 3 + cb * len(tokens) ** 2 + cc * len(tokens)
        prob_1 = weights[pointer : pointer + len(tokens)]

        rand_1 = prob_1[:]
        random.shuffle(rand_1)
        rand_1.sort()
        # rand_1.reverse()

        total = 0
        rand = min(1.0, random.random() * temp)
        for c_ in range(len(prob_1)):
            total += prob_1[c_]

            if rand <= total:
                return tokens[c_]

        return ""
