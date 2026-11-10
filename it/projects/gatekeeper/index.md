# Telegram Gatekeeper Bot: filtrare chi entra in un gruppo privato

> Come ho costruito un bot Telegram che filtra chi entra nei gruppi privati: questionario, segnali di account falsi e inviti monouso. Usato in 10 gruppi.

Filtra chi vuole entrare in un gruppo Telegram privato.

## Il problema

I gruppi crypto privati attirano account falsi e farmati appena c'è qualcosa da guadagnare. Far entrare le persone a mano non regge, e un link d'invito aperto finisce inoltrato ovunque.

## Cosa ho costruito

Ho costruito la prima versione nel 2023 per gruppi crypto privati: chi voleva entrare rispondeva a un breve questionario in chat privata, gli admin lo valutavano e chi veniva accettato riceveva un link d'invito che funziona una sola volta. Le prime versioni hanno girato in 10 gruppi.

La versione 3 è la riscrittura per qualsiasi community. Domande, regole e messaggi stanno in un solo file di configurazione. Controlla i link ai profili social su sei piattaforme, cerca i segnali di account falsi o farmati e poi fa entrare le persone da solo oppure passa la richiesta agli admin, con i pulsanti Approva e Rifiuta.

Ogni decisione, automatica o no, viene pubblicata per gli admin e salvata, e la stessa persona non può ripresentarsi prima che sia passato un tempo minimo.

## I risultati

- 10 gruppi privati hanno usato le prime versioni.
- 6 piattaforme social controllate: X, Instagram, TikTok, YouTube, GitHub e LinkedIn.
- 40 test su regole, configurazione, archivio e chiamate a Telegram.
- 3 versioni, dalla revisione a mano a un solo bot configurato da un file.

## Le scelte e il perché

### Perché link d'invito monouso?

Un link d'invito normale viene inoltrato. Un link che funziona per una sola persona, e può scadere, tiene il gruppo chiuso a chi non è passato dal filtro.

### Perché un segnale sospetto non rifiuta nessuno?

Niente username, o un nome pieno di numeri, è un sospetto, non una prova. Rifiutare solo per quello lascerebbe fuori persone vere, quindi un segnale passa la richiesta a una persona.

### Perché un solo file di configurazione?

Così lo stesso bot funziona per qualsiasi community senza toccare il codice: gli admin cambiano domande e regole, non il Python.

## I limiti

- Regole e archivio della versione 3 sono coperti dai test, ma il suo flusso su Telegram non ha ancora girato in un gruppo vero.

## Codice e demo

[Codice](https://github.com/anthonygozzini/telegram-gatekeeper-bot), [Release](https://github.com/anthonygozzini/telegram-gatekeeper-bot/releases)

## Se ti serve qualcosa di simile

- [Bot Telegram su misura](https://anthonygozzini.github.io/it/services/telegram-bots/index.md): Bot che filtrano chi entra, gestiscono programmi referral o copiano canali, con test e release versionate.

[Prenota una call di 30 minuti](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Altri case study

- [GuardBot](https://anthonygozzini.github.io/it/projects/guardbot/index.md): Sicurezza prima di comprare, su EVM, Solana e TRON, con scambi simulati invece di un'API esterna.
- [channel-miner](https://anthonygozzini.github.io/it/projects/channel-miner/index.md): Leggere un canale YouTube invece di guardarlo.
- [Telegram Referral System](https://anthonygozzini.github.io/it/projects/referral/index.md): Link referral, punti e classifica per una community Telegram.
