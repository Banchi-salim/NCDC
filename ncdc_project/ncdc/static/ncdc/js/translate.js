document.addEventListener('DOMContentLoaded', function () {
    const viewLanguageSelect = document.getElementById('language-select');

    async function translateText(text, targetLang) {
        try {
            const response = await fetch('/translate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ text, target_lang: targetLang })
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

    async function translateAllMessages(targetLang) {
        const messageElements = document.querySelectorAll('.message');
        for (const messageEl of messageElements) {
            const originalText = messageEl.getAttribute('data-original');

            try {
                const translatedText = await translateText(originalText, targetLang);
                messageEl.querySelector('.message-content').textContent = translatedText;
            } catch (error) {
                console.error('Message translation failed:', error);
            }
        }
    }

    if (viewLanguageSelect) {
        viewLanguageSelect.addEventListener('change', function () {
            const selectedLang = this.value;
            translateAllMessages(selectedLang);
        });
    }
});
