# draw_engine.py

import random

class TarotDrawEngine:
    def __init__(self):
        self.major_arcana = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
            "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
            "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
            "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
        ]

        suits = ["Cups", "Wands", "Swords", "Pentacles"]
        numbers = [str(i) for i in range(1, 11)]
        self.minor_arcana = [f"{suit} {num}" for suit in suits for num in numbers]
        self.full_deck = self.major_arcana + self.minor_arcana

    def draw_card(self):
        card = random.choice(self.full_deck)
        orientation = random.choice(["Upright", "Reversed"])
        return f"{card} {orientation}"

    def draw_spread(self, n=3):
        drawn = random.sample(self.full_deck, n)
        return [f"{card} {random.choice(['Upright', 'Reversed'])}" for card in drawn]

    def draw_timing_card(self):
        card = random.choice(self.minor_arcana)
        orientation = random.choice(["Upright", "Reversed"])
        return f"{card} {orientation}"