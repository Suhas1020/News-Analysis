from gtts import gTTS

def generate_tts(text, language="hi"):
    """
    Convert text to Hindi speech using gTTS.
    """
    text = " ".join(text.split())  # Clean text to remove unnecessary spaces
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")
    return "output.mp3"
