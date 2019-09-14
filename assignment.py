#.................url parsing for website and youtube using voice command.....................
import pyttsx3
import speech_recognition as sr
import webbrowser
import urllib.request
import urllib.parse
#import regex
import re
import sys

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()
speak('hey,friend, iam here help you to search on youtube, search website content')
speak('To search on youtube, say - youtube - and then give request, search website content say - website -  then give query, or if you want to exit,  say - stop -')

def myCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Say that again!')
        query=myCommand();
    return query

def website_search():
    q = str(input('type website address here : '))

    try:
        url=q.replace(" ", "")
        #use http or https according to your seaching website
        url1="https://"+url
        print(url1)
        #give what you want to search in key part , here website 'about' will be extracted
        key = str(input('which content of website should be searched (for eg:index,about): '))

        values={'s':key,'submit':'search'}
        data=urllib.parse.urlencode(values)
        data=data.encode('utf-8')
        req=urllib.request.Request(url1,data)
        resp=urllib.request.urlopen(req)
        respData=resp.read()

        #the content of website under tag <p> will be displayed
        para=re.findall(r'<p>(.*?)</p>',str(respData))

        for eachP in para:
            print(eachP)

    except sr.UnknownValueError:
        print('Sorry ! I didn\'t get that! Say that again!')
        website_search();


#to search in youtube
def youtube_search():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        # video name from user
        song = urllib.parse.urlencode({"search_query": query})
        print(song)

        # fetch the ?v=query_string
        result = urllib.request.urlopen("http://www.youtube.com/results?" + song)
        print(result)

        # make the url of the first result song
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', result.read().decode())
        print(search_results)

        # make the final url of song selects the very first result from youtube result (according to views)
        url = "http://www.youtube.com/watch?v=" + search_results[0]

        # play the video using webBrowser module which opens the browser
        webbrowser.open_new(url)


    except:
        print('Sorry sir! I didn\'t get that! Say that again!')
        youtube_search();
if __name__ == '__main__':

    while True:

        query = myCommand();
        query = query.lower()


        if 'youtube' in query:
            speak('okay')
            speak('what do you want to search on youtube')
            youtube_search()

        elif 'website' in query:
            speak('okay')
            speak('which website do you want to search type below')
            website_search()

        elif 'nothing' in query or 'abort' in query or 'stop' in query:
            speak('okay')
            speak('Bye friend')
            sys.exit()

        speak('give your next command  ')
