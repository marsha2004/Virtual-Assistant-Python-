import speech_recognition as sr #recognizes voice
import webbrowser #to open web browsers
import pyttsx3  #for voice
import musiclibrary #contains song with url to play
import requests#to get news

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi="" #newsapikey

# initializing for computer to say text
def speak(text): 
    engine.say(text)
    engine.runAndWait()

# commands
def processCommand(command):
    command = command.lower()

# commands to open webrowser
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
        
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open chatgpt" in command:
        speak("Opening chatgpt")
        webbrowser.open("https://www.chatgpt.com")

# command to play songs
    elif command.startswith("play"):
        words = command.split()
        if len(words) > 1:
            song = words[1]
            if song in musiclibrary.music:
                link = musiclibrary.music[song]
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find the song '{song}' in your music library.")
        else:
            speak("Please specify a song to play.")

# command to get headlines news
    elif "news" in command.lower():
        speak("Fetching the latest news headlines from US...")
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
    
        try:
            response = requests.get(url)
            news_data = response.json()

            if news_data["status"] == "ok":
                articles = news_data["articles"][:5]  # Limiting headlines to top 5 headlines
                for i, article in enumerate(articles, start=1):
                    headline = article["title"]
                    speak(f"Headline {i}: {headline}")
            else:
                speak("Failed to fetch news. Please check the API key or try again later.")
        
        except Exception as e:
            speak("There was an error while fetching the news.")
            print(f"Error: {e}")
  
        

# main program
if __name__ == "__main__":
    speak("Initializing your virtual assistant...")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Say hello...") 
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)

        #activate command by user
            if word.lower() == "hello":
                speak("Yes, how may I help you?")
                
                with sr.Microphone() as source:
                    print("Your Virtual Assistant is active...") #virtual assistant is activated
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

# if any error occurs:
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

