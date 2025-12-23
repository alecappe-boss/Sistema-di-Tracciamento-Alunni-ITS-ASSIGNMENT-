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

            if not check(email):
                print(f"⚠️ Email non valida per {nome} {cognome}: {email}")
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

def cerca_studente(input_utente):
    query = input_utente.strip().lower()

    # Caso diretto: matricola
    if query.upper() in lista_alunni:
        return query.upper()

    risultati = []

    for matricola, alunno in lista_alunni.items():
        nome = alunno["nome"].lower()
        cognome = alunno["cognome"].lower()
        nome_cognome = f"{nome} {cognome}"
        cognome_nome = f"{cognome} {nome}"

        if query in [nome, cognome, nome_cognome, cognome_nome]:
            risultati.append(matricola)

    if not risultati:
        print("❌ Nessuno studente trovato")
        return None

    if len(risultati) == 1:
        return risultati[0]

    print("\n🔍 Più studenti trovati:")
    for i, m in enumerate(risultati, start=1):
        a = lista_alunni[m]
        print(f"{i}) {a['nome']} {a['cognome']} – {m}")

    while True:
        try:
            scelta = int(input("➡️ Seleziona uno studente: "))
            if 1 <= scelta <= len(risultati):
                return risultati[scelta - 1]
        except ValueError:
            pass
        print("❌ Scelta non valida")

def valida_nome(nome):
    if not nome:
        return False
    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome))

def valida_email_univoca(email):
    if not check(email):
        return False
    return not any(alunno["email"] == email for alunno in lista_alunni.values())

def valida_data_nascita(data_nascita):
    try:
        data_validata = datetime.strptime(data_nascita, "%d-%m-%Y")
        oggi = datetime.now()
        eta = oggi.year - data_validata.year - (
            (oggi.month, oggi.day) < (data_validata.month, data_validata.day)
        )

        if data_validata > oggi:
            return False, "futura"
        if eta < 18:
            return False, "minore"
        if eta > 100:
            return False, "anziano"

        return True, data_validata.strftime("%Y-%m-%d")
    except ValueError:
        return False, "formato"


def genera_matricola():
    while True:
        matricola = "MAT" + datetime.now().strftime("%Y%m%d%H%M%S")
        if matricola not in lista_alunni:
            return matricola

def crea_alunno(nome, cognome, email, data_nascita_iso, note):
    ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    matricola = genera_matricola()

    lista_alunni[matricola] = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "data_nascita": data_nascita_iso,
        "note": note,
        "matricola": matricola,
        "data_creazione": ora,
        "data_modifica": ora,
        "archiviato": False,
        "data_archiviazione": None
    }

    salva_alunni()
    return matricola, ora

def stampa_info_alunno(matricola, info=None, mostra_stato=False, riepilogo=False):
    """
    Stampa le informazioni principali di uno studente.

    Args:
        matricola (str): Matricola dello studente.
        info (dict, optional): Dizionario dati studente. Se None, prende da lista_alunni.
        mostra_stato (bool): Se True mostra lo stato (archiviato/attivo).
        riepilogo (bool): Se True mostra intestazione 'Riepilogo dati studente'.
    """
    if info is None:
        info = lista_alunni.get(matricola)
        if info is None:
            print(f"❌ Studente con matricola {matricola} non trovato!")
            return

    if riepilogo:
        print("📋 ---- Riepilogo dati studente ----")

    print(f"\n🆔 Matricola: {matricola}")
    print(f"👤 Nome: {info['nome']}")
    print(f"👤 Cognome: {info['cognome']}")
    print(f"📧 E-mail: {info['email']}")
    print(f"⏱️ Data creazione: {info['data_creazione']}")

    if mostra_stato:
        stato = "archiviato" if info.get("archiviato") else "attivo"
        print(f"📦 Stato: {stato}" if stato == "archiviato" else f"🟢 Stato: {stato}")

    print("-" * 50)

def alunni_ordinati():
    return sorted(
        lista_alunni.items(),
        key=lambda item: (item[1]['cognome'], item[1]['nome'])
    )

def stampa_lista_alunni(filtro):
    trovati = False

    for matricola, info in alunni_ordinati():
        if filtro == "f" and info["archiviato"]:
            continue
        if filtro == "a" and not info["archiviato"]:
            continue

        trovati = True
        stampa_info_alunno(matricola, info)

    return trovati

def modifica_nome(matricola):
    while True:
        nuovo = " ".join(input("👤 Nuovo nome: ").strip().title().split())
        if valida_nome(nuovo):
            break
        print("❌ Il nome può contenere solo lettere e spazi.")

    if conferma_modifica():
        lista_alunni[matricola]["nome"] = nuovo

def modifica_cognome(matricola):
    while True:
        nuovo = " ".join(input("👤 Nuovo cognome: ").strip().title().split())
        if valida_nome(nuovo):
            break
        print("❌ Il cognome può contenere solo lettere e spazi.")

    if conferma_modifica():
        lista_alunni[matricola]["cognome"] = nuovo

def modifica_email(matricola):
    while True:
        nuova = " ".join(input("📧 Nuova email: ").strip().lower().split())

        if not check(nuova):
            print("❌ Formato email non valido!")
            continue

        if any(a["email"] == nuova for a in lista_alunni.values()):
            print("❌ Email già esistente!")
            continue

        if not nuova.endswith("allievi.itsdigitalacademy.it"):
            opzione = input("⚠️ Email esterna. Confermi? (s/n): ").lower().strip()
            if opzione != "s":
                continue
        break

    if conferma_modifica():
        lista_alunni[matricola]["email"] = nuova

def conferma_modifica():
    scelta = input("✅ Vuoi salvare queste modifiche? (s/n): ").lower().strip()
    while scelta not in ['s', 'n']:
        scelta = input("❌ Risposta non valida. (s/n): ").lower().strip()
    if scelta == 's':
        return True
    print("🚫 Operazione annullata")
    return False

# ===============================
# FUNZIONI DI LOGICA COMPITI
# ===============================
def genera_id_compito():
    return "TASK" + datetime.now().strftime("%Y%m%d%H%M%S")

def valida_descrizione_compito(descrizione):
    """Ritorna True se la descrizione è valida, altrimenti False"""
    return 5 <= len(descrizione) <= 200

def crea_compito_logico(descrizione, matricola):
    """Crea il compito e lo salva, senza stampare nulla"""
    id_compito = genera_id_compito()
    data_assegnazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    compito = {
        "id": id_compito,
        "descrizione": descrizione,
        "alunno_matricola": matricola,
        "stato": "assegnato",
        "data_assegnazione": data_assegnazione,
        "valutazione": -1
    }
    
    lista_compiti[id_compito] = compito
    salva_compiti()
    return compito

def statistiche_alunno(matricola):
    """Ritorna un dizionario con le statistiche di uno studente, evitando KeyError."""
    voti = []
    compiti_non_completati = []
    durate_compiti = {}

    for compito in lista_compiti.values():
        if compito.get("alunno_matricola") != matricola:
            continue

        stato = compito.get("stato", "assegnato")
        valutazione = compito.get("valutazione", -1)

        if stato == "completato" and valutazione != -1:
            voti.append(valutazione)

            # Calcolo durata solo se esiste data_completamento
            data_assegnazione = compito.get("data_assegnazione")
            data_completamento = compito.get("data_completamento")
            if data_assegnazione and data_completamento:
                try:
                    dt_inizio = datetime.strptime(data_assegnazione, "%Y-%m-%d %H:%M:%S")
                    dt_fine = datetime.strptime(data_completamento, "%Y-%m-%d %H:%M:%S")
                    durate_compiti[compito["id"]] = dt_fine - dt_inizio
                except Exception:
                    pass  # Se il formato della data è sbagliato, ignora

        elif stato == "assegnato":
            descrizione = compito.get("descrizione", "Compito senza descrizione")
            compiti_non_completati.append(descrizione)

    stats = {
        "voti": voti,
        "compiti_non_completati": compiti_non_completati,
        "durate_compiti": durate_compiti,
        "compiti_completati": len(voti),
        "compiti_assegnati": len(compiti_non_completati)
    }

    if voti:
        stats["media"] = mean(voti)
        stats["min"] = min(voti)
        stats["max"] = max(voti)
    else:
        stats["media"] = stats["min"] = stats["max"] = None

    return stats

def ranking_alunni():
    """Restituisce la lista di tuple (matricola, media) ordinata per media decrescente."""
    medie = {}
    for matricola, info in lista_alunni.items():
        if info["archiviato"]:
            continue
        stats = statistiche_alunno(matricola)
        medie[matricola] = stats["media"]  # media può essere None se non ci sono voti

    # Ordinamento decrescente per media, poi cognome, poi nome, gestendo None
    ranking = sorted(
        medie.items(),
        key=lambda item: (
            -(item[1] if item[1] is not None else -1),
            lista_alunni[item[0]]["cognome"],
            lista_alunni[item[0]]["nome"]
        )
    )
    return ranking

# ===============================
# FUNZIONI HELPER COMPITI
# ===============================

def aggiorna_stato_compiti_alunno(matricola, stato):
    """Aggiorna lo stato di tutti i compiti associati a uno studente."""
    for compito in lista_compiti.values():
        if compito["alunno_matricola"] == matricola:
            compito["stato"] = stato
    salva_compiti()

# ===============================
# FUNZIONI HELPER ALUNNO
# ===============================

def archivia_alunno(matricola):
    """Archivia uno studente e i suoi compiti."""
    alunno = lista_alunni[matricola]
    alunno["archiviato"] = True
    alunno["data_archiviazione"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alunno["data_modifica"] = alunno["data_archiviazione"]
    aggiorna_stato_compiti_alunno(matricola, "archiviato")
    salva_alunni()
    print(f"✅ Studente {alunno['nome']} {alunno['cognome']} e compiti archiviati con successo!")

def elimina_alunno(matricola):
    """Elimina uno studente solo se non ha compiti associati."""
    compiti_associati = [c for c in lista_compiti.values() if c["alunno_matricola"] == matricola]
    if compiti_associati:
        print("❌ Eliminazione impossibile: ci sono compiti associati!")
        return
    alunno = lista_alunni.pop(matricola)
    salva_alunni()
    print(f"✅ Studente {alunno['nome']} {alunno['cognome']} eliminato definitivamente!")

# ===============================
# FUNZIONE PRINCIPALE GESTIONE "d"
# ===============================

def gestione_alunno_d(matricola):
    """Gestione completa dell'archiviazione/eliminazione di uno studente e dei suoi compiti."""
    alunno = lista_alunni[matricola]
    stampa_info_alunno(matricola, riepilogo=True)

    compiti_associati = [c for c in lista_compiti.values() if c["alunno_matricola"] == matricola]

    if alunno["archiviato"]:
        print("⚠️ Lo studente è già archiviato.")
        if compiti_associati:
            print("❌ Eliminazione definitiva NON consentita (compiti associati).")
        else:
            conferma = input("🗑️ Vuoi eliminarlo definitivamente? (s/n): ").lower()
            if conferma == "s":
                elimina_alunno(matricola)
            else:
                print("🚫 Operazione annullata")
        return

    scelta = input("➡️ Vuoi (a)rchiviarlo o (e)liminarlo definitivamente?: ").lower()
    while scelta not in ["a", "e"]:
        scelta = input("❌ Scelta non valida. Digita 'a' o 'e': ").lower()

    if scelta == "a":
        conferma = input(f"📦 Sei sicuro di voler archiviare {alunno['nome']} {alunno['cognome']}? (s/n): ").lower()
        if conferma == "s":
            archivia_alunno(matricola)
        else:
            print("🚫 Operazione annullata")
    else:  # scelta == "e"
        if compiti_associati:
            conferma = input("⚠️ Lo studente ha compiti associati. Vuoi archiviare invece di eliminare? (s/n): ").lower()
            if conferma == "s":
                archivia_alunno(matricola)
            else:
                print("🚫 Eliminazione annullata per preservare storico")
        else:
            conferma = input(f"🗑️ Sei sicuro di voler eliminare definitivamente {alunno['nome']} {alunno['cognome']}? (s/n): ").lower()
            if conferma == "s":
                elimina_alunno(matricola)
            else:
                print("🚫 Operazione annullata")

def menu_principale():
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
    j) Visualizza alunni per range di voti
    k) Report compiti non completati
    l) Salva dati (backup) - JSON
    m) Carica dati - JSON
    n) Esporta dati CSV
    o) Importa dati CSV
    p) Esci""")

        scelta = input("\nDigita un comando: ").lower().strip()

        if scelta=="a":
            print("\n🧑‍🎓 INSERIMENTO NUOVO ALUNNO\n")

            while True:
                nome = " ".join(input("👤 Nome: ").strip().title().split())
                if not valida_nome(nome):
                    print("❌ Il nome può contenere solo lettere e spazi. Riprova!")
                    continue
                break

            while True:
                cognome = " ".join(input("👤 Cognome: ").strip().title().split())
                if not valida_nome(cognome):
                    print("❌ Il cognome può contenere solo lettere e spazi. Riprova!")
                    continue
                break

            if any(a["nome"] == nome and a["cognome"] == cognome for a in lista_alunni.values()):
                opzione = input("⚠️ Esiste un alunno con lo stesso nome e cognome. Proseguire comunque? (s/n): ").lower().strip()
                while opzione not in ["s", "n"]:
                    opzione = input("⚠️ Scelta non valida. Riprova! (s/n): ").lower().strip()
                if opzione == "n":
                    continue

            while True:
                email = " ".join(input("📧 Email: ").strip().lower().split())
                if not valida_email_univoca(email):
                    print("❌ Formato email non valido o email già esistente!")
                    continue

                if not email.endswith("allievi.itsdigitalacademy.it"):
                    opzione = input("⚠️ Sei sicuro di voler inserire una mail esterna alla scuola? (s/n): ").lower().strip()
                    while opzione not in ["s", "n"]:
                        opzione = input("⚠️ Inserisci un'opzione valida (s/n): ").lower().strip()
                    if opzione == "n":
                        continue
                break

            while True:
                data_nascita = input("📅 Data di nascita (gg-mm-aaaa): ").strip()
                valido, risultato = valida_data_nascita(data_nascita)

                if not valido:
                    if risultato == "formato":
                        print("❌ Errore: Il formato della data non è corretto. Riprova!")
                    elif risultato == "futura":
                        print("❌ Data futura non valida!")
                    elif risultato == "minore":
                        print("🚫 Lo studente deve avere almeno 18 anni.")
                    elif risultato == "anziano":
                        print("🚫 Età troppo elevata per un iscritto.")
                    continue

                data_nascita_iso = risultato
                print("✅ Formato data corretto:", data_nascita_iso)
                break

            opzione = input("📝 Vuoi aggiungere delle note relative allo studente? (s/n): ").lower().strip()
            while opzione not in ['s', 'n']:
                print("❌ Errore: scelta non corretta. Riprova!")
                opzione = input("📝 Vuoi aggiungere delle note relative allo studente? (s/n): ").lower().strip()

            if opzione == 's':
                note = input("🗒️ Note aggiuntive (max 500 caratteri): ").strip()
                while len(note) > 500:
                    print("❌ Errore: limite massimo di caratteri superato. Riprova!")
                    note = input("🗒️ Note aggiuntive (max 500 caratteri): ").strip()
            else:
                note = ""

            matricola, ora = crea_alunno(nome, cognome, email, data_nascita_iso, note)

            print("\n🎉 Alunno inserito con successo!")
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

                if opzione == "f":
                    print("\n📋 Alunni attivi in ordine alfabetico:")
                    trovati = stampa_lista_alunni("f")

                    if not trovati:
                        print("⚠️ Nessun alunno attivo trovato!")
                        scelta_extra = input("📂 Vuoi vedere comunque gli alunni archiviati? (s/n): ").lower().strip()
                        while scelta_extra not in ['s', 'n']:
                            print("❌ Errore: scelta non corretta. Riprova!")
                            scelta_extra = input("📂 Vuoi vedere comunque gli alunni archiviati? (s/n): ").lower().strip()
                        if scelta_extra == "s":
                            print("\n📋 Alunni archiviati in ordine alfabetico:")
                            stampa_lista_alunni("a")

                elif opzione == "a":
                    print("\n📋 Alunni archiviati in ordine alfabetico:")
                    trovati = stampa_lista_alunni("a")

                    if not trovati:
                        print("⚠️ Nessun alunno archiviato trovato!")
                        scelta_extra = input("👀 Vuoi vedere comunque gli alunni frequentanti? (s/n): ").lower().strip()
                        while scelta_extra not in ['s', 'n']:
                            print("❌ Errore: scelta non corretta. Riprova!")
                            scelta_extra = input("👀 Vuoi vedere comunque gli alunni frequentanti? (s/n): ").lower().strip()
                        if scelta_extra == "s":
                            print("\n📋 Alunni attivi in ordine alfabetico:")
                            stampa_lista_alunni("f")

                else:
                    print("\n📋 Elenco alunni in ordine alfabetico:")
                    for matricola, info in alunni_ordinati():
                        stampa_info_alunno(matricola, info, mostra_stato=True)

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="c":
            print("\n✏️ MODIFICA DATI ALUNNO\n")

            input_utente = input("🆔 Inserisci matricola, nome o cognome: ")
            matr = cerca_studente(input_utente)

            if matr is None:
                input("\n⏎ Premi Invio per continuare...")
                pulisci_schermo()
                continue

            # Sostituito con la nuova funzione
            stampa_info_alunno(matr, riepilogo=True)

            modifica = "s"
            while modifica == "s":
                print("✏️ Cosa vuoi modificare?")
                print("👤 n) nome")
                print("👤 c) cognome")
                print("📧 e) e-mail")

                opzione = input("➡️ Inserisci l'opzione: ").lower().strip()
                while opzione not in ["n", "c", "e"]:
                    opzione = input("❌ Opzione non valida. Riprova: ").lower().strip()

                if opzione == "n":
                    modifica_nome(matr)
                elif opzione == "c":
                    modifica_cognome(matr)
                else:
                    modifica_email(matr)

                lista_alunni[matr]["data_modifica"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                salva_alunni()

                print("✅ Dati modificati con successo!")
                # Nuova chiamata
                stampa_info_alunno(matr, riepilogo=True)

                modifica = input(f"🔁 Vuoi modificare altri dati della matricola {matr}? (s/n): ").lower().strip()
                while modifica not in ["s", "n"]:
                    modifica = input("❌ Risposta non valida! (s/n): ").lower().strip()

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="e":
            print("\n📝 ASSEGNA NUOVO COMPITO\n")
        
            # Input descrizione
            while True:
                descrizione = input("📝 Descrizione: ").strip()
                if valida_descrizione_compito(descrizione):
                    break
                print("🚫 Descrizione non valida. Lunghezza consentita: 5–200 caratteri.")
            
            # Input matricola
            while True:
                matr = input("🆔 Matricola studente: ").strip()
                if matr not in lista_alunni:
                    print("❌ La matricola inserita non corrisponde a nessuno studente! Riprova")
                elif lista_alunni[matr]['archiviato']:
                    print("🚫 Impossibile assegnare compiti a uno studente archiviato")
                else:
                    break

            # Creazione compito
            compito = crea_compito_logico(descrizione, matr)
            
            # Output stampato nel menu principale
            print(f"\n✅ Compito inserito con successo!")
            print(f"🆔 ID Compito: {compito['id']}")
            print(f"📝 Descrizione: {compito['descrizione']}")
            print(f"👤 Matricola studente: {compito['alunno_matricola']}")
            print(f"⏱️ Data assegnazione: {compito['data_assegnazione']}")

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="f":
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
                        compito["data_completamento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

            input_utente = input("🆔 Inserisci matricola, nome o cognome: ")
            matr = cerca_studente(input_utente)

            if matr is None:
                input("\n⏎ Premi Invio per continuare...")
                pulisci_schermo()
                continue

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

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="h":
            print("\n📊 STATISTICHE STUDENTE\n")

            input_utente = input("🆔 Inserisci matricola, nome o cognome: ")
            matr = cerca_studente(input_utente)

            if matr is None:
                input("\n⏎ Premi Invio per continuare...")
                pulisci_schermo()
                continue

            studente = lista_alunni[matr]
            stats = statistiche_alunno(matr)

            print(f"\n📋 Statistiche di {studente['nome']} {studente['cognome']}:")
            if studente["archiviato"]:
                print("⚠️ Studente archiviato!")

            # Durata compiti completati
            for id_comp, durata in stats["durate_compiti"].items():
                descrizione = lista_compiti[id_comp]["descrizione"]
                print(f"🕒 Compito '{descrizione}' completato in {durata}")

            print(f"✅ Compiti completati: {stats['compiti_completati']}")
            print(f"🕒 Compiti assegnati/non completati: {stats['compiti_assegnati']}")

            if stats["voti"]:
                print(f"📈 Media voti: {stats['media']:.2f}")
                print(f"🔻 Voto minimo: {stats['min']}")
                print(f"🔺 Voto massimo: {stats['max']}")
                print("📉 Progressione voti:", ", ".join(f"{v:.1f}" for v in stats["voti"]))

            if stats["compiti_non_completati"]:
                print("\n📌 Compiti non completati:")
                for c in stats["compiti_non_completati"]:
                    print("- 📝 ", c)

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta == "i":
            print("\n🏆 CLASSIFICA ALUNNI PER MEDIA VOTI\n")
            ranking = ranking_alunni()

            if not ranking:
                print("⚠️ Nessun alunno attivo con voti registrati")
            else:
                for i, (matricola, media) in enumerate(ranking, start=1):
                    nome = lista_alunni[matricola]["nome"]
                    cognome = lista_alunni[matricola]["cognome"]
                    print(f"🏅 {i}. {nome} {cognome} ({matricola}) - Media: {media:.2f}" if media is not None else
                        f"📌 {i}. {nome} {cognome} ({matricola}) - Media: N/A")

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="j":
            print("\n🎯 FILTRA ALUNNI PER RANGE DI VOTI\n")

            # --- Input sicuro dei voti ---
            while True:
                try:
                    voto_min = float(input("📉 Inserisci voto minimo: "))
                    voto_max = float(input("📈 Inserisci voto massimo: "))
                    if voto_min > voto_max:
                        print("❌ Il voto minimo non può essere maggiore del massimo! Riprova.")
                        continue
                    break
                except ValueError:
                    print("❌ Inserisci un numero valido! Riprova.")

            # --- Filtraggio alunni ---
            alunni_filtrati = []
            for matricola, info in lista_alunni.items():
                if info["archiviato"]:
                    continue
                stats = statistiche_alunno(matricola)
                media = stats["media"]
                if media is not None and voto_min <= media <= voto_max:
                    alunni_filtrati.append((matricola, media))

            # --- Ordinamento: media decrescente, poi cognome, poi nome ---
            alunni_filtrati.sort(key=lambda x: (-x[1], lista_alunni[x[0]]["cognome"], lista_alunni[x[0]]["nome"]))

            # --- Stampa risultati ---
            if not alunni_filtrati:
                print(f"⚠️ Nessun alunno trovato con media tra {voto_min} e {voto_max}")
            else:
                print(f"\n📋 Alunni con media tra {voto_min} e {voto_max}:")
                for matricola, media in alunni_filtrati:
                    nome = lista_alunni[matricola]["nome"]
                    cognome = lista_alunni[matricola]["cognome"]
                    print(f"- {nome} {cognome} ({matricola}) - Media: {media:.2f}")

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="k":
            print("\n📌 REPORT COMPITI NON COMPLETATI\n")

            non_completati_tutti = []

            # Scorri tutti gli studenti attivi
            for matricola, alunno in lista_alunni.items():
                if alunno["archiviato"]:
                    continue

                stats = statistiche_alunno(matricola)
                for compito in stats["compiti_non_completati"]:
                    # Recupero descrizione e ID del compito
                    for c in lista_compiti.values():
                        if c["alunno_matricola"] == matricola and c["descrizione"] == compito and c["stato"] == "assegnato":
                            non_completati_tutti.append({
                                "id": c["id"],
                                "descrizione": c["descrizione"],
                                "matricola": matricola,
                                "nome": alunno["nome"],
                                "cognome": alunno["cognome"],
                                "data_assegnazione": c["data_assegnazione"]
                            })

            if non_completati_tutti:
                # Ordinamento per cognome, nome, data assegnazione
                non_completati_ordinati = sorted(
                    non_completati_tutti,
                    key=lambda c: (c["cognome"], c["nome"], c["data_assegnazione"])
                )

                print("📝 COMPITI NON COMPLETATI:")
                for c in non_completati_ordinati:
                    print(f"- {c['id']}: {c['descrizione']} (👤 {c['nome']} {c['cognome']}) - ⏱️ Assegnato il {c['data_assegnazione']}")
            else:
                print("✅ Nessun compito non completato!")

            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="l":
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

        elif scelta=="m":
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
    
        elif scelta == "n":
            file_csv = input("📄 Nome file CSV esportazione: ").strip()
            tipo = input("Vuoi esportare (a)lunni o (c)ompiti?: ").lower().strip()
            if tipo == "a":
                esporta_alunni_csv(file_csv + ".csv")
            else:
                esporta_compiti_csv(file_csv + ".csv")
            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()

        elif scelta=="o":
            file_csv = input("📄 Nome file CSV da importare: ").strip()
            tipo = input("Vuoi importare (a)lunni o (c)ompiti?: ").lower().strip()
            if tipo == "a":
                importa_alunni_csv(file_csv + ".csv")
            else:
                importa_compiti_csv(file_csv + ".csv")
            input("\n⏎ Premi Invio per continuare...")
            pulisci_schermo()
    
        elif scelta=="p":
            print()
            break
        else:
            print("Scelta non valida!")

if __name__ == "__main__":
    menu_principale()