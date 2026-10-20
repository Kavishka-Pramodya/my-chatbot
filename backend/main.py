import os
import sys
import re

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
    title="Sync AI - Personal Portfolio Assistant",
    description="Virtual Assistant for Pramodya Rathnayaka (Kavishka Pramodya)",
    version="2.0.0"
)

# Universal CORS to allow seamless embedding from portfolio websites
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

def match_any(text: str, patterns: list) -> bool:
    """Matches any phrase or keyword using regex word boundaries to avoid false positives."""
    for p in patterns:
        escaped = re.escape(p).replace(r"\ ", r"\s+")
        if re.search(r"(?:\b|^)" + escaped + r"(?:\b|$)", text, re.IGNORECASE):
            return True
    return False

@app.get("/api/health")
@app.get("/health")
def health_check():
    return {"status": "online", "message": "Sync AI backend is active and healthy."}

@app.post("/api/chat")
@app.post("/chat")
def chat(data: ChatMessage):
    question = (data.message or "").strip().lower()

    if not question:
        return {"reply": "Please feel free to ask a question about Pramodya's projects, skills, or how to get in touch!"}

    # ---------------------------------------------------------
    # 1. SPECIFIC FEATURED PROJECTS (Priority)
    # ---------------------------------------------------------
    # 1a. Autonomous Micromouse Robot
    if match_any(question, ["micromouse", "maze solving", "maze-solving", "robot project", "embedded project", "robotics"]):
        answer = "Autonomous Micromouse Robot (v1.0) 🤖: An autonomous maze-solving robot engineered with real-time sensor processing, custom algorithms, and embedded C/C++.\n👉 GitHub: https://github.com/Kavishka-Pramodya/Micro-Mouse-Robot-Version-1.0"

    # 1b. Salon Management & Booking System
    elif match_any(question, ["salon", "salon booking", "salon management", "booking system"]):
        answer = "Salon Management & Booking System 💇‍♂️: A full-stack web application designed for appointment scheduling, real-time slot booking, and client management.\n👉 GitHub: https://github.com/Kavishka-Pramodya/Salon-Booking-System"

    # 1c. Linux Web Server Project
    elif match_any(question, ["linux server", "http server", "multi-process", "linux project", "socket programming"]):
        answer = "Multi-Process HTTP Web Server 🐧: A high-concurrency network server built on Linux using multi-processing architecture and network sockets.\n👉 GitHub: https://github.com/Kavishka-Pramodya/Linux-Server-Project"

    # 1d. Mobile Text Editor
    elif match_any(question, ["text editor", "mad project", "mobile text", "editor app", "android project"]):
        answer = "Modern Mobile Text Editor (MAD Project) 📱: A lightweight, responsive Android mobile text editor engineered for fast editing on mobile devices.\n👉 GitHub: https://github.com/Kavishka-Pramodya/MAD-Mini-Project"

    # 1e. Circulatory System Simulation
    elif match_any(question, ["circulatory", "biology simulation", "blood circulation", "simulation"]):
        answer = "Circulatory System Simulation 🫀: An interactive computational simulation written in C++ modeling biological blood circulation dynamics.\n👉 GitHub: https://github.com/Kavishka-Pramodya/circulatory-system-simulation"

    # ---------------------------------------------------------
    # 2. RESUME / CV
    # ---------------------------------------------------------
    elif match_any(question, ["resume", "cv", "curriculum vitae", "biodata", "profile pdf"]):
        answer = "📄 You can download Pramodya's complete Resume/CV directly from the '#resume' section on this portfolio, or email him at kavishkapramodya2004@gmail.com for a direct copy."

    # ---------------------------------------------------------
    # 3. SERVICES OFFERED / FREELANCE
    # ---------------------------------------------------------
    elif match_any(question, [
        "services", "service", "what services", "what do you offer", "what services do you offer",
        "what services do you provide", "what do you do", "offer", "freelance services",
        "what can you build", "services offered", "services monawada", "monawada karanne",
        "web hadanna", "software hadanna", "post design", "chatbot hadanna"
    ]):
        answer = (
            "Pramodya offers a versatile range of freelance & software services, including:\n"
            "• 🌐 Full-Stack Web Development (Custom business sites, portfolios & web apps)\n"
            "• 💻 Custom Software Development (Tailored software & system solutions)\n"
            "• 🤖 AI & Interactive Chatbot Integration (For customer engagement & websites)\n"
            "• 📱 Android Mobile App Development\n"
            "• 🎨 UI/UX & Graphic/Post Designing (Branding & social media creatives)\n"
            "• 🔌 IoT & Embedded Systems Prototyping\n\n"
            "Have a project in mind? Contact Pramodya at kavishkapramodya2004@gmail.com to discuss your requirements!"
        )

    # ---------------------------------------------------------
    # 4. PRICING / RATES / CHARGING / QUOTATION
    # ---------------------------------------------------------
    elif match_any(question, [
        "how much do you charge", "how much", "how much does it cost", "charge",
        "charging", "price", "pricing", "rates", "cost", "costing", "quote",
        "quotation", "budget", "fees", "fee", "gaana", "gana keeyada", "mudal", "mila"
    ]):
        answer = (
            "Pramodya's pricing is flexible, competitive, and tailored to the scope and requirements of each project:\n"
            "• 💼 Project-based: Fixed pricing based on deliverables (Websites, Apps, Chatbots, Designs)\n"
            "• ⏱️ Hourly / Milestone rates: For ongoing development and maintenance\n\n"
            "To get an accurate estimate or free consultation, feel free to reach out to Pramodya at kavishkapramodya2004@gmail.com with your project details!"
        )

    # ---------------------------------------------------------
    # 5. HIRING / INTERNSHIPS / FREELANCE / AVAILABILITY
    # ---------------------------------------------------------
    elif match_any(question, ["hire", "hiring", "intern", "internship", "internships", "job", "vacancy", "available", "recruit", "freelance", "contract", "work with", "wadata ganna"]):
        answer = "Pramodya is actively available for Software Engineering & Embedded Systems Internships, Junior Developer roles, and freelance projects! 💼 Feel free to email him at kavishkapramodya2004@gmail.com or connect via LinkedIn: https://www.linkedin.com/in/kavishka-pramodya-9bb5b933b/"

    # ---------------------------------------------------------
    # 4. TECHNICAL SKILLS & STACK
    # ---------------------------------------------------------
    elif match_any(question, ["skills", "skill", "tech stack", "technologies", "languages", "c++", "python", "java", "typescript", "frameworks", "tools", "danna dewal"]):
        answer = "Pramodya's core technical skills include:\n• Languages: Python, C/C++, Java, JavaScript, TypeScript\n• Web & APIs: Full-Stack Web Development, FastAPI, REST APIs, HTML5, CSS3, Modern UI/UX\n• Mobile & Systems: Android Development, Linux Server Architecture, Multi-processing\n• Embedded: Microcontrollers, Sensor Integration & Maze-solving Algorithms."

    # ---------------------------------------------------------
    # 5. ALL PROJECTS (General)
    # ---------------------------------------------------------
    elif match_any(question, ["projects", "project", "github repos", "repositories", "work", "monawada karapu"]):
        answer = "Pramodya has engineered several impressive projects:\n1. Autonomous Micromouse Robot (Embedded C++)\n2. Salon Management & Booking System (Full-Stack)\n3. Multi-Process Linux Web Server (C/Sockets)\n4. Mobile Text Editor App (Android)\n5. Circulatory System Simulation (C++)\n👉 Explore all repositories: https://github.com/Kavishka-Pramodya"

    # ---------------------------------------------------------
    # 6. CONTACT & SOCIAL PROFILES
    # ---------------------------------------------------------
    elif match_any(question, ["contact", "email", "phone", "linkedin", "github", "reach", "connect", "message", "whatsapp", "call"]):
        answer = "You can easily connect with Pramodya via:\n• 📧 Email: kavishkapramodya2004@gmail.com\n• 💼 LinkedIn: https://www.linkedin.com/in/kavishka-pramodya-9bb5b933b/\n• 🐙 GitHub: https://github.com/Kavishka-Pramodya\nHe looks forward to speaking with you!"

    # ---------------------------------------------------------
    # 7. EDUCATION / UNIVERSITY / DEGREE
    # ---------------------------------------------------------
    elif match_any(question, [
        "where do you study", "where does pramodya study", "where does he study",
        "where do they study", "study", "studying", "university", "campus", "degree",
        "education", "undergraduate", "ucsc", "colombo school of computing",
        "college", "academic", "koheda igena ganne", "mona campus", "degree eka"
    ]):
        answer = "Pramodya is currently an undergraduate pursuing his Bachelor's Degree in Information Systems at the University of Colombo School of Computing (UCSC) 🎓."

    # ---------------------------------------------------------
    # 8. CURRENT FOCUS / LEARNING / WORKING ON (FIVERR & AI CHATBOTS)
    # ---------------------------------------------------------
    elif match_any(question, [
        "what are you currently learning or working on", "what are you currently learning",
        "what are you currently working on", "currently learning", "currently working on",
        "what are you learning", "what are you working on", "what are you doing now",
        "current focus", "learning now", "working on now", "fiverr", "freelancing",
        "dan monawada karanne", "dan mokada karanne", "igena ganne monawada"
    ]):
        answer = (
            "Currently, Pramodya is actively mastering AI Chatbot development—specializing in how to build and deliver cutting-edge AI Chatbot solutions on freelancing platforms like Fiverr 🚀.\n\n"
            "Alongside his Information Systems degree at UCSC, he is deeply exploring conversational AI architectures, custom API integrations, and practical automation tools for international clients!"
        )

    # ---------------------------------------------------------
    # 9. ABOUT PRAMODYA RATHNAYAKA
    # ---------------------------------------------------------
    elif match_any(question, ["who is pramodya", "who is kavishka", "about pramodya", "about him", "tell me about", "introduce", "kawda pramodya", "pramodya kawda", "pramodya gana", "who is he"]):
        answer = "Pramodya Rathnayaka (Kavishka Pramodya) is an Information Systems undergraduate at UCSC (University of Colombo School of Computing) and Robotics & Embedded Systems enthusiast based in Sri Lanka. He builds practical full-stack applications, mobile apps, and autonomous robotics hardware."

    # ---------------------------------------------------------
    # 8. ABOUT SYNC AI (BOT IDENTITY)
    # ---------------------------------------------------------
    elif match_any(question, ["who are you", "what is sync ai", "your name", "what is your name", "oyaa kawda", "mokakda me"]):
        answer = "I am Sync AI 🤖, the personal virtual assistant for Pramodya Rathnayaka. I'm here to represent his portfolio, guide you through his projects, and connect you with him!"

    # ---------------------------------------------------------
    # 9. LOCATION
    # ---------------------------------------------------------
    elif match_any(question, ["location", "where is he", "country", "where do you live", "sri lanka", "city"]):
        answer = "Pramodya is based in Sri Lanka 🇱🇰, and is open to local opportunities as well as remote roles worldwide."

    # ---------------------------------------------------------
    # 10. GREETINGS (English & Sinhala)
    # ---------------------------------------------------------
    elif match_any(question, ["hello", "hi", "hey", "halo", "greetings", "good morning", "good evening", "good afternoon"]):
        answer = "Hello there! 👋 I'm Sync AI, personal assistant to Pramodya Rathnayaka. How can I help you explore his work, skills, or projects today?"

    elif match_any(question, ["ayubowan", "kohomada"]):
        answer = "ආයුබෝවන්! 🙏 මම ප්‍රමෝද්‍ය රත්නායකගේ පුද්ගලික AI සහයක (Sync AI). ප්‍රමෝද්‍යගේ projects, තාක්ෂණික කුසලතා (skills) හෝ සම්බන්ධ කරගත හැකි ආකාරය පිළිබඳ ඕනෑම දෙයක් අසන්න!"

    # ---------------------------------------------------------
    # 11. GRATITUDE & FAREWELL
    # ---------------------------------------------------------
    elif match_any(question, ["thank you", "thanks", "sthuthi", "bohoma sthuthi", "great", "awesome", "good"]):
        answer = "You're very welcome! 😊 Feel free to explore the rest of Pramodya's portfolio or leave a message."

    elif match_any(question, ["bye", "goodbye", "see you", "gihin ennam", "tata"]):
        answer = "Goodbye! 👋 Thank you for visiting Pramodya's portfolio. Have a wonderful day ahead!"

    # ---------------------------------------------------------
    # 12. DEFAULT FALLBACK
    # ---------------------------------------------------------
    else:
        answer = "Thanks for asking! I'm here to assist with Pramodya Rathnayaka's portfolio. You can ask about his projects (like Micromouse or Salon Booking), technical skills, resume, or how to contact him for internships and projects."

    return {"reply": answer}

# Mount frontend directory to serve UI directly from FastAPI at http://127.0.0.1:8000/
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn

    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    print("=" * 60)
    print("🤖 Sync AI - Personal Assistant for Pramodya Rathnayaka")
    print("👉 Portfolio Chatbot: http://127.0.0.1:8000")
    print("👉 API Docs:          http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir=current_dir)
