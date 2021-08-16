import random
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from script.utils import PATHS, DATA


class HeuresTravaillees():

    def __init__(self, specialty, offset=0):
        self.specialty = specialty
        self.offset = offset
        self.heures_travaillees = {}
        for membre in self.specialty['membres'].keys():
            if membre not in self.heures_travaillees.keys():
                self.heures_travaillees[membre] = {'heures totales': 0, 'moyenne hebdo': 0, 'SIM1': 0, 'INS1': 0, 'MOT2': 0,
                                                   'GES1': 0, 'ERG1': 0, 'COQ1': 0, 'CHA1': 0, 'DIR1': 0, 'FRE1': 0, 'TTH1': 0, 'SUS1': 0, 'MOT1': 0, 'BAT1': 0}

    def fetchData(self):
        # fetching data
        semaine_courante = DATA.FORMULA['Date Actuel'][1]
        data = DATA.CRTE[['#Requis', 'NOM', 'Semaine', 'heures']]

        # Heures totales et heures systemes
        for i, objectif in data.iterrows():
            print(objectif['NOM'])
            if objectif['NOM'] in self.heures_travaillees.keys():
                requis = objectif['#Requis']
                if semaine_courante == objectif['Semaine']:
                    self.heures_travaillees[objectif['NOM']][requis[0:4]
                                                             ] = self.heures_travaillees[objectif['NOM']][requis[0:4]] + objectif['heures']
                self.heures_travaillees[objectif['NOM']]['heures totales'] = self.heures_travaillees[objectif['NOM']
                                                                                                     ]['heures totales'] + DATA.CRTE['heures'][i]

        # Calcul de la moyenne des heures
        x = int(semaine_courante.split()[1])
        for membre in self.heures_travaillees:
            self.heures_travaillees[membre]['moyenne hebdo'] = self.heures_travaillees[membre]['heures totales'] / (x - self.offset)

    def graphSave(self):
        fig, axes = plt.subplots()
        colors = ['#23ccc1','#32cea9','#96c74c','#b8c02a','#dcb504','#ffa600', '#c20606', '#cd2e01', '#1f60c2', '#ff6c54' ]
        random.shuffle(colors)
        
        labels = []
        for name in self.heures_travaillees.keys():
            labels.append(self.specialty['membres'][name]['initials'])
        current_sum, somme = 0, 0
        legend = []
        tmp = [0,0,0,0,0,0,0,0,0]   
        for i, systeme in enumerate(self.specialty['systemes']):
            heures_systeme = []
            for nom in self.heures_travaillees:
                if np.isnan(self.heures_travaillees[nom][systeme['number']]):
                    raise Exception(
                        f"{nom} n'a pas rentré ses heures pour une tâche du système {systeme['name']}")
                heures_systeme.append(self.heures_travaillees[nom][systeme['number']])
                somme = somme + self.heures_travaillees[nom][systeme['number']]
            if somme - current_sum > 0: 
                legend.append(systeme['name'])
                axes.bar(labels, heures_systeme, color=colors.pop(), bottom=tmp)
                current_sum = somme
                tmp = np.add(tmp, heures_systeme)
        axes.legend(legend)

        moyennes_hebdo = []
        for nom in self.heures_travaillees:
            moyennes_hebdo.append(
                self.heures_travaillees[nom]['moyenne hebdo'])

        moyenne = somme / len(self.heures_travaillees)
        axes.plot(np.array(range(-1, len(self.heures_travaillees)+1)),
                  np.array([moyenne]*(len(self.heures_travaillees)+2)), "g--")

        for indexMembre, nom in enumerate(self.heures_travaillees):
            axes.plot(indexMembre, moyennes_hebdo[indexMembre],
                      "ko" if moyennes_hebdo[indexMembre] >= 9 else "kx")
        plt.xlim([-1, len(self.heures_travaillees)])
        plt.setp(axes.xaxis.get_majorticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        plt.savefig(PATHS["HOURS"], bbox_inches='tight', dpi=96)