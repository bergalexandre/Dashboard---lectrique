import subprocess
from datetime import datetime
import pandas
import os.path
from script.utils               import *
from script.HeuresTravaillees   import HeuresTravaillees
from script.TraceCourbeEnS      import CourbeEnS
from script.AvancementObjectifs import AvancementObjectifs
from script.AvancementSystemes  import AvancementSystemes
from script.Problemes           import Problemes
from script.TravailEffectue     import TravailEffectue
from PIL import Image

git_integration = True


def run(*args):
    return subprocess.check_call(['git'] + list(args))


def dateActuel(Depart = "5/6/2021"):
    semaines = pandas.date_range(start=Depart, periods=16, freq="7D") #trimeste = 16 semaines????
    #trouve la semaine courante
    semaineN = 0
    for index, date in enumerate(semaines):
        if date > datetime.today():
            semaineN = index
            break
    return semaineN

def pull():
    run("pull")

#pas call pour le moment
def tagDernierRapportEtPushTag():
    run("tag", "-a", f"vSem{dateActuel()-1}")

def add(relativeFilePath):
    if(os.path.isfile(relativeFilePath) == False):
        raise Exception(f"Ton fichier existe pas {relativeFilePath}")
    run("add", relativeFilePath)

def commitEtPush():
    commit_message = f"\nCréation du template semaine{dateActuel()}"

    run("commit", "-m", commit_message)
    run("push")


# dimension est un tupple (x, y)
def resizePicture(path, dimension):
    img = Image.open(path)
    resized_img = img.resize(dimension)
    resized_img.save(path)



spec = Speciality.ELEC
#avancement_objectifs = AvancementObjectifs("../DVP-Feuille-temps.xlsm")
#avancement_objectifs.graphSave()

heures_travaillees = HeuresTravaillees(spec, offset=8)
heures_travaillees.fetchData()
heures_travaillees.graphSave()

CourbeEnS("../DVP-Feuille-temps.xlsm")

taches_effectuees = TravailEffectue(spec)
taches_effectuees.fetchData()
taches_effectuees.writeTable()

avancement_systemes = AvancementSystemes(spec)
avancement_systemes.fetchData()
avancement_systemes.graphSave()

problemes = Problemes(spec)
problemes.fetchData()
problemes.writeTable()


#resizePicture("img/progression_objectifs.png", (1336, 405))
resizePicture("img/avancement.png", (1185, 483))
resizePicture("img/Courbe_S.png", (604, 436))
resizePicture("img/heures_travaillees.png", (511, 342)) 


if git_integration == True:
    pull()
    #add("img/progression_objectifs.png")
    add("img/avancement.png")
    add("img/Courbe_S.png")
    add("img/heures_travaillees.png")
    add("tableauDeTaches.tex")
    add("tableauDeProblemes.tex") #frog(?) #WhatTheBread
    commitEtPush()

#budget = Budget(spec)
#budget.fetchData()
#budget.graphSave()