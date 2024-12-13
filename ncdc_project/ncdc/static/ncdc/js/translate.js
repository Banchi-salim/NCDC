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


    // Optional: Auto-translate on page load to selected language
    function initializePageTranslation() {
        const defaultLang = viewLanguageSelect ? viewLanguageSelect.value : 'en';
        translateAllMessages(defaultLang);
    }

    // Initialize page translation
    initializePageTranslation();
});