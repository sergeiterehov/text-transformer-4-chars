import random
import pickle


class Transformer:
    """
    Глупый трансформер, который работает на чистой статистике.
    Контекст - 4 символа.
    """

    chars: list[str] = []
    prob_4: list[list[list[list[float]]]] = None

    def save(self, file: str):
        print("Saving")

        with open(file, "wb") as f:
            obj = {"prob_4": self.prob_4, "chars": self.chars}
            pickle.dump(obj, f)

        print("Model saved")

    def load(self, file: str):
        print("Loading")

        with open(file, "rb") as f:
            obj = pickle.load(f)
            self.prob_4 = obj["prob_4"]
            self.chars = obj["chars"]

        print("Model loaded")

    def train(self, corpus: str):
        print("Grub chars")

        chars = []

        for i in range(len(corpus)):
            a = corpus[i]

            if not a in chars:
                chars.append(a)

        self.chars = chars

        print("Init model")

        prob_4 = [
            [
                [[0 for _ in range(len(chars))] for _ in range(len(chars))]
                for _ in range(len(chars))
            ]
            for _ in range(len(chars))
        ]

        print("Calculate freq")

        for i in range(len(corpus) - 3):
            a = corpus[i]
            b = corpus[i + 1]
            c = corpus[i + 2]
            d = corpus[i + 3]

            ca = chars.index(a)
            cb = chars.index(b)
            cc = chars.index(c)
            cd = chars.index(d)

            prob_4[ca][cb][cc][cd] += 1

        print("Computing prob")

        for ca in range(len(chars)):
            print(f"{ca} / {len(chars)}")

            for cb in range(len(chars)):
                for cc in range(len(chars)):
                    total = 0

                    for c_ in range(len(chars)):
                        total += prob_4[ca][cb][cc][c_]

                    if total == 0:
                        continue

                    for c_ in range(len(chars)):
                        prob_4[ca][cb][cc][c_] /= total

        print("Clever!")

        self.prob_4 = prob_4

        return self

    def transform(self, text: str, temp=0.9):
        if self.prob_4 is None:
            raise "Transformer is not trained"

        chars = self.chars
        prob_4 = self.prob_4

        ca = chars.index(text[-3])
        cb = chars.index(text[-2])
        cc = chars.index(text[-1])

        prob_1 = prob_4[ca][cb][cc]

        rand_1 = prob_1[:]
        random.shuffle(rand_1)
        rand_1.sort()
        rand_1.reverse()

        total = 0
        rand = random.random() * temp
        for c_ in range(len(prob_1)):
            total += prob_1[c_]

            if rand <= total:
                return chars[c_]

        return ""
