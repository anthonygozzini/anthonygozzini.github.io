# Come ho ricostruito il mio primo gioco dall'unica build sopravvissuta

Di Anthony Gozzini · Pubblicato il 15 set 2026 · 5 min di lettura

> La cartella del progetto del mio gioco Unity del 2018 non c'era più, il gioco compilato sì. Come io e un agente AI l'abbiamo fatto tornare un progetto, e i due errori che ci hanno quasi fermati.

Nel 2018 ho fatto il mio primo gioco in Unity, seguendo i tutorial per principianti di Brackeys: un breve gioco 3D con menu principale, un livello e i titoli di coda. Anni dopo la cartella del progetto non c'era più. Restava solo il gioco compilato per Windows.

A settembre ho deciso di recuperarlo, come progetto vero da aprire, modificare e pubblicare. L'ho fatto con un agente AI per il codice. L'agente scavava; il mio compito era decidere cosa provare e controllare ogni risultato prima di crederci.

## 1. Da una build a un progetto

AssetRipper, uno strumento open source, sa leggere una build di Unity ed esportarne un progetto. Scene, materiali, texture, font e animazioni sono tornati com'erano. Gli script C# sono tornati decompilati dall'assembly principale del gioco: fanno quello che facevano gli originali, ma commenti e formattazione sono spariti.

Il gioco era fatto con Unity 2018.2. Invece di cercare un editor vecchio, l'ho portato su Unity 6 LTS. L'importazione è finita con zero errori di compilazione. Sembrava troppo bello, quindi abbiamo verificato che l'assembly del gioco fosse stato davvero compilato da tutti e nove gli script. Lo era.

## 2. Il primo errore: un'impostazione vuota

La prima build per il browser si è fermata all'ultimo passaggio, con un errore di "indice fuori intervallo" nel profondo del post-processing WebGL di Unity. La causa era un solo campo vuoto: l'esportazione aveva lasciato in bianco il nome del template WebGL, e Unity 6 si aspetta un nome da dividere in due. Impostarlo sul template predefinito ha risolto.

## 3. Il secondo errore: un'interfaccia che non c'era

Gli avvisi della build indicavano qualcosa di peggio. Nel 2018 i componenti dell'interfaccia di Unity stavano in una DLL; in Unity 6 sono codice sorgente dentro un pacchetto. Ogni testo, pulsante e canvas delle mie tre scene, 31 riferimenti in tutto, puntava ancora a una DLL che non esisteva più. Il gioco sarebbe partito senza menu.

Unity identifica uno script dentro una DLL con un numero ricavato da un hash MD4 del suo namespace e del nome della classe. Invece di indovinare quale numero fosse Button e quale Text, abbiamo calcolato l'hash di ogni classe dell'interfaccia di Unity 6, dopo aver provato la formula su un riferimento di cui conoscevamo già la risposta. Tutti gli undici numeri sconosciuti corrispondevano a una classe vera. Abbiamo riscritto 35 riferimenti, controllato che non ne restasse nessuno e rifatto la build.

## 4. Una prova, non una barra di caricamento

Il primo test automatico catturava solo la barra di caricamento di Unity, e non dimostrava niente. Così abbiamo guidato un browser vero tramite il protocollo DevTools: il menu è comparso, un clic su Start ha caricato il livello e la console non mostrava errori. Più tardi Quit nel browser non faceva nulla, perché una pagina web non può chiudere la propria scheda. Nella versione per browser ora Quit riporta al menu principale, provato partendo dai titoli di coda.

## Cosa mi porto a casa

Quasi ogni passaggio ha avuto un momento in cui la risposta facile era sbagliata: zero errori da verificare, un test che mostrava solo una barra di caricamento, una corrispondenza che si poteva indovinare. L'agente è veloce; il lavoro vero è controllare. È la stessa regola che seguo nelle operazioni di marketing.

Puoi [giocare a Sgamers nel browser](https://anthonygozzini.github.io/play/sgamers/). Serve una tastiera.
