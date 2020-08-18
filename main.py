
import face_recognition
import pickle
from gtts import gTTS
import speech_recognition as sr
import pyaudio
import playsound

def load_data_person(pickle_filename) -> dict:
    """ Charge le fichier .pkl contenant les features des visages déjà vu.
    
    Args: 
        pickle_filename (.pkl): fichier contenant les features des visages enregistrés.

    return:
        visage_connu (dict): le noms en clefs et 
                            en valeurs les caractéristiques des visages des personnes déjà connnus
    """

    try:
        with open(pickle_filename, "rb") as f:
            visage_connu = pickle.load(f)
    except:
        print("error when loading pickle")

    else:
        print("data loaded with sucess!")
        
    return visage_connu


def recognize_person(img_to_recognize, visage_connu) -> str:
    """ Identifie si la personne est déjà enregistré avec une photo
        Extrait les visages de l'image et leurs features
        Comparaison avec les features extraites des features déjà présentes dans la base de données
    
    Args:
        img_to_recognize (numpy.array): image en entrée à analyser
        visage_connu (dict): les noms, et les features des visages enregistrés.
    
    Return:
        keys (str): le nom de la personne identifiée
    """

    unknown_picture = face_recognition.load_image_file(img_to_recognize)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)


    if len(unknown_face_encoding) == 0:
        return "Visage non détecté"
    else:
        unknown_face_encoding = unknown_face_encoding[0]

        print("Visage connu:    ", len(visage_connu))
        for elem in visage_connu:
            for keys, features in elem.items():
                print("keys =",keys)
                print("Features:    ", features)
                

                results = face_recognition.compare_faces([features], unknown_face_encoding)
                print(results)
                if results[0] == True:
                    return keys
                        
        return "je ne connais pas cette personne"

#### Load data from database ####
person = load_data_person("data/person_data.pkl")


print(person)
# Now we can see the two face encodings are of the same person with `compare_faces`!

# -----------------------------  Partie Sonore  ------------------------------------------ #

def voice():
    """
    """
    bonjour = "je vous écoute"
    audio_salutation = gTTS(text = bonjour,lang = "fr") 
    audio_salutation.save("data/audio/bonjour.mp3") 
    playsound.playsound("data/audio/bonjour.mp3")

    print("Je vous écoute")
    
    
    r = sr.Recognizer()

    with sr.Microphone() as source:

        #audio= r.adjust_for_ambient_noise(source)
        audio = r.record(source, duration=2)

    print("Fin d'enregistrement.")
    try: 
        audio_to_txt = r.recognize_google(audio, language="fr-FR")
    
    except sr.UnknownValueError:

        pas_compris = "pardon , je ne vous ai pas compris" 
        audio_imcompris = gTTS(text = pas_compris,lang = "fr") 
        audio_imcompris.save("data/audio/incompréhension.mp3") 
        playsound.playsound("data/audio/incompréhension.mp3")

        return "Pardon, je ne vous ai pas compris"


    else:
        return audio_to_txt

def add_personnage(img_file_name):
    """ 
    """
    flag_person_exist = False

    unknown_picture = face_recognition.load_image_file(img_file_name)
    features = face_recognition.face_encodings(unknown_picture)

    if len(features) == 0:
        print("visage non detecté")
    else:
        features = features[0]


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
                with open("data/person_data.pkl", "wb") as f:
                    pickle.dump(person, f)

            except:
                print("error one saving pickle")

            else:
                print("data save with success!")


######  INPUT  ########## Reconnaissance des images #########

#add_personnage("data/image/Sylvere.jpeg")
ret = recognize_person("data/image/syl2.jpg", person)

print(ret)

if ret == "je ne connais pas cette personne":
    inconnu = "enchanté, c'est la première fois que je vous vois" 
    audio_inconnu = gTTS(text = inconnu,lang = "fr") 
    audio_inconnu.save("data/audio/inconnu.mp3") 
    playsound.playsound("data/audio/inconnu.mp3")

elif ret == "Visage non détecté":
    print(ret)

else:
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
                tts.save("data/audio/reponse.mp3")

                # bloque le reste en attendant la piste soit joué 
                blocking = True
                playsound.playsound("data/audio/reponse.mp3", block=blocking)


mots_attendus = []

