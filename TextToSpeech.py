from gtts import gTTS
import os, shutil
from pydub import AudioSegment

file1 = open('script.txt', 'r')
count = 0
paraCount = 0;
mytext = ""
language = 'en'

#initialize starting sound file
data = "Conversion of text to speech by group 2"
emptyWav = gTTS(text=data, lang=language, slow=False)
emptyWav.save("script.wav")

#add silence
start = AudioSegment.from_file("script.wav")
silence = AudioSegment.from_wav("3-second_Silence.wav")
paragraphs = []


folder = 'Paragraphs/'
#create directory
try:
    os.mkdir(folder)
except OSError:
    print ("Creation of the directory %s failed (could already exist)" % folder)
else:
    print ("Successfully created the directory %s " % folder)

#delete files inside directory
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

print ("Reading the text file...")
#read and create individual speech files as paragraphs
while True:
    count += 1

    # Get next line from file
    line = file1.readline()

    # if line is empty
    # end of file is reached
    if not line:
        paraCount += 1
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("Paragraphs/paragraph%d.wav" % (paraCount))
        paragraphs.append(AudioSegment.from_file("Paragraphs/paragraph%d.wav" % (paraCount)))
        paragraphs.append(silence)
        mytext = ""
        break

    if line.strip():
        mytext = mytext + " " + line.strip()
    else:
        paraCount += 1
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("Paragraphs/paragraph%d.wav" % (paraCount))
        paragraphs.append(AudioSegment.from_file("Paragraphs/paragraph%d.wav" % (paraCount)))
        paragraphs.append(silence)
        mytext = ""

#concatenate all paragraphs as final output
combined_sounds = start + silence
for sounds in paragraphs:
    combined_sounds = combined_sounds + sounds
combined_sounds.export("script.wav", format="wav")

file1.close()

print("Done! Opening audio file.")
os.system("script.wav")
