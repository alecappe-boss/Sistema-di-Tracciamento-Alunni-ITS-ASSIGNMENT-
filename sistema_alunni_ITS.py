import os
import json
import csv
import re
from datetime import datetime, timedelta
from statistics import mean

lista_alunni = {}

lista_compiti = {}

alunni="lista_alunni.json"

compiti="lista_compiti.json"

if os.path.exists(alunni):
    with open(alunni, "r", encoding="utf-8") as file:
        try:
            lista_alunni = json.load(file)
        except json.JSONDecodeError:
            lista_alunni = {}

if os.path.exists(compiti):
    with open(compiti, "r", encoding="utf-8") as file:
        try:
            lista_compiti = json.load(file)
        except json.JSONDecodeError:
            lista_compiti = {}

def check(email):
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$'
    if re.fullmatch(regex, email):
        return True
    else:
        return False
    
def salva_alunni():
    with open(alunni, "w", encoding="utf-8") as file:
        json.dump(lista_alunni, file, indent=4, ensure_ascii=False)

def salva_compiti():
    with open(compiti, "w", encoding="utf-8") as file:
        json.dump(lista_compiti, file, indent=4, ensure_ascii=False)

def controlla_struttura(dati, campi_previsti):
    for key, value in dati.items():
        if not isinstance(value, dict):
            print(f"❌ Errore: il valore di '{key}' non è un dizionario")
            return False
        if set(value.keys())!=campi_previsti:
            print(f"❌ Errore: il record '{key}' non ha i campi corretti")
            print("✅ Campi trovati:", set(value.keys()))
            print("✅ Campi attesi:", campi_previsti)
            return False
    return True

def pulisci_schermo():
    os.system('cls' if os.name == 'nt' else 'clear')

# =====================================
# IMPORT / EXPORT CSV
# =====================================

def importa_alunni_csv(file_csv):
    if not os.path.exists(file_csv):
        print("❌ Il file CSV non esiste!")
        return

    inseriti = 0
    ignorati = 0

    with open(file_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            matricola = row.get("matricola")
            nome = row.get("nome", "").title().strip()
            cognome = row.get("cognome", "").title().strip()
            email = row.get("email", "").strip().lower()
            data_nascita = row.get("data_nascita")
            note = row.get("note", "")

            if not matricola or not nome or not cognome or not email or not data_nascita:
                ignorati += 1
                continue

            if matricola in lista_alunni or any(a["email"] == email for a in lista_alunni.values()):
                ignorati += 1
                continue

            lista_alunni[matricola] = {
                "nome": nome,
                "cognome": cognome,
                "email": email,
                "data_nascita": data_nascita,
                "note": note,
                "matricola": matricola,
                "data_creazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_modifica": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "archiviato": False,
                "data_archiviazione": None
            }
            inseriti += 1

    salva_alunni()
    print(f"✅ Alunni importati: {inseriti}, ignorati: {ignorati}")

def esporta_alunni_csv(file_csv):
    if not lista_alunni:
        print("⚠️ Nessun alunno da esportare!")
        return

    campi = ["matricola", "nome", "cognome", "email", "data_nascita", "note", "archiviato"]

    with open(file_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campi)
        writer.writeheader()
        for alunno in lista_alunni.values():
            writer.writerow({campo: alunno.get(campo, "") for campo in campi})

    print(f"✅ Alunni esportati in CSV: {file_csv}")

def importa_compiti_csv(file_csv):
    if not os.path.exists(file_csv):
        print("❌ Il file CSV non esiste!")
        return

    inseriti = 0
    ignorati = 0

    with open(file_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id_compito = row.get("id")
            matr = row.get("alunno_matricola")
            descrizione = row.get("descrizione", "").strip()
            stato = row.get("stato", "assegnato")
            data_assegnazione = row.get("data_assegnazione", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            try:
                valutazione = float(row.get("valutazione", -1))
            except ValueError:
                valutazione = -1

            if not id_compito or not matr or not descrizione:
                ignorati += 1
                continue

            if id_compito in lista_compiti or matr not in lista_alunni:
                ignorati += 1
                continue

            lista_compiti[id_compito] = {
                "id": id_compito,
                "descrizione": descrizione,
                "alunno_matricola": matr,
                "stato": stato,
                "data_assegnazione": data_assegnazione,
                "valutazione": valutazione
            }
            inseriti += 1

    salva_compiti()
    print(f"✅ Compiti importati: {inseriti}, ignorati: {ignorati}")

def esporta_compiti_csv(file_csv):
    if not lista_compiti:
        print("⚠️ Nessun compito da esportare!")
        return

    campi = ["id", "descrizione", "alunno_matricola", "stato", "data_assegnazione", "valutazione"]

    with open(file_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campi)
        writer.writeheader()
        for compito in lista_compiti.values():
            writer.writerow({campo: compito.get(campo, "") for campo in campi})

    print(f"✅ Compiti esportati in CSV: {file_csv}")

while True:
    print("\nSISTEMA DI TRACCIAMENTO ALUNNI - ITS")
    print("""\nSeleziona un opzione:
    a) Inserisci nuovo alunno
    b) Visualizza alunni registrati
    c) Modifica dati alunno
    d) Elimina alunno
    e) Assegna compito a studente
    f) Registra valutazione
    g) Visualizza compiti di uno studente
    h) Visualizza statistiche alunno
    i) Ranking alunni per media voti
    j) Report compiti non completati
    k) Salva dati (backup) - JSON
    l) Carica dati - JSON
    m) Esporta dati CSV
    n) Importa dati CSV
    o) Esci""")

    scelta=input("\nDigita un comando: ").lower().strip()
    
    if scelta=="a":
        print("\n🧑‍🎓 INSERIMENTO NUOVO ALUNNO\n")

        while True:
            nome = " ".join(input("👤 Nome: ").strip().title().split())
            if not nome:
                continue
            if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
                print("❌ Il nome può contenere solo lettere e spazi. Riprova!")
                continue
            break
        
        while True:
            cognome = " ".join(input("👤 Cognome: ").strip().title().split())
            if not cognome:
                continue
            if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", cognome):
                print("❌ Il cognome può contenere solo lettere e spazi. Riprova!")
                continue
            break

        if any(alunno["nome"] == nome and alunno["cognome"] == cognome for alunno in lista_alunni.values()):
                opzione=input("⚠️ Esiste un alunno con lo stesso nome e cognome. Proseguire comunque? (s/n): ").lower().strip()
                while opzione not in ["s", "n"]:
                    opzione=input("⚠️ Scelta non valida. Riprova! (s/n): ").lower().strip()
                if opzione=="n":
                    continue
        
        while True:
            email=" ".join(input("📧 Email: ").strip().lower().split())
            if not check(email):
                print("❌ Formato email non valido!")
                continue

            if any(alunno["email"] == email for alunno in lista_alunni.values()):
                print("❌ L'email inserita esiste già! Riprova.")
                continue
            
            if not email.endswith("allievi.itsdigitalacademy.it"):
                opzione=input("⚠️ Sei sicuro di voler inserire una mail esterna alla scuola? (s/n): ").lower().strip()
                while opzione not in ["s", "n"]:
                    opzione=input("⚠️ Inserisci un'opzione valida (s/n): ").lower().strip()
                if opzione == "s":
                    break
                else:
                    continue
            else:
                break
        
        errato=True
        while errato:
            data_nascita=input("📅 Data di nascita (gg-mm-aaaa): ").strip()
            formato_atteso = "%d-%m-%Y"
            try:
                data_validata = datetime.strptime(data_nascita, formato_atteso)
                oggi = datetime.now()
                eta = oggi.year - data_validata.year - ((oggi.month, oggi.day) < (data_validata.month, data_validata.day))
                if data_validata > oggi:
                    print("❌ Data futura non valida!")
                elif eta < 18:
                    print("🚫 Lo studente deve avere almeno 18 anni.")
                elif eta > 100:
                    print("🚫 Età troppo elevata per un iscritto.")
                else:
                    data_nascita_iso = data_validata.strftime("%Y-%m-%d")
                    print("✅ Formato data corretto:", data_nascita_iso)
                    errato=False
            except ValueError:
                print("❌ Errore: Il formato della data non è corretto. Riprova!")
        
        opzione = input("📝 Vuoi aggiungere delle note relative allo studente? (s/n): ").lower().strip()
        while opzione not in ['s', 'n']:
            print("❌ Errore: scelta non corretta. Riprova!")
            opzione = input("📝 Vuoi aggiungere delle note relative allo studente? (s/n): ").lower().strip()
        if opzione == 's':
            note=input("🗒️ Note aggiuntive (max 500 caratteri): ").strip()
            while len(note) > 500:
                print("❌ Errore: limite massimo di caratteri superato. Riprova!")
                note=input("🗒️ Note aggiuntive (max 500 caratteri): ").strip()
        else:
            note = ""
        
        while True:
            matricola="MAT" + datetime.now().strftime("%Y%m%d%H%M%S")
            if matricola not in lista_alunni:
                break
        
        ora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n📋 Riepilogo dati alunno:")
        print("-"*30)
        print(f"👤 Nome: {nome}")
        print(f"👤 Cognome: {cognome}")
        print(f"📧 Email: {email}")
        print(f"📅 Data di nascita: {data_nascita_iso}")
        print(f"🗒️ Note: {note}")
        print(f"🆔 Matricola: {matricola}")
        print("-"*30)

        while True:
            conferma=input("✅ Confermi il salvataggio dei dati sopra indicati? (s/n): ").lower().strip()
            if conferma not in ['s', 'n']:
                print("❌ Errore: scelta errata. Riprova!")
            else:
                break

        if conferma == "n":
            print("❌ Inserimento annullato.")
            input("\n⏎ Premi Invio per tornare al menu...")
            pulisci_schermo()
            continue

        lista_alunni[matricola]={
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "data_nascita": data_nascita_iso,
            "note": note,
            "matricola": matricola,
            "data_creazione":ora,
            "data_modifica":ora,
            "archiviato": False,
            "data_archiviazione": None
        }
        
        salva_alunni()
        
        print(f"\n🎉 Alunno '{nome} {cognome}' inserito con successo!")
        print(f"🆔 Matricola: {matricola}")
        print(f"⏱️ Data creazione: {ora}")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo() 
    
    elif scelta=="b":
        print("\n📂 VISUALIZZAZIONE ALUNNI\n")

        if not lista_alunni:
            print("\n⚠️ Nessun alunno registrato!")
        else:
            opzione = input("👀 Quali alunni vuoi vedere? (f)requentanti, (a)rchiviati, (t)utti: ").lower().strip()
            while opzione not in ['f', 'a', 't']:
                print("❌ Errore: scelta non corretta. Riprova!")
                opzione = input("👀 Quali alunni vuoi vedere? (f)requentanti, (a)rchiviati, (t)utti: ").lower().strip()
            
            lista_alunni_ordinata = sorted(lista_alunni.items(), key=lambda item: (item[1]['cognome'], item[1]['nome']))

            if opzione == 'f':
                trovato=False
                print("\n📋 Alunni attivi in ordine alfabetico:")
                for matricola, info in lista_alunni_ordinata:
                    if info["archiviato"] == False:
                        trovato=True
                        print(f"\n🆔 Matricola: {matricola}")
                        print(f"👤 Nome: {info['nome']}")
                        print(f"👤 Cognome: {info['cognome']}")
                        print(f"📧 E-mail: {info['email']}")
                        print(f"⏱️ Data creazione: {info['data_creazione']}")
                        print("-" * 50)
                if not trovato:
                    print("⚠️ Nessun alunno attivo trovato!")
                    opzione = input("📂 Vuoi vedere comunque gli alunni archiviati? (s/n): ").lower().strip()
                    while opzione not in ['s', 'n']:
                        print("❌ Errore: scelta non corretta. Riprova!")
                        opzione = input("📂 Vuoi vedere comunque gli alunni archiviati? (s/n): ").lower().strip()
                    if opzione == 's':
                        print("\n📋 Alunni archiviati in ordine alfabetico:")
                        for matricola, info in lista_alunni_ordinata:
                            print(f"\n🆔 Matricola: {matricola}")
                            print(f"👤 Nome: {info['nome']}")
                            print(f"👤 Cognome: {info['cognome']}")
                            print(f"📧 E-mail: {info['email']}")
                            print(f"⏱️ Data creazione: {info['data_creazione']}")
                            print("-" * 50)
            
            elif opzione == 'a':
                trovato=False
                print("\n📋 Alunni archiviati in ordine alfabetico:")
                for matricola, info in lista_alunni_ordinata:
                    if info["archiviato"] == True:
                        trovato=True
                        print(f"\n🆔 Matricola: {matricola}")
                        print(f"👤 Nome: {info['nome']}")
                        print(f"👤 Cognome: {info['cognome']}")
                        print(f"📧 E-mail: {info['email']}")
                        print(f"⏱️ Data creazione: {info['data_creazione']}")
                        print("-" * 50)
                if not trovato:
                    print("⚠️ Nessun alunno archiviato trovato!")
                    opzione = input("👀 Vuoi vedere comunque gli alunni frequentanti? (s/n): ").lower().strip()
                    while opzione not in ['s', 'n']:
                        print("❌ Errore: scelta non corretta. Riprova!")
                        opzione = input("👀 Vuoi vedere comunque gli alunni frequentanti? (s/n): ").lower().strip()
                    if opzione == 's':
                        print("\n📋 Alunni attivi in ordine alfabetico:")
                        for matricola, info in lista_alunni_ordinata:
                            print(f"\n🆔 Matricola: {matricola}")
                            print(f"👤 Nome: {info['nome']}")
                            print(f"👤 Cognome: {info['cognome']}")
                            print(f"📧 E-mail: {info['email']}")
                            print(f"⏱️ Data creazione: {info['data_creazione']}")
                            print("-" * 50)
                
            else:
                print("\n📋 Elenco alunni in ordine alfabetico:")
                for matricola, info in lista_alunni_ordinata:
                    print(f"\n🆔 Matricola: {matricola}")
                    print(f"👤 Nome: {info['nome']}")
                    print(f"👤 Cognome: {info['cognome']}")
                    print(f"📧 E-mail: {info['email']}")
                    print(f"⏱️ Data creazione: {info['data_creazione']}")
                    if info['archiviato'] == False:
                        print(f"🟢 Stato: attivo")
                    else:
                        print(f"📦 Stato: archiviato")
                    print("-" * 50)
        
        input("\n⏎ Premi Invio per continuare...") 
        pulisci_schermo()

    elif scelta=="c":
        print("\n✏️ MODIFICA DATI ALUNNO\n")

        matr=input("🆔 Matricola: ").strip()
        
        if matr in lista_alunni:
            alunno = lista_alunni[matr]
            print("📋 ---- Riepilogo dati studente ----")
            print(f"\n🆔 Matricola: {matr}")
            print(f"👤 Nome: {alunno['nome']}")
            print(f"👤 Cognome: {alunno['cognome']}")
            print(f"📧 E-mail: {alunno['email']}")
            print(f"⏱️ Data creazione: {alunno['data_creazione']}")
            print("-" * 50)
            modifica="s"
            while modifica=="s":
                print("✏️ Cosa vuoi modificare?")
                print("👤 n) nome")
                print("👤 c) cognome")
                print("📧 e) e-mail")
                
                opzione=input("\n➡️ Inserisci l'opzione desiderata: ").lower().strip()
                while opzione not in ["n", "c", "e"]:
                    opzione=input("❌ Opzione non valida! Riprova: ").lower().strip()
                
                if opzione=="n":
                    while True:
                        new_nome = " ".join(input("👤 Nuovo nome: ").strip().title().split())
                        if not new_nome:
                            continue
                        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", new_nome):
                            print("❌ Il nome può contenere solo lettere e spazi. Riprova!")
                            continue
                        break
                    conferma = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
                    while conferma not in ['s', 'n']:
                        print("❌ Errore: scelta non corretta. Riprova!")
                        conferma = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
                    
                    if conferma == 's':
                        lista_alunni[matr]["nome"]=new_nome
                    else:
                        print("🚫 Operazione annullata")
                
                elif opzione=="c":
                    while True:
                        new_cognome = " ".join(input("👤 Nuovo cognome: ").strip().title().split())
                        if not new_cognome:
                            continue
                        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", new_cognome):
                            print("❌ Il cognome può contenere solo lettere e spazi. Riprova!")
                            continue
                        break
                    conferma = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
                    while conferma not in ['s', 'n']:
                        print("❌ Errore: scelta non corretta. Riprova!")
                        conferma = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
                    
                    if conferma == 's':
                        lista_alunni[matr]["cognome"]=new_cognome
                    else:
                        print("🚫 Operazione annullata")
                
                elif opzione=="e":
                    while True:
                        new_email = " ".join(input("📧 Nuova email: ").strip().lower().split())
                        if not check(new_email):
                            print("❌ Formato email non valido!")
                            continue

                        if any(alunno["email"] == new_email for alunno in lista_alunni.values()):
                            print("❌ L'email inserita esiste già! Riprova.")
                            continue
                        
                        if not new_email.endswith("allievi.itsdigitalacademy.it"):
                            opzione=input("⚠️ Sei sicuro di voler inserire una mail esterna alla scuola? (s/n): ").lower().strip()
                            while opzione not in ["s", "n"]:
                                opzione=input("⚠️ Inserisci un'opzione valida (s/n): ").lower().strip()
                            if opzione == "s":
                                break
                            else:
                                continue
                        else:
                            break
                    
                    conferma = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
                    while conferma not in ['s', 'n']:
                        print("❌ Errore: scelta non corretta. Riprova!")
                        conferma = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
                    if conferma == 's':
                        lista_alunni[matr]["email"] = new_email
                    else:
                        print("🚫 Operazione annullata")

                lista_alunni[matr]["data_modifica"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                salva_alunni()
                
                print("✅ Dati modificati con successo!")
                print("\n📋 ---- Riepilogo dati studente ----")
                print(f"\n🆔 Matricola: {matr}")
                print(f"👤 Nome: {alunno['nome']}")
                print(f"👤 Cognome: {alunno['cognome']}")
                print(f"📧 E-mail: {alunno['email']}")
                print(f"⏱️ Data creazione: {alunno['data_creazione']}")
                print("-" * 50)
                
                modifica=input(f"🔁 Vuoi modificare altri dati della matricola {matr}? (s)ì/(n)o: ").lower().strip()
                while modifica not in ["s", "n"]:
                    modifica = input("❌ Risposta non valida! Digita 's' o 'n': ").lower().strip()
        else:
            print("❌ La matricola indicata non è presente!")
        
        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta == "d":
        print("\n🗄️ ARCHIVIAZIONE / ELIMINAZIONE ALUNNO\n")
        
        matr = input("🆔 Matricola: ").strip().upper()

        if matr in lista_alunni:
            alunno = lista_alunni[matr]

            print("\n📋 ---- Riepilogo dati studente ----")
            print(f"\n🆔 Matricola: {matr}")
            print(f"👤 Nome: {alunno['nome']}")
            print(f"👤 Cognome: {alunno['cognome']}")
            print(f"📧 E-mail: {alunno['email']}")
            print(f"⏱️ Data creazione: {alunno['data_creazione']}")
            print("-" * 50)

            # Recupero compiti associati (attivi o archiviati)
            compiti_associati = []
            for compito in lista_compiti.values():
                if compito["alunno_matricola"] == matr:
                    compiti_associati.append(compito)

            # ===============================
            # CASO: STUDENTE GIÀ ARCHIVIATO
            # ===============================
            if alunno["archiviato"]:
                print("⚠️ Lo studente è già archiviato.")

                if compiti_associati:
                    print("❌ Eliminazione definitiva NON consentita.")
                    print("📦 Sono presenti compiti associati (storico da preservare).")
                else:
                    elimina = input("🗑️ Vuoi eliminarlo definitivamente? (s/n): ").lower().strip()
                    if elimina == "s":
                        conferma = input(f"⚠️ Sei sicuro di voler eliminare definitivamente {alunno['nome']} {alunno['cognome']}? (s/n): ").lower().strip()

                        if conferma == "s":
                            lista_alunni.pop(matr)
                            salva_alunni()
                            print("✅ Alunno eliminato definitivamente!")
                        else:
                            print("🚫 Operazione annullata")

            # ===============================
            # CASO: STUDENTE NON ARCHIVIATO
            # ===============================
            else:
                soft = input("➡️ Vuoi (a)rchiviarlo o (e)liminarlo definitivamente?: ").lower().strip()

                while soft not in ["a", "e"]:
                    soft = input("❌ Scelta non valida. Digita 'a' o 'e': ").lower().strip()

                # -------- ARCHIVIAZIONE --------
                if soft == "a":
                    conferma = input(f"📦 Sei sicuro di voler archiviare {alunno['nome']} {alunno['cognome']}? (s/n): ").lower().strip()

                    if conferma == "s":
                        lista_alunni[matr]["archiviato"] = True
                        lista_alunni[matr]["data_archiviazione"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        lista_alunni[matr]["data_modifica"] = lista_alunni[matr]["data_archiviazione"]

                        # Archivia anche i compiti associati
                        for compito in compiti_associati:
                            compito["stato"] = "archiviato"

                        salva_alunni()
                        salva_compiti()
                        print("✅ Studente e compiti associati archiviati con successo!")
                    else:
                        print("🚫 Operazione annullata")

                # -------- ELIMINAZIONE --------
                else:
                    if compiti_associati:
                        print("⚠️ Attenzione: lo studente ha compiti associati.")
                        scelta = input("📦 Vuoi archiviare studente e compiti invece di eliminarli? (s/n): ").lower().strip()

                        if scelta == "s":
                            lista_alunni[matr]["archiviato"] = True
                            lista_alunni[matr]["data_modifica"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            for compito in compiti_associati:
                                compito["stato"] = "archiviato"

                            salva_alunni()
                            salva_compiti()
                            print("✅ Studente e compiti archiviati con successo!")
                        else:
                            print("🚫 Eliminazione annullata per preservare i dati")
                    else:
                        conferma = input(f"🗑️ Sei sicuro di voler eliminare definitivamente {alunno['nome']} {alunno['cognome']}? (s/n): ").lower().strip()

                        if conferma == "s":
                            lista_alunni.pop(matr)
                            salva_alunni()
                            print("✅ Alunno eliminato definitivamente!")
                        else:
                            print("🚫 Operazione annullata")

        else:
            print("❌ La matricola inserita non corrisponde a nessuno studente!")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta=="e":
        print("\n📝 ASSEGNA NUOVO COMPITO\n")

        id="TASK" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        descrizione=input("📝 Descrizione: ").strip()
        while len(descrizione) < 5 or len(descrizione) > 200:
            print("🚫 Descrizione non valida. Lunghezza consentita: 5–200 caratteri.")
            descrizione=input("📝 Descrizione: ").strip()
        
        matr=input("🆔 Matricola studente: ").strip()
        while matr not in lista_alunni:
            print("❌ La matricola inserita non corrisponde a nessuno studente! Riprova")
            matr=input("🆔 Matricola studente: ").strip()
        
        if lista_alunni[matr]['archiviato']:
            print("🚫 Impossibile assegnare compiti a uno studente archiviato")
        else:
            data_assegnazione=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lista_compiti[id]={
                "id": id,
                "descrizione": descrizione,
                "alunno_matricola": matr,
                "stato": "assegnato",
                "data_assegnazione": data_assegnazione,
                "valutazione": -1
            }
            
            salva_compiti()
            print(f"\n✅ Compito inserito con successo!")
            print(f"🆔 ID Compito: {id}")
            print(f"📝 Descrizione: {descrizione}")
            print(f"👤 Matricola studente: {matr}")
            print(f"⏱️ Data assegnazione: {data_assegnazione}")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta == "f":
        print("\n⭐ REGISTRA VALUTAZIONE COMPITO\n")

        id = input("🆔 ID compito: ").strip().upper()

        if id in lista_compiti:
            compito = lista_compiti[id]
            alunno_id = compito["alunno_matricola"]
            studente = lista_alunni[alunno_id]

            if lista_alunni[alunno_id]["archiviato"]:
                print("🚫 Lo studente è archiviato. Impossibile registrare valutazioni!")

            elif compito["stato"] == "archiviato":
                print("📦 Il compito è archiviato perché lo studente è archiviato")

            elif compito["stato"] == "completato":
                print("⚠️ Il compito è già stato valutato!")

            else:
                print(f"\n📋 Compito: {compito['descrizione']}")
                print(f"👤 Studente: {studente['nome']} {studente['cognome']}")

                while True:
                    try:
                        valutazione = float(input("⭐ Valutazione (3-10): "))
                        if 3 <= valutazione <= 10:
                            break
                        print("❌ Devi inserire una valutazione compresa tra 3 e 10!")
                    except ValueError:
                        print("❌ Devi inserire un valore numerico valido!")
                
                conferma = input(f"✅ Confermi di voler registrare la valutazione {valutazione} per {studente['nome']} {studente['cognome']}? (s/n): ").lower().strip()
                while conferma not in ['s', 'n']:
                    conferma = input("❌ Risposta non valida. Digita s/n: ").lower().strip()
                if conferma == 's':
                    compito["valutazione"] = valutazione
                    compito["stato"] = "completato"
                    salva_compiti()
                    print(f"🎉 Valutazione registrata con successo per il compito {id}!")
                else:
                    print("🚫 Operazione annullata!")
        else:
            print("❌ L'ID inserito non corrisponde a nessun compito!")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta=="g":
        print("\n📚 VISUALIZZA COMPITI PER STUDENTE\n")

        matr=input("🆔 Matricola: ").strip()
        if matr in lista_alunni:
            if lista_alunni[matr]["archiviato"]:
                print("⚠️ Studente archiviato!")
            trovati=False
            print(f"\n📋 Compiti di {lista_alunni[matr]['nome']} {lista_alunni[matr]['cognome']}:")
            
            for compito in lista_compiti.values():
                if compito["alunno_matricola"] == matr:
                    trovati=True
                    if compito["valutazione"]==-1:
                        print(f"- 📝 ID: {compito['id']}, Descrizione: {compito['descrizione']}, Stato: {compito['stato']}")
                    else:
                        print(f"- 📝 ID: {compito['id']}, Descrizione: {compito['descrizione']}, Stato: {compito['stato']}, ⭐ Valutazione: {compito['valutazione']}")
            
            if not trovati:
                print("⚠️ Nessun compito trovato per questo studente!")
        else:
            print("❌ La matricola inserita non corrisponde a nessuno studente!")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta == "h":
        print("\n📊 STATISTICHE STUDENTE\n")

        matr = input("🆔 Matricola: ").strip().upper()

        if matr not in lista_alunni:
            print("❌ La matricola inserita non corrisponde a nessuno studente! Riprova")
        else:
            studente = lista_alunni[matr]

            print(f"\n📋 Statistiche di {studente['nome']} {studente['cognome']}:")

            if studente["archiviato"]:
                print("⚠️ Studente archiviato!")

            voti = []
            compiti_non_completati = []

            # Ciclo sui compiti dello studente
            for compito in lista_compiti.values():
                if compito["alunno_matricola"] == matr:
                    if compito["stato"] == "completato" and compito["valutazione"] != -1:
                        voti.append(compito["valutazione"])
                    elif compito["stato"] == "assegnato":
                        compiti_non_completati.append(compito["descrizione"])

            completati = len(voti)
            assegnati = len(compiti_non_completati)

            # Stampa riepilogo generale
            print(f"✅ Compiti completati: {completati}")
            print(f"🕒 Compiti assegnati/non completati: {assegnati}")

            # Statistiche sui voti
            if voti:
                media = mean(voti)
                voto_min = min(voti)
                voto_max = max(voti)
                print(f"📈 Media voti: {media:.2f}")
                print(f"🔻 Voto minimo: {voto_min}")
                print(f"🔺 Voto massimo: {voto_max}")
                print("📉 Progressione voti:", ", ".join(f"{v:.1f}" for v in voti))

            # Elenco compiti non completati
            if compiti_non_completati:
                print("\n📌 Compiti non completati:")
                for c in compiti_non_completati:
                    print("- 📝 ", c)

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta=="i":
        print("\n🏆 CLASSIFICA ALUNNI PER MEDIA VOTI\n")

        medie={}
        for matricola, info in lista_alunni.items():
            if info["archiviato"]==False:
                somma=0
                conteggio=0
                for compito in lista_compiti.values():
                    if compito["alunno_matricola"]==matricola and compito["stato"]=="completato":
                        somma+=compito["valutazione"]
                        conteggio+=1
                if conteggio>0:
                    media=somma/conteggio
                    medie[matricola] = media
                else:
                    medie[matricola] = None

        # Ordinamento: media decrescente, poi cognome, poi nome, gestendo None
        ranking=sorted(
            medie.items(),
            key=lambda item: (
                -(item[1] if item[1] is not None else -1),
                lista_alunni[item[0]]['cognome'],
                lista_alunni[item[0]]['nome']
            )
        )

        print("\n🏅 Ranking alunni per media voti:")
        if not medie:
            print("⚠️ Nessun alunno attivo con voti registrati")
        else:
            for i, (matricola, media) in enumerate(ranking, start=1):
                nome = lista_alunni[matricola]["nome"]
                cognome = lista_alunni[matricola]["cognome"]
                if media is not None:
                    print(f"🏅 {i}. {nome} {cognome} ({matricola}) - Media: {media:.2f}")
                else:
                    print(f"📌 {i}. {nome} {cognome} ({matricola}) - Media: N/A")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta=="j":
        non_completati={}
        
        for id, compito in lista_compiti.items():
            matr = compito["alunno_matricola"]
            if compito["stato"]=="assegnato" and not lista_alunni[matr]["archiviato"]:
                non_completati[id]=compito
        
        if non_completati:
            non_completati_ordinati = sorted(non_completati.values(), key=lambda c: (lista_alunni[c["alunno_matricola"]]["cognome"], lista_alunni[c["alunno_matricola"]]["nome"],c["data_assegnazione"]))
            
            print("\n📌 COMPITI NON COMPLETATI:")
            
            for c in non_completati_ordinati:
                matr = c["alunno_matricola"]
                nome = lista_alunni[matr]["nome"]
                cognome = lista_alunni[matr]["cognome"]
                data = c["data_assegnazione"]
                print(f"- 📝 {c['id']}: {c['descrizione']} (👤 {nome} {cognome}) - ⏱️ Assegnato il {data}")
        else:
            print("✅ Nessun compito non completato!")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta == "k":
        print("📦 Creazione backup...")
        cartella = "backup"
        
        if not os.path.exists(cartella):
            os.makedirs(cartella)
            print(f"✅ Cartella {cartella} creata!")
        
        now=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_alunni = os.path.join(cartella, "lista_alunni_" + now + ".json")
        backup_compiti = os.path.join(cartella, "lista_compiti_" + now + ".json")
       
        try:
            with open(backup_alunni, "w", encoding="utf-8") as f:
                json.dump(lista_alunni, f, indent=4, ensure_ascii=False)
            
            with open(backup_compiti, "w", encoding="utf-8") as f:
                json.dump(lista_compiti, f, indent=4, ensure_ascii=False)
            
            print("✅ File di backup creati con successo!")
        except Exception as e:
            print(f"❌ Errore durante la creazione dei backup: {e}")

        limite_data = datetime.now() - timedelta(days=7)
        print("📂 File presenti nella cartella backup:")
        
        # Lista solo file, ordinata per data di creazione
        try:
            files = [f for f in os.listdir(cartella) if os.path.isfile(os.path.join(cartella, f))]
            files_sorted = sorted(files, key=lambda f: os.path.getctime(os.path.join(cartella, f)))

            for nome in files_sorted:
                percorso_file = os.path.join(cartella, nome)
                try:
                    data_creazione = datetime.fromtimestamp(os.path.getctime(percorso_file))
                    if data_creazione < limite_data:
                        os.remove(percorso_file)
                    else:
                        print("- 📄 ", nome)
                except Exception as e:
                    print(f"⚠️ Impossibile gestire il file {nome}: {e}")
        except Exception as e:
            print(f"⚠️ Impossibile leggere la cartella {cartella}: {e}")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta == "l":
        print("\n📥 CARICAMENTO FILE JSON\n")

        file_caricato = input("📄 File JSON da caricare: ").strip()

        if not file_caricato.endswith(".json"):
            print("❌ L'estensione può essere esclusivamente '.json'")
        elif not os.path.exists(file_caricato):
            print("❌ Il file non esiste!")
        else:
            tipo = input("Il file caricato contiene (a)lunni o (c)ompiti?: ").lower().strip()
            while tipo not in ["a", "c"]:
                print("❌ Scelta errata! Riprova")
                tipo = input("Il file caricato contiene (a)lunni o (c)ompiti?: ").lower().strip()

            campi_alunni = {
                "nome", "cognome", "email", "data_nascita", "note",
                "matricola", "data_creazione", "data_modifica",
                "archiviato", "data_archiviazione"
            }

            campi_compiti = {
                "id", "descrizione", "alunno_matricola",
                "stato", "data_assegnazione", "valutazione"
            }

            campi_previsti = campi_alunni if tipo == "a" else campi_compiti

            print(f"📥 Caricamento file {file_caricato}...")

            try:
                with open(file_caricato, "r", encoding="utf-8") as file:
                    dati_caricati = json.load(file)

                if not controlla_struttura(dati_caricati, campi_previsti):
                    print("❌ Il file JSON non ha la struttura corretta. Caricamento annullato!")
                else:
                    inseriti = 0
                    ignorati = 0

                    # =======================
                    # CARICAMENTO ALUNNI
                    # =======================
                    if tipo == "a":
                        for m, info in dati_caricati.items():
                            try:
                                if not check(info["email"]):
                                    print(f"⚠️ Email non valida per {m}")
                                    ignorati += 1
                                    continue

                                if any(a["email"] == info["email"] for a in lista_alunni.values()):
                                    print(f"⚠️ Email duplicata per {m}")
                                    ignorati += 1
                                    continue

                                if not isinstance(info["archiviato"], bool):
                                    print(f"⚠️ 'archiviato' non booleano per {m}")
                                    ignorati += 1
                                    continue

                                datetime.strptime(info["data_creazione"], "%Y-%m-%d %H:%M:%S")
                                datetime.strptime(info["data_modifica"], "%Y-%m-%d %H:%M:%S")

                                if info["data_archiviazione"] is not None:
                                    datetime.strptime(info["data_archiviazione"], "%Y-%m-%d %H:%M:%S")

                            except Exception as e:
                                print(f"⚠️ Errore validazione alunno {m}: {e}")
                                ignorati += 1
                                continue

                            if m not in lista_alunni:
                                lista_alunni[m] = info
                                inseriti += 1
                            else:
                                ignorati += 1

                        salva_alunni()
                        print(f"✅ {inseriti} alunni caricati")
                        if ignorati:
                            print(f"⚠️ {ignorati} alunni ignorati")

                    # =======================
                    # CARICAMENTO COMPITI
                    # =======================
                    else:
                        for id, compito in dati_caricati.items():
                            try:
                                if compito["stato"] not in ["assegnato", "completato", "archiviato"]:
                                    print(f"⚠️ Stato non valido per compito {id}")
                                    ignorati += 1
                                    continue

                                if not isinstance(compito["valutazione"], (int, float)) or not -1 <= compito["valutazione"] <= 10:
                                    print(f"⚠️ Valutazione non valida per compito {id}")
                                    ignorati += 1
                                    continue

                                if compito["stato"] == "assegnato" and compito["valutazione"] != -1:
                                    print(f"⚠️ Compito {id}: valutazione presente ma stato assegnato")
                                    ignorati += 1
                                    continue

                                if compito["stato"] == "completato" and compito["valutazione"] == -1:
                                    print(f"⚠️ Compito {id}: completato senza valutazione")
                                    ignorati += 1
                                    continue

                                datetime.strptime(compito["data_assegnazione"], "%Y-%m-%d %H:%M:%S")

                                # 🔒 studente deve esistere
                                matr = compito["alunno_matricola"]
                                if matr not in lista_alunni:
                                    print(f"❌ Compito {id}: studente {matr} inesistente")
                                    ignorati += 1
                                    continue

                                # 🔒 compito archiviato solo se studente archiviato
                                if compito["stato"] == "archiviato" and not lista_alunni[matr]["archiviato"]:
                                    print(f"❌ Compito {id} archiviato ma studente attivo")
                                    ignorati += 1
                                    continue

                            except Exception as e:
                                print(f"⚠️ Errore validazione compito {id}: {e}")
                                ignorati += 1
                                continue

                            if id not in lista_compiti:
                                lista_compiti[id] = compito
                                inseriti += 1
                            else:
                                ignorati += 1

                        salva_compiti()
                        print(f"✅ {inseriti} compiti caricati")
                        if ignorati:
                            print(f"⚠️ {ignorati} compiti ignorati")

            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"❌ Errore nel file JSON: {e}")

        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()
    
    elif scelta == "m":
        file_csv = input("📄 Nome file CSV esportazione: ").strip()
        tipo = input("Vuoi esportare (a)lunni o (c)ompiti?: ").lower().strip()
        if tipo == "a":
            esporta_alunni_csv(file_csv + ".csv")
        else:
            esporta_compiti_csv(file_csv + ".csv")
        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta == "n":
        file_csv = input("📄 Nome file CSV da importare: ").strip()
        tipo = input("Vuoi importare (a)lunni o (c)ompiti?: ").lower().strip()
        if tipo == "a":
            importa_alunni_csv(file_csv + ".csv")
        else:
            importa_compiti_csv(file_csv + ".csv")
        input("\n⏎ Premi Invio per continuare...")
        pulisci_schermo()

    elif scelta=="o":
        print()
        break
    else:
        print("Scelta non valida!")