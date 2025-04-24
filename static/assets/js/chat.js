document.addEventListener('DOMContentLoaded', function() {
    const chatIcon = document.getElementById('chatIcon');
    const chatContainer = document.querySelector('.chat-container');
    const closeChat = document.querySelector('.close-chat');
    const chatForm = document.querySelector('.chat-form');
    const chatMessages = document.querySelector('.chat-messages');
    
    // باز و بسته کردن پنجره چت
    chatIcon.addEventListener('click', function() {
        chatContainer.style.display = chatContainer.style.display === 'flex' ? 'none' : 'flex';
    });
    
    closeChat.addEventListener('click', function() {
        chatContainer.style.display = 'none';
    });
    
    // ارسال پیام با AJAX
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const messageInput = this.querySelector('input');
        const message = messageInput.value.trim();
        
        if (message) {
            // افزودن پیام کاربر به چت
            addMessage(message, true);
            messageInput.value = '';
            
            // ارسال به سرور و دریافت پاسخ
            fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: `message=${encodeURIComponent(message)}`
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, false);
            });
        }
    });
    
    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});