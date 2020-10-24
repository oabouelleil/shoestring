from gtts import gTTS
import playsound
import speech_recognition as sr
import os
import random
adjusted_noise = False


def record_audio(query=False):
    # recogniser object
    global adjusted_noise  # use global variable
    rec = sr.Recognizer()

    # open mic and start recording
    with sr.Microphone() as source:
        if not adjusted_noise:
            rec.adjust_for_ambient_noise(source, duration=1)
            #  print('ADJUSTED FOR NOISE')
            adjusted_noise = True
        if query:
            # help - discord -- ss
            print(query)
        else:
            print("How can I help?")
        audio = rec.listen(source)
        data = ''
        try:
            data = rec.recognize_google(audio)
            print(f"You said {data}")
        except sr.UnknownValueError:
            print("Google speech recognition could not understand the audio, unknown error")
        except sr.RequestError as e:
            print("Request results from Google Speech Recognition Server error" + e)
        # return what we said as a string
        return data


def virtual_response(audio_string):
    print(audio_string)
    myObj = gTTS(text=audio_string, lang='en', slow=False)
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    #  save converted audio to a file
    myObj.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)


while True:
    text = record_audio()
    virtual_response(text)