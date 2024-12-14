document.addEventListener('DOMContentLoaded', function () {
    // Language selection dropdown
    const viewLanguageSelect = document.getElementById('language-select');

    // Translation function
    async function translateText(text, targetLang) {
        try {
            const response = await fetch('/translate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({
                    text: text,
                    target_lang: targetLang,
                }),
            });

            if (!response.ok) {
                throw new Error('Translation failed');
            }

            const data = await response.json();
            return data.translated_text;
        } catch (error) {
            console.error('Translation error:', error);
            return text; // Fallback to the original text
        }
    }

    // Function to translate all chat messages
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

    // Language selection event listener
    if (viewLanguageSelect) {
        viewLanguageSelect.addEventListener('change', function () {
            const selectedLang = this.value;
            translateAllMessages(selectedLang);
        });
    }

    // Auto-translate on page load to the default language
    function initializePageTranslation() {
        const defaultLang = viewLanguageSelect ? viewLanguageSelect.value : 'en';
        translateAllMessages(defaultLang);
    }

    initializePageTranslation();
});
