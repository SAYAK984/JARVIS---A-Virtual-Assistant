"""
Required packages......

1. speechRecognition
2. pyaudio  -> optional....
3. pyttsx3
4. setuptools
5. webbrowser
6. pocketsphinx   -> optional....
7. requests
8. openai
9. os
10. gTTS   -> instead of pyttsx3 if you want you can use gTTS (but later it requires subscription).....

"""

import speech_recognition as sr
import pyaudio
import webbrowser
import pyttsx3
import pocketsphinx
import Music_Library
import requests
import os
from openai import OpenAI
                    


recognize_object = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def AI_Process(command):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis AI assistant"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content



def Process_Command(command):
    print(f"Your command given -> {command}")
    
    if ("google" in command.lower().replace(" ","")):
        speak("Alright !!......Here you go sir !!!")
        speak("Opening google for you !!!")
        webbrowser.open("https://google.com")
        return "positive"

    elif ("youtube" in command.lower().replace(" ","")):
        speak("Alright !!......Here you go sir !!!")
        speak("Opening YouTube for you !!!")
        webbrowser.open("https://www.youtube.com")
        return "positive"

    
    elif ("music" in command.lower().replace(" ","")):
        try:
            recognize_object = sr.Recognizer()

            with sr.Microphone() as source:
                speak("Sir, Tell me the music name you want to hear.....")

                audio = recognize_object.listen(source, timeout = 6, phrase_time_limit = 4)
                music_name = recognize_object.recognize_google(audio)

                link = Music_Library.music_dictionary.get(music_name.lower().replace(" ", ""))

                if (link != None):
                    speak("Alright !!......Here you go sir !!!")
                    speak(f"Playing {music_name} for you !!!!")
                    webbrowser.open(link)
                else:
                    speak("Sir the music you have said is not found in the music library......")
                
                return "positive"

        except sr.WaitTimeoutError:
            speak("I'm sorry but beg your pardon ??.....")
            Process_Command(command)
            
            
    elif ("news" in command.lower().replace(" ", "")):
        try:
            url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=pub_876f4bb57c7344fcaf5a64fb63ec06c8"
            response = requests.get(url)

            if (response.status_code == 200):
                data = response.json()

                if (data["status"] != "ok"):
                    print("API Error:", data)
                    speak("There is an issue with the news service.")
                    return "positive"

                articles = data.get('articles', [])

                if not articles:
                    speak("No news articles found.")
                    return "positive"

                for article in articles[:5]:  # Limit to 5 headlines
                    title = article.get('title')
                    if title:
                        print(title)
                        speak(title)

            else:
                print("HTTP Error:", response.status_code)
                speak("Failed to fetch news.")
                return "positive"

        except requests.RequestException as e:
            print("Error:", e)
            speak("Sorry, I couldn't fetch the news.")
            return "positive"


    elif ("information" in command.lower().replace(" ", "") or "info" in command.lower().replace(" ", "")):
        output = AI_Process(command)  # Now let OpenAI handle the requests/commands given by the user....
        speak(output)
        return "positive"

    else:
        speak("Sorry......but your command is not understandable....")
        return "negative"


def final_acknowledgement():
    speak("Sir Do you need anything else ???")
    while(1):
        try:
            with sr.Microphone() as source:
                audio = recognize_object.listen(source, timeout = 5, phrase_time_limit = 3)
                command = recognize_object.recognize_google(audio)
                if (("yes" in command.lower().replace(" ", "")) or ("yea" in command.lower().replace(" ", ""))):
                    print("You said yes !!!")   # Just for sake of simplicity
                    return "yes"

                elif (("no" in command.lower().replace(" ", "")) or ("not" in command.lower().replace(" ", ""))):
                    print("You said no !!!")  # Just for sake of simplicity
                    return "no"

        except Exception:
            speak("I'm sorry but I'm not getting you.....")
            speak("Please command again !!!......")
            continue



if (__name__ == "__main__"):
    speak("Greetings !!!....")
    speak("Hello.......I am Jarvis !!!")

    while (1):
        # obtain the audio from the microphone.......
        # it will just listen the 'wake-word' from the user to initialize the operational tasks from jarvis.....
        
        recognize_object = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("I'm Listening......")

                audio = recognize_object.listen(source, timeout = 5, phrase_time_limit = 4)
                wake_up_statement = recognize_object.recognize_google(audio)

                print(f"You said -> {wake_up_statement}")


            if ("jarvis" in wake_up_statement.lower().replace(" ", "")):
                speak("Hi Sir, How may I help you ??")     # Jarvis is active now......
                
                while (1):    

                    try:
                        with sr.Microphone() as source:
                            audio = recognize_object.listen(source, timeout = 7, phrase_time_limit = 10)
                            command = recognize_object.recognize_google(audio)
                            
                            result = Process_Command(command)
                            
                            if (result == "negative"):
                                speak("Please give the valid command......")
                                continue


                    except Exception:
                        speak("I'm sorry but I'm not getting you.....")
                        speak("Please command again !!!......")
                        continue


                    else :
                        response = final_acknowledgement()

                        if (response == "yes"):
                            speak("What else can I do for you ???")
                            continue
                        
                        elif (response == "no"):
                            speak("Alright Sir.....Please enjoy with your work......")
                            speak("Call me whenever in need")
                            break


                
        
        except sr.UnknownValueError:
            print("Jarvis can't understand what you are saying !!!")
            print("Speak properly !!!\n")


        except Exception as error:
            print(f"Main error -> {error}")
            print("Try again to speak with Jarvis !!!\n")

