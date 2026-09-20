const API_URL = "http://127.0.0.1:8000";
const CHAT_ENDPOINT = "/chat";

const input = document.getElementById("message");
const send = document.getElementById("send");
const conversation = document.getElementById("conversationArea");
const languageSelect = document.getElementById("language");
const welcomeCard = document.getElementById("welcomeCard");

// Modals & Elements
const grievanceModal = document.getElementById("grievanceModal");
const closeGrievanceModal = document.getElementById("closeGrievanceModal");
const openGrievanceTopBtn = document.getElementById("openGrievanceTopBtn");
const quickGrievanceBtn = document.getElementById("quickGrievanceBtn");
const clipBtn = document.getElementById("clipBtn");
const previewGrievanceBtn = document.getElementById("previewGrievanceBtn");
const downloadGrievancePdfBtn = document.getElementById("downloadGrievancePdfBtn");
const grievancePreviewArea = document.getElementById("grievancePreviewArea");
const grievancePreviewText = document.getElementById("grievancePreviewText");

const procedureModal = document.getElementById("procedureModal");
const closeProcedureModal = document.getElementById("closeProcedureModal");
const procModalTitle = document.getElementById("procModalTitle");
const procModalRef = document.getElementById("procModalRef");
const procedureModalBody = document.getElementById("procedureModalBody");
const downloadProcPdfModalBtn = document.getElementById("downloadProcPdfModalBtn");

let currentSelectedProcId = null;

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(unsafe) {
    if (!unsafe) return "";
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
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
                Consulting statutory provisions under Telangana Cooperative Societies Act, 1964...
                <small>${getCurrentTime()}</small>
            </div>
        </div>
    `;
    conversation.appendChild(botMsg);
    botMsg.scrollIntoView({ behavior: "smooth", block: "end" });
    return botMsg;
}

function formatBotAnswer(data) {
    const answer = data.answer || "No response received.";
    const category = data.category || "GENERAL";
    const procedure = data.procedure;
    const grievance = data.grievance_suggestion;
    const pdfUrl = data.pdf_url;
    const followups = data.suggested_followups || [];

    let categoryBadge = "";
    if (category && category !== "GENERAL") {
        categoryBadge = `<span class="category-badge">🏷️ ${escapeHtml(category)}</span><br>`;
    }

    let formattedText = escapeHtml(answer)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>");

    let actionButtons = "";
    if (pdfUrl) {
        actionButtons += `
            <div class="action-btn-row">
                <button class="pdf-download-btn" onclick="downloadPdfDirect('${pdfUrl}')">
                    📥 Download Official Guide (PDF)
                </button>
            </div>
        `;
    }

    if (grievance) {
        actionButtons += `
            <div class="action-btn-row">
                <button class="btn-primary" onclick="openGrievanceModalWithCategory('${grievance.category_id}')">
                    ✍️ Draft Formal Grievance Representation
                </button>
            </div>
        `;
    }

    let followupHtml = "";
    if (followups.length > 0) {
        const chips = followups.map(f => 
            `<button class="followup-chip" onclick="sendQuestion('${escapeHtml(f)}')">${escapeHtml(f)}</button>`
        ).join("");
        followupHtml = `<div class="followup-container"><span style="font-size: 11px; color:#557872; width:100%;">Suggested follow-ups:</span>${chips}</div>`;
    }

    return categoryBadge + formattedText + actionButtons + followupHtml;
}

function sendQuestion(text) {
    if (!text || text.trim() === "") return;

    const trimmedText = text.trim();
    appendUserMessage(trimmedText);

    input.value = "";
    input.placeholder = "Ask anything about cooperative governance, procedures, or disputes...";

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
        if (loadingElem && loadingElem.parentNode) {
            loadingElem.innerHTML = `
                <div class="mini-bot">🤖</div>
                <div>
                    <div class="bubble bot-bubble" style="white-space: normal; line-height: 1.6;">
                        ${formatBotAnswer(data)}
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

// Download PDF directly from API URL
window.downloadPdfDirect = function(pdfPath) {
    const url = API_URL + (pdfPath.startsWith("/") ? pdfPath : "/" + pdfPath);
    window.open(url, "_blank");
};

// ==========================================
// GRIEVANCE MODAL LOGIC
// ==========================================
function openGrievanceModal() {
    grievanceModal.classList.add("active");
    grievancePreviewArea.style.display = "none";
}

function closeGrievanceModalFn() {
    grievanceModal.classList.remove("active");
}

window.openGrievanceModalWithCategory = function(catId) {
    openGrievanceModal();
    const select = document.getElementById("gCategory");
    if (select && catId) {
        select.value = catId;
    }
};

function getGrievanceFormData() {
    return {
        complainant_name: document.getElementById("gCompName").value.trim(),
        complainant_phone: document.getElementById("gCompPhone").value.trim() || null,
        complainant_address: document.getElementById("gCompAddress").value.trim(),
        complainant_membership_no: document.getElementById("gCompMemNo").value.trim() || null,
        society_name: document.getElementById("gSocName").value.trim(),
        society_reg_no: document.getElementById("gSocRegNo").value.trim() || null,
        society_address: document.getElementById("gSocAddress").value.trim(),
        category_id: document.getElementById("gCategory").value,
        statement_of_facts: document.getElementById("gFacts").value.trim(),
        relief_sought: document.getElementById("gRelief").value.trim() || null,
        jurisdiction: "Telangana"
    };
}

if (previewGrievanceBtn) {
    previewGrievanceBtn.addEventListener("click", () => {
        const formData = getGrievanceFormData();
        if (!formData.complainant_name || !formData.society_name || !formData.statement_of_facts) {
            alert("Please fill in Complainant Name, Society Name, and Statement of Facts.");
            return;
        }

        fetch(API_URL + "/grievance/draft", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        })
        .then(r => r.json())
        .then(data => {
            grievancePreviewText.textContent = data.formal_letter;
            grievancePreviewArea.style.display = "block";
            grievancePreviewArea.scrollIntoView({ behavior: "smooth" });
        })
        .catch(err => {
            alert("Failed to generate preview: " + err.message);
        });
    });
}

if (downloadGrievancePdfBtn) {
    downloadGrievancePdfBtn.addEventListener("click", () => {
        const formData = getGrievanceFormData();
        if (!formData.complainant_name || !formData.society_name || !formData.statement_of_facts) {
            alert("Please fill in Complainant Name, Society Name, and Statement of Facts before downloading.");
            return;
        }

        fetch(API_URL + "/grievance/download-pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) throw new Error("Failed to generate PDF");
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `Grievance_Petition_${formData.complainant_name.replace(/ /g, '_')}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        })
        .catch(err => {
            alert("Failed to download PDF: " + err.message);
        });
    });
}

// ==========================================
// PROCEDURE MODAL LOGIC
// ==========================================
function openProcedureModal(procId) {
    currentSelectedProcId = procId;
    fetch(API_URL + `/procedures/${procId}`)
    .then(r => r.json())
    .then(proc => {
        procModalTitle.textContent = "📋 " + proc.title;
        procModalRef.textContent = proc.act_reference + " | Timeline: " + proc.estimated_days;
        
        let stepsHtml = proc.steps.map(s => `
            <div style="background:#f8fbfa; border:1px solid #d8e8df; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                <strong style="color:#004c43;">Step ${s.step_number}: ${escapeHtml(s.title)}</strong>
                <p style="margin:4px 0 6px; font-size:12px; color:#222;">${escapeHtml(s.description)}</p>
                <small style="color:#087e68; font-weight:600;">💡 ${escapeHtml(s.tips)}</small>
            </div>
        `).join("");

        let docsHtml = proc.required_documents.map((d, i) => `
            <li style="font-size:12px; color:#333; margin-bottom:4px;">${escapeHtml(d)}</li>
        `).join("");

        procedureModalBody.innerHTML = `
            <div>
                <p style="font-size:12px; color:#444; margin-top:0;">${escapeHtml(proc.summary)}</p>
                <h4 style="color:#004c43; margin:10px 0 6px; font-size:13px;">Procedural Steps</h4>
                ${stepsHtml}
                <h4 style="color:#004c43; margin:14px 0 6px; font-size:13px;">Mandatory Documents Checklist</h4>
                <ul style="padding-left:18px; margin:0;">${docsHtml}</ul>
            </div>
        `;

        procedureModal.classList.add("active");
    })
    .catch(err => {
        alert("Failed to load procedure details: " + err.message);
    });
}

function closeProcedureModalFn() {
    procedureModal.classList.remove("active");
}

if (downloadProcPdfModalBtn) {
    downloadProcPdfModalBtn.addEventListener("click", () => {
        if (currentSelectedProcId) {
            window.downloadPdfDirect(`/procedures/${currentSelectedProcId}/download-pdf`);
        }
    });
}

// Attach Event Listeners
if (openGrievanceTopBtn) openGrievanceTopBtn.addEventListener("click", openGrievanceModal);
if (quickGrievanceBtn) quickGrievanceBtn.addEventListener("click", openGrievanceModal);
if (clipBtn) clipBtn.addEventListener("click", openGrievanceModal);
if (closeGrievanceModal) closeGrievanceModal.addEventListener("click", closeGrievanceModalFn);
if (closeProcedureModal) closeProcedureModal.addEventListener("click", closeProcedureModalFn);

// Sidebar Procedure Clicks
document.querySelectorAll("[data-proc]").forEach(btn => {
    btn.addEventListener("click", () => {
        openProcedureModal(btn.dataset.proc);
    });
});

// Quick question & Right panel buttons
document.querySelectorAll("[data-question]").forEach(button => {
    button.addEventListener("click", () => {
        sendQuestion(button.dataset.question);
    });
});

// Send button
send.addEventListener("click", () => {
    sendQuestion(input.value);
});

// Enter key
input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion(input.value);
    }
});

// Header links
const hdrGrievance = document.getElementById("hdrGrievance");
if (hdrGrievance) hdrGrievance.addEventListener("click", openGrievanceModal);

const navGrievance = document.getElementById("navGrievance");
if (navGrievance) navGrievance.addEventListener("click", openGrievanceModal);

const navProcedures = document.getElementById("navProcedures");
if (navProcedures) navProcedures.addEventListener("click", () => openProcedureModal("registration"));

const hdrProcedures = document.getElementById("hdrProcedures");
if (hdrProcedures) hdrProcedures.addEventListener("click", () => openProcedureModal("registration"));