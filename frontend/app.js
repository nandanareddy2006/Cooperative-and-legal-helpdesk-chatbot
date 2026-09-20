const API_URL = "http://127.0.0.1:8000";
const CHAT_ENDPOINT = "/chat";

const input = document.getElementById("message");
const send = document.getElementById("send");
const conversation = document.querySelector(".conversation");
const languageSelect = document.getElementById("language");

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function appendUserMessage(text) {
    const userMsg = document.createElement("div");
    userMsg.className = "user-msg";
    userMsg.innerHTML = `
        <div class="avatar">M</div>
        <div class="bubble user-bubble">
            ${escapeHtml(text)}
            <small>${getCurrentTime()}</small>
        </div>
    `;
    conversation.appendChild(userMsg);
    userMsg.scrollIntoView({ behavior: "smooth", block: "end" });
}

function appendLoadingBotMessage() {
    const botMsg = document.createElement("div");
    botMsg.className = "bot-msg";
    botMsg.id = "bot-loading-msg";
    botMsg.innerHTML = `
        <div class="mini-bot">🤖</div>
        <div>
            <div class="bubble bot-bubble" style="font-style: italic; color: #5a7374;">
                Consulting legal documents and thinking...
                <small>${getCurrentTime()}</small>
            </div>
        </div>
    `;
    conversation.appendChild(botMsg);
    botMsg.scrollIntoView({ behavior: "smooth", block: "end" });
    return botMsg;
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function formatBotAnswer(answer, category) {
    let formatted = escapeHtml(answer).replace(/\n/g, "<br>");
    let categoryBadge = "";
    if (category && category !== "GENERAL") {
        categoryBadge = `<span style="display:inline-block; margin-bottom: 6px; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; background: #dff3e8; color: #004c43;">🏷️ ${escapeHtml(category)}</span><br>`;
    }
    return categoryBadge + formatted;
}

function sendQuestion(text) {
    if (!text || text.trim() === "") return;

    const trimmedText = text.trim();
    appendUserMessage(trimmedText);

    input.value = "";
    input.placeholder = "Type your question here...";

    const loadingElem = appendLoadingBotMessage();

    fetch(API_URL + CHAT_ENDPOINT, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: trimmedText,
            question: trimmedText,
            jurisdiction: "Telangana",
            language: languageSelect ? languageSelect.value : "English"
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }
        return response.json();
    })
    .then(data => {
        const answer = data.answer || data.response || "No response received.";
        const category = data.category || "";

        if (loadingElem && loadingElem.parentNode) {
            loadingElem.innerHTML = `
                <div class="mini-bot">🤖</div>
                <div>
                    <div class="bubble bot-bubble" style="white-space: normal; line-height: 1.6;">
                        ${formatBotAnswer(answer, category)}
                        <small>${getCurrentTime()}</small>
                    </div>
                </div>
            `;
            loadingElem.scrollIntoView({ behavior: "smooth", block: "end" });
        }
    })
    .catch(error => {
        console.error(error);
        if (loadingElem && loadingElem.parentNode) {
            loadingElem.innerHTML = `
                <div class="mini-bot">🤖</div>
                <div>
                    <div class="bubble bot-bubble" style="color: #b3261e; background: #fdf2f2; border-color: #f5c2c7;">
                        ⚠️ Unable to reach backend server. Please verify the FastAPI backend is running on <code>http://127.0.0.1:8000</code>.
                        <small>${getCurrentTime()}</small>
                    </div>
                </div>
            `;
            loadingElem.scrollIntoView({ behavior: "smooth", block: "end" });
        }
    });
}

/* QUICK CARDS & INFO BUTTONS */
document.querySelectorAll("[data-question]").forEach(button => {
    button.addEventListener("click", () => {
        sendQuestion(button.dataset.question);
    });
});

/* SEND BUTTON */
send.addEventListener("click", () => {
    sendQuestion(input.value);
});

/* ENTER TO SEND (Shift+Enter for newline) */
input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion(input.value);
    }
});

/* PROCEDURE BUTTON */
const nextStepBtn = document.getElementById("nextStep");
if (nextStepBtn) {
    nextStepBtn.addEventListener("click", () => {
        alert(
            "Step 2: Please keep relevant notices, receipts, membership records and other evidence ready."
        );
    });
}