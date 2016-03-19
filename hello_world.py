from flask import Flask
from os import environ
import speech_recognition as sr
import pyaudio

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
@app.route("/home")
def say_hi(): # does it matter what these functions that are returning views are named?
    return "Hello World"

@app.route("/hello/<name>") # what is the term for whats inside < > ? its not interpolation...
def hi_person(name):
    html = """
        <h1>
            Hello {}!
        </h1>
        <p>
            Here's a picture of a kitten.  Awww...
        </p>
        <img src="http://placekitten.com/g/200/300">
    """
    return html.format(name.title())
    # return "Hello {}!".format(name.title()) :: default behavior is to return html and 200

@app.route("/jedi/<first>/<last>")
def some_test(first, last):
    ending = last[:3]
    beginning = first[:2]
    return "{}".format(ending + beginning)

@app.route('/speaking')
def get_audio():
    r = sr.Recognizer()
    m = sr.Microphone()
    total_text = ""
    try:
        NLP_USERNAME =  app.config["NLP_USERNAME"] # NLP Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        NLP_PASSWORD =  app.config["NLP_PASSWORD"] # NLP Speech to Text passwords are mixed-case alphanumeric strings

        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            with m as source: audio = r.listen(source, 5)
            print("Got it! Now to recognize it...")
            try:
                # recognize speech using Google Speech Recognition
                # value = r.recognize_google(audio)
                # value2 = r.recognize_wit(audio, key=WIT_AI_KEY)
                # value3 = r.recognize_sphinx(audio)
                sentence = r.recognize_ibm(audio, username=NLP_USERNAME, password=NLP_PASSWORD)

                if str is bytes: # this version of Python uses bytes for strings (Python 2)
                    print("string in bytes")
                    total_text += (str(sentence) + "\n")
                    print("Watson thinks You said: \n {}".format(sentence).encode("utf-8"))
                else: # this version of Python uses unicode for strings (Python 3+)
                    total_text += str(sentence)
                    print("Watson thinks You said: \n {}".format(sentence))

            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from the Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass
    except sr.WaitTimeoutError:
        print('Waiting timeout, quitting')
    print(total_text)
    return "{}".format(total_text)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
