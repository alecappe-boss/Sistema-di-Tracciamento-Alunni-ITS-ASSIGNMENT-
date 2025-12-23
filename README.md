# 🎓 Sistema di Tracciamento Alunni - ITS

Un sistema completo di gestione studenti e compiti progettato per istituti tecnici superiori, con funzionalità di archiviazione, statistiche e import/export dati.

## 📋 Caratteristiche Principali

### Gestione Alunni
- ✅ Registrazione studenti con validazione email e dati anagrafici
- 📝 Modifica dati (nome, cognome, email)
- 📦 Archiviazione studenti (soft delete)
- 🗑️ Eliminazione definitiva (solo se non ci sono compiti associati)
- 🔍 Ricerca avanzata per matricola, nome o cognome
- 📊 Visualizzazione ordinata alfabeticamente

### Gestione Compiti
- 📝 Assegnazione compiti a studenti
- ⭐ Registrazione valutazioni (scala 3-10)
- 📈 Tracciamento stato compiti (assegnato/completato/archiviato)
- 🕒 Calcolo durata completamento compiti
- 📋 Visualizzazione compiti per studente

### Statistiche e Report
- 📊 Statistiche individuali per studente:
  - Media voti
  - Voto minimo e massimo
  - Progressione voti
  - Compiti completati/non completati
  - Tempo di completamento per compito
- 🏆 Ranking studenti per media voti
- 🎯 Filtraggio alunni per range di voti
- 📌 Report compiti non completati globale

### Import/Export Dati
- 💾 Salvataggio/caricamento JSON con validazione struttura
- 📁 Backup automatico con pulizia file più vecchi di 7 giorni
- 📄 Esportazione dati in formato CSV
- 📥 Importazione massiva da CSV

## 🚀 Installazione

### Requisiti
- Python 3.7 o superiore
- Nessuna libreria esterna richiesta (usa solo moduli standard)

### Setup
```bash
# Clona il repository
git clone https://github.com/alecappe-boss/Sistema-di-Tracciamento-Alunni-ITS-ASSIGNMENT-.git

# Naviga nella cartella
cd Sistema-di-Tracciamento-Alunni-ITS-ASSIGNMENT-

# Esegui il programma
python sistema_alunni_ITS.py
```

## 📖 Utilizzo

### Menu Principale
All'avvio del programma, apparirà un menu interattivo con le seguenti opzioni:

```
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
p) Esci
```

### Esempi d'Uso

#### Inserire un Nuovo Alunno
1. Seleziona opzione `a`
2. Inserisci nome, cognome, email (validazione automatica)
3. Inserisci data di nascita (formato gg-mm-aaaa)
4. Aggiungi note opzionali
5. Il sistema genera automaticamente una matricola univoca

#### Assegnare un Compito
1. Seleziona opzione `e`
2. Inserisci descrizione compito (5-200 caratteri)
3. Inserisci matricola studente
4. Il sistema genera automaticamente l'ID compito

#### Registrare una Valutazione
1. Seleziona opzione `f`
2. Inserisci ID compito
3. Inserisci valutazione (scala 3-10)
4. Conferma l'operazione

## 📁 Struttura Dati

### File JSON

#### lista_alunni.json
```json
{
  "MAT20240315123456": {
    "nome": "Mario",
    "cognome": "Rossi",
    "email": "mario.rossi@allievi.itsdigitalacademy.it",
    "data_nascita": "2000-05-15",
    "note": "Ottimo studente",
    "matricola": "MAT20240315123456",
    "data_creazione": "2024-03-15 12:34:56",
    "data_modifica": "2024-03-15 12:34:56",
    "archiviato": false,
    "data_archiviazione": null
  }
}
```

#### lista_compiti.json
```json
{
  "TASK20240315123456": {
    "id": "TASK20240315123456",
    "descrizione": "Progetto Python gestione database",
    "alunno_matricola": "MAT20240315123456",
    "stato": "completato",
    "data_assegnazione": "2024-03-15 12:34:56",
    "data_completamento": "2024-03-20 15:30:00",
    "valutazione": 9.5
  }
}
```

### Formato CSV

#### alunni.csv
```csv
matricola,nome,cognome,email,data_nascita,note,archiviato
MAT20240315123456,Mario,Rossi,mario.rossi@allievi.itsdigitalacademy.it,2000-05-15,Ottimo studente,False
```

#### compiti.csv
```csv
id,descrizione,alunno_matricola,stato,data_assegnazione,valutazione
TASK20240315123456,Progetto Python,MAT20240315123456,completato,2024-03-15 12:34:56,9.5
```

## 🔐 Validazioni

### Email
- Formato standard RFC 5322
- Unicità garantita (no duplicati)
- Preferenza per dominio @allievi.itsdigitalacademy.it (con avviso per email esterne)

### Data di Nascita
- Formato: gg-mm-aaaa
- Età minima: 18 anni
- Età massima: 100 anni
- Nessuna data futura

### Compiti
- Descrizione: 5-200 caratteri
- Valutazione: scala 3-10
- Stati validi: assegnato, completato, archiviato

## 📦 Sistema di Backup

Il sistema implementa un meccanismo automatico di backup:
- Backup creati con timestamp nella cartella `backup/`
- Formato: `lista_alunni_YYYY-MM-DD_HH-MM-SS.json`
- Pulizia automatica backup più vecchi di 7 giorni
- Backup manuale disponibile tramite menu

## 🛡️ Gestione Archiviazione

### Logica Archiviazione
- Gli studenti archiviati mantengono tutti i dati storici
- I compiti dello studente vengono automaticamente archiviati
- Non è possibile assegnare nuovi compiti a studenti archiviati
- Non è possibile registrare valutazioni per compiti archiviati

### Eliminazione
- Eliminazione definitiva possibile solo se lo studente non ha compiti
- Se ci sono compiti associati, il sistema propone l'archiviazione

## 🔍 Funzionalità di Ricerca

Il sistema permette ricerca flessibile degli studenti tramite:
- Matricola esatta
- Nome
- Cognome
- Nome e cognome (in entrambi gli ordini)

In caso di risultati multipli, viene mostrata una lista numerata per la selezione.

## 📊 Report e Statistiche

### Statistiche Individuali
Per ogni studente il sistema calcola:
- Numero compiti completati e assegnati
- Media, minimo e massimo dei voti
- Progressione temporale dei voti
- Durata completamento per ogni compito
- Lista compiti non completati

### Ranking Globale
Classifica studenti attivi per media voti decrescente, con ordinamento secondario per cognome e nome.

### Filtraggio per Voti
Possibilità di visualizzare studenti con media in un range specificato, con ordinamento per media decrescente.

## 🐛 Gestione Errori

Il sistema implementa validazione robusta per:
- File JSON corrotti o mancanti
- Dati CSV malformati
- Email duplicate
- Studenti inesistenti
- Compiti senza studente associato
- Date non valide
- Valutazioni fuori range

## 🤝 Contribuire

I contributi sono benvenuti! Per contribuire:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Licenza

MIT License – libero uso, modifica e distribuzione.

## 👥 Autori

Cappelletto Alessandro - Sistema sviluppato per ITS Digital Academy

## 📞 Supporto

Per problemi o domande:
- Apri una issue su GitHub
- Contatta il team di sviluppo

## 🗺️ Roadmap

Funzionalità future pianificate:
- [ ] Interfaccia grafica (GUI)
- [ ] Autenticazione multi-utente
- [ ] Dashboard web
- [ ] Grafici statistiche avanzate

---

**Versione:** 1.0.0  
**Ultimo aggiornamento:** Dicembre 2025
