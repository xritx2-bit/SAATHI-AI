"""
SAATHI AI - Voice & Speech Accessibility Engine
Provides multilingual Text-to-Speech (TTS) formatting and browser-native Speech-to-Text (STT) components.
"""
from typing import Dict, Any

class VoiceEngine:
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

    @staticmethod
    def generate_browser_mic_input_html() -> str:
        """
        Generates a speech recognition microphone widget that transcribes voice in real-time.
        """
        html_mic = """
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <button id="micBtn" onclick="toggleSpeechRec()" style="background: #EF4444; color: white; border: none; border-radius: 50%; width: 34px; height: 34px; cursor: pointer; font-size: 1rem; display: flex; align-items: center; justify-content: center;">
                    🎤
                </button>
                <span id="micStatus" style="font-size: 0.85rem; color: #475569; font-weight: 500;">Click mic to speak (हिंदी / English / Hinglish)</span>
            </div>
            <span style="font-size: 0.75rem; color: #94A3B8; font-weight: 600;">WEB SPEECH API</span>
        </div>
        <script>
            var recognizing = false;
            var recognition;
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'hi-IN'; // Indian multilingual recognition

                recognition.onstart = function() {
                    recognizing = true;
                    document.getElementById('micStatus').innerHTML = '🔴 Listening... बोलिए...';
                    document.getElementById('micBtn').style.background = '#10B981';
                };

                recognition.onresult = function(event) {
                    var transcript = event.results[0][0].transcript;
                    document.getElementById('micStatus').innerHTML = '✅ Heard: "' + transcript + '"';
                    // Copy to clipboard for easy pasting into chat
                    navigator.clipboard.writeText(transcript);
                };

                recognition.onerror = function(event) {
                    document.getElementById('micStatus').innerHTML = '⚠️ Mic Error or Permission Denied';
                    recognizing = false;
                    document.getElementById('micBtn').style.background = '#EF4444';
                };

                recognition.onend = function() {
                    recognizing = false;
                    document.getElementById('micBtn').style.background = '#EF4444';
                };
            }

            function toggleSpeechRec() {
                if (recognition) {
                    if (recognizing) {
                        recognition.stop();
                    } else {
                        recognition.start();
                    }
                } else {
                    alert('Speech Recognition is not supported by your browser. Please use Chrome or Edge.');
                }
            }
        </script>
        """
        return html_mic
