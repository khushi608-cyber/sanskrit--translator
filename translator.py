import streamlit as st
from io import BytesIO

# Translators (use googletrans first; fall back to deep-translator if needed)
try:
    from googletrans import Translator
    GOOGLETRANS_OK = True
except Exception:
    GOOGLETRANS_OK = False

try:
    from deep_translator import GoogleTranslator as DTGoogleTranslator
    DEEPTRANS_OK = True
except Exception:
    DEEPTRANS_OK = False

from gtts import gTTS

st.set_page_config(page_title="Sanskrit → English", page_icon="🕉️")
st.title("🕉️ Sanskrit Shloka Translator (Free)")
st.write("Type/paste a Sanskrit shloka. Get an English meaning and optional audio pronunciation.")

# Input box
sanskrit_text = st.text_area("Enter Sanskrit text", height=160, placeholder="धर्मक्षेत्रे कुरुक्षेत्रे समवेता…")
make_audio = st.checkbox("Also generate English audio", value=True)

def translate_text(txt: str) -> str:
    txt = txt.strip()
    if not txt:
        return ""
    # Try googletrans first
    if GOOGLETRANS_OK:
        try:
            result = Translator().translate(txt, src="sa", dest="en")
            return result.text
        except Exception:
            pass
    # Fallback to deep-translator
    if DEEPTRANS_OK:
        try:
            return DTGoogleTranslator(source="auto", target="en").translate(txt)
        except Exception:
            pass
    # If all fail
    return ""

def tts_mp3_bytes(text: str, lang="en") -> bytes:
    mp3_buffer = BytesIO()
    # gTTS can fail on very long text; keep it reasonable
    snippet = text if len(text) < 4000 else text[:4000]
    tts = gTTS(text=snippet, lang=lang)
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    return mp3_buffer.read()

if st.button("Translate"):
    if not sanskrit_text.strip():
        st.warning("Please enter some Sanskrit text.")
    else:
        with st.spinner("Translating..."):
            eng = translate_text(sanskrit_text)

        if eng:
            st.subheader("English Translation")
            st.write(eng)

            if make_audio:
                with st.spinner("Generating audio..."):
                    audio_bytes = tts_mp3_bytes(eng, lang="en")
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    "Download MP3",
                    data=audio_bytes,
                    file_name="translation_en.mp3",
                    mime="audio/mpeg",
                )
        else:
            st.error("Translation failed. Try again or check your internet connection.")
