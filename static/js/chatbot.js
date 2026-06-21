document.addEventListener("DOMContentLoaded", function () {
    // 1. Selector Elemen Input & Kontainer Pesan
    const chatInput = document.querySelector('input[placeholder="Ketik pesan Anda di sini..."]');
    const sendButton = document.getElementById("btn-kirim-chat") || 
                       document.querySelector('button[style*="background: rgb(255, 117, 151)"]') ||
                       document.querySelector('.card button:last-of-type') ||
                       document.querySelectorAll("button")[document.querySelectorAll("button").length - 1];

    // Mengambil area putih tempat balon-balon chat muncul
    const chatContainer = document.getElementById("chat-box-messages") || 
                          (chatInput ? chatInput.closest('.card').querySelector('div[style*="display: flex"][style*="column"]') : null) ||
                          (chatInput ? chatInput.parentElement.previousElementSibling : null);

    if (!chatInput || !sendButton) {
        console.error("SkinAI Error: Komponen input chat atau tombol kirim tidak ditemukan di DOM.");
        return;
    }

    // Amankan ID tombol jika belum ada agar selector event tidak meleset
    if (!sendButton.id) sendButton.id = "btn-kirim-chat";

    // 2. Fungsi Menambahkan Balon Chat ke Layar
    function appendMessage(text, isUser = false) {
        const messageWrapper = document.createElement("div");
        messageWrapper.style.display = "flex";
        messageWrapper.style.justifyContent = isUser ? "flex-end" : "flex-start";
        messageWrapper.style.marginBottom = "15px";
        messageWrapper.style.width = "100%";

        const messageBubble = document.createElement("div");
        messageBubble.textContent = text;
        
        if (isUser) {
            // REVISI: Bubble chat user diganti dari pink ke Hijau Sage (#708238)
            messageBubble.style.background = "#708238";
            messageBubble.style.color = "white";
            messageBubble.style.borderRadius = "16px 16px 0px 16px";
        } else {
            // REVISI: Bubble chat AI diganti dari pink muda ke Soft Sage-Light (#f4f6f0) dengan border netral
            messageBubble.style.background = "#f4f6f0";
            messageBubble.style.color = "#2c3e35";
            messageBubble.style.border = "1px solid #e3e8e5";
            messageBubble.style.borderRadius = "16px 16px 16px 0px";
        }
        
        messageBubble.style.padding = "12px 18px";
        messageBubble.style.maxWidth = "70%";
        messageBubble.style.fontSize = "14px";
        messageBubble.style.lineHeight = "1.5";
        messageBubble.style.wordBreak = "break-word";

        messageWrapper.appendChild(messageBubble);
        chatContainer.appendChild(messageWrapper);
        
        // Auto-scroll ke pesan paling bawah
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return messageWrapper;
    }

    // 3. Fungsi Kirim Data ke API Blueprint Flask
    async function sendMessage() {
        const messageText = chatInput.value.trim();
        if (!messageText) return;

        // Tampilkan pesan user ke layar & kosongkan form input
        appendMessage(messageText, true);
        chatInput.value = "";

        // Tampilkan indikator loading mengetik
        const typingIndicator = appendMessage("SkinAI sedang mengetik...", false);

        try {
            // MENEMBAK PREFIX BLUEPRINT YANG BENAR: /api/chatbot/chat
            const response = await fetch("/api/chatbot/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) {
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }

            const data = await response.json();
            
            // Hapus loading, tampilkan jawaban dari server
            typingIndicator.remove();
            appendMessage(data.reply, false);

        } catch (error) {
            console.error("Error Fetch Chatbot:", error);
            typingIndicator.remove();
            appendMessage("Maaf, gagal terhubung ke server SkinAI. Sila hubungi kembali nanti.", false);
        }
    }

    // 4. Event Listeners
    sendButton.addEventListener("click", function (e) {
        e.preventDefault();
        sendMessage();
    });

    chatInput.addEventListener("keypress", function (e) {
        e.key === "Enter" && (e.preventDefault(), sendMessage());
    });
});