# channel-miner: leggere anni di YouTube invece di guardarli

> Come ho costruito channel-miner: un intero canale YouTube trasformato in testo da cercare, e un'AI locale che segnala solo le novità.

Leggere un canale YouTube invece di guardarlo.

## Il problema

Parte delle conoscenze migliori su un argomento di nicchia sta in anni di lunghi video e dirette su YouTube: centinaia di ore, senza indice né ricerca. Guardare tutto non è realistico, e scorrere velocemente fa perdere proprio la frase che conta.

## Cosa ho costruito

Gli dai un canale: raccoglie tutti i video con i sottotitoli, trascrive sul tuo computer quelli che non li hanno e trasforma tutto in testo semplice da cercare o leggere.

Poi gli dici cosa sai già, con un breve elenco di argomenti. Un modello AI locale legge le trascrizioni confrontandole con quell'elenco, e un secondo passaggio giudica ogni scoperta: tenere, tenere d'occhio o scartare, con un motivo. Il modello propone, non decide.

Un altro passaggio usa solo il conteggio, senza AI, per far emergere le idee su cui il canale torna spesso e che non rientrano in nessuno dei tuoi argomenti.

## I risultati

- 377 ore di video, in 179 puntate, trasformate in 237 MB di testo.
- Una ricerca ha trovato una frase a 1 ora e 39 minuti di una diretta di quattro ore del 2024.
- Un video di quattro ore senza sottotitoli si trascrive in circa 3 minuti con una scheda video.
- Nessun account, nessuna chiave API, niente da pagare.

## Le scelte e il perché

### Perché gira tutto in locale?

Quello che sai e quello che cerchi non escono mai dal tuo computer, e non c'è un costo per ogni ora di video.

### Perché la parte AI è facoltativa?

Un paio di gigabyte non devono mai iniziare a scaricarsi a sorpresa. Anche senza, hai comunque l'archivio completo del canale, da cercare.

### Perché le esecuzioni programmate avvisano così tanto?

Un downloader rotto sembra identico a una settimana tranquilla senza novità. Così un'esecuzione che non riesce a scaricare lo dice, può riprendere da dove si era fermata e non può sovrapporsi a un'altra.

## I limiti

- Su una scheda video piccola i modelli più grandi passano al processore, a circa 5 parole al secondo, quindi la lettura è lenta sui computer modesti.
- Il modello può sbagliare, ed è per questo che si limita a proporre e un secondo passaggio giudica ogni scoperta.

## Codice e demo

[Codice](https://github.com/anthonygozzini/channel-miner), [Guardalo in azione](https://anthonygozzini.github.io/channel-miner/demo.html)

## Se ti serve qualcosa di simile

- [Automazioni AI per il marketing](https://anthonygozzini.github.io/it/services/ai-automation/index.md): Pipeline che tolgono il lavoro ripetitivo da localizzazione, report e contenuti, controllate prima che esca qualsiasi cosa.

[Prenota una call di 30 minuti](https://cal.com/anthony-gozzini-amzx2u/30min) · Email: anthony.gozzini@gmail.com

## Altri case study

- [GuardBot](https://anthonygozzini.github.io/it/projects/guardbot/index.md): Sicurezza prima di comprare, su EVM, Solana e TRON, con scambi simulati invece di un'API esterna.
- [Telegram Gatekeeper Bot](https://anthonygozzini.github.io/it/projects/gatekeeper/index.md): Filtra chi vuole entrare in un gruppo Telegram privato.
- [Telegram Referral System](https://anthonygozzini.github.io/it/projects/referral/index.md): Link referral, punti e classifica per una community Telegram.
