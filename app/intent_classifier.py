# intent_classifier.py

from sentence_transformers import SentenceTransformer, util

class IntentClassifier:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

        self.intent_examples = {
            "yes_no": [
                "Will I get the job?", "Should I move?", "Can I trust them?", "Do they love me?"
            ],
            "timing": [
                "When will I get married?", "How long until I succeed?", "What day will I find love?"
            ],
            "insight": [
                "What should I know about this situation?", "What’s blocking me?", "What energy surrounds me?"
            ],
            "diplomatic": [
                "Will I die?", "Will my cancer be cured?", "Is she pregnant?", "When will I die?", "Will my child be okay?"
            ]
        }

        self.embeddings = {
            intent: self.model.encode(examples, convert_to_tensor=True)
            for intent, examples in self.intent_examples.items()
        }

    def classify(self, question):
        query_vec = self.model.encode(question, convert_to_tensor=True)

        scores = {
            intent: max(util.cos_sim(query_vec, embeds).cpu().numpy().flatten())
            for intent, embeds in self.embeddings.items()
        }

        best_intent = max(scores, key=scores.get)
        return best_intent, scores