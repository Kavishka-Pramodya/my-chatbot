# 🤖 Modern AI Chatbot

A responsive, ultra-modern full-stack AI customer support chatbot built with **FastAPI (Python)** and **Vanilla HTML/CSS/JS**.

---

## 🚀 How to Run / ක්‍රියාත්මක කරන ආකාරය

### ක්‍රමය 1: One-Click Run (ලෙහෙසිම ක්‍රමය - Windows)
1. Project folder එකේ ඇති `run.bat` file එක **Double Click** කරන්න.
2. අවශ්‍ය dependencies automatically install වී default browser එකේ `http://127.0.0.1:8000` auto-open වේ.

---

### ක්‍රමය 2: Terminal / Command Prompt මගින් (Manual Run)
1. Terminal එකක් (PowerShell හෝ CMD) open කර project directory එකට යන්න:
   ```bash
   cd e:\my-chatbot
   ```

2. Dependencies install කරන්න:
   ```bash
   pip install -r requirements.txt
   ```

3. Backend server එක start කරන්න:
   ```bash
   python backend\main.py
   ```
   *හෝ:*
   ```bash
   uvicorn backend.main:app --reload
   ```

4. Browser එකෙන් පහත link එක open කරන්න:
   👉 **http://127.0.0.1:8000**

---

## 🛠️ Features & Improvements Made
- **Full-Stack Single Server**: Backend එකෙන්ම frontend static files automatically serve කරයි.
- **Universal CORS Support**: `file://`, VS Code Live Server (`http://localhost:5500`), හෝ FastAPI direct port 8000 ඕනෑම එකකින් බාධාවකින් තොරව ක්‍රියා කරයි.
- **Real-Time Health Status**: Backend එක online ද offline ද යන්න header එකේ සහ banner එකේ පෙන්වයි.
- **Modern Glassmorphic UI**: Ambient glow backgrounds, Google Fonts (Outfit & Inter), සහ smooth animations.
- **Quick Action Chips**: එක click එකකින් සාමාන්‍ය ප්‍රශ්න (Hello, Services, Pricing, Contact) ඇසීමට buttons.
- **Interactive Typing Indicator**: Bot එක පිළිතුරු සපයන තුරු animated bouncing dots පෙන්වයි.
- **UTF-8 Console Safe**: Windows cmd / powershell වල unicode / emojis නිසා ඇතිවන errors fix කර ඇත.
- **Vercel Serverless Ready**: `vercel.json` සහ `api/index.py` මගින් zero-configuration Vercel deployment සහාය දක්වයි.

---

## 🌐 Vercel Deployment & Portfolio Integration (Option 2)

### 1. Chatbot එක Vercel වෙත Deploy කිරීම:
1. මෙම `my-chatbot` repository එක ඔබගේ GitHub ගිණුමට push කරන්න.
2. [Vercel Dashboard](https://vercel.com/dashboard) වෙත ගොස් **Add New > Project** තෝරන්න.
3. `my-chatbot` repository එක import කර **Deploy** කරන්න.
4. Deployment එක අවසන් වූ පසු ඔබට URL එකක් ලැබේ (උදා: `https://my-chatbot.vercel.app`).

### 2. Portfolio Website එකට Chatbot එක Embed කිරීම:
ඔබගේ portfolio project එකෙහි `index.html` file එකේ `</body>` tag එකට පෙර [`portfolio-embed/embed-snippet.html`](file:///e:/my-chatbot/portfolio-embed/embed-snippet.html) හි ඇති code එක paste කරන්න. එහි ඇති `src="https://your-chatbot.vercel.app"` කොටස ඔබගේ සැබෑ Vercel URL එකට වෙනස් කරන්න.
