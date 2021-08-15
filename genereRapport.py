"""
File: genereRapport.py
Author(s):
    Cabana,  Gabriel         | CABG2101
    Granger, Charles-Etienne | GRAC2310
Date(s):
    2021-07-12 (Creation)
Description:
    Main program.
    Diagram generation and repository update.
"""

### Official modules
import subprocess
import pandas
import os.path
import matplotlib.pyplot as plt
from datetime import datetime
# from PIL import Image

### Custom modules
from script.utils               import *
from script.HeuresTravaillees   import HeuresTravaillees
from script.TraceCourbeEnS      import CourbeEnS
from script.AvancementObjectifs import AvancementObjectifs
from script.AvancementSystemes  import AvancementSystemes
from script.Problemes           import Problemes
from script.TravailEffectue     import TravailEffectue


##################################################
### GLOBAL VARIABLES                           ###
##################################################

git_integration = False
plt.style.use("./script/dashboard.mplstyle")
SPEC             = Speciality.ELEC
PATH_DVP         = "../DVP-Feuille-Temps.xlsm"
PATH_ADVANCEMENT = "img/avancement.pdf"
PATH_CURVE       = "img/Courbe_S.pdf"
PATH_HOURS       = "img/heures_travaillees.pdf"
PATH_ISSUES      = "tableauDeProblemes.tex"
PATH_OBJECTIVES  = "img/progression_objectifs.png"
PATH_TASKS       = "tableauDeTaches.tex"
START_DATE       = "5/6/2021"

##################################################
### METHODS                                    ###
##################################################

def run(*args):
    return subprocess.check_call(['git'] + list(args))


def dateActuel(Depart = START_DATE):
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

if __name__ == "__main__":
    heures_travaillees = HeuresTravaillees(SPEC, offset=8)
    heures_travaillees.fetchData()
    heures_travaillees.graphSave()

    CourbeEnS(PATH_DVP)

    # taches_effectuees = TravailEffectue(SPEC)
    # taches_effectuees.fetchData()
    # taches_effectuees.writeTable()

    avancement_systemes = AvancementSystemes(SPEC)
    avancement_systemes.fetchData()
    avancement_systemes.graphSave()

    # problemes = Problemes(SPEC)
    # problemes.fetchData()
    # problemes.writeTable()

    # budget = Budget(SPEC)
    # budget.fetchData()
    # budget.graphSave()

    if git_integration == True:
        pull()
        # add(PATH_OBJECTIVES)
        add(PATH_ADVANCEMENT)
        add(PATH_CURVE)
        add(PATH_HOURS)
        # add(PATH_TASKS)
        # add(PATH_ISSUES)
        commitEtPush()