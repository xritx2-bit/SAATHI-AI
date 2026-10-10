"""
SAATHI AI - Voice & Speech Accessibility Engine
Provides multilingual Text-to-Speech (TTS) formatting and Speech-to-Text (STT) transcription.
"""
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceEngine:
    @staticmethod
    def transcribe_audio_bytes(audio_bytes: bytes, language: str = "hi-IN") -> str:
        """
        Transcribes microphone audio bytes into text using speech recognition.
        Supports Hindi ('hi-IN'), Indian English ('en-IN'), and English ('en-US').
        """
        if not audio_bytes or len(audio_bytes) < 100:
            return ""

        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            
            # Load audio buffer
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                # Adjust for ambient noise and record
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = r.record(source)

            # Try primary requested language (e.g. 'hi-IN' or 'en-IN')
            try:
                text = r.recognize_google(audio_data, language=language)
                if text and text.strip():
                    return text.strip()
            except Exception:
                pass

            # Fallback 1: Indian English (en-IN)
            if language != "en-IN":
                try:
                    text = r.recognize_google(audio_data, language="en-IN")
                    if text and text.strip():
                        return text.strip()
                except Exception:
                    pass

            # Fallback 2: Hindi (hi-IN)
            if language != "hi-IN":
                try:
                    text = r.recognize_google(audio_data, language="hi-IN")
                    if text and text.strip():
                        return text.strip()
                except Exception:
                    pass

            # Fallback 3: Standard English (en-US)
            try:
                text = r.recognize_google(audio_data, language="en-US")
                if text and text.strip():
                    return text.strip()
            except Exception:
                pass

            return ""
        except Exception as e:
            logger.warning(f"Audio transcription error: {e}")
            return ""

    @staticmethod
    def generate_browser_speech_html(text: str, language: str = "english", button_id: str = "btn_tts") -> str:
        """
        Generates lightweight HTML/JavaScript that uses the browser's native Web Speech API
        to speak out the answer in Hindi or Indian English without needing external heavy audio files.
        """
        clean_text = text.replace('"', '&quot;').replace("'", "\\'").replace("\n", " ")
        lang_code = "hi-IN" if language == "hindi" else ("en-IN" if language == "hinglish" else "en-US")
        
        html_code = f"""
        <div style="margin-top: 8px;">
            <button id="{button_id}" onclick="speakText_{button_id}()" 
                style="background-color: #F1F5F9; color: #334155; border: 1px solid #CBD5E1; border-radius: 6px; padding: 4px 10px; font-size: 0.85rem; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
                🔊 Listen / आवाज़ सुनें
            </button>
            <script>
                function speakText_{button_id}() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var msg = new SpeechSynthesisUtterance('{clean_text[:400]}');
                        msg.lang = '{lang_code}';
                        msg.rate = 0.95;
                        window.speechSynthesis.speak(msg);
                    }} else {{
                        alert('Speech synthesis is not supported in this browser.');
                    }}
                }}
            </script>
        </div>
        """
        return html_code
