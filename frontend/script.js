// ==========================================================================
// DOM Elements
// ==========================================================================
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatForm = document.getElementById("chatForm");
const typingIndicator = document.getElementById("typingIndicator");
const clearChatBtn = document.getElementById("clearChatBtn");
const statusDot = document.getElementById("statusDot");
const headerStatusText = document.getElementById("headerStatusText");
const connectionBanner = document.getElementById("connectionBanner");
const connectionBannerText = document.getElementById("connectionBannerText");
const retryConnectionBtn = document.getElementById("retryConnectionBtn");
const suggestionChips = document.getElementById("suggestionChips");

// ==========================================================================
// API Configuration
// ==========================================================================
// Dynamically resolve backend endpoint (works locally and in production on Vercel)
const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const isFileProtocol = window.location.protocol === "file:";

const BACKEND_BASE = (isFileProtocol || (isLocalhost && window.location.port !== "8000"))
    ? "http://127.0.0.1:8000"
    : window.location.origin;

const CHAT_ENDPOINT = `${BACKEND_BASE}/api/chat`;
const HEALTH_ENDPOINT = `${BACKEND_BASE}/api/health`;

// ==========================================================================
// Utility Functions
// ==========================================================================
function formatCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}

function setOnlineState(isOnline, customMessage = "") {
    if (isOnline) {
        statusDot.className = "status-indicator online";
        statusDot.title = "Online";
        headerStatusText.textContent = customMessage || "Online • Ready to assist";
        connectionBanner.style.display = "none";
    } else {
        statusDot.className = "status-indicator offline";
        statusDot.title = "Offline";
        headerStatusText.textContent = "Offline • Backend not connected";
        connectionBanner.style.display = "flex";
        if (customMessage) {
            connectionBannerText.textContent = customMessage;
        }
    }
}

// Check backend connectivity
async function checkBackendHealth() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);

        const response = await fetch(HEALTH_ENDPOINT, {
            method: "GET",
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (response.ok) {
            setOnlineState(true);
            return true;
        } else {
            setOnlineState(false, "Backend returned an unexpected status.");
            return false;
        }
    } catch (err) {
        setOnlineState(false, "Backend server is offline. Please run 'run.bat' or 'python backend/main.py'.");
        return false;
    }
}

// ==========================================================================
// Chat Logic
// ==========================================================================
function addMessage(messageText, sender = "bot") {
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("message");
    messageContainer.classList.add(sender === "user" ? "user-message" : "bot-message");

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");
    contentDiv.textContent = messageText;

    const timeSpan = document.createElement("span");
    timeSpan.classList.add("message-time");
    timeSpan.textContent = formatCurrentTime();

    messageContainer.appendChild(contentDiv);
    messageContainer.appendChild(timeSpan);

    chatMessages.appendChild(messageContainer);
    scrollToBottom();
}

function showTypingIndicator() {
    typingIndicator.style.display = "flex";
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = "none";
}

async function handleSendMessage(customText = null) {
    const rawText = customText !== null ? customText : messageInput.value;
    const message = (rawText || "").trim();

    if (!message || sendButton.disabled) {
        return;
    }

    // Hide suggestion chips after the first user interaction to keep UI clean
    if (suggestionChips && suggestionChips.style.display !== "none") {
        suggestionChips.style.display = "none";
    }

    // Add user message to UI
    addMessage(message, "user");

    // Clear input & disable buttons during transmission
    messageInput.value = "";
    sendButton.disabled = true;
    messageInput.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch(CHAT_ENDPOINT, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();
        hideTypingIndicator();

        const botReply = data.reply || "Sorry, I couldn't generate a response.";
        addMessage(botReply, "bot");
        setOnlineState(true);

    } catch (error) {
        console.error("Chat error:", error);
        hideTypingIndicator();
        setOnlineState(false, "Connection error. Make sure the backend server is running.");
        
        addMessage(
            "⚠️ Unable to reach the backend server. Please make sure the Python server is running (e.g., run `python backend/main.py` or double-click `run.bat`).",
            "bot"
        );
    } finally {
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

// ==========================================================================
// Event Listeners
// ==========================================================================

// Form submit / Send button click
chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleSendMessage();
});

// Clear conversation
clearChatBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to clear the conversation?")) {
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    Conversation cleared. How can I help you today?
                </div>
                <span class="message-time">${formatCurrentTime()}</span>
            </div>
            <div class="suggestion-chips" id="suggestionChips">
                <button type="button" class="chip" data-prompt="Hello!">👋 Say Hello</button>
                <button type="button" class="chip" data-prompt="What services do you provide?">🚀 Services</button>
                <button type="button" class="chip" data-prompt="How much does it cost?">💰 Pricing</button>
                <button type="button" class="chip" data-prompt="How can I contact you?">📞 Contact</button>
            </div>
        `;
        attachChipListeners();
    }
});

// Suggestion chips handler
function attachChipListeners() {
    document.querySelectorAll(".chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            const prompt = chip.getAttribute("data-prompt");
            if (prompt) {
                handleSendMessage(prompt);
            }
        });
    });
}
attachChipListeners();

// Retry connection button
retryConnectionBtn.addEventListener("click", async () => {
    retryConnectionBtn.textContent = "Checking...";
    await checkBackendHealth();
    retryConnectionBtn.textContent = "Retry";
});

// Initial health check on page load
window.addEventListener("DOMContentLoaded", () => {
    checkBackendHealth();
    messageInput.focus();
});
