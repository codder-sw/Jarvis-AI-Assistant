import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary 
import os 
import pyautogui 
import pywhatkit
import wikipedia 
import psutil 
import requests 
from google import genai

# --- 1. AI Configuration (Speech-Friendly) ---
# Tip: Agar quota error baar-baar aaye, toh Google AI Studio se nayi key generate karein.
client = genai.Client(api_key="AIzaSyDzmRud71cphGGdeQsjnNhKXdKH_-ardVQ")

def aiProcess(command):
    try:
        prompt = f"Act as Jarvis, a polite AI assistant for your boss Shivam Sir. Respond to this briefly in Hinglish (Hindi + English): {command}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        clean_text = response.text.replace("*", "").replace("#", "").strip()
        return clean_text
    except Exception:
        # Fallback message agar Gemini API fail ho jaye
        return "Sir, mera AI quota khatam ho gaya hai. Main abhi local brain use kar raha hoon."

# --- 2. Voice Setup (Tone & Speed Optimized) ---
engine = pyttsx3.init()
r = sr.Recognizer()

engine.setProperty('rate', 180) 
engine.setProperty('volume', 1.0) 

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# --- 3. Independent Brain Functions ---

def getWeather(city):
    weather_key = "dc3a6de323d24977b6dc66ddf0345687" 
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric"
    try:
        res = requests.get(base_url).json()
        if res["cod"] != "404":
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"Sir, {city} ka temperature {temp} degree Celsius hai aur wahan {desc} ho raha hai."
        else:
            return "Sir, mujhe wo city nahi mili. Please naam check karein."
    except:
        return "Sir, weather servers se connection nahi ho paa raha."

def getNews():
    news_key = "f11a43a0429a43369a45610ec1f26a11"
    url = f"https://newsapi.org/v2/top-headlines?sources=google-news&apiKey={news_key}"
    try:
        res = requests.get(url).json()
        articles = res["articles"][:3] 
        headlines = [a['title'] for a in articles]
        result = "Sir, aaj ki headlines ye hain: " + " . Agli khabar: ".join(headlines)
        return result
    except:
        return "Sir, news fetch karne mein dikkat ho rahi hai."

# --- 4. Central Command Logic ---
def processCommand(c):
    c = c.lower()
    
    # --- 1. Smart Weather & Temperature Logic ---
    # Ab 'temperature' ya 'mausam' bolne par bhi ye block trigger hoga
    if any(word in c for word in ["weather", "temperature", "mausam", "temp"]):
        if "in " in c:
            city = c.split("in ")[-1].strip()
        elif "of " in c:
            city = c.split("of ")[-1].strip()
        else:
            speak("Kaunsi city ka weather check karun, sir?")
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=3)
                    city = r.recognize_google(audio)
            except:
                city = input("Mic Issue. City Name type karein: ")
        
        report = getWeather(city)
        speak(report)

    # --- 2. OS & App Automation ---
    elif "open whatsapp" in c:
        os.system("start whatsapp://") 
        speak("Opening WhatsApp, Shivam Sir.")

    elif "open telegram" in c:
        os.system("start telegram") 
        speak("Telegram khul gaya hai, sir.")

    elif "open file manager" in c or "open explorer" in c:
        os.system("explorer")
        speak("File Explorer active hai, sir.")

    # --- 3. News Logic ---
    elif "news" in c or "headlines" in c:
        speak("Latest news fetch kar raha hoon...")
        headlines = getNews()
        speak(headlines)

    # --- 4. WhatsApp Messaging ---
    elif "send whatsapp" in c or "message" in c:
        speak("Number bataiye Shivam sir?")
        num = input("Enter Number: ")
        speak("Message kya bhejna hai?")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1.0)
                audio = r.listen(source, timeout=5)
                msg = r.recognize_google(audio)
                speak(f"Bhej raha hoon: {msg}")
                pywhatkit.sendwhatmsg_instantly(f"+91{num}", msg, wait_time=15)
                pyautogui.press("enter") 
        except:
            msg = input("Mic error. Message type karein: ")
            pywhatkit.sendwhatmsg_instantly(f"+91{num}", msg, wait_time=15)
            pyautogui.press("enter")

    # --- 5. System Status ---
    elif "system status" in c or "battery" in c:
        battery = psutil.sensors_battery()
        usage = psutil.cpu_percent()
        speak(f"Sir, CPU usage {usage}% hai aur battery levels {battery.percent}% par hain.")

    # --- 6. Memory Feature ---
    elif "remember that" in c:
        info = c.replace("remember that", "").replace("jarvis", "").strip()
        speak(f"Theek hai sir, main yaad rakhunga: {info}")
        with open("memory.txt", "w") as f:
            f.write(info)

    elif "recall" in c or "remember" in c:
        try:
            with open("memory.txt", "r") as f:
                content = f.read()
                speak(f"Sir, aapne kaha tha ki: {content}")
        except:
            speak("Sir, meri memory abhi khali hai.")

    # --- 7. Wikipedia ---
    elif "wikipedia" in c:
        query = c.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("Wikipedia ke mutabik...")
            speak(results)
        except:
            speak("Sir, mujhe Wikipedia par kuch nahi mila.")

    # --- 8. Exit ---
    elif any(word in c for word in ["exit", "stop", "bye"]):
        speak("Good bye Shivam Sir! Take care.")
        exit()
        
    # --- 9. AI Brain Fallback (Gemini) ---
    # Ye tabhi chalega jab upar ka koi keyword match nahi hoga
    else:
        print("Jarvis: Thinking...")
        answer = aiProcess(c)
        speak(answer)

# --- 5. Execution Loop ---
if __name__ == "__main__":
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                print("\n[Standby] Say 'Jarvis'...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
                wake_word = r.recognize_google(audio).lower()

            if "jarvis" in wake_word:
                speak("Ji Shivam Sir?")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print(f"You said: {command}")
                    processCommand(command)
        except Exception as e:
            continue