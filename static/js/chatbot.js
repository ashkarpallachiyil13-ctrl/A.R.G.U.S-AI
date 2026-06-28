const menuBtn = document.getElementById("menuBtn");
const dropdown = document.getElementById("dropdown");
const chatArea = document.getElementById("chatArea");
const msgInput = document.getElementById("msgInput");
const sendBtn = document.getElementById("sendBtn");

// ===========================
// Dropdown Menu
// ===========================

menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("open");
});

document.addEventListener("click", () => {
    dropdown.classList.remove("open");
});

// ===========================
// Chat Functions
// ===========================

function addMessage(text, sender) {

    const row = document.createElement("div");
    row.className = `msg-row ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    row.appendChild(bubble);
    chatArea.appendChild(row);

    chatArea.scrollTop = chatArea.scrollHeight;
}

function createBotMessage() {

    const row = document.createElement("div");
    row.className = "msg-row bot";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    row.appendChild(bubble);
    chatArea.appendChild(row);

    chatArea.scrollTop = chatArea.scrollHeight;

    return bubble;
}

// ===========================
// Send Message (Streaming)
// ===========================

async function handleSend() {

    const text = msgInput.value.trim();

    if (!text) return;

    addMessage(text, "user");

    msgInput.value = "";

    msgInput.disabled = true;
    sendBtn.disabled = true;

    const botBubble = createBotMessage();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        if (!response.ok) {
            throw new Error("Server error.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value, {
                stream: true
            });

            botBubble.textContent += chunk;

            chatArea.scrollTop = chatArea.scrollHeight;

        }

    }

    catch (error) {

        botBubble.textContent = "Connection error.";

        console.error(error);

    }

    finally {

        msgInput.disabled = false;
        sendBtn.disabled = false;

        msgInput.focus();

    }

}

// ===========================
// Event Listeners
// ===========================

sendBtn.addEventListener("click", handleSend);

msgInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        handleSend();
    }

});