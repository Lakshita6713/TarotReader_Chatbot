# response_logic.py

class TarotResponseGenerator:
    def __init__(self, embedder, timing_dates=None):
        self.embedder = embedder
        self.timing_dates = timing_dates or {}

    def get_meaning(self, card):
        base = card.strip()
        results = self.embedder.search(base, top_k=1)
        return results["documents"][0][0] if results["documents"] else "No info found."

    def yes_no_answer(self, card):
        meaning = self.get_meaning(card)
        meaning_lower = meaning.lower()

        if any(x in meaning_lower for x in ["success", "confidence", "joy", "manifest", "clarity", "love", "yes"]):
            return f"Card Drawn: {card}\nAnswer: Yes\nMeaning: {meaning}"
        elif any(x in meaning_lower for x in ["failure", "destruction", "deception", "blocked", "loss", "no"]):
            return f"Card Drawn: {card}\nAnswer: No\nMeaning: {meaning}"
        else:
            return f"Card Drawn: {card}\nAnswer: Maybe\nMeaning: {meaning}"

    def timing_answer(self, card):
        base = " ".join(card.split()[:2])  # e.g. Cups 5
        date_options = self.timing_dates.get(base, [])
        date = date_options[0] if date_options else "soon"
        return f"Card Drawn: {card}\nEstimated Time: {date}"

    def insight_answer(self, cards, question):
        meanings = [self.get_meaning(card) for card in cards]
        labels = ["Past", "Present", "Future"][:len(cards)]
        result = [f"🔮 Question: {question}\n"]
        for label, card, meaning in zip(labels, cards, meanings):
            result.append(f"{label} – {card}: {meaning}")
        return "\n".join(result)

    def diplomatic_response(self, question):
        return (
            f"This question touches on sensitive matters.\n"
            f"While Tarot offers symbolic guidance, we encourage you to reflect inward or consult a professional for matters like this.\n"
            f"🙏 Question: {question}"
        )

    def generate(self, intent, question, drawn_cards):
        if intent == "diplomatic":
            return self.diplomatic_response(question)
        elif intent == "yes_no":
            return self.yes_no_answer(drawn_cards[0])
        elif intent == "timing":
            return self.timing_answer(drawn_cards[0])
        else:  # insight
            return self.insight_answer(drawn_cards, question)