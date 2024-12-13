document.addEventListener('DOMContentLoaded', function() {
    // Language selection elements
    const viewLanguageSelect = document.getElementById('language-select');
    const inputLanguageSelect = document.getElementById('input-language-select');

    // Supported languages
    const LANGUAGES = {
        'en': 'English',
        'ha': 'Hausa',
        'yo': 'Yoruba',
        'ig': 'Igbo'
    };

    // Translation function
    async function translateText(text, targetLang) {
        try {
            const response = await fetch('/translate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    text: text,
                    target_lang: targetLang
                })
            });

            if (!response.ok) {
                throw new Error('Translation failed');
            }

            const data = await response.json();
            return data.translated_text;
        } catch (error) {
            console.error('Translation error:', error);
            return text;  // Fallback to original text
        }
    }

    // Function to translate all messages
    async function translateAllMessages(targetLang) {
        const messageContents = document.querySelectorAll('.message-content');

        for (const messageEl of messageContents) {
            const originalText = messageEl.getAttribute('data-original');

            try {
                const translatedText = await translateText(originalText, targetLang);
                messageEl.textContent = translatedText;
            } catch (error) {
                console.error('Message translation failed:', error);
            }
        }
    }

    // Language view selection event listener
    if (viewLanguageSelect) {
        viewLanguageSelect.addEventListener('change', function() {
            const selectedLang = this.value;
            translateAllMessages(selectedLang);
        });
    }

    // Modify send message functionality to support input language
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user');
    const messageInput = document.getElementById('message');

    if (sendButton) {
        sendButton.addEventListener('click', async function() {
            const user = userInput.value.trim() || 'Visitor';
            const message = messageInput.value.trim();
            const inputLanguage = inputLanguageSelect.value;

            if (!message) {
                alert('Message cannot be empty!');
                return;
            }

            try {
                const response = await fetch('/post-message/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        user: user,
                        message: message,
                        language: inputLanguage
                    })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Create new message element
                    const chatMessages = document.getElementById('chat-messages');
                    const newMessageEl = document.createElement('div');
                    newMessageEl.classList.add('message');
                    newMessageEl.innerHTML = `
                        <strong>${user}</strong>:
                        <span class="message-content" data-original="${message}">
                            ${message}
                        </span>
                        <span class="timestamp">Just now</span>
                        <button class="reply-button">Reply</button>
                    `;

                    // Append to chat messages
                    chatMessages.appendChild(newMessageEl);

                    // Clear inputs
                    messageInput.value = '';
                } else {
                    alert('Error sending message');
                }
            } catch (error) {
                console.error('Message sending error:', error);
                alert('Error sending message');
            }
        });
    }

    // Optional: Auto-translate on page load to selected language
    function initializePageTranslation() {
        const defaultLang = viewLanguageSelect ? viewLanguageSelect.value : 'en';
        translateAllMessages(defaultLang);
    }

    // Initialize page translation
    initializePageTranslation();
});