"""
SAATHI AI - Voice & Speech Accessibility Engine
=================================================
Provides multimodal voice-first accessibility for Indian citizens:
1. Speech-to-Text (STT) transcription supporting 8+ Indic languages (Hindi, Marathi, Bengali, Tamil, Telugu, Gujarati, Kannada, Hinglish).
2. Voice Note (.ogg, .wav, .mp3, .webm, .m4a) audio ingestion.
3. Multilingual Text-to-Speech (TTS) formatting for village & low-literacy users.
"""
import io
import os
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Supported Indic language codes for speech processing
INDIC_LANGUAGE_MAP: Dict[str, str] = {
    "hindi": "hi-IN",
    "hinglish": "hi-IN",
    "english": "en-IN",
    "marathi": "mr-IN",
    "bengali": "bn-IN",
    "gujarati": "gu-IN",
    "tamil": "ta-IN",
    "telugu": "te-IN",
    "kannada": "kn-IN"
}

class VoiceEngine:
    @staticmethod
    def transcribe_audio_bytes(audio_bytes: bytes, language: str = "hi-IN") -> str:
        """
        Transcribes audio bytes into text using Google Speech API & SpeechRecognition.
        Fallback sequence: requested language -> Indian English -> Hindi -> English US.
        """
        if not audio_bytes or len(audio_bytes) < 100:
            return ""

        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True

            # Ingest audio buffer
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = r.record(source)

            # Map user language name to BCP-47 tag if needed
            target_lang = INDIC_LANGUAGE_MAP.get(language.lower(), language)

            # Attempt 1: Target Indic Language
            try:
                text = r.recognize_google(audio_data, language=target_lang)
                if text and text.strip():
                    return text.strip()
            except Exception:
                pass

            # Attempt 2: Indian English (en-IN)
            if target_lang != "en-IN":
                try:
                    text = r.recognize_google(audio_data, language="en-IN")
                    if text and text.strip():
                        return text.strip()
                except Exception:
                    pass

            # Attempt 3: Hindi (hi-IN)
            if target_lang != "hi-IN":
                try:
                    text = r.recognize_google(audio_data, language="hi-IN")
                    if text and text.strip():
                        return text.strip()
                except Exception:
                    pass

            # Attempt 4: Standard English (en-US)
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

    @classmethod
    def transcribe_audio_file(cls, file_path: str, language: str = "hindi") -> str:
        """Transcribes an audio file on disk (.wav, .ogg, .mp3, .webm)."""
        if not os.path.exists(file_path):
            return ""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return cls.transcribe_audio_bytes(data, language=language)
        except Exception as e:
            logger.error(f"Failed to read audio file {file_path}: {e}")
            return ""

    @staticmethod
    def generate_browser_speech_html(text: str, language: str = "hindi", button_id: str = "btn_tts") -> str:
        """
        Generates lightweight HTML/JavaScript utilizing browser native Web Speech API
        to speak out answers in Hindi, Marathi, Bengali, Tamil, Telugu, or Indian English.
        """
        # Clean text for JavaScript payload
        clean_text = text.replace('"', '&quot;').replace("'", "\\'").replace("\n", " ")
        lang_code = INDIC_LANGUAGE_MAP.get(language.lower(), "hi-IN")
        
        html_code = f"""
        <div style="margin-top: 8px;">
            <button id="{button_id}" onclick="speakText_{button_id}()" 
                style="background-color: #0284C7; color: white; border: none; border-radius: 6px; padding: 6px 14px; font-size: 0.85rem; font-weight: 500; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                🔊 Listen / आवाज़ सुनें ({language.title()})
            </button>
            <script>
                function speakText_{button_id}() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var msg = new SpeechSynthesisUtterance('{clean_text[:500]}');
                        msg.lang = '{lang_code}';
                        msg.rate = 0.95;
                        msg.pitch = 1.0;
                        window.speechSynthesis.speak(msg);
                    }} else {{
                        alert('Speech synthesis is not supported in this browser.');
                    }}
                }}
            </script>
        </div>
        """
        return html_code
