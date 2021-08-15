from matplotlib import pyplot as plt
from script.utils import *
import shutil

class Problemes():

    def __init__(self, specialty):
        shutil.copyfile("template/tableauDeProblemes.tex", "tableauDeProblemes.tex")
        self.specialty = specialty
        self.travail_effectue = {}
        for membre in self.specialty['membres'].keys():
            if membre not in self.travail_effectue.keys():
                self.travail_effectue[membre] = []
       

    def fetchData(self):
        # fetching data
        semaine_courante = 'Sem 10' #df_formule['Date Actuel'][1]
        data = df_travail_effectue[['NOM', 'Nom Système', 'Problème']].dropna()[df_travail_effectue['Semaine'] == semaine_courante]
    
        # Heures taches de la semaine
        for i, objectif in data.iterrows():
            if objectif['NOM'] in self.travail_effectue.keys():
                self.travail_effectue[objectif['NOM']].append(objectif.values.tolist())

                
    def writeTable(self):
        outputFile = []
        
        cell_text = []
        for membre in self.travail_effectue.keys():
            for row in self.travail_effectue[membre]:
                if bool(row):
                    cell_text.append(row)

        with open('tableauDeProblemes.tex', 'r', encoding='utf8') as tableauFile:
            Lines = tableauFile.readlines()

            # Strips the newline character
            for i, line in enumerate(Lines):
                if i < len(cell_text):
                    line = line.replace("tache1", cell_text[i][2].replace("&", "\&").replace("_", " "))
                    line = line.replace("sys1", cell_text[i][1].replace("&", "\&").replace("_", " "))
                    line = line.replace("res1", cell_text[i][0].replace("&", "\&").replace("_", " "))
                else: # :'(
                    line = line.replace("tache1", " ")
                    line = line.replace("sys1", " ")
                    line = line.replace("res1", " ")
                outputFile.append(line)
                print(outputFile[-1])

        with open('tableauDeProblemes.tex', 'w', encoding='utf8') as tableauFile:
            tableauFile.writelines(outputFile)


    def graphSave(self):
        
        column_headers = ['Membre', 'Nom Système', 'Problème']
        

        cell_text = []
        for membre in self.travail_effectue.keys():
            for row in self.travail_effectue[membre]:
                if bool(row):
                    cell_text.append(row)
        
        fig = plt.subplot()
        table = fig.table(cellText=cell_text, colColours=['g', 'g', 'g'], colLabels=column_headers, loc='center', cellLoc='center')
        fig.axis("off")
        #fig.set_size_inches(5, 8)
        #[t.auto_set_font_size(False) for t in [tab1, tab2]]
        #[t.set_fontsize(8) for t in [tab1, tab2]]

        table.auto_set_column_width(col=list(range(len(column_headers)))) # Provide integer list of columns to adjust
        plt.savefig('img/problemes.pdf', transparent=True, bbox_inches='tight', pad_inches=0, dpi=96)
