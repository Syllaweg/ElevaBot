
import face_recognition
import pickle
from gtts import gTTS
import speech_recognition as sr
import pyaudio
import playsound

def load_data_person(pickle_filename):
    """
    """

    try:
        with open(pickle_filename, "rb") as f:
            person = pickle.load(f)
    except:
        print("error when loading pickle")

    else:
        print("data loaded with sucess!")
        
    return person

def recognize_person(img_fileTest, person):
    """
    """

    unknown_picture = face_recognition.load_image_file(img_fileTest)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    
    if len(unknown_face_encoding) > 0:
        unknown_face_encoding = unknown_face_encoding[0]

    for elem in person:
        
        for keys, features in elem.items():
            print("keys =",keys)
            

            results = face_recognition.compare_faces([features], unknown_face_encoding)
            if results[0] == True:
                return keys
            
            else:
                inconnu = "enchanté, c'est la première fois que je vous vois" 
                audio_inconnu = gTTS(text = inconnu,lang = "fr") 
                audio_inconnu.save("inconnu.mp3") 
                playsound.playsound("inconnu.mp3")
                
                return "je ne connais pas cette personne"

#### Load data from database ####
person = load_data_person("person_data.pkl")


print(person)
# Now we can see the two face encodings are of the same person with `compare_faces`!


def add_personnage(img_file_name):
    """ 
    """
    flag_person_exist = False

    unknown_picture = face_recognition.load_image_file(img_file_name)
    features = face_recognition.face_encodings(unknown_picture)[0]

    print(features)

    for p in person:
        for k in p.keys(): 
            if img_file_name.split(".")[0].split("/")[-1] == k:
                flag_person_exist = True
                print("Cette personne est bien présente dans la base de données") 
                break 
    
    if not flag_person_exist:
        
        new_person = dict()
        new_person[img_file_name.split(".")[0].split("/")[-1]] = features
        person.append(new_person)
        try:
            with open("person_data.pkl", "wb") as f:
                pickle.dump(person, f)

        except:
            print("error one saving pickle")

        else:
            print("data save with success!")


#### Reconnaissance des images ####

#add_personnage("data/Guillaume.jpeg")
ret = recognize_person("data/Guillaume.jpeg", person)

print(ret)


# -----------------------------  Partie Sonore  ------------------------------------------ #

def voice():
    """
    """
    bonjour = "je vous écoute"
    audio_salutation = gTTS(text = bonjour,lang = "fr") 
    audio_salutation.save("bonjour.mp3") 
    playsound.playsound("bonjour.mp3")

    r = sr.Recognizer()

    print("Je vous écoute")

    with sr.Microphone() as source:

        #audio= r.adjust_for_ambient_noise(source)
        audio = r.record(source, duration=2)

    print("Fin d'enregistrement.")
    try: 
        audio_to_txt = r.recognize_google(audio, language="fr-FR")
    
    except sr.UnknownValueError:

        pas_compris = "pardon , je ne vous ai pas compris" 
        audio_imcompris = gTTS(text = pas_compris,lang = "fr") 
        audio_imcompris.save("incompréhension.mp3") 
        playsound.playsound("incompréhension.mp3")

        return "Pardon, je ne vous ai pas compris"


    else:
        return audio_to_txt

text_speech = voice()
print(text_speech)

Salutations = {"keywords":"bonjour,coucou,ça va", "reponses": "Que puis-je faire pour vous ?"}
Remerciements = {"keywords":"ciao,au revoir,merci", "reponses": "Merci au revoir"}


intentions = {"Salutations": Salutations, "Remerciements":Remerciements}

for key, value in intentions.items():
    for mot in value["keywords"].split(","):
        if mot in text_speech.lower():
            print(value["reponses"])

            tts = gTTS(value["reponses"], lang='fr', slow=False)
            tts.save("reponse.mp3")

            # bloque le reste en attendant la piste soit joué 
            blocking = True
            playsound.playsound("reponse.mp3", block=blocking)

mots_attendus = []

