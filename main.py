import os
import webbrowser
import speech_recognition as sr
import pyttsx3
import re
import subprocess

# ---------------- Initialization ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text):
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()


# ---------------- App Paths ----------------
apps = {
    # --- System & Browsers ---
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "file explorer": "explorer",

    # --- Editors ---
    "vs code": r"C:\Users\sharm\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": r"C:\Program Files\Notepad++\notepad++.exe",

    # --- Media ---
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "capcut": r"C:\Users\sharm\AppData\Local\CapCut\Apps\CapCut.exe --src1",

    # --- Office ---
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "power point": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "onedrive": r"C:\Program Files\Microsoft OneDrive\OneDrive.exe",

    # --- Websites (no local app) ---
    "youtube": "https://www.youtube.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "eduskills": "https://eduskillsfoundation.org/login",
    "chat gpt": "https://chat.openai.com",
    "gemini": "https://gemini.google.com",
    "whatsapp": "https://web.whatsapp.com"
}

# ---------------- Fallback Websites ----------------
websites = {
    "word": "https://www.microsoft.com/en/microsoft-365/word",
    "excel": "https://www.microsoft.com/en/microsoft-365/excel",
    "powerpoint": "https://www.microsoft.com/en/microsoft-365/powerpoint",
    "vs code": "https://code.visualstudio.com/download",
    "vlc": "https://www.videolan.org/vlc/",
    "notepad": "https://notepad-plus-plus.org/downloads/",
    "whatsapp": "https://web.whatsapp.com",
}


# ---------------- Voice Input ----------------
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("⏳ No speech detected. Waiting again...")
            return ""

        try:
            command = recognizer.recognize_google(audio, language="en-IN")
            print("Recognized:", command)
            if not re.match(r'^[a-zA-Z0-9\s]+$', command):
                speak("Please speak in English only.")
                return ""
            return command.lower()
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return ""
        except sr.RequestError:
            speak("Network error. Please check your connection.")
            return ""


# ---------------- App / Website Launcher ----------------
def open_app_or_website(name):
    normalized_input = name.lower().strip()

    for key, app_path in apps.items():
        if key in normalized_input:
            speak(f"Opening {key}")

            try:
                # ✅ Handle File Explorer separately
                if "explorer" in key:
                    subprocess.Popen(["explorer"])
                    return

                # ✅ Check if local app exists
                exe_path = app_path.split(" ")[0]
                if os.path.exists(exe_path) or app_path.endswith(".exe"):
                    subprocess.Popen(app_path, shell=True)
                    return
                
                 # ✅ Check if local app exists
                exe_path = app_path.split(" ")[0]
                if os.path.exists(exe_path) or app_path.endswith(".EXE"):
                    subprocess.Popen(app_path, shell=True)
                    return

                # ✅ Otherwise, use fallback website if available
                if key in websites:
                    speak(f"{key} opening website instead.")
                    webbrowser.open(websites[key])
                    return

                # ✅ Default: open URL directly
                if app_path.startswith("http"):
                    webbrowser.open(app_path)
                    return

            except Exception as e:
                speak(f"Error opening {key}: {e}")
                return

    # Default fallback
    speak(f"{name} searching on Google.")
    webbrowser.open(f"https://www.google.com/search?q={name}")


# ---------------- Main Assistant Logic ----------------
def main():
    speak("Jarvis is online. Say 'Activate' to begin.")
    active = False

    while True:
        command = listen_command()
        if not command:
            continue

        # Activation / Deactivation
        if "hi jarvis" in command or "hey jarvis" in command or "hello jarvis" in command or "activate" in command:
            active = True
            speak("Hello Sir.")
            continue
        elif "jarvis disconnect" in command or "deactivate" in command:
            active = False
            speak("Deactivating systems. Waiting for your call, Sir.")
            continue

        if not active:
            print("🕓 Waiting for 'Activate'...")
            continue

        # Active commands
        if "close" in command or "exit" in command or "shutdown" in command:
            speak("Shutting down Jarvis. Goodbye Sir.")
            break
        elif "open" in command:
            normalized = command.replace("open", "").strip()
            open_app_or_website(normalized)
        else:
            speak("Command not recognized, Sir. Please try again.")


# ---------------- Run Jarvis ----------------
if __name__ == "__main__":
    main()
