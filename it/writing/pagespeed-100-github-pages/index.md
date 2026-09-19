# Come ho portato un sito su GitHub Pages a 100 in ogni categoria di PageSpeed

Di Anthony Gozzini · Pubblicato il 19 set 2026 · 5 min di lettura

> I caratteri, un'immagine e una cache che non controllo. Quanto è costata ogni correzione in millisecondi, e le tre voci che da un repository non si sistemano.

Questo sito è HTML semplice. Uno script Python trasforma un file di contenuti in pagine, e GitHub Pages le serve gratis. Non c'è niente di pesante. Arrivare a 100 in ogni categoria di PageSpeed mi è costato comunque una settimana di serate, perché quasi tutto quello che lo rallentava era invisibile finché non l'ho misurato.

La regola che mi sono dato è semplice: nessun avviso lasciato lì. Un punteggio verde con sotto un elenco di segnalazioni è un punteggio di cui non mi fido.

## I caratteri mi sono costati tre tentativi

Il sito usa Geist. Precaricarlo sembrava la mossa ovvia ed è stata la peggiore: Chrome trattiene il primo disegno della pagina finché un carattere precaricato è in viaggio, fino al suo limite di 1,5 secondi. La pagina compariva quando compariva il carattere.

Collegarlo come un normale foglio di stile è andata peggio in un altro modo. Il testo si vedeva subito con un carattere di ripiego e poi saltava all'arrivo di Geist: uno spostamento di 0,317 su una pagina dove non si era mai mosso niente.

Mettere il carattere dentro il CSS come dato ha risolto tutti e due i problemi e ne ha aggiunto un terzo: 14 KB del foglio di stile erano byte che nessuna regola usava, e Lighthouse li conta come CSS inutilizzato.

Quello che ha funzionato: ridurre i due caratteri ai soli segni che il sito disegna davvero, 13,8 KB e 2,3 KB, e passarli alla pagina dentro blocchi di dati che il browser non compila mai. Uno script di tre righe li trasforma in caratteri veri prima del primo disegno. Gli stessi byte, messi in uno script normale, erano un'attività da 50-78 ms; come blocchi di dati non costano niente.

Un dettaglio che non avevo previsto: le frecce che uso nei testi mancano dalla versione ridotta di Geist di Google, e ogni segno mancante mandava Chrome a cercare tra i caratteri di sistema. Quella ricerca erano 10 dei 14 ms del primo calcolo della home. Il pacchetto di Vercel le ha.

## Una sola immagine decide il tempo di caricamento

In ogni pagina l'elemento più grande è un'immagine di copertina. Presa da una CDN ha bisogno di una seconda connessione prima ancora di partire: sul telefono di PageSpeed erano 0,7 s in più, sul desktop 0,5 s. Presa da GitHub Pages finisce invece nell'elenco dei file con cache troppo corta.

Così l'unica misura che serve a tutti e due gli schermi di PageSpeed viaggia dentro l'HTML in formato AVIF, e le copie più grandi restano sulla CDN per gli schermi ad alta densità. La pagina si porta dietro i pixel che contano; tutto il resto si scarica solo se serve.

## La cache che non controllo

GitHub Pages manda dieci minuti di cache per qualsiasi file e non permette di cambiarli. Dieci minuti sono abbastanza pochi da far chiedere a PageSpeed una cache più lunga su ogni file statico.

I file già salvati nel repository passano da una CDN che mette il numero della versione dentro l'indirizzo: così restano validi per un anno. La pagina invece tiene i suoi dieci minuti, perché è proprio il file che voglio venga riletto.

## A ogni pagina solo il CSS che le serve

Ogni pagina si porta il proprio foglio di stile, tagliato sulle regole che possono riguardare quello che contiene. Tagliare gli stili a mano è il modo classico di rompere un sito senza accorgersene, quindi lo fa il generatore e un secondo script lo dimostra: apre ogni pagina in un browser senza finestra, su tre schermi, in quattro stati, prima con lo stile tagliato e poi con quello intero, e confronta ogni proprietà calcolata di ogni elemento. L'ultima volta erano 356.148 valori e zero differenze.

## L'attività lunga era la favicon

PageSpeed continuava a segnalare un'attività lunga che riusciva solo a chiamare "non attribuibile". Era la favicon: un'immagine SVG con dentro del testo. Un'immagine SVG non può usare i caratteri della pagina, quindi a ogni caricamento il browser andava a cercarne uno tra quelli di sistema, dai 9 ai 17 ms. Adesso quelle due lettere sono tracciati, disegnati dallo stesso script che riduce i caratteri.

Il tema salvato e il saluto in base all'ora sono usciti dalla fase di lettura della pagina per lo stesso motivo: leggerli dalla memoria del browser mentre la pagina veniva letta bastava a portare quell'attività oltre i 50 ms.

## Quello che un repository non può risolvere

Alcune voci restano aperte e resteranno così. Content Security Policy, HSTS, COOP, X-Frame-Options e Trusted Types sono intestazioni della risposta del server, e GitHub Pages non permette di mandarne nessuna. Per sistemarle servono un dominio mio e un servizio davanti al sito. Anche la CDN viene segnalata, giustamente, come servizio di terze parti, e una voce sulla compatibilità dei browser conta contro chiunque usi i caratteri via FontFace.

Preferisco dirlo che far finta che l'elenco sia vuoto.

## La parte che vale la pena copiare

Non i trucchi: i controlli. Un comando ricostruisce il sito, verifica che il risultato sia identico a quello salvato, poi controlla ogni link interno, ogni descrizione, i dati strutturati, le copie in markdown, i file sulla CDN e i caratteri incorporati. Il controllo degli stili confronta i valori calcolati. Un terzo script misura cosa scaricherebbe davvero il telefono di PageSpeed per ogni immagine, perché Lighthouse ignora la densità dello schermo quando decide che un'immagine è troppo grande. Poi Lighthouse gira su tutte le 27 pagine, telefono e desktop: 54 esecuzioni, 100 ovunque.

Il sito e tutto questo sono [pubblici](https://github.com/anthonygozzini/anthonygozzini.github.io). Un numero che hai verificato vale più di un numero che speri.
