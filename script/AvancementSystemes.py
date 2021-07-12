from os import system
from typing import cast
from matplotlib import pyplot as plt
from matplotlib.patches import Wedge
import pandas as pd
import numpy as np
from copy import copy
from enum import Enum
from datetime import date
from script.utils import *


"""  
systemes = pd.DataFrame(columns=['# système', 'avancement %']            
systemes = systemes.append({'# système': r[0:4],'avancement %': avancement}, ignore_index=True)
"""



class AvancementSystemes():

    def __init__(self, excelFile, specialty = Speciality.INFO):
        print("ayoo")
        self.specialty = specialty

        self.today = date.today()

        self.df_travail_effectue = pd.read_excel(
            io=excelFile, sheet_name='Travail_Effectue', usecols='B:L', engine='openpyxl')

        self.df_DVP = pd.read_excel(
            io=excelFile, sheet_name='DVP', header=1, usecols='B:M', engine='openpyxl')

        self.df_Prevision_Courbe_S = pd.read_excel(
            io=excelFile, sheet_name='Prevision_Courbe_S', header=2, usecols='B:U', engine='openpyxl')

        self.df_Avancement_Courbe_S = pd.read_excel(
            io=excelFile, sheet_name='Avancement_Courbe_S', header=2, usecols='B:U', engine='openpyxl')

    def fetchData(self, specialty = Speciality.INFO):
        """This a method to generate progress data from the 
            DVP, Travail Effectue, Prévision courbe S sheets. 

        Pseudocode:
            - Compute the weight of each objective for a system
            - Fetch the last data from Travail_Effectue for

        Returns:
            systemes [dictionnary]: Data to generate radial progress graphs for each system
        """
        # weights
        systemes = {}
        for i, sys in enumerate(self.df_Prevision_Courbe_S['Requis'].dropna()[self.df_Prevision_Courbe_S['Total'] > 0]):
            avancement = self.df_Avancement_Courbe_S['Avancement'][i]

            semaines = self.df_Prevision_Courbe_S.columns[5:]
            avancement_estime = np.float64(0.0)
            for j, s in enumerate(semaines):
                if not np.isnan(self.df_Prevision_Courbe_S[s][i]) and not self.today < date(int(s[6:]), int(s[3:5]), int(s[:2])) :
                    avancement_estime = avancement_estime + self.df_Prevision_Courbe_S[s][i]
                else:
                    if not np.isnan(self.df_Prevision_Courbe_S[s][i]):
                        avancement_estime = avancement_estime + self.df_Prevision_Courbe_S[s][i]
                        break


                    


            weight = self.df_Prevision_Courbe_S['Total'][i] / Systeme.mapSysteme(sys[0:4])['hours']
            if sys[0:4] not in systemes.keys():
                systemes[sys[0:4]] = round(avancement * weight, 2)
            else:
                systemes[sys[0:4]] = round(systemes[sys[0:4]] + avancement * weight, 2)
            print(avancement)
            print(avancement_estime)
            print(weight)

        # systèmes
        requis = self.df_DVP['# Requis'][self.df_DVP['S-6'] == "OUI"]
        systemes = {}
        for r in requis:
            avancement = 0
            index = self.df_travail_effectue.where(
                self.df_travail_effectue == r).last_valid_index()
            if index != None:
                avancement = self.df_travail_effectue["Pourcentage d'avancement"][index]
            if r[0:4] not in systemes.keys():
                systemes[r[0:4]] = avancement * 100
            else:
                systemes[r[0:4]] = round(
                    systemes[r[0:4]] + avancement * 100, 2)

        return systemes

    

    def graphSave(self, data={"Simulateur": {"Avancement réel": 0.15, "Avancement estimé": 0.20}, 
                                "Contrôle": {"Avancement réel": 0.01, "Avancement estimé": 0.05},
                                "Télémétrie": {"Avancement réel": 0.01, "Avancement estimé": 0.05}}):
        
        fig, axs = plt.subplots(1, len(data), figsize=(6, 3), subplot_kw=dict(aspect="equal"),constrained_layout=True)
        
        # Data prep
        for i, s in enumerate(data):
            new_data = copy(data[s])
            new_data['Fill'] = 1 - new_data['Avancement réel'] 
            new_data['Avancement estimé'] = round(
                new_data["Avancement réel"] - new_data["Avancement estimé"], 2)  # pos = avance | neg = retard
                
            if new_data['Avancement estimé'] >= 0:  # En avance sur le système
                new_data['Avancement réel'] = round(
                    new_data['Avancement réel'] - new_data['Avancement estimé'], 2)
                new_data['Fill'] = 1 - new_data['Avancement réel'] 
                columns = ['Avancement réel', 'Avance', 'Fill']
                colors = ['tab:blue', 'tab:green', 'tab:grey']
            else:  # En retard
                new_data['Avancement estimé'] = new_data['Avancement estimé'] * -1
                columns = ['Avancement réel', 'Retard', 'Fill']
                colors = ['tab:blue', 'tab:red', 'tab:grey']

            #  Matplotlib
            wedges, texts = axs[i].pie(new_data.values(), wedgeprops=dict(
                width=0.5), startangle=-90, colors=colors, radius=1.1)

            bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=0.72)
            kw = dict(arrowprops=dict(arrowstyle="-"),
                    bbox=bbox_props, zorder=0, va="center")
            #p = wedges[1]
            #ang = (p.theta2 - p.theta1)/2. + p.theta1
            #y = np.sin(np.deg2rad(ang))
            #x = np.cos(np.deg2rad(ang))
            #horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            #connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            #kw["arrowprops"].update({"connectionstyle": connectionstyle})
            #axs[i].annotate(columns[1], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
            #            horizontalalignment=horizontalalignment, **kw) """    

            axs[i].annotate(str(data[s]['Avancement réel'] * 100) +
                        "%", xy=(0, 0), ha='center', va='center')
            axs[i].set_title(s, y=1.1)
        
        #plt.show()
        plt.savefig('img/avancement.png')
           