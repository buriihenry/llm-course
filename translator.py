#pip install googletrans==4.0.0-rc1

from googletrans import Translator

def translate_text(text, source_lang, target_lang):
    """
    Translate text from one language to another using Google Translate.
    
    Args:
    text (str): The text to be translated.
    source_lang (str): The source language code (e.g., 'en', 'es', 'fr').
    target_lang (str): The target language code (e.g., 'es', 'fr', 'en').

    Returns:
    str: The translated text, or an error message if translation fails.
    """
    try:
        translator = Translator()
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except AttributeError:
        return "Error: Failed to translate. The translation service returned None."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Example usage
    input_text = "Hello, how are you?"
    source_language = "en"
    target_language = "es"

    translated_text = translate_text(input_text, source_language, target_language)
    print(f"Original text: {input_text}")
    print(f"Translated text: {translated_text}")
