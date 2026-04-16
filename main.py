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

# --- 1. AI Configuration ---
client = genai.Client(api_key="AIzaSyDzmRud71cphGGdeQsjnNhKXdKH_-ardVQ")

def aiProcess(command):
    try:
        prompt = f"Act as Jarvis, a polite AI assistant for your boss Shivam Sir. Respond to this briefly in Hinglish: {command}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        clean_text = response.text.replace("*", "").replace("#", "").strip()
        return clean_text
    except Exception:
        return "Sir, mera AI quota khatam ho gaya hai. Main abhi local brain use kar raha hoon."

# --- 2. Voice Setup ---
engine = pyttsx3.init()
r = sr.Recognizer()
engine.setProperty('rate', 180) 

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
            return "Sir, mujhe wo city nahi mili."
    except:
        return "Sir, weather servers offline hain."

def getNews():
    news_key = "f11a43a0429a43369a45610ec1f26a11"
    url = f"https://newsapi.org/v2/top-headlines?sources=google-news&apiKey={news_key}"
    try:
        res = requests.get(url).json()
        articles = res["articles"][:3] 
        headlines = [a['title'] for a in articles]
        return "Sir, aaj ki headlines ye hain: " + " . ".join(headlines)
    except:
        return "Sir, news fetch nahi ho paa rahi."

# --- 4. Central Command Logic ---
def processCommand(c):
    c = c.lower()
    
    # --- 1. Universal App Opener with Mapping ---
    if "open" in c:
        app_name = c.replace("open", "").strip()
        
        # Mapping Dictionary: User kya bolega -> Windows kya samjhega
        app_map = {
            "calculator": "calc",
            "calendar": "outlookcal:",
            "notepad": "notepad",
            "paint": "mspaint",
            "chrome": "chrome",
            "browser": "start msedge"
        }
        
        # Agar mapping mein naam hai toh wo use karo, nahi toh wahi jo bola
        command_to_run = app_map.get(app_name, app_name)
        
        speak(f"Opening {app_name}, Shivam Sir.")
        
        # Try-Except taaki agar app na mile toh crash na ho
        try:
            os.system(f"start {command_to_run}")
        except Exception as e:
            speak(f"Sir, {app_name} kholne mein dikkat ho rahi hai.")
        return 

    # 2. Math Calculation Logic (Offline Math)
    elif any(op in c for op in ["plus", "minus", "multiply", "divide", "+", "-", "*", "/"]):
        try:
            # Simple math solve karne ke liye
            calculation = c.replace("plus", "+").replace("minus", "-").replace("multiply", "*").replace("divide", "/")
            # Filter only math parts
            result = eval(''.join(filter(lambda x: x in '0123456789+-*/. ', calculation)))
            speak(f"Sir, iska answer {result} hai.")
            return
        except:
            pass # Agar math na ho toh AI ke paas jaane do

    # 3. Weather & Temperature
    elif any(word in c for word in ["weather", "temperature", "mausam", "temp"]):
        city = ""
        if "in " in c: city = c.split("in ")[-1].strip()
        elif "of " in c: city = c.split("of ")[-1].strip()
        
        if not city:
            speak("Kaunsi city, sir?")
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=3)
                    city = r.recognize_google(audio)
            except: return
        
        speak(getWeather(city))
        return

    # 4. News
    elif "news" in c or "headlines" in c:
        speak(getNews())
        return

    # 5. WhatsApp
    elif "send whatsapp" in c or "message" in c:
        speak("Number aur message type karein sir.")
        num = input("Enter Number: ")
        msg = input("Enter Message: ")
        pywhatkit.sendwhatmsg_instantly(f"+91{num}", msg, wait_time=15)
        pyautogui.press("enter")
        return

    # 6. System Status
    elif "system status" in c or "battery" in c:
        usage = psutil.cpu_percent()
        speak(f"Sir, CPU usage {usage}% hai.")
        return

    # 7. Exit
    elif "exit" in c or "stop" in c:
        speak("Good bye Shivam Sir!")
        exit()
        
    # 8. AI Brain Fallback (Gemini)
    else:
        print("Jarvis: Thinking...")
        answer = aiProcess(c)
        speak(answer)

# --- 5. Execution Loop ---
if __name__ == "__main__":
    speak("Jarvis initialized. Welcome back Shivam Sir.")
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                print("\n[Standby] Say 'Jarvis'...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
                wake_word = r.recognize_google(audio).lower()

            if "jarvis" in wake_word:
                speak("Ji Sir?")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except:
            continue