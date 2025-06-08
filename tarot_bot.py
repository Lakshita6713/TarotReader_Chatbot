# tarot_chatbot.py (fully local, no OpenAI)

from app.intent_classifier import IntentClassifier
from app.draw_engine import TarotDrawEngine
from app.pdf_embedder import TarotPDFEmbedder
from app.response_logic import TarotResponseGenerator

# === Load Components ===
embedder = TarotPDFEmbedder(r"C:\Users\DELL\Summer intern\Newtarotreader\Tarot_reader.pdf")
embedder.build_vector_store()  # One-time per run

classifier = IntentClassifier()
drawer = TarotDrawEngine()
responder = TarotResponseGenerator(embedder)

# === User Interaction ===
if __name__ == "__main__":
    question = input("🔮 Ask your Tarot question: ")
    
    # Step 1: Determine intent (yes_no, timing, insight, diplomatic)
    intent, scores = classifier.classify(question)
    print(f"[DEBUG] Intent: {intent} | Scores: {scores}")

    # Step 2: Draw cards based on intent
    if intent == "timing":
        cards = [drawer.draw_timing_card()]
    elif intent == "yes_no":
        cards = [drawer.draw_card()]
    elif intent == "insight":
        cards = drawer.draw_spread(3)
    else:  # diplomatic
        cards = []

    # Step 3: Generate response
    response = responder.generate(intent, question, cards)

    print("\n===== Tarot Reading =====")
    print(response)
