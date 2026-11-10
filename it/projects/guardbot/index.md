# GuardBot: controllare un token provando a scambiarlo, non fidandosi di un bollino

> Come ho costruito GuardBot: controlli sui token che simulano un acquisto e una vendita veri su 8 blockchain, con un benchmark pubblico.

Sicurezza prima di comprare, su EVM, Solana e TRON, con scambi simulati invece di un'API esterna.

## Il problema

I bot di trading e gli agenti AI che comprano token da soli di solito si fidano del verdetto di qualcun altro: un'API restituisce un bollino verde e il bot compra. Quando il bollino è sbagliato i soldi sono persi, e nessuno può vedere perché l'API diceva che era sicuro.

## Cosa ho costruito

Prima di un acquisto, GuardBot fa lo scambio da solo in simulazione: un acquisto e una vendita veri sulla liquidità reale, fissati a un solo blocco. Un honeypot si vede come una vendita che fallisce, con la chiamata fallita come prova, non come un punteggio.

Poi, incollando un indirizzo, controlla le autorizzazioni di un wallet sulle blockchain EVM, su Solana e su TRON e revoca quelle rischiose. Si possono costruire solo tre tipi di revoca, ognuna viene simulata prima della firma e la chiamata esatta viene mostrata prima.

Gira sul tuo computer usando solo la libreria standard di Python: niente da installare, nessuna chiave, nessun account. Ha un suo firmatario delle transazioni e un server MCP, così un agente AI può usarlo come strumento.

## I risultati

- 8 blockchain: Ethereum, Arbitrum, Polygon, Base, Optimism, BSC, Solana e TRON.
- Benchmark pubblico del 19 settembre 2026: 5 honeypot attivi bloccati su 5, e nessuno dei 21 token principali bloccato o segnalato per errore.
- 51 test offline, più 19 che girano su blockchain reali.
- Circa 2 secondi per un controllo dal vivo su più blockchain.

## Le scelte e il perché

### Perché simulare invece di usare un'API di sicurezza?

Perché la risposta di un'API non si può verificare. Una vendita che fallisce in simulazione è una prova che chiunque può ripetere. Le etichette esterne servono solo come indizio, mai come verdetto.

### Perché solo la libreria standard di Python?

Uno strumento che protegge un wallet deve essere facile da leggere e non avere niente da installare. Meno dipendenze vuol dire meno punti in cui qualcosa può rompersi o essere sostituito.

### Perché pubblicare gli errori?

Il primo giro del benchmark ha trovato un errore vero: USDT su Ethereum risultava un honeypot, per colpa di un'autorizzazione da 4 USDT lasciata da uno sconosciuto che il contratto di Tether si rifiuta di sovrascrivere. La correzione è entrata lo stesso giorno. Un numero che nessuno può controllare non vale la pena di pubblicarlo.

## I limiti

- Cinque honeypot attivi sono pochi: dei 155 pool lanciati su BSC e Base il 19 settembre, dopo dodici ore solo due avevano ancora un pool.
- La liquidità si misura solo sulla coppia con la moneta nativa, quindi un token scambiato soprattutto contro USDT può sembrare meno liquido di quanto è.

## Codice e demo

[Codice](https://github.com/anthonygozzini/guardbot), [Demo di 35 secondi](https://anthonygozzini.github.io/guardbot/demo.html), [Pagina del progetto](https://anthonygozzini.github.io/guardbot/)

## Se ti serve qualcosa di simile

- [Automazioni AI per il marketing](https://anthonygozzini.github.io/it/services/ai-automation/index.md): Pipeline che tolgono il lavoro ripetitivo da localizzazione, report e contenuti, controllate prima che esca qualsiasi cosa.

[Prenota una call di 30 minuti](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Altri case study

- [channel-miner](https://anthonygozzini.github.io/it/projects/channel-miner/index.md): Leggere un canale YouTube invece di guardarlo.
- [Telegram Gatekeeper Bot](https://anthonygozzini.github.io/it/projects/gatekeeper/index.md): Filtra chi vuole entrare in un gruppo Telegram privato.
- [Telegram Referral System](https://anthonygozzini.github.io/it/projects/referral/index.md): Link referral, punti e classifica per una community Telegram.
