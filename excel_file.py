import xlsxwriter

# =========================
# Création du fichier Excel
# =========================
wb = xlsxwriter.Workbook("SystèmeVie2026_Ultime.xlsx")

# =========================
# Formats
# =========================
bold_center = wb.add_format({'bold': True, 'align': 'center'})
green_fill = wb.add_format({'bg_color': '#C6EFCE'})
red_fill = wb.add_format({'bg_color': '#FFC7CE'})
orange_fill = wb.add_format({'bg_color': '#FFEB9C'})
progress_bar = wb.add_format({'bg_color': '#63C384'})
money_fmt = wb.add_format({'num_format':'#,##0'})
center_align = wb.add_format({'align':'center'})

# =========================
# Feuille Finances
# =========================
finances = wb.add_worksheet("Finances")
finances.set_column("A:A",15)  # Date Recette
finances.set_column("B:B",20)  # Catégorie Recette
finances.set_column("C:C",12)  # Montant Recette
finances.set_column("D:D",20)  # Catégorie Dépense
finances.set_column("E:E",12)  # Montant Dépense
finances.set_column("F:F",12)  # Solde
finances.set_column("G:G",30)  # Note

# ---- Recettes ----
finances.write_row('A1', ["Date","Catégorie Recette","Montant Recette","Note"], bold_center)
recette_categories = ["Salaire","Don","Consultation","Autre"]
finances.data_validation('A2:A11', {'validate':'date','criteria':'between','minimum':'2026-01-01','maximum':'2026-12-31'})
finances.data_validation('B2:B11', {'validate':'list','source':recette_categories})

recettes_fictives = [
    ("2026-01-01","Salaire",2000,"Salaire Janvier"),
    ("2026-01-05","Don",100,"Donation famille"),
    ("2026-01-10","Consultation",300,"Consultation médicale"),
    ("2026-01-12","Autre",50,"Petit gain"),
    ("2026-01-15","Salaire",2000,"Salaire Février"),
    ("2026-01-18","Don",200,"Donation église"),
    ("2026-01-20","Consultation",150,"Consultation santé"),
    ("2026-01-22","Autre",100,"Vente objet"),
    ("2026-01-25","Salaire",2000,"Salaire Mars"),
    ("2026-01-28","Don",50,"Donation amie"),
]
for i,row in enumerate(recettes_fictives,start=2):
    finances.write_row(f"A{i}", row)

# ---- Dépenses ----
start_row_depense = 14
finances.write_row(f"A{start_row_depense}", ["Date","Catégorie Dépense","Montant Dépense","Solde","Note"], bold_center)
depense_categories = ["Nourriture","Transport","Loyer","Don","Offrande","Habillement","Tresse","Beauté","Prêt","Portable","Santé","Autre"]
finances.data_validation(f'A{start_row_depense+1}:A{start_row_depense+20}', {'validate':'date','criteria':'between','minimum':'2026-01-01','maximum':'2026-12-31'})
finances.data_validation(f'B{start_row_depense+1}:B{start_row_depense+20}', {'validate':'list','source':depense_categories})

depenses_fictives = [
    ("2026-01-02","Nourriture",150,"Courses"),
    ("2026-01-04","Transport",50,"Bus"),
    ("2026-01-06","Loyer",600,"Appartement"),
    ("2026-01-08","Santé",100,"Pharmacie"),
    ("2026-01-10","Beauté",80,"Salon"),
    ("2026-01-12","Offrande",50,"Église"),
    ("2026-01-15","Nourriture",120,"Courses"),
    ("2026-01-18","Transport",60,"Taxi"),
    ("2026-01-20","Loyer",600,"Appartement"),
    ("2026-01-22","Santé",200,"Consultation"),
]
for i,row in enumerate(depenses_fictives,start=start_row_depense+1):
    finances.write_row(f"A{i}", row)

# Solde réel automatique
for i in range(start_row_depense+1, start_row_depense+11):
    finances.write_formula(f'D{i}', f'=SUM(C$2:C$11)-SUM(C${start_row_depense+1}:C{i})')
finances.conditional_format(f'D{start_row_depense+1}:D{start_row_depense+20}', {'type':'cell','criteria':'>=', 'value':0,'format':green_fill})
finances.conditional_format(f'D{start_row_depense+1}:D{start_row_depense+20}', {'type':'cell','criteria':'<', 'value':0,'format':red_fill})

# Camembert Dépenses
finances.write_row('I1', ['Catégorie', 'Total'], bold_center)
for i, cat in enumerate(depense_categories, start=2):
    finances.write(f'I{i}', cat)
    finances.write_formula(f'J{i}', f'=SUMIF(B${start_row_depense+1}:B${start_row_depense+20},"{cat}",C${start_row_depense+1}:C${start_row_depense+20})')

chart_depenses = wb.add_chart({'type':'pie'})
chart_depenses.add_series({
    'name':'Répartition des dépenses',
    'categories':'=Finances!$I$2:$I$13',
    'values':'=Finances!$J$2:$J$13',
    'data_labels': {'percentage': True}
})
chart_depenses.set_title({'name':'Répartition des dépenses'})
finances.insert_chart('I15', chart_depenses, {'x_scale':1.2,'y_scale':1.2})

# =========================
# Routine quotidienne
# =========================
routine = wb.add_worksheet("Routine")
routine.set_column("A:A",15)
routine.set_column("B:F",18)
routine.set_column("G:G",12)
routine.write_row('A1', ["Date","Prière matin","Méditation","Préparation maison","Prière soir","Coucher","Score"], bold_center)
routine.data_validation('A2:A11', {'validate':'date','criteria':'between','minimum':'2026-01-01','maximum':'2026-12-31'})
for col in ['B','C','D','E','F']:
    routine.data_validation(f'{col}2:{col}11', {'validate':'list','source':['Oui','Non']})
routine_data = [
    ("2026-01-01","Oui","Oui","Oui","Oui","Oui"),
    ("2026-01-02","Oui","Non","Oui","Oui","Non"),
    ("2026-01-03","Non","Oui","Oui","Non","Oui"),
    ("2026-01-04","Oui","Oui","Oui","Oui","Oui"),
    ("2026-01-05","Oui","Oui","Non","Oui","Oui"),
]
for i,row in enumerate(routine_data,start=2):
    routine.write_row(f"A{i}", row)
for i in range(2,7):
    routine.write_formula(f'G{i}', f'=SUMPRODUCT((B{i}:F{i}="Oui")*20)')
routine.conditional_format('G2:G11', {'type':'data_bar','bar_color':'#63C384'})

# =========================
# Objectifs
# =========================
objectifs = wb.add_worksheet("Objectifs")
objectifs.set_column("A:A",15)
objectifs.set_column("B:B",40)
objectifs.set_column("C:E",15)
objectifs.write_row('A1', ["Date","Objectif","Fait","Statut","Score (%)"], bold_center)
objectifs.data_validation('A2:A11', {'validate':'date','criteria':'between','minimum':'2026-01-01','maximum':'2026-12-31'})
objectifs.data_validation('C2:C11', {'validate':'list','source':['Oui','Non','En cours']})
objectifs_data = [
    ("2026-01-01","Méditation 15 min","Oui"),
    ("2026-01-02","Lecture Bible 30 min","En cours"),
    ("2026-01-03","Balayer maison","Non"),
]
for i,row in enumerate(objectifs_data,start=2):
    objectifs.write_row(f"A{i}", row)
for i in range(2,5):
    objectifs.write_formula(f'D{i}', f'=IF(C{i}="Oui","✅",IF(C{i}="En cours","⏳","❌"))')
    objectifs.write_formula(f'E{i}', f'=IF(C{i}="Oui",100,IF(C{i}="En cours",50,0))')
objectifs.conditional_format('D2:D11', {'type':'cell','criteria':'containing','value':'"✅"','format':green_fill})
objectifs.conditional_format('D2:D11', {'type':'cell','criteria':'containing','value':'"⏳"','format':orange_fill})
objectifs.conditional_format('D2:D11', {'type':'cell','criteria':'containing','value':'"❌"','format':red_fill})

# =========================
# Journal spirituel
# =========================
journal = wb.add_worksheet("Journal spirituel")
journal.set_column("A:A",15)
journal.set_column("B:B",60)
journal.write_row('A1', ["Date","Entrée spirituelle"], bold_center)
journal.data_validation('A2:A11', {'validate':'date','criteria':'between','minimum':'2026-01-01','maximum':'2026-12-31'})
journal_data = [
    ("2026-01-01","Merci Seigneur pour cette journée."),
    ("2026-01-02","Prière pour sagesse."),
    ("2026-01-03","Méditation sur gratitude."),
]
for i,row in enumerate(journal_data,start=2):
    journal.write_row(f"A{i}", row)

# Formats
bold_center = wb.add_format({'bold': True, 'align': 'center'})
data_bar = wb.add_format({'bg_color':'#63C384'})

# Création feuille Tableau de bord
dashboard = wb.add_worksheet("Tableau de bord")
dashboard.set_column("A:A",12)
dashboard.set_column("B:F",18)

# Entêtes
dashboard.write_row('A1', ["Mois","Objectifs (%)","Journal (%)","Routine (%)","Finances (%)","Score global (%)"], bold_center)

mois = ["Jan","Fév","Mar","Avr","Mai","Juin","Juil","Août","Sep","Oct","Nov","Déc"]

for i, m in enumerate(mois, start=2):
    dashboard.write(i-1,0,m)
    
    # Objectifs (%) : moyenne des scores Objectifs!E:E pour le mois
    dashboard.write_formula(i-1,1,
        f'=IFERROR(AVERAGEIFS(Objectifs!E:E,Objectifs!A:A,">=2026-{i:02}-01",Objectifs!A:A,"<2026-{i+1:02}-01"),0)')
    
    # Journal (%) : % de jours avec texte rempli
    dashboard.write_formula(i-1,2,
        f'=IFERROR(COUNTIFS(\'Journal spirituel\'!A:A,">=2026-{i:02}-01",\'Journal spirituel\'!A:A,"<2026-{i+1:02}-01",\'Journal spirituel\'!B:B,"<>") / '
        f'COUNTIFS(\'Journal spirituel\'!A:A,">=2026-{i:02}-01",\'Journal spirituel\'!A:A,"<2026-{i+1:02}-01")*100,0)')
    
    # Routine (%) : moyenne des scores Routine!G:G pour le mois
    dashboard.write_formula(i-1,3,
        f'=IFERROR(AVERAGEIFS(Routine!G:G,Routine!A:A,">=2026-{i:02}-01",Routine!A:A,"<2026-{i+1:02}-01"),0)')
    
    # Finances (%) : 100 si solde >=0
    dashboard.write_formula(i-1,4,
        f'=IFERROR(IF(MAX(Finances!D:D)>=0,100,0),0)')
    
    # Score global : moyenne des modules
    dashboard.write_formula(i-1,5,f'=AVERAGE(B{i}:E{i})')

# Barres de progression pour Score global
dashboard.conditional_format('F2:F13', {'type':'data_bar','bar_color':'#4F81BD'})

# Graphique ligne pour Score global
chart = wb.add_chart({'type':'line'})
chart.add_series({
    'name':'Score global',
    'categories':'=Tableau de bord!$A$2:$A$13',
    'values':'=Tableau de bord!$F$2:$F$13'
})
chart.set_title({'name':'Évolution du score global'})
chart.set_x_axis({'name':'Mois'})
chart.set_y_axis({'name':'Score (%)','min':0,'max':100})
dashboard.insert_chart('H2', chart, {'x_scale':1.5,'y_scale':1.5})
# =========================
# Sauvegarde
# =========================
wb.close()
print("✅ Fichier 'SystèmeVie2026_Ultime.xlsx' créé, complet et interactif !")
