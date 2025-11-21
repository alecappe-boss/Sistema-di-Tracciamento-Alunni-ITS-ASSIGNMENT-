import os
import json
import re
from datetime import datetime

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

def check(email):
    regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
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
    k) Salva dati (backup)
    l) Carica dati
    m) Visualizza menu
    n) Esci""")

    scelta=input("\nDigita un comando: ")
    if scelta=="a":
        nome=input("Nome: ")
        cognome=input("Cognome: ")
        email=input("Email: ")
        while True:
            while check(email) is False:
                print("Indirizzo email non valido! Riprova")
                email=input("Email: ")
            if not email.endswith("allievi.itsdigitalacademy.it"):
                opzione=input("Sei sicuro di voler inserire una mail esterna alla scuola? (s)ì/(n)o: ").lower()
                while opzione not in ["s", "n"]:
                    opzione=input("Inserisci un'opzione valida (s)ì/(n)o: ").lower()
                if opzione == "s":
                    break
                else:
                    email = input("Inserisci una nuova email: ")
            else:
                break
        matricola="MAT" + datetime.now().strftime("%Y%m%d%H%M%S")
        ora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista_alunni[matricola]={
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "matricola": matricola,
            "data_creazione":ora,
            "data_modifica":ora,
            "archiviato": False
        }
        salva_alunni()
        print(f"\n✅ Alunno '{nome} {cognome}' inserito con successo!")
        print(f"Matricola: {matricola}")
        print(f"Data creazione: {ora}")
    elif scelta=="b":
        if not lista_alunni:
            print("\n⚠️ Nessun alunno registrato!")
        else:
            trovato=False
            print("\n📋 Alunni registrati:")
            for matricola, info in lista_alunni.items():
                if info["archiviato"] == False:
                    trovato=True
                    print(f"\nMatricola: {matricola}")
                    print(f"Nome: {info['nome']}")
                    print(f"Cognome: {info['cognome']}")
                    print(f"E-mail: {info['email']}")
                    print(f"Data creazione: {info['data_creazione']}")
            if not trovato:
                print("⚠️ Nessun alunno attivo trovato!")
    elif scelta=="c":
        matr=input("Matricola: ")
        if matr in lista_alunni:
            modifica="s"
            while modifica=="s":
                print("Cosa vuoi modificare?")
                print("n) nome")
                print("c) cognome")
                print("e) e-mail")
                opzione=input("Inserisci l'opzione desiderata: ").lower()
                while opzione not in ["n", "c", "e"]:
                    opzione=input("L'opzione inserita non esiste! Riprova: ").lower()
                if opzione=="n":
                    new_name=input("Nuovo nome: ")
                    lista_alunni[matr]["nome"]=new_name
                elif opzione=="c":
                    new_cognome=input("Nuovo cognome: ")
                    lista_alunni[matr]["cognome"]=new_cognome
                elif opzione=="e":
                    while True:
                        new_email = input("Nuova e-mail: ")
                        if not check(new_email):
                            print("❌ Formato e-mail errato! Riprova.")
                        elif not new_email.endswith("allievi.itsdigitalacademy.it"):
                            conferma = input("Sei sicuro di voler inserire una mail esterna alla scuola? (s)ì/(n)o: ").lower()
                            while conferma not in ["s", "n"]:
                                conferma = input("Risposta non valida. Digita 's' o 'n': ").lower()
                            if conferma == "s":
                                lista_alunni[matr]["email"] = new_email
                                break
                            else:
                                print("Inserisci un'altra email.")
                        else:
                            lista_alunni[matr]["email"] = new_email
                            break
                lista_alunni[matr]["data_modifica"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                salva_alunni()
                print("✅ Dati modificati con successo!")
                modifica=input(f"Vuoi modificare altri dati della matricola {matr}? (s)ì/(n)o: ").lower()
                while modifica not in ["s", "n"]:
                    modifica = input("Risposta non valida! Digita 's' o 'n': ").lower()
        else:
            print("❌ La matricola indicata non è presente!")
    elif scelta=="d":
        matr=input("Matricola: ")
        if matr in lista_alunni:
            if lista_alunni[matr]["archiviato"]:
                print("⚠️ Lo studente è già archiviato!")
                elimina = input("Vuoi eliminarlo definitivamente? (s/n): ").lower()
                if elimina == "s":
                    lista_alunni.pop(matr)
                    salva_alunni()
                    print("✅ Alunno eliminato con successo!")
            else:
                soft=input("Vuoi (a)rchiviarlo o (e)limarlo definitivamente?: ")
                if soft=="a":
                    lista_alunni[matr]["archiviato"] = True
                    lista_alunni[matr]["data_modifica"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    salva_alunni()
                    print("✅ L'alunno è stato archiviato!")
                elif soft=="e":
                    conferma = input(f"Sei sicuro di voler eliminare definitivamente {lista_alunni[matr]['nome']} {lista_alunni[matr]['cognome']}? (s/n): ").lower()
                    if conferma == "s":
                        lista_alunni.pop(matr)
                        salva_alunni()
                        print("✅ Alunno eliminato con successo!")
                    else:
                        print("❌ Operazione annullata")
                else:
                    print("❌ Scelta errata!")
    elif scelta=="e":
        id="TASK" + datetime.now().strftime("%Y%m%d%H%M%S")
        descrizione=input("Descrizione: ")
        alunno_matricola=input("Matricola: ")
        while alunno_matricola not in lista_alunni:
            print("La matricola inserita non corrisponde a nessuno studente! Riprova")
            alunno_matricola=input("Matricola: ")
        data_assegnazione=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista_compiti[id]={
            "id": id,
            "descrizione": descrizione,
            "alunno_matricola": alunno_matricola,
            "stato": "assegnato",
            "data_assegnazione": data_assegnazione
        }
        salva_compiti()
        print(f"\n✅ Compito '{descrizione}' inserito con successo!")
        print(f"Matricola: {alunno_matricola}")
        print(f"Data assegnazione: {data_assegnazione}")
    elif scelta=="f":
        print()
    elif scelta=="g":
        print()
    elif scelta=="h":
        print()
    elif scelta=="i":
        print()
    elif scelta=="l":
        print()
    elif scelta=="m":
        print()
    elif scelta=="n":
        print()
        break
    else:
        print("Scelta non valida!")