import matplotlib.pyplot as plt
import numpy as np
# from PIL import Image
from copy import copy
from datetime import date
from script.utils import DATES, PATHS, DATA, Systeme


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
        for i, objectif in DATA.CBTP[DATA.CBTP['Total'] > 0].iterrows():
            if  isinstance(objectif['Requis'], str):
                avancement = DATA.CBTE['Avancement'][i]
                semaines = DATA.CBTP.columns[5:]
                avancement_estime = 0
                for s in semaines:
                    if not np.isnan(objectif[s]) and not DATES["TODAY"] < date(int(s[6:]), int(s[3:5]), int(s[:2])) :
                        avancement_estime = avancement_estime + objectif[s]
                    else:
                        if not np.isnan(objectif[s]):
                            avancement_estime = avancement_estime + objectif[s]
                            break
                weight = DATA.CBTP['Total'][i] / Systeme.mapSysteme(objectif['Requis'][0:4])['hours']
                avancement_estime = (avancement_estime / DATA.CBTP['Total'][i]) * weight
                avancement = avancement * weight
        
                if objectif['Requis'][:4] not in self.systemes.keys():
                    self.systemes[objectif['Requis'][:4]] = {'Avancement réel' : avancement, 'Avancement estimé' : avancement_estime}
                else:
                    self.systemes[objectif['Requis'][:4]]['Avancement réel'] = self.systemes[objectif['Requis'][:4]]['Avancement réel'] + avancement
                    self.systemes[objectif['Requis'][:4]]['Avancement estimé'] = self.systemes[objectif['Requis'][:4]]['Avancement estimé'] + avancement_estime


    def graphSave(self):
        data = self.systemes
        x = 0
        for s in data:
            if Systeme.mapSysteme(s) in self.specialty['systemes']:
                x = x + 1
        _, ax = plt.subplots(1, x, figsize=(6, 3), subplot_kw=dict(aspect="equal"),constrained_layout=False)
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
                    # columns = ['Avancement réel', 'Avance', 'Fill']
                    colors = ['tab:blue', 'tab:green', 'tab:grey']
                else:  # En retard
                    new_data['Avancement estimé'] = new_data['Avancement estimé'] * -1
                    # columns = ['Avancement réel', 'Retard', 'Fill']
                    colors = ['tab:blue', 'tab:red', 'tab:grey']

                ###  Matplotlib
                wedges, texts = ax[index].pie(
                    new_data.values(),
                    wedgeprops = dict(width=0.4),
                    startangle = -90,
                    colors     = colors,
                    radius     = 1.1
                )
                bbox_props = dict(
                    boxstyle = "round, pad=0.3",
                    fc       = "w",
                    ec       = "k",
                    lw       = 0.72
                )
                kw = dict(
                    arrowprops = dict(arrowstyle="-"),
                    bbox       = bbox_props,
                    zorder     = 0,
                    va         = "center"
                )

                ax[index].annotate(str(round(data[s]['Avancement réel'] * 100)) +
                            "%", xy=(0, 0), ha='center', va='center')
                ax[index].set_title(s, y=1.1)
                index = index + 1

        plt.savefig(PATHS["ADVANCEMENT"], bbox_inches="tight", dpi=96)