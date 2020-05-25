import speech_recognition as sr
import os
from pydub import AudioSegment
from natsort import natsorted

from tkinter import Tk
from tkinter.filedialog import askopenfilename

#main menu
while True:
    try:
        print("Choose an option to convert speech to text: ")
        print("1. Open File")
        print("2. File generated from TextToSpeech.py")
        choice = int(input())
        if (choice == 1):
            #choose a file if human script
            Tk().withdraw()
            filename = askopenfilename()
            r = sr.Recognizer()
            try:
                with sr.AudioFile(filename) as source:
                    audio = r.record(source)  # read the entire audio file
                    print("Transcript: " + r.recognize_google(audio))
            except sr.UnknownValueError:
                print("*Google Speech Recognition could not understand audio of the file" + str(count))
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                proportion = 4
                print("Attempting to split into %d audio file as solution: " % (proportion))
                sound = AudioSegment.from_file(filename)
                start = 0
                end = len(sound) // proportion
                soundIncrement = len(sound) // proportion
                #delete files
                folder = "Split/"
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                #create and split into files
                for i in range(proportion):
                    part = sound[start:end]
                    part.export("Split/split%d.wav" % (i+1), format="wav")
                    start += soundIncrement
                    end += soundIncrement

                #iterate through folder and put in a list
                sorted = []
                directory = os.fsencode("Split/")
                for file in os.listdir(directory):
                     filename = os.fsdecode(file)
                     if filename.endswith(".wav"):
                         audio_path = "Split/" + str(filename)
                         sorted.append(audio_path)
                         continue
                     else:
                         continue
                count = 0;
                #natural number sort
                sorted = natsorted(sorted)
                #iterate through sorted list from folder
                for audio_path in sorted:
                    count += 1
                    sound = AudioSegment.from_file(audio_path)
                    sound.export(audio_path, format="wav")
                    with sr.AudioFile(audio_path) as source:
                        try:
                            audio = r.record(source)  # read the entire audio file
                            print("Split " + str(count) + ": " + r.recognize_google(audio))
                        except sr.UnknownValueError:
                            print("***Google Speech Recognition could not understand audio in paragraph " + str(count) + "***")
                        except sr.RequestError as e:
                            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            finally:
                break
        elif (choice == 2):
            r = sr.Recognizer()
            sorted = []
            directory = os.fsencode("Paragraphs/")
            #add files as list
            for file in os.listdir(directory):
                 filename = os.fsdecode(file)
                 if filename.endswith(".wav"):
                     audio_path = "Paragraphs/" + str(filename)
                     sorted.append(audio_path)
                     continue
                 else:
                     continue
            count = 0;
            #natural number sort
            sorted = natsorted(sorted)
            #iterate through list
            for audio_path in sorted:
                count += 1
                sound = AudioSegment.from_file(audio_path)
                sound.export(audio_path, format="wav")
                with sr.AudioFile(audio_path) as source:
                    try:
                        audio = r.record(source)  # read the entire audio file
                        print("Paragraph " + str(count) + ": " + r.recognize_google(audio))
                    except sr.UnknownValueError:
                        print("***Google Speech Recognition could not understand audio in paragraph " + str(count) + "***")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
            break
        else:
            print("Please choose from only 1 and 2.")
            print()
    except ValueError:
        print("Invalid input.")
        continue
    else:
        break
