# 🤖 Sync AI — Personal Portfolio Virtual Assistant

A lightweight, ultra-modern, and responsive full-stack AI chatbot and virtual assistant engineered for **Pramodya Rathnayaka (Kavishka Pramodya)**. Built with **FastAPI (Python)** and **Vanilla HTML/CSS/JavaScript**, designed to run serverlessly on **Vercel** or locally on any desktop.

---

## ✨ Features & Capabilities

- **⚡ Serverless & Lightweight:** Native support for Vercel Serverless Functions via `@vercel/python`, eliminating the need for expensive 24/7 dedicated servers.
- **🎨 Modern Glassmorphic UI:** Ambient animated backdrop glow, sleek glassmorphism cards, Google Fonts (`Outfit` & `Inter`), custom scrollbars, and interactive micro-animations.
- **🧠 Boundary-Safe Knowledge Engine:** Regex word-boundary pattern matching that accurately answers inquiries about:
  - Background & Information Systems degree at **UCSC**
  - Core Technical Skills (Python, C/C++, Java, JS/TS, Android, Linux, Robotics)
  - Key Projects (Autonomous Micromouse Robot, Salon Management System, Linux Web Server, etc.)
  - Services Offered (Full-Stack Web, Software, Android Apps, AI Chatbot Integrations, UI/UX, IoT)
  - Pricing & Project Rates
  - Current Learning Focus (Fiverr AI Chatbot services)
  - Resume / CV Downloads & Direct Contact Details (Email, LinkedIn, GitHub)
- **💬 Drop-In Floating Widget:** Complete embeddable floating toggle button and modal snippet ready to drop into any portfolio or business website.
- **🌐 Universal CORS:** Zero-configuration Cross-Origin Resource Sharing allowing requests from `file://`, VS Code Live Server, or custom external domains.
- **🟢 Real-Time Health & Status:** Dynamic online/offline indicator, connection retry banner, and typing indicator simulation.

---

## 📁 Repository Structure

```text
my-chatbot/
├── api/
│   └── index.py             # Vercel Serverless Function entrypoint
├── backend/
│   └── main.py              # FastAPI app, knowledge base & local uvicorn runner
├── frontend/
│   ├── index.html           # Standalone chatbot web interface
│   ├── style.css            # Modern glassmorphism CSS styles & animations
│   └── script.js            # Frontend chat logic, dynamic API endpoint resolver
├── portfolio-embed/
│   └── embed-snippet.html   # Copy-paste floating chat widget for portfolio sites
├── requirements.txt         # Python dependencies (fastapi, uvicorn, pydantic)
├── run.bat                  # One-click Windows development launcher
├── vercel.json              # Vercel build and routing configuration
└── README.md                # Project documentation
```

---

## 🚀 How to Run Locally

### Option 1: One-Click Run (Windows)
1. Double-click [**`run.bat`**](file:///e:/my-chatbot/run.bat) in the project root.
2. Dependencies will be installed automatically, and your default web browser will open to:
   👉 **http://127.0.0.1:8000**

---

### Option 2: Manual Terminal Run
1. Open PowerShell or Command Prompt and navigate to the project directory:
   ```bash
   cd e:\my-chatbot
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the FastAPI server:
   ```bash
   python backend\main.py
   ```
   *or:*
   ```bash
   uvicorn backend.main:app --reload
   ```

4. Open your browser and navigate to:
   - **Chatbot Web App:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Interactive API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🌐 Deploying to Vercel (Free Serverless)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Update project documentation"
   git push origin main
   ```

2. **Deploy via Vercel Dashboard:**
   - Log into [Vercel](https://vercel.com/dashboard).
   - Click **Add New > Project** and import the `my-chatbot` repository.
   - Vercel will automatically detect `requirements.txt` and `api/index.py` with the **FastAPI** preset.
   - Click **Deploy**.

3. Once deployed, you will receive a production URL (e.g., `https://my-chatbot-xyz.vercel.app`).

---

## 💼 How to Embed into Your Portfolio Website

To add Sync AI as a bottom-right floating chat bubble on your existing portfolio:

1. Open your portfolio's `index.html` file.
2. Copy the code from [**`portfolio-embed/embed-snippet.html`**](file:///e:/my-chatbot/portfolio-embed/embed-snippet.html).
3. Paste it right before the closing `</body>` tag.
4. Replace `https://your-chatbot.vercel.app` in the `<iframe>` `src` attribute with your live deployed Vercel URL:
   ```html
   <iframe 
       id="ai-chat-iframe" 
       src="https://your-chatbot-url.vercel.app" 
       title="AI Chatbot Assistant"
       allow="clipboard-write">
   </iframe>
   ```

---

## 👨‍💻 Author

**Pramodya Rathnayaka (Kavishka Pramodya)**
- 🎓 Undergraduate in Information Systems — University of Colombo School of Computing (UCSC)
- 📧 Email: [kavishkapramodya2004@gmail.com](mailto:kavishkapramodya2004@gmail.com)
- 💼 LinkedIn: [kavishka-pramodya](https://www.linkedin.com/in/kavishka-pramodya-9bb5b933b/)
- 🐙 GitHub: [Kavishka-Pramodya](https://github.com/Kavishka-Pramodya)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
