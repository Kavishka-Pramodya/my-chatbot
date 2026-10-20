import os
import sys
import re
import json
import urllib.request
import urllib.error

# Ensure UTF-8 output on Windows consoles to prevent cp1252 charmap encoding errors
if sys.platform.startswith("win"):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Attempt to load .env file for local development
try:
    from dotenv import load_dotenv
    # Look for .env in current directory and parent directory
    env_paths = [
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    ]
    for p in env_paths:
        if os.path.exists(p):
            load_dotenv(p)
            break
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="Sync AI - Personal Portfolio Assistant",
    description="Virtual Assistant for Pramodya Rathnayaka (Kavishka Pramodya) powered by Google Gemini AI",
    version="3.0.0"
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

# -------------------------------------------------------------
# SYSTEM KNOWLEDGE PROMPT FOR GEMINI AI
# -------------------------------------------------------------
SYSTEM_INSTRUCTION = """
You are "Sync AI", the friendly, knowledgeable, and professional personal AI assistant for Pramodya Rathnayaka (Kavishka Pramodya).
Your goal is to represent Pramodya, showcase his technical skills, guide visitors through his projects, and help potential clients, recruiters, or collaborators connect with him.

ABOUT PRAMODYA:
- Name: Pramodya Rathnayaka (Kavishka Pramodya)
- Education: Information Systems Undergraduate at University of Colombo School of Computing (UCSC), Sri Lanka.
- Role: Full-Stack Developer, AI Chatbot Engineer, and Embedded Robotics Enthusiast.
- Location: Based in Sri Lanka (open to remote opportunities worldwide and local roles).
- Status: Actively open for Software Engineering / Junior roles, Internships, and Freelance AI / Web projects.

KEY PROJECTS:
1. Autonomous Micromouse Robot (v1.0): Maze-solving robot with real-time sensor processing, embedded C/C++, and custom algorithms. GitHub: https://github.com/Kavishka-Pramodya/Micro-Mouse-Robot-Version-1.0
2. Salon Management & Booking System: Full-stack web application for appointment scheduling, real-time slots, and client management. GitHub: https://github.com/Kavishka-Pramodya/Salon-Booking-System
3. Multi-Process Linux Web Server: High-concurrency network server built on Linux with multi-processing and network sockets. GitHub: https://github.com/Kavishka-Pramodya/Linux-Server-Project
4. Modern Mobile Text Editor (MAD Project): Lightweight Android text editor for quick on-the-go editing. GitHub: https://github.com/Kavishka-Pramodya/MAD-Mini-Project
5. Circulatory System Simulation: Computational simulation in C++ modeling biological blood circulation dynamics. GitHub: https://github.com/Kavishka-Pramodya/circulatory-system-simulation

SKILLS & TECH STACK:
- Languages: Python, C/C++, Java, JavaScript, TypeScript, SQL
- Web & Backend: FastAPI, REST APIs, Node.js, HTML5, CSS3, Modern Responsive UI/UX
- AI & Automation: Gemini API, OpenAI GPT, Prompt Engineering, RAG Architectures, Chatbot Deployment, Workflow Automation
- Systems & Mobile: Android App Development, Linux Architecture, Sockets
- Embedded: Microcontrollers, Sensors, Robotics algorithms

FREELANCE & SERVICES OFFERED:
- Full-Stack Web Development (Custom sites, portfolios, business web apps)
- AI & Interactive Chatbot Engineering (Custom AI assistants, LLM integration, Vercel/Cloud deployment)
- Custom Software Development
- Android Mobile App Development
- UI/UX & Graphic/Post Designing
- IoT & Embedded Systems Prototyping

CONTACT DETAILS:
- Email: kavishkapramodya2004@gmail.com
- LinkedIn: https://www.linkedin.com/in/kavishka-pramodya-9bb5b933b/
- GitHub: https://github.com/Kavishka-Pramodya

BEHAVIOR RULES:
- Be warm, polite, and concise. Use emojis naturally where appropriate.
- If the user asks in Sinhala or Singlish, reply naturally in Sinhala/Singlish! If asked in English, reply in English.
- If asked about topics completely unrelated to Pramodya, tech, or business, answer politely and gently bring the focus back to Pramodya's portfolio and projects.
- Keep answers informative yet crisp (around 2-4 sentences or structured bullet points).
"""

def generate_gemini_reply(user_message: str) -> str:
    """Calls Google Gemini API (gemini-3.8-flash) using lightweight standard HTTP."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    # Try fast models in order
    candidate_models = ["gemini-3.5-flash", "gemini-3.1-flash-lite"]

    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_message}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2500
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=18) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "").strip()
                        if text:
                            return text
        except Exception as e:
            print(f"Gemini API request failed for {model}: {e}")
            continue

    return None

# -------------------------------------------------------------
# RULE-BASED FALLBACK (When offline or API unavailable)
# -------------------------------------------------------------
def match_any(text: str, patterns: list) -> bool:
    for p in patterns:
        escaped = re.escape(p).replace(r"\ ", r"\s+")
        if re.search(r"(?:\b|^)" + escaped + r"(?:\b|$)", text, re.IGNORECASE):
            return True
    return False

def get_rule_based_fallback(question: str) -> str:
    q = question.lower()

    if match_any(q, ["micromouse", "maze solving", "maze-solving", "robot project", "embedded project", "robotics"]):
        return "Autonomous Micromouse Robot (v1.0) 🤖: An autonomous maze-solving robot engineered with real-time sensor processing, custom algorithms, and embedded C/C++.\n👉 GitHub: https://github.com/Kavishka-Pramodya/Micro-Mouse-Robot-Version-1.0"

    elif match_any(q, ["salon", "salon booking", "salon management", "booking system"]):
        return "Salon Management & Booking System 💇‍♂️: A full-stack web application designed for appointment scheduling, real-time slot booking, and client management.\n👉 GitHub: https://github.com/Kavishka-Pramodya/Salon-Booking-System"

    elif match_any(q, ["linux server", "http server", "multi-process", "linux project", "socket programming"]):
        return "Multi-Process HTTP Web Server 🐧: A high-concurrency network server built on Linux using multi-processing architecture and network sockets.\n👉 GitHub: https://github.com/Kavishka-Pramodya/Linux-Server-Project"

    elif match_any(q, ["text editor", "mad project", "mobile text", "editor app", "android project"]):
        return "Modern Mobile Text Editor (MAD Project) 📱: A lightweight, responsive Android mobile text editor engineered for fast editing on mobile devices.\n👉 GitHub: https://github.com/Kavishka-Pramodya/MAD-Mini-Project"

    elif match_any(q, ["circulatory", "biology simulation", "blood circulation", "simulation"]):
        return "Circulatory System Simulation 🫀: An interactive computational simulation written in C++ modeling biological blood circulation dynamics.\n👉 GitHub: https://github.com/Kavishka-Pramodya/circulatory-system-simulation"

    elif match_any(q, ["resume", "cv", "curriculum vitae", "biodata", "profile pdf"]):
        return "📄 You can download Pramodya's complete Resume/CV directly from the '#resume' section on his portfolio, or email him at kavishkapramodya2004@gmail.com for a direct copy."

    elif match_any(q, ["services", "service", "what do you offer", "what can you build", "offer", "freelance"]):
        return (
            "Pramodya offers a versatile range of freelance & software services:\n"
            "• 🌐 Full-Stack Web Development (Custom business sites & portfolios)\n"
            "• 🤖 AI & Interactive Chatbot Engineering (Custom Gemini/OpenAI integrations)\n"
            "• 💻 Custom Software & System Development\n"
            "• 📱 Android Mobile App Development\n"
            "• 🎨 UI/UX & Graphic/Post Designing\n\n"
            "Contact Pramodya at kavishkapramodya2004@gmail.com to discuss your project!"
        )

    elif match_any(q, ["skills", "skill", "tech stack", "languages", "python", "c++", "java", "frameworks"]):
        return "Pramodya's technical stack includes:\n• Languages: Python, C/C++, Java, JavaScript, TypeScript, SQL\n• Web & APIs: FastAPI, REST APIs, HTML5, CSS3, Modern Responsive UI/UX\n• AI: Gemini API, OpenAI, Prompt Engineering, RAG\n• Systems & Mobile: Android Development, Linux Sockets, Robotics & Microcontrollers."

    elif match_any(q, ["contact", "email", "phone", "linkedin", "github", "reach", "connect"]):
        return "You can easily connect with Pramodya via:\n• 📧 Email: kavishkapramodya2004@gmail.com\n• 💼 LinkedIn: https://www.linkedin.com/in/kavishka-pramodya-9bb5b933b/\n• 🐙 GitHub: https://github.com/Kavishka-Pramodya"

    elif match_any(q, ["who is pramodya", "who is kavishka", "about him", "about pramodya"]):
        return "Pramodya Rathnayaka (Kavishka Pramodya) is an Information Systems undergraduate at UCSC and a passionate Full-Stack Developer & Robotics enthusiast based in Sri Lanka."

    elif match_any(q, ["hello", "hi", "hey", "greetings"]):
        return "Hello there! 👋 I'm Sync AI, personal assistant to Pramodya Rathnayaka. How can I help you explore his work or skills today?"

    elif match_any(q, ["ayubowan", "kohomada"]):
        return "ආයුබෝවන්! 🙏 මම ප්‍රමෝද්‍ය රත්නායකගේ පුද්ගලික AI සහයක (Sync AI). ප්‍රමෝද්‍යගේ projects හෝ skills පිළිබඳ ඕනෑම දෙයක් අසන්න!"

    else:
        return "Thanks for asking! I'm Sync AI, personal assistant for Pramodya Rathnayaka. You can ask about his projects (Micromouse, Salon Booking, Web Server), technical skills, or how to contact him for projects and internships."

# -------------------------------------------------------------
# FASTAPI ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/health")
@app.get("/health")
def health_check():
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "online",
        "ai_engine": "Google Gemini 3.8 Flash" if has_gemini else "Rule-based Fallback",
        "gemini_active": has_gemini
    }

@app.post("/api/chat")
@app.post("/chat")
def chat(data: ChatMessage):
    question = (data.message or "").strip()

    if not question:
        return {"reply": "Please feel free to ask a question about Pramodya's projects, skills, or how to get in touch!"}

    # 1. Try Google Gemini AI First
    gemini_reply = generate_gemini_reply(question)
    if gemini_reply:
        return {"reply": gemini_reply}

    # 2. Fallback to Rule-based system if API is unavailable or offline
    fallback_reply = get_rule_based_fallback(question)
    return {"reply": fallback_reply}

# Mount frontend directory to serve UI directly at http://127.0.0.1:8000/
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
    print("⚡ Powered by: Google Gemini AI (gemini-3.8-flash)")
    print("👉 Portfolio Chatbot: http://127.0.0.1:8000")
    print("👉 API Docs:          http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir=current_dir)
