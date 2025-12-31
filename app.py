import streamlit as st
from datetime import date
import json
st.set_page_config(
    page_title="Mon système de vie – 2026",
    layout="wide"
)

# Menu latéral
menu = st.sidebar.selectbox(
    "Choisis une section",
    ["Accueil", "Finances", "Routine", "Objectifs","Journal","Score global"]
)

if menu == "Accueil":
    st.title("🌱 Mon système de vie – 2026")
    today = date.today()
    st.info(f"📅 Aujourd’hui : {today}")

    st.markdown("""
    ###  Intention de l’année
    - Discipline quotidienne
    - Vie spirituelle profonde
    - Finances maîtrisées
    - Objectifs clairs

    > *« Celui qui est fidèle dans les petites choses l’est aussi dans les grandes »*
    """)

elif menu == "Finances":
    st.header("💰 Module Finances & Budget")
    st.info("Ici tu pourras gérer tes dépenses et revenus .")

elif menu == "Routine":
    st.header("🕰️ Routine quotidienne")
    st.info("Ici tu pourras suivre ta routine spirituelle et tes tâches quotidiennes.")

elif menu == "Objectifs":
    st.header(" Journal spirituel écrit")
    st.info("Ici tu pourras définir et suivre tes objectifs mensuels et journaliers.")
elif menu == "Journal":
    st.header("💰 Module Finances & Budget")
    st.info("Ici tu pourras écrire tes pensées, prières, méditations profondes…).")
elif menu == "Score global":
    import matplotlib.pyplot as plt
    import pandas as pd
    st.header("📊 Score global & Tableau de bord")

    today = date.today()
    mois = today.strftime("%B")
    annee = today.year

    # -------------------------
    # Charger les modules existants
    # -------------------------
    # Objectifs
    FICHIER_OBJECTIFS = "objectifs.json"
    try:
        with open(FICHIER_OBJECTIFS, "r") as f:
            objectifs = json.load(f)
    except FileNotFoundError:
        objectifs = {}

    key_mois = mois
    total_objectifs = len(objectifs.get(key_mois, []))
    objectifs_faits = sum(1 for obj in objectifs.get(key_mois, []) if obj.get("fait"))
    score_objectifs = int((objectifs_faits / total_objectifs) * 100) if total_objectifs > 0 else 0

    # Journal spirituel
    FICHIER_JOURNAL = "journal_spirituel.json"
    try:
        with open(FICHIER_JOURNAL, "r") as f:
            journal = json.load(f)
    except FileNotFoundError:
        journal = {}

    jours_journal = sum(1 for d in journal if d.startswith(f"{annee}-{today.month:02d}"))
    total_jours_mois = 30  # approximatif
    score_journal = int((jours_journal / total_jours_mois) * 100)

    # Routine quotidienne
    FICHIER_ROUTINE = "routine.json"
    try:
        with open(FICHIER_ROUTINE, "r") as f:
            routine = json.load(f)
    except FileNotFoundError:
        routine = {}

    jours_routine = sum(1 for d in routine if d.startswith(f"{annee}-{today.month:02d}") and all(routine[d].values()))
    score_routine = int((jours_routine / total_jours_mois) * 100)

    # Finances
    FICHIER_FINANCES = "depenses.json"
    try:
        with open(FICHIER_FINANCES, "r") as f:
            finances = json.load(f)
    except FileNotFoundError:
        finances = []

    total_depenses = sum(f["montant"] for f in finances 
                         if f["type"]=="dépense" and f["date"].startswith(f"{annee}-{today.month:02d}"))
    budget = st.number_input("📌 Entrez votre budget pour le mois", min_value=0, step=1000)
    score_finances = int((budget - total_depenses)/budget * 100) if budget > 0 else 0
    score_finances = max(min(score_finances, 100), 0)  # limiter entre 0 et 100

    # -------------------------
    # Score global
    # -------------------------
    score_global = int((score_objectifs + score_journal + score_routine + score_finances)/4)
    st.metric("🌟 Score global du mois", f"{score_global} / 100")

    # -------------------------
    # Graphique comparatif
    # -------------------------
    labels = ["Objectifs", "Journal", "Routine", "Finances"]
    scores = [score_objectifs, score_journal, score_routine, score_finances]

    fig, ax = plt.subplots()
    ax.bar(labels, scores, color=["blue","purple","green","orange"])
    ax.set_ylim(0,100)
    ax.set_ylabel("Score (%)")
    ax.set_title(f"Évolution des différents modules - {mois} {annee}")
    st.pyplot(fig)

    # Détail
    st.markdown("### Détail des scores")
    st.write(f"Objectifs atteints : {score_objectifs}% ({objectifs_faits}/{total_objectifs})")
    st.write(f"Jours de journal complétés : {score_journal}% ({jours_journal}/{total_jours_mois})")
    st.write(f"Routine quotidienne complétée : {score_routine}% ({jours_routine}/{total_jours_mois})")
    st.write(f"Finances dans le budget : {score_finances}% (budget restant: {max(budget - total_depenses,0)}€)")
elif menu == "Score global":
    import matplotlib.pyplot as plt
    import pandas as pd
    st.header("📊 Score global & Tableau de bord")

    today = date.today()
    mois = today.strftime("%B")
    annee = today.year

    # -------------------------
    # Charger les modules existants
    # -------------------------
    # Objectifs
    FICHIER_OBJECTIFS = "objectifs.json"
    try:
        with open(FICHIER_OBJECTIFS, "r") as f:
            objectifs = json.load(f)
    except FileNotFoundError:
        objectifs = {}

    key_mois = mois
    total_objectifs = len(objectifs.get(key_mois, []))
    objectifs_faits = sum(1 for obj in objectifs.get(key_mois, []) if obj.get("fait"))
    score_objectifs = int((objectifs_faits / total_objectifs) * 100) if total_objectifs > 0 else 0

    # Journal spirituel
    FICHIER_JOURNAL = "journal_spirituel.json"
    try:
        with open(FICHIER_JOURNAL, "r") as f:
            journal = json.load(f)
    except FileNotFoundError:
        journal = {}

    jours_journal = sum(1 for d in journal if d.startswith(f"{annee}-{today.month:02d}"))
    total_jours_mois = 30  # approximatif
    score_journal = int((jours_journal / total_jours_mois) * 100)

    # Routine quotidienne
    FICHIER_ROUTINE = "routine.json"
    try:
        with open(FICHIER_ROUTINE, "r") as f:
            routine = json.load(f)
    except FileNotFoundError:
        routine = {}

    jours_routine = sum(1 for d in routine if d.startswith(f"{annee}-{today.month:02d}") and all(routine[d].values()))
    score_routine = int((jours_routine / total_jours_mois) * 100)

    # Finances
    FICHIER_FINANCES = "depenses.json"
    try:
        with open(FICHIER_FINANCES, "r") as f:
            finances = json.load(f)
    except FileNotFoundError:
        finances = []

    total_depenses = sum(f["montant"] for f in finances 
                         if f["type"]=="dépense" and f["date"].startswith(f"{annee}-{today.month:02d}"))
    budget = st.number_input("📌 Entrez votre budget pour le mois", min_value=0, step=1000)
    score_finances = int((budget - total_depenses)/budget * 100) if budget > 0 else 0
    score_finances = max(min(score_finances, 100), 0)  # limiter entre 0 et 100

    # -------------------------
    # Score global
    # -------------------------
    score_global = int((score_objectifs + score_journal + score_routine + score_finances)/4)
    st.metric("🌟 Score global du mois", f"{score_global} / 100")

    # -------------------------
    # Graphique comparatif
    # -------------------------
    labels = ["Objectifs", "Journal", "Routine", "Finances"]
    scores = [score_objectifs, score_journal, score_routine, score_finances]

    fig, ax = plt.subplots()
    ax.bar(labels, scores, color=["blue","purple","green","orange"])
    ax.set_ylim(0,100)
    ax.set_ylabel("Score (%)")
    ax.set_title(f"Évolution des différents modules - {mois} {annee}")
    st.pyplot(fig)

    # Détail
    st.markdown("### Détail des scores")
    st.write(f"Objectifs atteints : {score_objectifs}% ({objectifs_faits}/{total_objectifs})")
    st.write(f"Jours de journal complétés : {score_journal}% ({jours_journal}/{total_jours_mois})")
    st.write(f"Routine quotidienne complétée : {score_routine}% ({jours_routine}/{total_jours_mois})")
    st.write(f"Finances dans le budget : {score_finances}% (budget restant: {max(budget - total_depenses,0)}€)")

