from datetime import datetime
import openpyxl
import matplotlib.pyplot as plt
import pandas

# apparament python peut pas te dire si l'objet est numérique pour un float
def isNumber(s):
    try:
        if(s is not None):
            complex(s) # for int, long, float and complex
        else:
            return False
    except ValueError:
        return False

    return True


class CourbeEnS():
    previsionSheetName = "Prevision_Courbe_S"
    progressSheetName = "Avancement_Courbe_S"
    workSheetName = "Travail_Courbe_S"

    def __init__(self, excelFile):
        self.wb = openpyxl.load_workbook(excelFile, data_only=True)

        heurePrevue = []
        heureProgress = []
        heureTravailler = []

        if(self.previsionSheetName in self.wb.sheetnames):
            previsionSheet = self.wb[self.previsionSheetName]
            heurePrevue = self.heurePrevue(previsionSheet)

        if(self.progressSheetName in self.wb.sheetnames):
            progressSheet = self.wb[self.progressSheetName]
            heureProgress = self.heureProgress(progressSheet)

        if(self.workSheetName in self.wb.sheetnames):
            workSheet = self.wb[self.workSheetName]
            heureTravailler = self.heureTravailler(workSheet)

        self.genereGraphique(heureProgress, heurePrevue, heureTravailler)

    def heurePrevue(self, feuille):
        colD_valeur = list(feuille.iter_cols(min_col=5, max_col=5, min_row=1, max_row=1000, values_only=True))[0]
        index = colD_valeur.index(max(cellule for cellule in colD_valeur if isNumber(cellule)))+1
        heurePrevueParSemaine = []
        for cell in feuille[F"F{index}":F"U{index}"][0]:
            heurePrevueParSemaine.append(cell.value)
        print(heurePrevueParSemaine)
        return heurePrevueParSemaine

    def heureProgress(self, feuille):
        colB_valeur = list(feuille.iter_cols(min_col=2, max_col=2, min_row=1, max_row=1000, values_only=True))[0]
        index = colB_valeur.index("TOTAL")+1
        
        heureAvancement = []
        for cell in feuille[F"F{index}":F"U{index}"][0]:
            heureAvancement.append(cell.value)
        print(heureAvancement)
        return heureAvancement 

    def heureTravailler(self, feuille):
        #iter_cols retourne un itérateur. Convertie l'itérateur en list (pour faire des recherches facilement) pis prendre le premier tuple dedans
        colB_valeur = list(feuille.iter_cols(min_col=2, max_col=2, min_row=1, max_row=50, values_only=True))[0]
        index = colB_valeur.index("Total")+1
        
        heureParSemaine = []
        for cell in feuille[F"D{index}":F"S{index}"][0]:
            heureParSemaine.append(cell.value)
        print(heureParSemaine)
        return heureParSemaine



    def genereGraphique(self, realProgressHours, BudgetedHours, workedHours):
        #range de date (axe X)
        figure, axe = plt.subplots()
        axeXDate = pandas.date_range(start="5/6/2021", periods=len(BudgetedHours), freq="7D")
        #trouve la semaine
        semaine = 0
        for index, date in enumerate(axeXDate):
            if date > datetime.today():
                semaine = index
                break
        
        axe.plot(BudgetedHours, "k")
        axe.plot(range(index+1), workedHours[:semaine+1], "g--")
        axe.plot(range(index+1), realProgressHours[:semaine+1], "b")
        axe.plot(range(index, len(BudgetedHours)), workedHours[index:], "r--")
        axe.set_xticks(range(len(BudgetedHours)))
        plt.xticks(rotation=45)
        axe.set_xticklabels(axeXDate.strftime("%Y-%m-%d"))
        axe.legend(("heures totales", "Heures travaillées", "Heures acquises", "heures restantes"))
        plt.savefig('img/courbe_S.png', bbox_inches='tight')
