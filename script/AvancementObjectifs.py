from os import system
from typing import cast
from matplotlib import pyplot as plt
import pandas as pd
import numpy  as np




class AvancementObjectifs():

    def __init__(self, excelPath):
        print("ayoo")
        self.df_travail_effectue = pd.read_excel(io=excelPath, sheet_name='Travail_Effectue', usecols='B:L', engine='openpyxl')
        self.df_DVP = pd.read_excel(io=excelPath, sheet_name='DVP', header=1, usecols='B:M', engine='openpyxl')
        

    def graphData(self):
        #df_travail_effectue = pd.read_excel(io='Tableau_De_Bord.xlsm', sheet_name='Travail_Effectue', usecols='B:L')
        #df_DVP = pd.read_excel(io='Tableau_De_Bord.xlsm', sheet_name='DVP', usecols='B:M')
        requis = self.df_DVP['# Requis'][self.df_DVP['S-6'] == "OUI"]
        systemes = {}
        for r in requis:
            avancement = 0
            index = self.df_travail_effectue.where(self.df_travail_effectue==r).last_valid_index()
            if index != None:
                avancement = self.df_travail_effectue["Pourcentage d'avancement"][index]
            if r[0:4] not in systemes.keys():
                systemes[r[0:4]] = avancement * 100
            else:
                systemes[r[0:4]] = round(systemes[r[0:4]] + avancement * 100, 2)
            """  systemes = pd.DataFrame(columns=['# système', 'avancement %']            
            systemes = systemes.append({'# système': r[0:4],'avancement %': avancement}, ignore_index=True)
            """
        return systemes
    
    def graphSave(self):
        data = self.graphData()
        plt.rcdefaults()
        fig, axes = plt.subplots()

        y_pos = np.arange(len(data.keys()))
        
        axes.barh(y_pos, data.values(), align='center')
        axes.set_yticks(y_pos)
        axes.set_yticklabels(data.keys())
        axes.invert_yaxis() # read top to bottom
        axes.set_xlabel("Avancement %")
        axes.set_title("Avancement systèmes")

        plt.savefig('img/progression_objectifs.png')
