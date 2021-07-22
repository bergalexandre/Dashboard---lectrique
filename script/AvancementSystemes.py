from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from copy import copy
from datetime import date
from script.utils import *



class AvancementSystemes():

    def __init__(self, specialty):
        self.specialty = specialty
        self.systemes = {}

    def fetchData(self):
        """This a method to generate progress data from the 
            DVP, Travail Effectue, Prévision courbe S sheets. 

        Pseudocode:
            - Compute the weight of each objective for a system
            - Fetch the last data from Travail_Effectue for

        Returns:
            systemes [dictionnary]: Data to generate radial progress graphs for each system
        """
        # weights
        for i, objectif in df_Prevision_Courbe_S[df_Prevision_Courbe_S['Total'] > 0].iterrows():
            if  isinstance(objectif['Requis'], str):
                avancement = df_Avancement_Courbe_S['Avancement'][i]
                semaines = df_Prevision_Courbe_S.columns[5:]
                avancement_estime = 0
                for s in semaines:
                    if not np.isnan(objectif[s]) and not today < date(int(s[6:]), int(s[3:5]), int(s[:2])) :
                        avancement_estime = avancement_estime + objectif[s]
                    else:
                        if not np.isnan(objectif[s]):
                            avancement_estime = avancement_estime + objectif[s]
                            break
                weight = df_Prevision_Courbe_S['Total'][i] / Systeme.mapSysteme(objectif['Requis'][0:4])['hours']
                avancement_estime = (avancement_estime / df_Prevision_Courbe_S['Total'][i]) * weight
                avancement = avancement * weight
        
                if objectif['Requis'][:4] not in self.systemes.keys():
                    self.systemes[objectif['Requis'][:4]] = {'Avancement réel' : avancement, 'Avancement estimé' : avancement_estime}
                else:
                    self.systemes[objectif['Requis'][:4]]['Avancement réel'] = self.systemes[objectif['Requis'][:4]]['Avancement réel'] + avancement
                    self.systemes[objectif['Requis'][:4]]['Avancement estimé'] = self.systemes[objectif['Requis'][:4]]['Avancement estimé'] + avancement_estime


    

    def graphSave(self):
        
        data = self.systemes
        x = 0
        for i, s in enumerate(data):
            if Systeme.mapSysteme(s) in self.specialty['systemes']:
                x = x + 1
        fig, axs = plt.subplots(1, x, figsize=(6, 3), subplot_kw=dict(aspect="equal"),constrained_layout=True)
        # Data prep
        index = 0
        for s in data:
            if Systeme.mapSysteme(s) in self.specialty['systemes']:
                new_data = copy(data[s])
                new_data['Fill'] = 1 - new_data['Avancement réel'] 
                new_data['Avancement estimé'] = new_data["Avancement réel"] - new_data["Avancement estimé"]  # pos = avance | neg = retard
                if new_data['Avancement estimé'] >= 0:  # En avance sur le système
                    new_data['Avancement réel'] = new_data['Avancement réel'] - new_data['Avancement estimé']
                    new_data['Fill'] = 1 - new_data['Avancement réel'] 
                    columns = ['Avancement réel', 'Avance', 'Fill']
                    colors = ['tab:blue', 'tab:green', 'tab:grey']
                else:  # En retard
                    new_data['Avancement estimé'] = new_data['Avancement estimé'] * -1
                    columns = ['Avancement réel', 'Retard', 'Fill']
                    colors = ['tab:blue', 'tab:red', 'tab:grey']

                #  Matplotlib
                wedges, texts = axs[index].pie(new_data.values(), wedgeprops=dict(
                    width=0.4), startangle=-90, colors=colors, radius=1.1)

                bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=0.72)
                kw = dict(arrowprops=dict(arrowstyle="-"),
                        bbox=bbox_props, zorder=0, va="center")

                axs[index].annotate(str(round(data[s]['Avancement réel'] * 100)) +
                            "%", xy=(0, 0), ha='center', va='center')
                axs[index].set_title(s, y=1.1)
                index = index + 1
        plt.tight_layout()
        plt.savefig('img/avancement.png', dpi=400)
        
        img = Image.open(r"img/avancement.png")
        width, height = img.size

        left = 1
        top = height / 8
        right = width
        bottom = 3 * height / 4       

        img = img.crop([left, top, right, bottom])
        #img.show()
        img.save('img/avancement.png')