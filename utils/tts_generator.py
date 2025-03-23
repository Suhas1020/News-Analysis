from gtts import gTTS
import os


def generate_tts(text, language="hi", output_dir="tts_outputs"):
    """
    Generates a Text-to-Speech (TTS) audio file in Hindi.

    :param text: The text to convert into speech.
    :param language: The language for TTS (default: Hindi "hi").
    :param output_dir: Directory to store generated TTS files.
    :return: Path to the generated audio file.
    """
    if not text:
        return None

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    file_path = os.path.join(output_dir, "summary_hindi.mp3")

    # Generate TTS audio
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(file_path)

    return file_path
