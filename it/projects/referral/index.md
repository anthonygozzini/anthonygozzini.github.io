# Telegram Referral System: da un gruppo vuoto a circa 2.000 iscritti

> Come ho costruito un bot referral Telegram per un creator crypto: verifica iscrizioni, wallet, punti e classifica. Circa 2.000 iscritti da zero.

Link referral, punti e classifica per una community Telegram.

## Il problema

Un creator crypto partiva da zero con un canale e un gruppo Telegram, e voleva premiare gli iscritti che portavano altre persone, senza contare gli inviti a mano.

## Cosa ho costruito

Gli iscritti avviano il bot, che prima controlla che siano entrati sia nel canale sia nel gruppo. Poi inviano l'indirizzo del proprio wallet e ricevono un link referral personale.

Ogni persona che portano vale punti, e gli admin possono vedere in qualsiasi momento i primi dieci con un solo comando.

La versione 1.1.0, quella pubblica, recupera la verifica delle iscrizioni e l'invio del wallet dalla versione completa fatta per il cliente.

## I risultati

- Circa 2.000 iscritti, partendo da un gruppo senza nessuno.

## Le scelte e il perché

### Perché verificare l'iscrizione prima di dare il link?

I punti valgono qualcosa solo se le persone sono davvero nella community. Controllare prima canale e gruppo fa sì che un invito sia un iscritto, non un clic.

### Perché raccogliere i wallet dentro il bot?

Così il wallet di ogni iscritto è legato ai suoi punti fin dall'inizio, senza un modulo a parte da rincorrere dopo.

## Codice e demo

[Codice](https://github.com/anthonygozzini/Telegram-Referral-System), [Release](https://github.com/anthonygozzini/Telegram-Referral-System/releases)

## Se ti serve qualcosa di simile

- [Bot Telegram su misura](https://anthonygozzini.github.io/it/services/telegram-bots/index.md): Bot che filtrano chi entra, gestiscono programmi referral o copiano canali, con test e release versionate.

[Prenota una call di 30 minuti](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Altri case study

- [GuardBot](https://anthonygozzini.github.io/it/projects/guardbot/index.md): Sicurezza prima di comprare, su EVM, Solana e TRON, con scambi simulati invece di un'API esterna.
- [channel-miner](https://anthonygozzini.github.io/it/projects/channel-miner/index.md): Leggere un canale YouTube invece di guardarlo.
- [Telegram Gatekeeper Bot](https://anthonygozzini.github.io/it/projects/gatekeeper/index.md): Filtra chi vuole entrare in un gruppo Telegram privato.
