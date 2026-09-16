# Progetti — Anthony Gozzini

> Quello che costruisco fuori dal lavoro, pubblicato con il codice: GuardBot, channel-miner, bot Telegram per community crypto e Sgamers, il mio primo gioco.

Cose che ho costruito fuori dal lavoro. Alcune sono nate per clienti paganti, altre sono mie; tutte sono pubblicate con il loro codice.

## GuardBot (2026)

Sicurezza prima di comprare, su EVM, Solana e TRON, con scambi simulati invece di un'API esterna.

Prima di comprare un token, GuardBot simula davvero un acquisto e una vendita sulla liquidità reale: un honeypot si vede come una vendita che fallisce, non come un bollino verde dato dall'API di qualcun altro. Poi, incollando un indirizzo, controlla le autorizzazioni di un wallet su EVM, Solana e TRON e revoca quelle rischiose, simulando ogni revoca prima della firma. Gira in locale, usa solo la libreria standard di Python e include un server MCP, così anche gli agenti AI possono usarlo come strumento.

Tag: Python, MCP, Progetto personale

Link: [Codice](https://github.com/anthonygozzini/guardbot), [Demo di 35 secondi](https://anthonygozzini.github.io/guardbot/demo.html)

## channel-miner (2026)

Leggere un canale YouTube invece di guardarlo.

Gli dai un canale YouTube: raccoglie tutti i video e li trasforma in testo da cercare o leggere con calma. Se gli dici cosa sai già, un'AI legge tutto e ti restituisce solo le cose nuove per te. Gira tutto sul tuo computer, senza account, senza chiavi API e senza pagare niente. Su un canale ha trasformato 377 ore di video, in 179 puntate, in 237 MB di testo.

Tag: Python, Shell, Progetto personale

Link: [Codice](https://github.com/anthonygozzini/channel-miner), [Guardalo in azione](https://anthonygozzini.github.io/channel-miner/demo.html)

## Telegram Gatekeeper Bot (2023 – 2026)

Filtra chi vuole entrare in un gruppo Telegram privato.

Chi vuole entrare risponde a un breve questionario in chat privata. Il bot controlla le risposte e cerca i segnali di account falsi o farmati, come la mancanza di username, un nome pieno di numeri o un profilo social già usato da qualcun altro. Poi lo fa entrare con un link d'invito monouso oppure passa la richiesta agli admin, con i pulsanti Approva e Rifiuta. Domande, regole e messaggi stanno in un solo file di configurazione, quindi lo stesso bot funziona per qualsiasi community. La versione 3 è la riscrittura generica di un bot che avevo costruito nel 2023 per gruppi crypto privati.

Tag: Python, SQLite, 40 test, v3.0.0

Link: [Codice](https://github.com/anthonygozzini/telegram-gatekeeper-bot), [Release](https://github.com/anthonygozzini/telegram-gatekeeper-bot/releases)

## Sgamers (2018 · 2026)

Il mio primo gioco, fatto in Unity nel 2018 e ricostruito nel 2026.

Un breve gioco 3D con menu principale, un livello e i titoli di coda, fatto mentre imparavo Unity con i tutorial di Brackeys. La cartella del progetto era andata persa ed era sopravvissuto solo il gioco compilato, così nel 2026 ho ricostruito il progetto da quella build, l'ho aggiornato a Unity 6 e l'ho riportato in vita nel browser. Puoi giocarci qui con la tastiera: frecce oppure A e D per muoverti, Spazio per saltare. La build Windows originale è allegata alla release.

Tag: Unity, C#, Giocabile nel browser

Link: [Gioca nel browser](https://anthonygozzini.github.io/play/sgamers/index.md), [Codice](https://github.com/anthonygozzini/sgamers), [Build Windows](https://github.com/anthonygozzini/sgamers/releases/tag/v1.0.0), [Come l'ho ricostruito](https://anthonygozzini.github.io/it/writing/rebuilding-sgamers/index.md)

## Telegram Referral System (2024)

Link referral, punti e classifica per una community Telegram.

Gli iscritti entrano nel canale e nel gruppo, inviano l'indirizzo del proprio wallet e ricevono un link referral personale. Ogni persona che portano vale punti, e gli admin possono vedere in qualsiasi momento chi ha invitato di più. L'ho costruito nel 2024 per la community di un creator crypto; la versione 1.1.0 recupera la verifica delle iscrizioni e l'invio del wallet dalla versione completa fatta per il cliente.

Tag: Python, Per un cliente, v1.1.0

Link: [Codice](https://github.com/anthonygozzini/Telegram-Referral-System), [Release](https://github.com/anthonygozzini/Telegram-Referral-System/releases)

## Telegram Channel Message Copier (2024)

Copia i post da un canale Telegram ad altri.

Un bot in produzione che copia i messaggi da un canale di origine a più canali di destinazione e può programmare gli invii. Ha lavorato per un cliente che pubblicava su sei canali; la versione 1.0.1 corregge un errore di formattazione che ne impediva l'avvio.

Tag: Python, Per un cliente, v1.0.1

Link: [Codice](https://github.com/anthonygozzini/Telegram-Channel-Message-Copier-Bot), [Release](https://github.com/anthonygozzini/Telegram-Channel-Message-Copier-Bot/releases)

## The Legend of Dragoon in italiano (2026)

Una mod in italiano per la versione PC, fatta dai fan, di un GDR PlayStation del 1999.

Severed Chains è la versione PC di The Legend of Dragoon fatta dai fan. Ci sto aggiungendo l'italiano: finora nella mod ci sono 611 stringhe di testo, mentre altre 339 sono scritte direttamente nel codice e richiedono modifiche al motore. Non è ancora stata provata in gioco, quindi non c'è una release pubblica.

Tag: Localizzazione, Modding, In corso
