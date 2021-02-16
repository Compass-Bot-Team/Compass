import io


def tts(text):
    import gtts
    _bytes = io.BytesIO()
    speech = gtts.gTTS(text)
    speech.write_to_fp(_bytes)
    _bytes.seek(0)
    return _bytes
