"""
File: genereRapport.py
Author(s):
    Bergeron, Alexandre       | BERA2920
    Cabana,   Gabriel         | CABG2101
    Granger,  Charles-Etienne | GRAC2310
Date(s):
    2021-07-12 (Creation)
Description:
    Main program.
    Diagram generation and repository update.
"""

### Official modules
import subprocess
import os.path
import matplotlib.pyplot as plt
from datetime import datetime
# from PIL import Image

### Custom modules
from script.utils               import Speciality, PATHS, DATES
from script.HeuresTravaillees   import HeuresTravaillees
from script.TraceCourbeEnS      import CourbeEnS, findWeek
from script.AvancementObjectifs import AvancementObjectifs
from script.AvancementSystemes  import AvancementSystemes
from script.Problemes           import Problemes
from script.TravailEffectue     import TravailEffectue


##################################################
### METHODS                                    ###
##################################################

def run(*args):
    return subprocess.check_call(['git'] + list(args))


def add(relative_file_path):
    if(os.path.isfile(relative_file_path) == False):
        raise Exception(f"Ton fichier existe pas {relative_file_path}")
    run("add", relative_file_path)


#pas call pour le moment
def tag():
    run("tag", "-a", f"vSem{findWeek()-1}")


def commit(message = f"Création des graphiques du tableau de bord (semaine {findWeek()})"):
    run("commit", "-m", message)


def pull():
    run("pull")


def push():
    run("push")


##################################################
### MAIN                                       ###
##################################################

if __name__ == "__main__":
    speciality = Speciality.ELEC
    git        = False
    plt.style.use(PATHS["STYLE"])

    heures_travaillees = HeuresTravaillees(speciality, offset=8)
    heures_travaillees.fetchData()
    heures_travaillees.graphSave()

    CourbeEnS(PATHS["DVP"])

    # taches_effectuees = TravailEffectue(SPEC)
    # taches_effectuees.fetchData()
    # taches_effectuees.writeTable()

    avancement_systemes = AvancementSystemes(speciality)
    avancement_systemes.fetchData()
    avancement_systemes.graphSave()

    # problemes = Problemes(SPEC)
    # problemes.fetchData()
    # problemes.writeTable()

    # budget = Budget(SPEC)
    # budget.fetchData()
    # budget.graphSave()

    if git == True:
        pull()
        # add(PATH_OBJECTIVES)
        add(PATHS["ADVANCEMENT"])
        add(PATHS["CURVE"])
        add(PATHS["HOURS"])
        # add(PATH_TASKS)
        # add(PATH_ISSUES)
        commit()
        push()