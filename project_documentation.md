# The Perfect Reunion - Documentazione Tecnica

## 1. Introduzione

"The Perfect Reunion" è un'applicazione web che aiuta gruppi di amici che vivono in luoghi diversi a trovare la destinazione ideale per incontrarsi. Il sistema utilizza un algoritmo di raccomandazione content-based che analizza le preferenze individuali degli utenti e le aggrega per suggerire destinazioni che soddisfino gli interessi del gruppo.

## 2. Architettura del Sistema

### 2.1 Stack Tecnologico
- **Frontend**: React con TypeScript
- **Backend**: Python (Flask o FastAPI)
- **Database**: SQLite
- **Architettura**: Tradizionale client-server

### 2.2 Componenti Principali
```
├── Frontend (React + TypeScript)
│   ├── Pagine
│   │   ├── Auth (Login/Registrazione)
│   │   ├── Onboarding (Valutazione città)
│   │   ├── Dashboard personale
│   │   └── Dashboard di gruppo
│   └── Componenti
│       ├── Card città
│       ├── Interfaccia swipe
│       ├── Ricerca voli
│       └── Sistema di votazione
├── Backend (Python)
│   ├── API RESTful
│   ├── Sistema di autenticazione
│   ├── Algoritmo di raccomandazione
│   └── Generazione dati simulati
└── Database (SQLite)
    ├── Schema relazionale
    └── Dati pre-popolati
```

## 3. Requisiti Funzionali

### 3.1 Gestione Utenti
- **RF1.1:** Il sistema deve permettere agli utenti di registrarsi fornendo email, username e password
- **RF1.2:** Il sistema deve permettere agli utenti autenticati di accedere alle funzionalità
- **RF1.3:** Il sistema deve generare un profilo latente dell'utente basato sulle valutazioni delle città
- **RF1.4:** Il sistema deve richiedere la valutazione di almeno 5 città prima di generare raccomandazioni

### 3.2 Sistema di Raccomandazione
- **RF2.1:** Il sistema deve implementare un algoritmo content-based utilizzando Cosine Similarity
- **RF2.2:** Il sistema deve permettere agli utenti di valutare le città con like/dislike
- **RF2.3:** Il sistema deve aggiornare il profilo utente ad ogni nuova valutazione
- **RF2.4:** Il sistema deve generare raccomandazioni personalizzate basate sulle categorie rilevanti per l'utente

### 3.3 Gestione Gruppi
- **RF3.1:** Il sistema deve permettere agli utenti di creare gruppi con codice univoco
- **RF3.2:** Il sistema deve permettere agli utenti di unirsi a gruppi esistenti tramite codice
- **RF3.3:** Il sistema deve permettere agli utenti di appartenere a più gruppi contemporaneamente
- **RF3.4:** Il sistema deve limitare il numero di membri per gruppo a 10
- **RF3.5:** Il sistema deve generare raccomandazioni di gruppo basate sulla media delle preferenze

### 3.4 Ricerca e Prenotazione Voli
- **RF4.1:** Il sistema deve permettere la ricerca di voli con vari filtri (budget, impatto ambientale, distanza, compagnia)
- **RF4.2:** Il sistema deve visualizzare alternative di volo in base ai criteri specificati
- **RF4.3:** Il sistema deve permettere all'owner di selezionare itinerari da proporre al gruppo
- **RF4.4:** Il sistema deve implementare un meccanismo di votazione like/dislike per gli itinerari

### 3.5 Interfaccia Utente
- **RF5.1:** Il sistema deve implementare un'interfaccia stile Tinder per la valutazione delle città
- **RF5.2:** Il sistema deve fornire interfacce separate per raccomandazioni individuali e di gruppo
- **RF5.3:** Il sistema deve visualizzare descrizioni personalizzate nelle card delle città
- **RF5.4:** Il sistema deve mostrare indicatori di consenso del gruppo sulle proposte

## 4. Requisiti Non Funzionali

- **RNF1:** I dati (città, voli, utenti, gruppi) saranno simulati e generati tramite script
- **RNF2:** Il sistema non utilizzerà API esterne
- **RNF3:** Il database sarà pre-popolato con dati di esempio realistici
- **RNF4:** Il sistema sarà ospitato su un servizio gratuito
- **RNF5:** La sicurezza sarà implementata a livello base (hashing password)
- **RNF6:** Non è richiesta la gestione delle connessioni intermittenti

## 5. Struttura del Database

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│     User      │      │   GroupTable  │      │     City      │
├───────────────┤      ├───────────────┤      ├───────────────┤
│ email (PK)    │      │ code (PK)     │      │ name (PK)     │
│ username      │      └───────────────┘      └───────────────┘
│ password      │             │                      │
└───────────────┘             │                      │
      │                       │                      │
      │                       │                      │
┌─────┴───────────┐    ┌─────┴───────────┐    ┌─────┴───────────┐
│  ImportanceUC   │    │     UGroup      │    │     VoteUC      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ email (PK,FK)   │    │ email (PK,FK)   │    │ email (PK,FK)   │
│ category (PK,FK)│    │ code (PK,FK)    │    │ city (PK,FK)    │
│ importance      │    └─────────────────┘    │ value           │
└─────────────────┘                           └─────────────────┘
      │
      │
┌─────┴───────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Category     │    │  FlightCompany  │    │     Flight      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ name (PK)       │    │ name (PK)       │    │ code (PK)       │
└─────────────────┘    └─────────────────┘    │ cost            │
      │                       │                │ depCity (FK)    │
      │                       │                │ arrCity (FK)    │
┌─────┴───────────┐          │                │ depTime         │
│    CityCateg    │          │                │ timeDuration    │
├─────────────────┤          │                │ distance        │
│ city (PK,FK)    │          │                │ planeModel      │
│ category (PK,FK)│          │                │ company (FK)    │
│ descr           │          └────────────────┘─────────────────┘
│ value           │
└─────────────────┘
```

### 5.1 Descrizione delle Tabelle

- **User**: Memorizza le informazioni degli utenti (email, username, password)
- **GroupTable**: Memorizza i gruppi tramite codice univoco
- **UGroup**: Associa utenti ai gruppi (relazione many-to-many)
- **City**: Memorizza le informazioni sulle città
- **VoteUC**: Registra i voti degli utenti per le città (like/dislike)
- **FlightCompany**: Contiene le compagnie aeree
- **Flight**: Memorizza informazioni sui voli
- **Category**: Categorie per classificare le città (food, history, etc.)
- **CityCateg**: Associa città a categorie con descrizioni e valori (1-10)
- **ImportanceUC**: Memorizza l'importanza delle categorie per gli utenti (1-10)

## 6. Algoritmo di Raccomandazione

### 6.1 Profilo Utente
Il profilo latente dell'utente è rappresentato come un vettore di pesi ("importanza") per ciascuna categoria, compreso tra 0 e 10. Questo vettore viene calcolato e aggiornato iterativamente in base ai voti (like/dislike) espressi dall'utente sulle città proposte.

**Logica di Calcolo dell'Importanza:**
- **Inizializzazione:** Se un utente non ha ancora espresso voti, l'importanza per ogni categoria viene inizializzata a un valore neutro (es. 5).
- **Aggiornamento Iterativo:** Per ogni voto (like o dislike) espresso su una città:
    - Si confronta l'importanza attuale dell'utente per ogni categoria con il valore di quella categoria per la città votata.
    - Se il voto è **Like (1)**, l'importanza dell'utente per quella categoria si sposta leggermente *verso* il valore della città.
    - Se il voto è **Dislike (0)**, l'importanza dell'utente si sposta leggermente *lontano* dal valore della città.
    - L'entità dello spostamento è controllata da un `learning_rate`.
    - I valori di importanza vengono mantenuti nell'intervallo [0, 10].
- **Salvataggio:** I valori aggiornati vengono salvati nel database (tabella `ImportanceUC`).

### 6.2 Calcolo della Similarità
Per calcolare la similarità tra il profilo utente (vettore di importanza) e una città (vettore dei valori delle categorie), viene utilizzata la Cosine Similarity:

```
cos(θ) = (A·B)/(||A||·||B||)
```

dove:
- A è il vettore del profilo utente
- B è il vettore delle caratteristiche della città
- · rappresenta il prodotto scalare
- ||A|| e ||B|| sono le norme dei vettori

### 6.3 Raccomandazioni di Gruppo
Per le raccomandazioni di gruppo, il sistema calcola la media dei vettori di preferenza degli utenti:

```
GruppoProfilo = (U₁ + U₂ + ... + Uₙ)/n
```

dove U₁, U₂, ..., Uₙ sono i vettori di preferenza degli n utenti nel gruppo.

## 7. Flussi Utente Principali

### 7.1 Onboarding
1. Registrazione utente
2. Login
3. Valutazione iniziale città (minimo 5)
4. Generazione profilo utente

### 7.2 Esperienza Individuale
1. Login
2. Visualizzazione dashboard con città consigliate
3. Esplorazione dettagli città
4. Valutazione nuove città

### 7.3 Esperienza di Gruppo
1. Creazione nuovo gruppo o ingresso in gruppo esistente
2. Visualizzazione destinazioni consigliate per il gruppo
3. Ricerca voli con filtri specifici
4. Selezione itinerari da proporre
5. Votazione sugli itinerari proposti

## 8. Implementazione e Sviluppo

### 8.1 Priorità di Sviluppo
1. Setup database e generazione dati
2. Sistema di autenticazione
3. Componenti UI base
4. Interfaccia valutazione città
5. Algoritmo di raccomandazione
6. Visualizzazione raccomandazioni personali
7. Creazione e gestione gruppi
8. Raccomandazioni di gruppo
9. Sistema di ricerca voli e votazione

### 8.2 Divisione del Lavoro
- 2 sviluppatori backend: implementazione API, algoritmo di raccomandazione, database
- 1 sviluppatore frontend (React/TypeScript): implementazione interfaccia utente
- 1 sviluppatore per integrazione e funzionalità AI-based

## 9. Conclusioni

"The Perfect Reunion" rappresenta un'innovativa soluzione per risolvere il problema comune di trovare una destinazione di viaggio che soddisfi le preferenze di un gruppo di amici. Utilizzando un approccio content-based e un'interfaccia user-friendly, l'applicazione semplifica il processo decisionale e migliora l'esperienza di pianificazione del viaggio. 