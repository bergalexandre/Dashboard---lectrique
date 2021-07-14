from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from script.utils import *





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
        semaine_courante = "Sem 10" #df_formule['Date Actuel'][1]
        data = df_travail_effectue[['#Requis', 'NOM', 'Semaine', 'heures']]

        # Heures totales et heures systemes
        for i, objectif in data.iterrows():
            print(objectif['NOM'])
            if objectif['NOM'] in self.heures_travaillees.keys():
                requis = objectif['#Requis']
                if semaine_courante == objectif['Semaine']:
                    self.heures_travaillees[objectif['NOM']][requis[0:4]
                                                             ] = self.heures_travaillees[objectif['NOM']][requis[0:4]] + objectif['heures']
                self.heures_travaillees[objectif['NOM']]['heures totales'] = self.heures_travaillees[objectif['NOM']
                                                                                                     ]['heures totales'] + df_travail_effectue['heures'][i]

        # Calcul de la moyenne des heures
        x = int(semaine_courante.split()[1])
        for membre in self.heures_travaillees:
            self.heures_travaillees[membre]['moyenne hebdo'] = self.heures_travaillees[membre]['heures totales'] / (
                x - self.offset)

    def graphSave(self):
        fig, axes = plt.subplots()
        colors = ['tab:blue', 'tab:red', 'tab:orange','chartreuse', 'gold', 'deeppink', 'tab:cyan', 
                  'orangered', 'chartreuse']
        
        labels = []
        for name in self.heures_travaillees.keys():
            labels.append(self.specialty['membres'][name]['initials'])
        somme = 0
        legend = []

        for i, systeme in enumerate(self.specialty['systemes']):
            heures_systeme = []
            legend.append(systeme['name'])
            for nom in self.heures_travaillees:
                if np.isnan(self.heures_travaillees[nom][systeme['number']]):
                    raise Exception(
                        f"{nom} n'a pas rentré ses heures pour une tâche du système {systeme['name']}")
                heures_systeme.append(self.heures_travaillees[nom][systeme['number']])
                somme = somme + self.heures_travaillees[nom][systeme['number']]
            axes.bar(labels, heures_systeme, color=colors[i], )
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
        plt.xticks(rotation=45)
        plt.savefig("img/heures_travaillees.png", bbox_inches='tight')




