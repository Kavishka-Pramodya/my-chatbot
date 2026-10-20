import os
import sys

# Ensure UTF-8 output on Windows consoles to prevent cp1252 charmap encoding errors
if sys.platform.startswith("win"):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="Chatbot Backend API",
    description="Backend API for customer support chatbot",
    version="1.0.0"
)

# Allow all origins so the chatbot can be accessed from any port, Live Server, or file://
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.get("/api/health")
@app.get("/health")
def health_check():
    return {"status": "online", "message": "Chatbot backend is healthy and running."}

@app.post("/api/chat")
@app.post("/chat")
def chat(data: ChatMessage):
    question = (data.message or "").strip().lower()

    if not question:
        return {"reply": "Please type a message so I can assist you."}

    # Common greetings (English, Sinhala, Singlish)
    if any(greet in question for greet in ["hello", "hi", "hey", "ayubowan", "kohomada", "halo", "morning", "evening"]):
        answer = "Hello there! 👋 Welcome. How can I help you today? You can ask about our services, pricing, or contact info."
    
    # Services
    elif any(srv in question for srv in ["service", "services", "monawada karanne", "mokakda karanne", "what do you do", "offer"]):
        answer = "We specialize in modern web application development, AI chatbot integrations, mobile apps, and custom cloud solutions! 🚀"
    
    # Pricing
    elif any(prc in question for prc in ["price", "pricing", "cost", "gaana", "gana keeyada", "rates", "how much", "quotation"]):
        answer = "Our pricing is flexible and customized based on your project requirements. Feel free to contact our team for a free quote!"
    
    # Contact information
    elif any(cnt in question for cnt in ["contact", "call", "email", "phone", "reach", "whatsapp", "address", "location"]):
        answer = "You can contact us via email at contact@mychatbot.com or call/WhatsApp at +94 77 123 4567. We'd love to chat!"
    
    # About / Who are you
    elif any(abt in question for abt in ["who are you", "what is this", "oyaa kawda", "about you", "ai assistant", "your name"]):
        answer = "I am Sync AI, an intelligent virtual assistant designed to assist you with quick answers and guide you through our services! 🤖"
    
    # Help
    elif any(hlp in question for hlp in ["help", "udaw", "support", "assist"]):
        answer = "I'm here to assist you! Try asking:\n• 'What services do you provide?'\n• 'How much does it cost?'\n• 'How can I contact your team?'"
    
    # Appreciation / Thanks
    elif any(thx in question for thx in ["thank", "thanks", "sthuthi", "bohoma sthuthi", "great", "awesome"]):
        answer = "You're very welcome! Let me know if you need anything else. 😊"
    
    # Farewell
    elif any(bye in question for bye in ["bye", "goodbye", "see you", "gihin ennam", "tata"]):
        answer = "Goodbye! Have a wonderful day ahead! Feel free to come back anytime. 👋"
    
    # Default fallback
    else:
        answer = "Thank you for reaching out! I'm still learning, but you can ask about our services, pricing, or contact details, or leave your query for our support team."

    return {"reply": answer}

# Mount frontend directory to serve the UI directly from FastAPI at http://127.0.0.1:8000/
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn

    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    print("=" * 60)
    print("🤖 Chatbot Server is starting...")
    print("👉 Open your browser at: http://127.0.0.1:8000")
    print("👉 Swagger API Docs at:   http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir=current_dir)
