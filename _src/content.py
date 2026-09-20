"""Everything the site says, in English and Italian. build.py turns it into pages."""


def L(en, it):
    return {"en": en, "it": it}


SITE = {
    "name": "Anthony Gozzini",
    "url": "https://anthonygozzini.github.io",
    "email": "anthony.gozzini@gmail.com",
    "cal": "https://cal.com/anthony-gozzini-amzx2u/30min",
    "linkedin": "https://www.linkedin.com/in/anthonygozzini",
    "github": "https://github.com/anthonygozzini",
    # Google Business Profile: the review form, and the profile itself by its Maps id (the id inside the review link).
    "google_review": "https://g.page/r/CTh1FZ7BnsCWEBM/review",
    "google_profile": "https://maps.google.com/?cid=10862856855635719480",
    "repo": "anthonygozzini/anthonygozzini.github.io",
    "telegram": "https://t.me/TonyGoz",
    "whatsapp": "https://wa.me/message/3TTWEPNJGQSWL1",
    "cv": "assets/Anthony-Gozzini-CV.pdf",
    "description": L(
        "CRM & lifecycle marketer. Eight years inside Trust Wallet's community, from volunteer to the Marketing & Communications team. I build my own tools.",
        "CRM e lifecycle marketing. Otto anni nella community di Trust Wallet, da volontario al team Marketing & Communications. Costruisco i miei strumenti.",
    ),
    "job_title": "CRM & Lifecycle Marketer",
    "knows_about": ["CRM", "Lifecycle marketing", "Community management", "Localization", "Telegram bots", "Web3"],
    # Public location: the region only. The town stays private.
    "region": "Piemonte",
    # Google Search Console, "HTML tag" method: the content value only. Printed on the English home page.
    "google_verification": "",
}

UI = {
    "greeting_fallback": L("Hello", "Ciao"),
    "greeting_who": L("I'm Anthony Gozzini", "sono Anthony Gozzini"),
    "greeting_name": L("CRM & lifecycle marketing, community, and the tools I build",
                       "CRM e lifecycle marketing, community e strumenti che costruisco da solo"),
    "greetings": L(["Good morning", "Good afternoon", "Good evening"], ["Buongiorno", "Buon pomeriggio", "Buonasera"]),
    "resources": L("Resources", "Risorse"),
    "connect": L("Connect", "Contatti"),
    "book_call": L("Book a call", "Prenota una call"),
    "view_all": L("View all", "Vedi tutti"),
    "theme_light": L("Light", "Chiaro"),
    "theme_dark": L("Dark", "Scuro"),
    "theme_auto": L("Auto", "Auto"),
    "language": L("Language", "Lingua"),
    "theme": L("Theme", "Tema"),
    "pages": L("Pages", "Pagine"),
    "min_read": L("min read", "min di lettura"),
    "read": L("Read the article", "Leggi l'articolo"),
    "share": L("Share on", "Condividi su"),
    "published": L("Published", "Pubblicato il"),
    "by": L("By", "Di"),
    "on_affidaty": L("On Affidaty", "Su Affidaty"),
    "all_categories": L("All", "Tutti"),
    "copy": L("Copy", "Copia"),
    "copied": L("Copied", "Copiata"),
    "skip": L("Skip to content", "Vai al contenuto"),
    "footer": L("Plain HTML, no trackers, no cookies.", "HTML semplice, niente tracker, niente cookie."),
}

NAV = [
    {"key": "home", "path": "", "icon": "home", "label": L("Home", "Home")},
    {"key": "about", "path": "about/", "icon": "user", "label": L("About", "Chi sono")},
    {"key": "services", "path": "services/", "icon": "briefcase", "label": L("Services", "Servizi")},
    {"key": "projects", "path": "projects/", "icon": "code", "label": L("Projects", "Progetti")},
    {"key": "writing", "path": "writing/", "icon": "pen", "label": L("Writing", "Articoli"), "group": "resources"},
    # Six tabs fit a 360 px phone; Tools stays reachable from the home page and the sidebar.
    {"key": "tools", "path": "tools/", "icon": "box", "label": L("Tools", "Strumenti"), "group": "resources", "tabbar": False},
    {"key": "contact", "path": "contact/", "icon": "chat", "label": L("Contact", "Contattami"), "group": "connect"},
]

HOME = {
    "title": L("Anthony Gozzini — CRM & Lifecycle Marketing", "Anthony Gozzini — CRM e Lifecycle Marketing"),
    "intro": L(
        "Eight years inside Trust Wallet's community, seven as a volunteer and then on the Marketing & Communications team. When the tools I need don't exist, I build them and publish the code.",
        "Otto anni nella community di Trust Wallet, sette da volontario e poi nel team Marketing & Communications. Quando gli strumenti che mi servono non esistono, li costruisco da solo e ne pubblico il codice.",
    ),
    "intro_link": L("More about me", "Scopri chi sono"),
    "tips": [
        {"id": "keys", "desktop": True,
         "text": L("Move around quickly with keyboard shortcuts 1 → 7. Try pressing 2, 3 and 4.",
                   "Muoviti velocemente con le scorciatoie da tastiera 1 → 7. Prova a premere 2, 3 e 4.")},
        {"id": "story", "href": "about/",
         "text": L("Grew up near Varese, six years in Kraków, in crypto since 2017", "Cresciuto in provincia di Varese, sei anni a Cracovia, nelle crypto dal 2017"),
         "link": L("Read my story →", "Leggi la mia storia →")},
        {"id": "role", "href": "contact/",
         "text": L("Looking for my next role in CRM, lifecycle or community marketing", "Cerco il prossimo ruolo in CRM, lifecycle o community marketing"),
         "link": L("How to reach me →", "Come contattarmi →")},
        {"id": "call", "href": "cal",
         "text": L("Happy to talk: pick a 30-minute slot that suits you", "Parliamone: scegli uno slot da 30 minuti quando ti è comodo"),
         "link": L("Book a call ↗", "Prenota una call ↗")},
        {"id": "projects", "href": "projects/",
         "text": L("I publish what I build, with tests and versioned releases", "Pubblico quello che costruisco, con test e release versionate"),
         "link": L("See projects →", "Vedi i progetti →")},
        {"id": "writing", "href": "writing/",
         "text": L("In 2024 I wrote a weekly crypto market column; now I write about what I build", "Nel 2024 ho scritto una rubrica settimanale sul mercato crypto; ora scrivo di quello che costruisco"),
         "link": L("Read my articles →", "Leggi gli articoli →")},
        {"id": "ai", "href": "about/#how-i-work",
         "text": L("I work with AI agents every day, and nothing they produce ships unchecked", "Lavoro ogni giorno con agenti AI, e niente di quello che producono esce senza controllo"),
         "link": L("How I work →", "Come lavoro →")},
        {"id": "cv", "href": "cv",
         "text": L("Prefer a PDF? My one-page CV is ready", "Preferisci un PDF? Il mio CV di una pagina è pronto"),
         "link": L("Download CV ↓", "Scarica il CV ↓")},
    ],
    "projects": L("Projects", "Progetti"),
    "writing": L("Recent writing", "Articoli recenti"),
    "updates": L("Updates", "Aggiornamenti"),
    "tools": L("Tools I use", "Strumenti che uso"),
    "home_tools": ["amplitude", "databricks", "telegram", "claude"],
}

# Newest first. Dates are YYYY-MM or YYYY-MM-DD; icon is a key in build.ICONS.
UPDATES = [
    {"date": "2026-09-15", "icon": "tag", "href": "https://github.com/anthonygozzini/telegram-gatekeeper-bot/releases",
     "title": L("Released Telegram Gatekeeper Bot v3.0.0", "Pubblicato Telegram Gatekeeper Bot v3.0.0"),
     "text": L("The bot that screens people before they join a private group is now generic: any community sets its own questions in one config file.",
               "Il bot che filtra chi entra in un gruppo privato ora è generico: ogni community imposta le sue domande in un solo file di configurazione.")},
    {"date": "2026-09-15", "icon": "game", "href": "writing/rebuilding-sgamers/",
     "title": L("Rebuilt Sgamers, my first game", "Ricostruito Sgamers, il mio primo gioco"),
     "text": L("The original project was lost. I rebuilt it from the only surviving build and got it running again, in a browser too.",
               "Il progetto originale era andato perso. L'ho ricostruito dall'unica build rimasta e l'ho fatto ripartire, anche nel browser.")},
    {"date": "2026-09-15", "icon": "tag", "href": "https://github.com/anthonygozzini/Telegram-Referral-System/releases",
     "title": L("Referral System v1.1.0 and Channel Copier v1.0.1", "Referral System v1.1.0 e Channel Copier v1.0.1"),
     "text": L("Two bots I first built for paying clients, cleaned up and released with proper versions.",
               "Due bot nati per clienti paganti, ripuliti e pubblicati con versioni vere.")},
    {"date": "2026-09-13", "icon": "code", "href": "projects/",
     "title": L("Published GuardBot and channel-miner", "Pubblicati GuardBot e channel-miner"),
     "text": L("A pre-trade safety checker for three blockchains, and a tool that turns a YouTube channel into searchable text.",
               "Un controllo di sicurezza prima di comprare, per tre blockchain, e uno strumento che trasforma un canale YouTube in testo da cercare.")},
    {"date": "2026-08", "icon": "flag",
     "title": L("Closed my chapter at Trust Wallet", "Chiuso il mio capitolo in Trust Wallet"),
     "text": L("Nearly a year and a half on the Marketing & Communications team, after seven years as a volunteer. Now looking for what's next.",
               "Quasi un anno e mezzo nel team Marketing & Communications, dopo sette anni da volontario. Ora cerco il prossimo passo.")},
    {"date": "2025-04", "icon": "briefcase",
     "title": L("Joined Trust Wallet's Marketing & Communications team", "Entrato nel team Marketing & Communications di Trust Wallet"),
     "text": L("Hired to run CRM and lifecycle after seven years as a volunteer ambassador in the same community.",
               "Assunto per occuparmi di CRM e lifecycle, dopo sette anni da ambassador volontario nella stessa community.")},
    {"date": "2025-03", "icon": "cap",
     "title": L("Completed Harvard's CS50", "Completato CS50 di Harvard"),
     "text": L("Three months of C, Python, SQL and web fundamentals, to fill the gaps the tutorials had left.",
               "Tre mesi di C, Python, SQL e basi del web, per colmare i vuoti lasciati dai tutorial.")},
    {"date": "2024-08", "icon": "code", "href": "https://github.com/anthonygozzini",
     "title": L("Put my first Telegram bots on GitHub", "Messi su GitHub i miei primi bot Telegram"),
     "text": L("The referral and channel-copier bots behind my client work.",
               "I bot per referral e copia dei canali nati dal lavoro per i clienti.")},
    {"date": "2024-01", "icon": "pen", "href": "writing/",
     "title": L("Started a weekly crypto column for Affidaty", "Iniziata una rubrica settimanale sulle crypto per Affidaty"),
     "text": L("Market analysis and news every week, in Italian and English, until March 2024.",
               "Analisi e notizie di mercato ogni settimana, in italiano e in inglese, fino a marzo 2024.")},
    {"date": "2023-09", "icon": "bot",
     "title": L("Started building Telegram bots for crypto communities", "Iniziato a costruire bot Telegram per community crypto"),
     "text": L("Referral programs, private-group screening and channel mirroring, for paying clients.",
               "Programmi referral, selezione degli ingressi nei gruppi privati e copia dei post tra canali, per clienti paganti.")},
    {"date": "2019-09", "icon": "mic",
     "title": L("Wrote a voice assistant in Python", "Scritto un assistente vocale in Python"),
     "text": L("It listened and answered in Italian.", "Ascoltava e rispondeva in italiano.")},
    {"date": "2018-11", "icon": "game", "href": "projects/",
     "title": L("Made my first game in Unity", "Fatto il mio primo gioco in Unity"),
     "text": L("Sgamers: a short 3D game built by following Brackeys' beginner tutorials.",
               "Sgamers: un breve gioco 3D costruito seguendo i tutorial per principianti di Brackeys.")},
    {"date": "2018", "icon": "users",
     "title": L("Joined Trust Wallet's Trust Squad", "Entrato nella Trust Squad di Trust Wallet"),
     "text": L("Became a volunteer ambassador and an admin of Trust Wallet's global Telegram community.",
               "Diventato ambassador volontario e admin della community Telegram globale di Trust Wallet.")},
    {"date": "2017-09", "icon": "briefcase",
     "title": L("Joined Motorola Solutions in Kraków", "Entrato in Motorola Solutions a Cracovia"),
     "text": L("Customer support for EMEA on Salesforce: lead conversion up 14%, data accuracy up 28%.",
               "Assistenza clienti per l'area EMEA su Salesforce: conversione dei lead +14%, accuratezza dei dati +28%.")},
    {"date": "2017-04", "icon": "coin",
     "title": L("Started freelancing in crypto", "Iniziato a lavorare da freelance nelle crypto"),
     "text": L("Customer support and CRM for Bitgrail, with a 95% satisfaction rate.",
               "Assistenza clienti e CRM per Bitgrail, con il 95% di clienti soddisfatti.")},
    {"date": "2017-03", "icon": "briefcase",
     "title": L("Worked on a Google project with Accenture", "Lavorato a un progetto Google con Accenture"),
     "text": L("Reviewed web content for policy compliance at 98% accuracy.",
               "Revisione di contenuti web per il rispetto delle policy, con il 98% di accuratezza.")},
    {"date": "2013-06", "icon": "plane",
     "title": L("Moved to Kraków", "Trasferito a Cracovia"),
     "text": L("Joined Sabre Travel Network in customer business support, and later trained a 20-person team.",
               "Entrato in Sabre Travel Network nell'assistenza clienti business, dove poi ho formato un team di 20 persone.")},
    {"date": "2011", "icon": "cap",
     "title": L("Graduated in aeronautics", "Diplomato perito aeronautico"),
     "text": L("Technical diploma after six years of aeronautical engineering school.",
               "Diploma tecnico dopo sei anni di istituto aeronautico.")},
]

ABOUT = {
    "title": L("About", "Chi sono"),
    "description": L(
        "Thirteen years in customer engagement and data, the last nine in Web3: from support desks in Kraków to running CRM and lifecycle at Trust Wallet.",
        "Tredici anni tra clienti e dati, gli ultimi nove nel Web3: dall'assistenza clienti a Cracovia alla gestione di CRM e lifecycle in Trust Wallet.",
    ),
    "bio_default": L(
        [
            "I'm Anthony Gozzini, a CRM and lifecycle marketer with thirteen years in customer engagement and data, the last nine in Web3. From April 2025 to August 2026 I ran CRM and lifecycle at Trust Wallet, one of the world's most-used self-custodial crypto wallets, after seven years as a volunteer ambassador in its community.",
            "I work where data, communities and automation meet: segments and journeys in Amplitude, campaigns in ten languages, Telegram communities at scale, and tools I build myself when nothing on the shelf fits. I live between Novara, Varese and Milan, work remotely in English and Italian, and I'm looking for my next role.",
        ],
        [
            "Sono Anthony Gozzini e mi occupo di CRM e lifecycle marketing: tredici anni tra rapporto con i clienti e dati, gli ultimi nove nel Web3. Da aprile 2025 ad agosto 2026 ho gestito CRM e lifecycle in Trust Wallet, uno dei wallet crypto self-custodial più usati al mondo, dopo sette anni da ambassador volontario nella sua community.",
            "Lavoro dove si incontrano dati, community e automazione: segmenti e percorsi in Amplitude, campagne in dieci lingue, community Telegram su larga scala e strumenti che costruisco da solo quando non trovo quello giusto. Vivo tra Novara, Varese e Milano, lavoro da remoto in italiano e in inglese, e cerco il mio prossimo ruolo.",
        ],
    ),
    "bio_long": L(
        [
            "I grew up in a small village in the province of Varese, in northern Italy, and spent six years at a technical school for aeronautics. I came out with a diploma, a certificate in 2D CAD and no clear idea of what I wanted to do.",
            "So in 2013 I moved to Kraków, to find my own way and try something completely new. I stayed six years. At Sabre Travel Network I handled billing and customer profiles in SAP for travel agencies, made the process 15% more efficient and ended up training a team of twenty on the new procedures. In 2017 I spent six months with Accenture on a Google project, reviewing web content for policy compliance, then moved to Motorola Solutions to support customers across Europe, the Middle East and Africa on Salesforce. That's where I learned that a CRM is only as good as its data: cleaning it up lifted lead conversion by 14%.",
            "Crypto found me in 2017, alongside the day job. I started freelancing in customer support and CRM for Bitgrail, an Italian exchange, and in 2018 I joined the Trust Squad, Trust Wallet's volunteer ambassadors. Very quickly I became one of the admins of its global Telegram community. Running a crypto community at that scale teaches you fast: every day there were scams to catch, panics to calm and questions to answer in plain words.",
            "I couldn't really code yet, so I learned by making things. In 2018 I built a small 3D game in Unity by following Brackeys' tutorials. In 2019 I wrote a voice assistant in Python that listened and answered in Italian. A PHP and MySQL course had me build an online shop from scratch. Between 2023 and 2024 the experiments became paid work: Telegram bots for crypto communities, from referral programs with points and wallets to private groups that screen who gets in. The freelance side grew too: community campaigns that lifted participation by 40% for The OGz Club, SEO and paid campaigns for Affidaty, where I also wrote a weekly market column, and project planning for The Jungle Industry.",
            "Trust Wallet stayed the constant. Over seven years as a volunteer I coordinated a squad of thirty ambassadors around the world and built anti-scam bots for the regional groups. In early 2025 I took Harvard's CS50, to fill the gaps the tutorials had left, and in April the team hired me into Marketing & Communications.",
            "For the next year and a half I ran CRM and lifecycle for a wallet with millions of users. I wrote the strategy across three pillars, new-user activation, cross-sell and retention, each with its own segments, triggers, messages and KPIs. I mapped where people dropped out of onboarding and turned those gaps into segments to target. I ran localization for announcements in ten languages and app push in eight, configured homepage banners for launches such as Cash App Pay and Banxa, wrote the playbook for high-severity incidents and looked after a Telegram network of more than fifteen regional communities.",
            "Across all of it I work with AI agents every day, for localization, analysis and code. They're fast, and they're often wrong in convincing ways, so I follow one rule: nothing they produce is trusted until it has been checked. This site was built the same way.",
            "My contract ended in August 2026. I'm looking for my next role in CRM, lifecycle or community marketing, full-time or fractional, remote or in person around Varese, Novara, Verbano-Cusio-Ossola and Milan. In the meantime I'm publishing the tools I've built, bringing Sgamers back to life and adding Italian to The Legend of Dragoon on PC.",
            "Outside work I'm with my partner, often playing video games together, Genshin Impact above all. The rest goes into DIY: my latest project was a whole piece of furniture for the living room, and I enjoy doing the electrical and plumbing work around the house myself.",
            "Support desks taught me to listen, communities taught me to moderate, bots taught me to build. I'm still doing all three.",
        ],
        [
            "Sono cresciuto in un paesino in provincia di Varese e ho passato sei anni in un istituto tecnico aeronautico. Ne sono uscito con un diploma, un attestato di CAD 2D e nessuna idea chiara di cosa volessi fare.",
            "Così nel 2013 mi sono trasferito a Cracovia, per trovare la mia strada e fare un'esperienza completamente nuova. Ci sono rimasto sei anni. In Sabre Travel Network gestivo fatturazione e profili cliente in SAP per le agenzie di viaggio, ho reso il processo più efficiente del 15% e alla fine ho formato un team di venti persone sulle nuove procedure. Nel 2017 ho passato sei mesi con Accenture su un progetto per Google, a controllare contenuti web per il rispetto delle policy, poi sono passato a Motorola Solutions, assistenza clienti per Europa, Medio Oriente e Africa su Salesforce. Lì ho capito che un CRM vale quanto i suoi dati: sistemarli ha fatto crescere la conversione dei lead del 14%.",
            "Le crypto mi hanno trovato nel 2017, accanto al lavoro. Ho iniziato da freelance nell'assistenza clienti e nel CRM per Bitgrail, un exchange italiano, e nel 2018 sono entrato nella Trust Squad, gli ambassador volontari di Trust Wallet. Molto presto sono diventato uno degli admin della sua community Telegram globale. Gestire una community crypto di quelle dimensioni ti insegna in fretta: ogni giorno c'erano truffe da bloccare, panico da calmare e domande a cui rispondere con parole semplici.",
            "Programmare ancora non lo sapevo fare, quindi ho imparato costruendo. Nel 2018 ho fatto un piccolo gioco 3D in Unity seguendo i tutorial di Brackeys. Nel 2019 ho scritto in Python un assistente vocale che ascoltava e rispondeva in italiano. Con un corso di PHP e MySQL ho costruito un negozio online da zero. Tra il 2023 e il 2024 gli esperimenti sono diventati lavoro pagato: bot Telegram per community crypto, dai programmi referral con punti e wallet ai gruppi privati che filtrano chi entra. È cresciuto anche il lavoro da freelance: campagne per la community di The OGz Club che hanno alzato la partecipazione del 40%, SEO e campagne a pagamento per Affidaty, dove ho scritto anche una rubrica settimanale sul mercato, e pianificazione dei progetti per The Jungle Industry.",
            "Trust Wallet è rimasta la costante. In sette anni da volontario ho coordinato una squadra di trenta ambassador in giro per il mondo e costruito bot anti-truffa per i gruppi regionali. All'inizio del 2025 ho seguito CS50 di Harvard, per colmare i vuoti lasciati dai tutorial, e ad aprile il team mi ha assunto in Marketing & Communications.",
            "Per il successivo anno e mezzo ho gestito CRM e lifecycle di un wallet con milioni di utenti. Ho scritto la strategia su tre pilastri, attivazione dei nuovi utenti, cross-sell e retention, ognuno con i suoi segmenti, trigger, messaggi e KPI. Ho mappato dove le persone abbandonavano l'onboarding e ho trasformato quei buchi in segmenti da raggiungere. Ho gestito la localizzazione degli annunci in dieci lingue e delle notifiche push in otto, configurato i banner della home per lanci come Cash App Pay e Banxa, scritto il playbook per gli incidenti più gravi e seguito una rete Telegram di oltre quindici community regionali.",
            "In tutto questo lavoro ogni giorno con agenti AI, per localizzazione, analisi e codice. Sono veloci e spesso sbagliano in modo convincente, quindi seguo una regola sola: niente di quello che producono è affidabile finché non è stato verificato. Anche questo sito è stato costruito così.",
            "Il mio contratto è finito ad agosto 2026. Cerco il prossimo ruolo in CRM, lifecycle o community marketing, full-time o part-time, da remoto o in presenza tra Varese, Novara, Verbano-Cusio-Ossola e Milano. Nel frattempo pubblico gli strumenti che ho costruito, riporto in vita Sgamers e aggiungo l'italiano a The Legend of Dragoon su PC.",
            "Fuori dal lavoro sto con la mia compagna, spesso a giocare insieme ai videogiochi, soprattutto a Genshin Impact. Il resto del tempo va nel fai-da-te: l'ultimo progetto è stato un mobile intero per la sala, e mi diverte occuparmi da solo della parte elettrica e idraulica di casa.",
            "L'assistenza mi ha insegnato ad ascoltare, le community a moderare, i bot a costruire. Faccio ancora tutte e tre le cose.",
        ],
    ),
    "bio_label": L("Bio", "Bio"),
    "bio_short": L("Short", "Breve"),
    "bio_long_label": L("Long", "Lunga"),
    "updates": L("Recent updates", "Aggiornamenti recenti"),
    "updates_count": 6,
    "career": L("Career", "Carriera"),
    "career_intro": L(
        "The short version of thirteen years in customer engagement and data; the full one is on LinkedIn.",
        "La versione breve di tredici anni tra clienti e dati; quella completa è su LinkedIn.",
    ),
    "career_link": L("LinkedIn profile ↗", "Profilo LinkedIn ↗"),
    "education": L("Education", "Formazione"),
    "how": L("How I work", "Come lavoro"),
}

CAREER = [
    {"when": L("Apr 2025 – Aug 2026", "apr 2025 – ago 2026"), "role": L("CRM & Lifecycle Marketing", "CRM & Lifecycle Marketing"), "org": "Trust Wallet",
     "text": L("CRM strategy, localization in ten languages, the crisis playbook and a Telegram network of 15+ communities.",
               "Strategia CRM, localizzazione in dieci lingue, il playbook di crisi e una rete Telegram di oltre 15 community.")},
    {"when": L("2018 – Apr 2025", "2018 – apr 2025"), "role": L("Community Ambassador, Trust Squad", "Community Ambassador, Trust Squad"), "org": L("Trust Wallet · volunteer", "Trust Wallet · volontario"),
     "text": L("Coordinated thirty ambassadors and administered the global Telegram community.",
               "Coordinato trenta ambassador e amministrato la community Telegram globale.")},
    {"when": L("Apr 2017 – now", "apr 2017 – oggi"), "role": L("Web3 Freelancer", "Freelance Web3"), "org": "Bitgrail · The OGz Club · Affidaty · The Jungle Industry",
     "text": L("Support and CRM, community campaigns, SEO and a weekly market column.",
               "Assistenza e CRM, campagne per community, SEO e una rubrica settimanale sul mercato.")},
    {"when": L("Sep 2017 – Apr 2019", "set 2017 – apr 2019"), "role": L("Customer Support Specialist", "Customer Support Specialist"), "org": L("Motorola Solutions · Kraków", "Motorola Solutions · Cracovia"),
     "text": L("EMEA support on Salesforce; lead conversion up 14%.", "Assistenza EMEA su Salesforce; conversione dei lead +14%.")},
    {"when": L("Mar – Aug 2017", "mar – ago 2017"), "role": L("Web Data Analyst for Google", "Web Data Analyst per Google"), "org": L("Accenture · Kraków", "Accenture · Cracovia"),
     "text": L("Policy-compliance review at 98% accuracy.", "Revisione per il rispetto delle policy, con il 98% di accuratezza.")},
    {"when": L("Jun 2013 – Feb 2017", "giu 2013 – feb 2017"), "role": L("Customer Business Support", "Customer Business Support"), "org": L("Sabre Travel Network · Kraków", "Sabre Travel Network · Cracovia"),
     "text": L("SAP billing and customer profiles; trained a team of twenty.", "Fatturazione e profili cliente in SAP; formato un team di venti persone.")},
]

EDUCATION = [
    {"when": L("Jan – Mar 2025", "gen – mar 2025"), "role": L("CS50: Introduction to Computer Science", "CS50: Introduction to Computer Science"), "org": "Harvard Online",
     "text": L("C, Python, SQL and the web.", "C, Python, SQL e il web.")},
    {"when": L("2005 – 2011", "2005 – 2011"), "role": L("Aeronautical technical diploma", "Diploma di perito aeronautico"), "org": L("Technical institute", "Istituto tecnico"),
     "text": L("Six years of aeronautical engineering.", "Sei anni di tecnica aeronautica.")},
]

PRINCIPLES = [
    {"title": L("Nothing ships unchecked", "Niente esce senza controllo"),
     "text": L("AI agents are fast and often wrong in convincing ways. Every output, from a translated push notification to a line of code, is untrusted until it has been verified.",
               "Gli agenti AI sono veloci e spesso sbagliano in modo convincente. Ogni risultato, da una notifica push tradotta a una riga di codice, non è affidabile finché non è stato verificato.")},
    {"title": L("Size the problem first", "Prima misuro il problema"),
     "text": L("Before proposing a campaign I look at where people actually drop out. At Trust Wallet that meant mapping the onboarding funnel before deciding who to message.",
               "Prima di proporre una campagna guardo dove le persone si perdono davvero. In Trust Wallet voleva dire mappare il funnel di onboarding prima di decidere a chi scrivere.")},
    {"title": L("I take the problems nobody owns", "Mi prendo i problemi senza un responsabile"),
     "text": L("Four fragmented internal tools, a campaign calendar nobody kept, an incident with no playbook: I'd rather write the document that fixes it than wait for someone else to.",
               "Quattro strumenti interni sparpagliati, un calendario delle campagne che nessuno teneva, un incidente senza playbook: preferisco scrivere io il documento che risolve, invece di aspettare qualcun altro.")},
    {"title": L("Write it down", "Metto tutto per iscritto"),
     "text": L("Playbooks, calendars and templates, so the next person, or the next incident, doesn't start from zero.",
               "Playbook, calendari e modelli, così la prossima persona, o il prossimo incidente, non riparte da zero.")},
]

PROJECTS = {
    "title": L("Projects", "Progetti"),
    "description": L(
        "What I build outside my job, published with the code: GuardBot, channel-miner, Telegram bots for crypto communities and Sgamers, my first Unity game.",
        "Quello che costruisco fuori dal lavoro, pubblicato con il codice: GuardBot, channel-miner, bot Telegram per community crypto e Sgamers, il mio primo gioco.",
    ),
    "intro": L(
        "Things I've built outside my job. Some started as work for paying clients, some are my own; all of them are published with their code.",
        "Cose che ho costruito fuori dal lavoro. Alcune sono nate per clienti paganti, altre sono mie; tutte sono pubblicate con il loro codice.",
    ),
    "items": [
        {"slug": "guardbot", "name": "GuardBot", "year": "2026", "cover": "cover-guardbot.jpg", "home": True,
         "summary": L("Pre-trade safety for EVM, Solana and TRON, from simulated trades instead of a vendor API.",
                      "Sicurezza prima di comprare, su EVM, Solana e TRON, con scambi simulati invece di un'API esterna."),
         "text": L("Before you buy a token, GuardBot simulates a real buy and a real sell against live liquidity, so a honeypot shows up as a sell that fails instead of a green badge from someone else's API. One paste field then audits a wallet's token approvals across EVM, Solana and TRON and revokes the risky ones, simulating every revoke before signing. It runs locally, uses only Python's standard library and includes an MCP server, so AI agents can call it as a tool.",
                   "Prima di comprare un token, GuardBot simula davvero un acquisto e una vendita sulla liquidità reale: un honeypot si vede come una vendita che fallisce, non come un bollino verde dato dall'API di qualcun altro. Poi, incollando un indirizzo, controlla le autorizzazioni di un wallet su EVM, Solana e TRON e revoca quelle rischiose, simulando ogni revoca prima della firma. Gira in locale, usa solo la libreria standard di Python e include un server MCP, così anche gli agenti AI possono usarlo come strumento."),
         "tags": L(["Python", "MCP", "Side project"], ["Python", "MCP", "Progetto personale"]),
         "links": [{"label": L("Code", "Codice"), "href": "https://github.com/anthonygozzini/guardbot"},
                   {"label": L("35-second demo", "Demo di 35 secondi"), "href": "https://anthonygozzini.github.io/guardbot/demo.html"},
                   {"label": L("Project page", "Pagina del progetto"), "href": "https://anthonygozzini.github.io/guardbot/"}]},
        {"slug": "channel-miner", "name": "channel-miner", "year": "2026", "cover": "cover-channel-miner.jpg", "home": True,
         "summary": L("Read a YouTube channel instead of watching it.", "Leggere un canale YouTube invece di guardarlo."),
         "text": L("Point it at a YouTube channel and it collects every video and turns it into text you can search, grep or read at your own pace. Tell it what you already know and an AI reads the lot and hands back only what is new to you. Everything runs on your own computer, with no accounts, no API keys and nothing to pay. On one channel it turned 377 hours across 179 videos into 237 MB of text.",
                   "Gli dai un canale YouTube: raccoglie tutti i video e li trasforma in testo da cercare o leggere con calma. Se gli dici cosa sai già, un'AI legge tutto e ti restituisce solo le cose nuove per te. Gira tutto sul tuo computer, senza account, senza chiavi API e senza pagare niente. Su un canale ha trasformato 377 ore di video, in 179 puntate, in 237 MB di testo."),
         "tags": L(["Python", "Shell", "Side project"], ["Python", "Shell", "Progetto personale"]),
         "links": [{"label": L("Code", "Codice"), "href": "https://github.com/anthonygozzini/channel-miner"},
                   {"label": L("See it run", "Guardalo in azione"), "href": "https://anthonygozzini.github.io/channel-miner/demo.html"}]},
        {"slug": "gatekeeper", "name": "Telegram Gatekeeper Bot", "year": "2023 – 2026", "cover": "cover-gatekeeper.jpg", "home": True,
         "summary": L("Screens people before they join a private Telegram group.", "Filtra chi vuole entrare in un gruppo Telegram privato."),
         "text": L("Applicants answer a short questionnaire in a private chat. The bot checks the answers and looks for signs of fake or farmed accounts, such as no username, a name full of digits or a social profile already used by someone else. Then it either admits them with a single-use invite link or sends the request to the admins with Approve and Reject buttons. Questions, rules and messages live in one config file, so the same bot works for any community. Version 3 is the generic rewrite of a bot I first built for private crypto groups in 2023.",
                   "Chi vuole entrare risponde a un breve questionario in chat privata. Il bot controlla le risposte e cerca i segnali di account falsi o farmati, come la mancanza di username, un nome pieno di numeri o un profilo social già usato da qualcun altro. Poi lo fa entrare con un link d'invito monouso oppure passa la richiesta agli admin, con i pulsanti Approva e Rifiuta. Domande, regole e messaggi stanno in un solo file di configurazione, quindi lo stesso bot funziona per qualsiasi community. La versione 3 è la riscrittura generica di un bot che avevo costruito nel 2023 per gruppi crypto privati."),
         "tags": L(["Python", "SQLite", "40 tests", "v3.0.0"], ["Python", "SQLite", "40 test", "v3.0.0"]),
         "links": [{"label": L("Code", "Codice"), "href": "https://github.com/anthonygozzini/telegram-gatekeeper-bot"},
                   {"label": L("Releases", "Release"), "href": "https://github.com/anthonygozzini/telegram-gatekeeper-bot/releases"}]},
        {"slug": "sgamers", "name": "Sgamers", "year": "2018 · 2026", "cover": "cover-sgamers.jpg", "home": True,
         "summary": L("My first game, made in Unity in 2018 and rebuilt in 2026.", "Il mio primo gioco, fatto in Unity nel 2018 e ricostruito nel 2026."),
         "text": L("A short 3D game with a main menu, one level and a credits screen, made while learning Unity with Brackeys' tutorials. The project folder was lost and only the compiled game survived, so in 2026 I rebuilt the project from that build, upgraded it to Unity 6 and brought it back to life in the browser. You can play it right here with a keyboard: arrow keys or A and D to move, Space to jump. The original Windows build is attached to the release.",
                   "Un breve gioco 3D con menu principale, un livello e i titoli di coda, fatto mentre imparavo Unity con i tutorial di Brackeys. La cartella del progetto era andata persa ed era sopravvissuto solo il gioco compilato, così nel 2026 ho ricostruito il progetto da quella build, l'ho aggiornato a Unity 6 e l'ho riportato in vita nel browser. Puoi giocarci qui con la tastiera: frecce oppure A e D per muoverti, Spazio per saltare. La build Windows originale è allegata alla release."),
         "tags": L(["Unity", "C#", "Playable in the browser"], ["Unity", "C#", "Giocabile nel browser"]),
         "links": [{"label": L("Play in your browser", "Gioca nel browser"), "href": "play/sgamers/", "raw": True},
                   {"label": L("Code", "Codice"), "href": "https://github.com/anthonygozzini/sgamers"},
                   {"label": L("Windows build", "Build Windows"), "href": "https://github.com/anthonygozzini/sgamers/releases/tag/v1.0.0"},
                   {"label": L("How I rebuilt it", "Come l'ho ricostruito"), "href": "writing/rebuilding-sgamers/", "internal": True}]},
        {"slug": "referral", "name": "Telegram Referral System", "year": "2024", "cover": "cover-referral.jpg",
         "summary": L("Referral links, points and a leaderboard for a Telegram community.", "Link referral, punti e classifica per una community Telegram."),
         "text": L("Members join the channel and the group, submit their wallet address and get a personal referral link. Every person they bring in earns them points, and admins can see the top referrers at any time. I built it for a crypto creator's community in 2024; version 1.1.0 restores the join checks and wallet submission from the full client version.",
                   "Gli iscritti entrano nel canale e nel gruppo, inviano l'indirizzo del proprio wallet e ricevono un link referral personale. Ogni persona che portano vale punti, e gli admin possono vedere in qualsiasi momento chi ha invitato di più. L'ho costruito nel 2024 per la community di un creator crypto; la versione 1.1.0 recupera la verifica delle iscrizioni e l'invio del wallet dalla versione completa fatta per il cliente."),
         "tags": L(["Python", "Client work", "v1.1.0"], ["Python", "Per un cliente", "v1.1.0"]),
         "links": [{"label": L("Code", "Codice"), "href": "https://github.com/anthonygozzini/Telegram-Referral-System"},
                   {"label": L("Releases", "Release"), "href": "https://github.com/anthonygozzini/Telegram-Referral-System/releases"}]},
        {"slug": "copier", "name": "Telegram Channel Message Copier", "year": "2024", "cover": "cover-copier.jpg",
         "summary": L("Mirrors posts from one Telegram channel to others.", "Copia i post da un canale Telegram ad altri."),
         "text": L("A production bot that copies messages from a source channel to several destination channels and can schedule sends. It ran for a client who cross-posted to six channels; version 1.0.1 fixes a formatting slip that stopped it from starting.",
                   "Un bot in produzione che copia i messaggi da un canale di origine a più canali di destinazione e può programmare gli invii. Ha lavorato per un cliente che pubblicava su sei canali; la versione 1.0.1 corregge un errore di formattazione che ne impediva l'avvio."),
         "tags": L(["Python", "Client work", "v1.0.1"], ["Python", "Per un cliente", "v1.0.1"]),
         "links": [{"label": L("Code", "Codice"), "href": "https://github.com/anthonygozzini/Telegram-Channel-Message-Copier-Bot"},
                   {"label": L("Releases", "Release"), "href": "https://github.com/anthonygozzini/Telegram-Channel-Message-Copier-Bot/releases"}]},
        {"slug": "lod", "name": L("The Legend of Dragoon in Italian", "The Legend of Dragoon in italiano"), "year": "2026", "cover": "cover-lod.jpg",
         "summary": L("An Italian language mod for the fan-made PC version of a 1999 PlayStation RPG.", "Una mod in italiano per la versione PC, fatta dai fan, di un GDR PlayStation del 1999."),
         "text": L("Severed Chains is the fan-made PC version of The Legend of Dragoon. I'm adding Italian to it: 611 text strings are in the mod so far, and another 339 are hardcoded and need changes to the engine itself. It hasn't been tested in game yet, so there's no public release.",
                   "Severed Chains è la versione PC di The Legend of Dragoon fatta dai fan. Ci sto aggiungendo l'italiano: finora nella mod ci sono 611 stringhe di testo, mentre altre 339 sono scritte direttamente nel codice e richiedono modifiche al motore. Non è ancora stata provata in gioco, quindi non c'è una release pubblica."),
         "tags": L(["Localization", "Modding", "In progress"], ["Localizzazione", "Modding", "In corso"]),
         "links": []},
    ],
}

WRITING = {
    "title": L("Writing", "Articoli"),
    "description": L(
        "What I build and how I check it, plus the weekly crypto market column I wrote for Affidaty in early 2024, in English and Italian.",
        "Quello che costruisco e come lo verifico, più la rubrica settimanale sul mercato crypto che ho scritto per Affidaty a inizio 2024.",
    ),
    "intro": L(
        "In early 2024 I wrote a weekly crypto market column for Affidaty, in Italian and English. Now I write about what I build and how I check it.",
        "All'inizio del 2024 ho scritto una rubrica settimanale sul mercato crypto per Affidaty, in italiano e in inglese. Ora scrivo di quello che costruisco e di come lo verifico.",
    ),
    "posts": [
        {"slug": "pagespeed-100-github-pages", "date": "2026-09-19", "minutes": 5, "cover": "cover-pagespeed.jpg",
         "title": L("Getting 100 in every PageSpeed category on GitHub Pages",
                    "Come ho portato un sito su GitHub Pages a 100 in ogni categoria di PageSpeed"),
         "excerpt": L("Fonts, one image and a cache I don't control. What each fix cost in milliseconds, and the three items nobody can fix from a repository.",
                      "I caratteri, un'immagine e una cache che non controllo. Quanto è costata ogni correzione in millisecondi, e le tre voci che da un repository non si sistemano."),
         "description": L("Fonts, one inlined image and a cache I can't change: what each fix cost in milliseconds, and what a repository alone can never fix.",
                          "Caratteri, un'immagine dentro l'HTML e una cache che non posso cambiare: cosa è costata ogni correzione in millisecondi e cosa resta fuori portata."),
         "body": L(
             """<p>This site is plain HTML. A Python script turns one content file into pages, and GitHub Pages serves them for free. Nothing about it is heavy. Reaching 100 in every PageSpeed category still took a week of evenings, because most of what held it back was invisible until I measured it.</p>
<p>The rule I set myself was simple: no insight left unread. A green score with a list of warnings under it is a score I don't trust.</p>
<h2>The fonts took three attempts</h2>
<p>The site is set in Geist. Preloading it was the obvious first move, and the worst: Chrome holds the first paint while a preloaded font is in flight, up to its own 1.5-second cap. The page appeared when the font did.</p>
<p>A normal stylesheet link was worse in a different way. The text painted immediately in a fallback face and then jumped when Geist arrived: a layout shift of 0.317 on a page where nothing had ever moved.</p>
<p>Putting the font inside the CSS as a data URI fixed both, and added a third problem: 14 KB of the stylesheet were now bytes no rule referenced, which Lighthouse counts as unused CSS.</p>
<p>What finally worked: cut the two faces down to the characters the site actually draws, 13.8 KB and 2.3 KB, and hand them to the page as data blocks in script tags the browser never compiles. A three-line script turns each block into a FontFace before the first layout. The same bytes as a regular script were a 50 to 78 ms long task; as data blocks they cost nothing.</p>
<p>One detail I didn't see coming: the arrows in the copy are missing from Google's Latin cut of Geist, and every missing character sent Chrome hunting through the system fonts. That search was 10 of the 14 ms of the home page's first layout. Vercel's own package has the arrows.</p>
<h2>One image decides the LCP</h2>
<p>On every page the largest element is a cover image. Served from a CDN it needs a second connection before it can even start: on PageSpeed's phone that was 0.7 s of extra LCP, on its desktop 0.5 s. Served from GitHub Pages it lands in the caching report instead.</p>
<p>So the one size both of PageSpeed's screens need travels inside the HTML as an AVIF, and the larger copies stay on the CDN for dense screens. The page carries its own most important pixels; everything else is still fetched only when a browser needs it.</p>
<h2>The cache I don't control</h2>
<p>GitHub Pages sends the same ten-minute cache for every file and offers no way to change it. Ten minutes is short enough that PageSpeed asks for a longer one on every static file.</p>
<p>Files that are committed now travel through a CDN with the commit written into the URL, which makes them immutable for a year. The page itself keeps its ten minutes, because that is the file I actually want re-fetched.</p>
<h2>Each page gets only the CSS it can use</h2>
<p>Every page carries its own stylesheet, cut to the rules that can match what is on it. Cutting styles by hand is how sites break quietly, so the build does it and a second script proves it: it opens every page in a headless browser, on three screen sizes, in four states, once with the cut stylesheet and once with the full one, and compares every computed property of every element and pseudo-element. On the last run that was 356,148 values and zero differences.</p>
<h2>The long task was the favicon</h2>
<p>PageSpeed kept reporting a long task it could only label "unattributable". It was the favicon: an SVG with a text element in it. An SVG can't use the page's fonts, so on every load the browser went looking through the system ones, 9 to 17 ms of it. Now those two letters are outlines, drawn by the same script that cuts the fonts.</p>
<p>The saved theme and the time-of-day greeting moved out of the parsing task for the same reason. Reading them from local storage while the page was being parsed was enough to push that task past 50 ms.</p>
<h2>What a repository can't fix</h2>
<p>Some items stay open and always will. A content security policy, HSTS, COOP, X-Frame-Options and Trusted Types are all response headers, and GitHub Pages doesn't let you send any. Fixing them means a domain of my own and a service in front of the site. The CDN is also flagged, correctly, as a third party, and one browser-support item counts against any use of FontFace at all.</p>
<p>I'd rather say that out loud than pretend the list is empty.</p>
<h2>The part worth copying</h2>
<p>Not the tricks: the checks. One command rebuilds the site, confirms the output matches what is committed, then verifies every internal link, every description, the structured data, the markdown copies, the pinned CDN files and the embedded fonts. The style check compares computed values. A third script measures what PageSpeed's phone would really download for each image, because Lighthouse ignores pixel density when it decides an image is too big. Then Lighthouse runs on all 27 pages, phone and desktop: 54 runs, 100 everywhere.</p>
<p>The site and all of it are <a href="https://github.com/anthonygozzini/anthonygozzini.github.io">in the open</a>. A number you have checked is worth more than a number you hope for.</p>""",
             """<p>Questo sito è HTML semplice. Uno script Python trasforma un file di contenuti in pagine, e GitHub Pages le serve gratis. Non c'è niente di pesante. Arrivare a 100 in ogni categoria di PageSpeed mi è costato comunque una settimana di serate, perché quasi tutto quello che lo rallentava era invisibile finché non l'ho misurato.</p>
<p>La regola che mi sono dato è semplice: nessun avviso lasciato lì. Un punteggio verde con sotto un elenco di segnalazioni è un punteggio di cui non mi fido.</p>
<h2>I caratteri mi sono costati tre tentativi</h2>
<p>Il sito usa Geist. Precaricarlo sembrava la mossa ovvia ed è stata la peggiore: Chrome trattiene il primo disegno della pagina finché un carattere precaricato è in viaggio, fino al suo limite di 1,5 secondi. La pagina compariva quando compariva il carattere.</p>
<p>Collegarlo come un normale foglio di stile è andata peggio in un altro modo. Il testo si vedeva subito con un carattere di ripiego e poi saltava all'arrivo di Geist: uno spostamento di 0,317 su una pagina dove non si era mai mosso niente.</p>
<p>Mettere il carattere dentro il CSS come dato ha risolto tutti e due i problemi e ne ha aggiunto un terzo: 14 KB del foglio di stile erano byte che nessuna regola usava, e Lighthouse li conta come CSS inutilizzato.</p>
<p>Quello che ha funzionato: ridurre i due caratteri ai soli segni che il sito disegna davvero, 13,8 KB e 2,3 KB, e passarli alla pagina dentro blocchi di dati che il browser non compila mai. Uno script di tre righe li trasforma in caratteri veri prima del primo disegno. Gli stessi byte, messi in uno script normale, erano un'attività da 50-78 ms; come blocchi di dati non costano niente.</p>
<p>Un dettaglio che non avevo previsto: le frecce che uso nei testi mancano dalla versione ridotta di Geist di Google, e ogni segno mancante mandava Chrome a cercare tra i caratteri di sistema. Quella ricerca erano 10 dei 14 ms del primo calcolo della home. Il pacchetto di Vercel le ha.</p>
<h2>Una sola immagine decide il tempo di caricamento</h2>
<p>In ogni pagina l'elemento più grande è un'immagine di copertina. Presa da una CDN ha bisogno di una seconda connessione prima ancora di partire: sul telefono di PageSpeed erano 0,7 s in più, sul desktop 0,5 s. Presa da GitHub Pages finisce invece nell'elenco dei file con cache troppo corta.</p>
<p>Così l'unica misura che serve a tutti e due gli schermi di PageSpeed viaggia dentro l'HTML in formato AVIF, e le copie più grandi restano sulla CDN per gli schermi ad alta densità. La pagina si porta dietro i pixel che contano; tutto il resto si scarica solo se serve.</p>
<h2>La cache che non controllo</h2>
<p>GitHub Pages manda dieci minuti di cache per qualsiasi file e non permette di cambiarli. Dieci minuti sono abbastanza pochi da far chiedere a PageSpeed una cache più lunga su ogni file statico.</p>
<p>I file già salvati nel repository passano da una CDN che mette il numero della versione dentro l'indirizzo: così restano validi per un anno. La pagina invece tiene i suoi dieci minuti, perché è proprio il file che voglio venga riletto.</p>
<h2>A ogni pagina solo il CSS che le serve</h2>
<p>Ogni pagina si porta il proprio foglio di stile, tagliato sulle regole che possono riguardare quello che contiene. Tagliare gli stili a mano è il modo classico di rompere un sito senza accorgersene, quindi lo fa il generatore e un secondo script lo dimostra: apre ogni pagina in un browser senza finestra, su tre schermi, in quattro stati, prima con lo stile tagliato e poi con quello intero, e confronta ogni proprietà calcolata di ogni elemento. L'ultima volta erano 356.148 valori e zero differenze.</p>
<h2>L'attività lunga era la favicon</h2>
<p>PageSpeed continuava a segnalare un'attività lunga che riusciva solo a chiamare "non attribuibile". Era la favicon: un'immagine SVG con dentro del testo. Un'immagine SVG non può usare i caratteri della pagina, quindi a ogni caricamento il browser andava a cercarne uno tra quelli di sistema, dai 9 ai 17 ms. Adesso quelle due lettere sono tracciati, disegnati dallo stesso script che riduce i caratteri.</p>
<p>Il tema salvato e il saluto in base all'ora sono usciti dalla fase di lettura della pagina per lo stesso motivo: leggerli dalla memoria del browser mentre la pagina veniva letta bastava a portare quell'attività oltre i 50 ms.</p>
<h2>Quello che un repository non può risolvere</h2>
<p>Alcune voci restano aperte e resteranno così. Content Security Policy, HSTS, COOP, X-Frame-Options e Trusted Types sono intestazioni della risposta del server, e GitHub Pages non permette di mandarne nessuna. Per sistemarle servono un dominio mio e un servizio davanti al sito. Anche la CDN viene segnalata, giustamente, come servizio di terze parti, e una voce sulla compatibilità dei browser conta contro chiunque usi i caratteri via FontFace.</p>
<p>Preferisco dirlo che far finta che l'elenco sia vuoto.</p>
<h2>La parte che vale la pena copiare</h2>
<p>Non i trucchi: i controlli. Un comando ricostruisce il sito, verifica che il risultato sia identico a quello salvato, poi controlla ogni link interno, ogni descrizione, i dati strutturati, le copie in markdown, i file sulla CDN e i caratteri incorporati. Il controllo degli stili confronta i valori calcolati. Un terzo script misura cosa scaricherebbe davvero il telefono di PageSpeed per ogni immagine, perché Lighthouse ignora la densità dello schermo quando decide che un'immagine è troppo grande. Poi Lighthouse gira su tutte le 27 pagine, telefono e desktop: 54 esecuzioni, 100 ovunque.</p>
<p>Il sito e tutto questo sono <a href="https://github.com/anthonygozzini/anthonygozzini.github.io">pubblici</a>. Un numero che hai verificato vale più di un numero che speri.</p>"""),
         },
        {"slug": "rebuilding-sgamers", "date": "2026-09-15", "minutes": 5, "cover": "cover-sgamers.jpg",
         "title": L("How I rebuilt my first game from its only surviving build", "Come ho ricostruito il mio primo gioco dall'unica build sopravvissuta"),
         "excerpt": L("The project folder of my 2018 Unity game was gone; the compiled game wasn't. How an AI agent and I turned it back into a project, and the two bugs that almost stopped us.",
                      "La cartella del progetto del mio gioco Unity del 2018 non c'era più, il gioco compilato sì. Come io e un agente AI l'abbiamo fatto tornare un progetto, e i due errori che ci hanno quasi fermati."),
         "description": L("Only the compiled build of my 2018 Unity game survived. How an AI agent and I rebuilt the project from it, and the two bugs that almost stopped us.",
                          "Del mio gioco Unity del 2018 restava solo la build. Come io e un agente AI ne abbiamo ricostruito il progetto, e i due errori che ci hanno quasi fermati."),
         "body": L(
             """<p>In 2018 I made my first game in Unity, following Brackeys' beginner tutorials: a short 3D runner with a main menu, one level and a credits screen. Years later the project folder was gone. The only thing left was the compiled Windows game.</p>
<p>This September I decided to get it back, as a real project I could open, change and publish. I did it with an AI coding agent. The agent did the digging; my job was to decide what to try and to check every result before believing it.</p>
<h2>1. From a build back to a project</h2>
<p>AssetRipper, an open-source tool, can read a Unity build and export a project from it. Scenes, materials, textures, fonts and animations came back as they were. The C# scripts came back decompiled from the game's main assembly: they do what the originals did, but the comments and the formatting are gone.</p>
<p>The game was made with Unity 2018.2. Instead of hunting down an old editor, I moved it to Unity 6 LTS. The import finished with zero compile errors. That sounded too good, so we checked that the game's assembly had really been built from all nine scripts. It had.</p>
<h2>2. The first bug: an empty setting</h2>
<p>The first browser build failed at the very last step, with an "index out of range" error deep inside Unity's WebGL post-processing. The cause was a single empty field: the export had left the WebGL template name blank, and Unity 6 expects a name it can split in two. Setting it to the default template fixed it.</p>
<h2>3. The second bug: an interface that wasn't there</h2>
<p>The build warnings pointed at something worse. In 2018 Unity's UI components lived in a DLL; in Unity 6 they are source code inside a package. Every text, button and canvas in my three scenes, 31 references in all, still pointed at a DLL that no longer existed. The game would have started without a menu.</p>
<p>Unity identifies a script inside a DLL with a number derived from an MD4 hash of its namespace and class name. Instead of guessing which number meant Button and which meant Text, we computed the hash for every UI class in Unity 6, after first testing the formula on a reference whose answer we already knew. All eleven unknown numbers matched a real class. We rewrote 35 references, confirmed that none were left, and built again.</p>
<h2>4. Proof, not a loading bar</h2>
<p>The first automated test captured only Unity's loading bar, which proved nothing. So we drove a real browser through its DevTools protocol: the menu appeared, a click on Start loaded the level, and the console showed no errors. Later, Quit did nothing in the browser, because a web page can't close its own tab. In the browser version Quit now takes you back to the main menu, tested all the way from the credits screen.</p>
<h2>What I took from it</h2>
<p>Almost every step had a moment where the easy answer was wrong: zero errors that needed checking, a test that only showed a loading bar, a mapping that could have been guessed. The agent is fast; the checking is the job. It's the same rule I follow in marketing operations.</p>
<p>You can <a href="{play}">play Sgamers in your browser</a>. You'll need a keyboard.</p>""",
             """<p>Nel 2018 ho fatto il mio primo gioco in Unity, seguendo i tutorial per principianti di Brackeys: un breve gioco 3D con menu principale, un livello e i titoli di coda. Anni dopo la cartella del progetto non c'era più. Restava solo il gioco compilato per Windows.</p>
<p>A settembre ho deciso di recuperarlo, come progetto vero da aprire, modificare e pubblicare. L'ho fatto con un agente AI per il codice. L'agente scavava; il mio compito era decidere cosa provare e controllare ogni risultato prima di crederci.</p>
<h2>1. Da una build a un progetto</h2>
<p>AssetRipper, uno strumento open source, sa leggere una build di Unity ed esportarne un progetto. Scene, materiali, texture, font e animazioni sono tornati com'erano. Gli script C# sono tornati decompilati dall'assembly principale del gioco: fanno quello che facevano gli originali, ma commenti e formattazione sono spariti.</p>
<p>Il gioco era fatto con Unity 2018.2. Invece di cercare un editor vecchio, l'ho portato su Unity 6 LTS. L'importazione è finita con zero errori di compilazione. Sembrava troppo bello, quindi abbiamo verificato che l'assembly del gioco fosse stato davvero compilato da tutti e nove gli script. Lo era.</p>
<h2>2. Il primo errore: un'impostazione vuota</h2>
<p>La prima build per il browser si è fermata all'ultimo passaggio, con un errore di "indice fuori intervallo" nel profondo del post-processing WebGL di Unity. La causa era un solo campo vuoto: l'esportazione aveva lasciato in bianco il nome del template WebGL, e Unity 6 si aspetta un nome da dividere in due. Impostarlo sul template predefinito ha risolto.</p>
<h2>3. Il secondo errore: un'interfaccia che non c'era</h2>
<p>Gli avvisi della build indicavano qualcosa di peggio. Nel 2018 i componenti dell'interfaccia di Unity stavano in una DLL; in Unity 6 sono codice sorgente dentro un pacchetto. Ogni testo, pulsante e canvas delle mie tre scene, 31 riferimenti in tutto, puntava ancora a una DLL che non esisteva più. Il gioco sarebbe partito senza menu.</p>
<p>Unity identifica uno script dentro una DLL con un numero ricavato da un hash MD4 del suo namespace e del nome della classe. Invece di indovinare quale numero fosse Button e quale Text, abbiamo calcolato l'hash di ogni classe dell'interfaccia di Unity 6, dopo aver provato la formula su un riferimento di cui conoscevamo già la risposta. Tutti gli undici numeri sconosciuti corrispondevano a una classe vera. Abbiamo riscritto 35 riferimenti, controllato che non ne restasse nessuno e rifatto la build.</p>
<h2>4. Una prova, non una barra di caricamento</h2>
<p>Il primo test automatico catturava solo la barra di caricamento di Unity, e non dimostrava niente. Così abbiamo guidato un browser vero tramite il protocollo DevTools: il menu è comparso, un clic su Start ha caricato il livello e la console non mostrava errori. Più tardi Quit nel browser non faceva nulla, perché una pagina web non può chiudere la propria scheda. Nella versione per browser ora Quit riporta al menu principale, provato partendo dai titoli di coda.</p>
<h2>Cosa mi porto a casa</h2>
<p>Quasi ogni passaggio ha avuto un momento in cui la risposta facile era sbagliata: zero errori da verificare, un test che mostrava solo una barra di caricamento, una corrispondenza che si poteva indovinare. L'agente è veloce; il lavoro vero è controllare. È la stessa regola che seguo nelle operazioni di marketing.</p>
<p>Puoi <a href="{play}">giocare a Sgamers nel browser</a>. Serve una tastiera.</p>"""),
         },
    ],
    "affidaty": [
        {"date": L("18 Mar 2024", "20 mar 2024"), "sort": "2024-03-18", "cover": L("affidaty-2024-03-18-en.jpg", "affidaty-2024-03-18-it.jpg"),
         "title": L("Blockchain and Crypto News: March 13 – 20, 2024", "News mondo Blockchain e Crypto: 13 – 20 marzo 2024"),
         "excerpt": L("New EU sanctions and crypto laws, and the other stories that moved the market that week.", "Hyperledger Fabric V2 come blockchain autorizzata e le altre notizie che hanno mosso il mercato quella settimana."),
         "url": L("https://affidaty.io/blog/en/2024/03/news-blockchain-crypto-13-20mar-24-eng/", "https://affidaty.io/blog/it/2024/03/news-blockchain-crypto-13-20mar-24/")},
        {"date": L("4 Mar 2024", "1 mar 2024"), "sort": "2024-03-04", "cover": L("affidaty-2024-03-04-en.jpg", "affidaty-2024-03-04-it.jpg"),
         "title": L("Blockchain and Crypto World News: February 24 – March 1, 2024", "News mondo Blockchain e Crypto: 24 febbraio – 1 marzo 2024"),
         "excerpt": L("A historic surge for Bitcoin in February, and what else shaped the crypto market.", "L'impennata di BTC, SEC contro Kraken, i Layer 2 per Bitcoin e le altre notizie della settimana."),
         "url": L("https://affidaty.io/blog/en/2024/03/news-blockchain-crypto-24feb-1mar-24-2/", "https://affidaty.io/blog/it/2024/03/news-blockchain-crypto-24feb-01mar-2024/")},
        {"date": L("23 Feb 2024", "23 feb 2024"), "sort": "2024-02-23", "cover": L("affidaty-2024-02-23-en.jpg", "affidaty-2024-02-23-it.jpg"),
         "title": L("Blockchain and Crypto World News: February 17-23, 2024", "News mondo Blockchain e Crypto: 17-23 febbraio 2024"),
         "excerpt": L("Humanity Protocol by Animoca and Polygon, a step forward for Web3 adoption, and the week's other news.", "Humanity Protocol di Animoca e Polygon, un passo avanti per l'adozione del Web3, e le altre notizie della settimana."),
         "url": L("https://affidaty.io/blog/en/2024/02/blockchain-and-crypto-world-news-february-17-23-2024/", "https://affidaty.io/blog/it/2024/02/news-crypto-blockchain-23-febbraio/")},
        {"date": L("16 Feb 2024", "16 feb 2024"), "sort": "2024-02-16", "cover": L("affidaty-2024-02-16-en.jpg", "affidaty-2024-02-16-it.jpg"),
         "title": L("Blockchain and Crypto World News: February 10-16, 2024", "News mondo Blockchain e Crypto: 10-16 febbraio 2024"),
         "excerpt": L("Bitcoin breaks $50,000 for the first time since December 2021.", "Bitcoin supera i 50.000 dollari per la prima volta da dicembre 2021."),
         "url": L("https://affidaty.io/blog/en/2024/02/news-blockchain-crypto-10-16-feb-24/", "https://affidaty.io/blog/it/2024/02/news-blockchain-crypto-10-16-feb-24-it/")},
        {"date": L("9 Feb 2024", "9 feb 2024"), "sort": "2024-02-09", "cover": L("affidaty-2024-02-09-en.jpg", "affidaty-2024-02-09-it.jpg"),
         "title": L("Blockchain and Crypto World News: February 3-9, 2024", "News mondo Blockchain e Crypto: 3-9 febbraio 2024"),
         "excerpt": L("Bitcoin's market movements and trends, and the week's main stories.", "Movimenti e andamenti del mercato Bitcoin e le principali notizie della settimana."),
         "url": L("https://affidaty.io/blog/en/2024/02/blockchain-crypto-3-9-february/", "https://affidaty.io/blog/it/2024/02/news-blockchain-crypto-3-9-febbraio/")},
        {"date": L("26 Jan 2024", "26 gen 2024"), "sort": "2024-01-26", "cover": L("affidaty-2024-01-26-en.jpg", "affidaty-2024-01-26-it.jpg"),
         "title": L("Blockchain and Crypto World News: January 22-26, 2024", "News mondo Blockchain e Crypto: 22-26 gennaio 2024"),
         "excerpt": L("Uncertainty over an Ether ETF, falling funding for Web3 startups and crypto price trends.", "Incertezza sull'ETF di Ether, calo dei finanziamenti alle startup Web3 e andamento dei prezzi delle crypto."),
         "url": L("https://affidaty.io/blog/en/2024/01/blockchain-crypto-news-january-22-26-2024/", "https://affidaty.io/blog/it/2024/01/news-blockchain-crypto-22-26-gennaio-2024/")},
        {"date": L("19 Jan 2024", "19 gen 2024"), "sort": "2024-01-19", "cover": L("affidaty-2024-01-19-en.jpg", "affidaty-2024-01-19-it.jpg"),
         "title": L("Crypto and blockchain news: January 15-19, 2024", "News Blockchain e Crypto: 15-19 gennaio 2024"),
         "excerpt": L("Bitcoin drops after the ETF approval, and the rest of the week in crypto.", "Il calo di Bitcoin dopo l'approvazione degli ETF e il resto della settimana nelle crypto."),
         "url": L("https://affidaty.io/blog/en/2024/01/blockchain-crypto-news-january-15-19-2024/", "https://affidaty.io/blog/it/2024/01/news-blockchain-crypto-15-19-gennaio-2024/")},
        {"date": L("12 Jan 2024", "11 gen 2024"), "sort": "2024-01-12", "cover": L("affidaty-2024-01-12-en.jpg", "affidaty-2024-01-12-it.jpg"),
         "title": L("Bitcoin ETFs: A New Era in Financial Markets and Challenges for Traditional Investors", "ETF Bitcoin: nuova era nei mercati finanziari e sfide per gli investitori tradizionali"),
         "excerpt": L("What the approval of spot Bitcoin ETFs means for financial markets and for traditional investors.", "Cosa significa l'approvazione degli ETF spot su Bitcoin per i mercati finanziari e per gli investitori tradizionali."),
         "url": L("https://affidaty.io/blog/en/2024/01/bitcoin-etfs-financial-markets/", "https://affidaty.io/blog/it/2024/01/etf-bitcoin-nuova-era-mercati-finanziari/")},
        {"date": L("5 Jan 2024", "5 gen 2024"), "sort": "2024-01-05", "cover": L("affidaty-2024-01-05-en.jpg", "affidaty-2024-01-05-it.jpg"),
         "title": L("The Cryptocurrency Landscape in 2023: a Year of Turning Points and Challenges", "Il panorama delle criptovalute nel 2023: un anno di svolte e sfide"),
         "excerpt": L("A year of growth and transition: the key events that marked crypto in 2023.", "Un anno di crescita e di transizione: gli eventi chiave che hanno segnato le crypto nel 2023."),
         "url": L("https://affidaty.io/blog/en/2024/01/cryptocurrency-2023-ethereum/", "https://affidaty.io/blog/it/2024/01/criptovalute-2023-ethereum/")},
    ],
    "affidaty_label": L("Affidaty column · 2024", "Rubrica Affidaty · 2024"),
    "mine_label": L("My articles", "I miei articoli"),
}

TOOLS = {
    "title": L("Tools", "Strumenti"),
    "description": L(
        "The tools I use for CRM, data, communities and building, from Amplitude and Databricks to Telegram and Claude, and what I use each one for.",
        "Gli strumenti che uso per CRM, dati, community e sviluppo, da Amplitude e Databricks a Telegram e Claude, e per cosa uso ognuno.",
    ),
    "intro": L(
        "The tools I use across CRM, data, communities and building, and what I actually use each one for.",
        "Gli strumenti che uso tra CRM, dati, community e sviluppo, e per cosa uso davvero ognuno.",
    ),
    "categories": {
        "crm": L("CRM & lifecycle", "CRM e lifecycle"),
        "data": L("Data", "Dati"),
        "community": L("Community & support", "Community e assistenza"),
        "marketing": L("Marketing", "Marketing"),
        "build": L("Build & AI", "Sviluppo e AI"),
    },
    "items": [
        {"key": "amplitude", "name": "Amplitude", "cat": "crm", "url": "https://amplitude.com",
         "use": L("Segments and funnels for activation, cross-sell and retention.", "Segmenti e funnel per attivazione, cross-sell e retention.")},
        {"key": "salesforce", "name": "Salesforce", "cat": "crm", "url": "https://www.salesforce.com",
         "use": L("EMEA customer records at Motorola Solutions, where cleaner data lifted accuracy 28%.", "Anagrafiche dei clienti EMEA in Motorola Solutions, dove dati più puliti hanno alzato l'accuratezza del 28%.")},
        {"key": "hubspot", "name": "HubSpot", "cat": "crm", "url": "https://www.hubspot.com",
         "use": L("CRM records and pipelines for freelance work.", "Anagrafiche e pipeline CRM per il lavoro da freelance.")},
        {"key": "databricks", "name": "Databricks SQL", "cat": "data", "url": "https://www.databricks.com",
         "use": L("Funnel, cohort and on-chain analysis to back marketing decisions.", "Analisi di funnel, coorti e dati on-chain a supporto delle decisioni di marketing.")},
        {"key": "sap", "name": "SAP", "cat": "data", "url": "https://www.sap.com",
         "use": L("Billing and customer profiles at Sabre, made 15% more efficient.", "Fatturazione e profili cliente in Sabre, resi più efficienti del 15%.")},
        {"key": "telegram", "name": "Telegram", "cat": "community", "url": "https://telegram.org",
         "use": L("A network of 15+ regional communities, and home to every bot on my Projects page.", "Una rete di oltre 15 community regionali, e la casa di tutti i bot della pagina Progetti.")},
        {"key": "discord", "name": "Discord", "cat": "community", "url": "https://discord.com",
         "use": L("Community management and automation for The OGz Club.", "Gestione e automazione della community di The OGz Club.")},
        {"key": "zealy", "name": "Zealy", "cat": "community", "url": "https://zealy.io",
         "use": L("Quest campaigns that lifted participation 40% for The OGz Club.", "Campagne a quest che hanno alzato la partecipazione del 40% per The OGz Club.")},
        {"key": "questn", "name": "QuestN", "cat": "community", "url": "https://questn.com",
         "use": L("More quest campaigns for The OGz Club, alongside Zealy.", "Altre campagne a quest per The OGz Club, insieme a Zealy.")},
        {"key": "intercom", "name": "Intercom", "cat": "community", "url": "https://www.intercom.com",
         "use": L("Support conversations turned into standard alerts for the team.", "Conversazioni di assistenza trasformate in avvisi standard per il team.")},
        {"key": "freshdesk", "name": "Freshdesk", "cat": "community", "url": "https://www.freshworks.com/freshdesk/",
         "use": L("Support tickets turned into stories developers can act on.", "Ticket di assistenza trasformati in schede su cui gli sviluppatori possono lavorare.")},
        {"key": "semrush", "name": "Semrush", "cat": "marketing", "url": "https://www.semrush.com",
         "use": L("Keyword research and SEO work that grew Affidaty's social visibility 50%.", "Ricerca di parole chiave e lavoro SEO che hanno fatto crescere del 50% la visibilità social di Affidaty.")},
        {"key": "googleads", "name": "Google Ads", "cat": "marketing", "url": "https://ads.google.com",
         "use": L("Paid campaigns that lifted lead generation 20% at Affidaty.", "Campagne a pagamento che hanno aumentato del 20% i lead per Affidaty.")},
        {"key": "notion", "name": "Notion", "cat": "marketing", "url": "https://www.notion.com",
         "use": L("The CRM deployment calendar, the crisis playbook and its templates.", "Il calendario delle campagne CRM, il playbook di crisi e i suoi modelli.")},
        {"key": "python", "name": "Python", "cat": "build", "url": "https://www.python.org",
         "use": L("Every bot and tool I publish, with tests and versioned releases.", "Tutti i bot e gli strumenti che pubblico, con test e release versionate.")},
        {"key": "github", "name": "GitHub", "cat": "build", "url": "https://github.com/anthonygozzini",
         "use": L("Code, releases and history for everything on this site.", "Codice, release e storico di tutto quello che trovi su questo sito.")},
        {"key": "claude", "name": "Claude", "cat": "build", "url": "https://claude.ai",
         "use": L("Agentic pipelines for localization, analysis and code, checked before anything ships.", "Pipeline di agenti per localizzazione, analisi e codice, controllate prima che esca qualsiasi cosa.")},
        {"key": "unity", "name": "Unity", "cat": "build", "url": "https://unity.com",
         "use": L("Sgamers, in 2018 and in its 2026 rebuild.", "Sgamers, nel 2018 e nella ricostruzione del 2026.")},
    ],
}

# The browser build of Sgamers: one English page around the Unity player, shared by both languages.
PLAY = {
    "path": "play/sgamers/",
    "project": "sgamers",
    "title": "Sgamers: play my first Unity game in your browser — Anthony Gozzini",
    "description": "Play Sgamers, the short 3D game I made in Unity in 2018 and rebuilt in 2026, right in your browser: arrow keys or A and D to move, Space to jump.",
    "play_label": "Play Sgamers",
    "created": "2018-11",
    "published": "2026-09-15",
}

# Labels used only in the markdown copies of the pages (index.md) and in llms.txt.
MD = {
    "pages": L("Pages", "Pagine"),
    "articles": L("Articles", "Articoli"),
    "tags": L("Tags", "Tag"),
    "links": L("Links", "Link"),
    "proof": L("Proof", "Esempio"),
    "short_bio": L("Bio", "Bio"),
    "long_bio": L("Long bio", "Bio lunga"),
    "html": L("Web page", "Pagina web"),
    "italian": "Italian versions",
    "optional": "Optional",
}

NOT_FOUND = {
    "title": L("Page not found", "Pagina non trovata"),
    "text": L("This page doesn't exist or has moved.", "Questa pagina non esiste o è stata spostata."),
    "home": L("Back to the home page", "Torna alla home"),
}

AREA = L("Remote for teams anywhere, in English or Italian. In person across the provinces of Varese, Novara and Verbano-Cusio-Ossola and in Milan.",
         "Da remoto per team di tutto il mondo, in italiano o in inglese. In presenza nelle province di Varese, Novara e Verbano-Cusio-Ossola e a Milano.")

SERVICES = {
    "title": L("Services", "Servizi"),
    "description": L(
        "CRM and lifecycle marketing, community management, Telegram bots and AI automation. Remote worldwide, in person around Varese, Novara and Milan.",
        "CRM e lifecycle marketing, community, bot Telegram e automazioni AI. Da remoto in tutto il mondo, in presenza tra Varese, Novara, VCO e Milano.",
    ),
    "intro": L(
        "What I do for companies and communities, and the work that shows it. I work remotely with teams anywhere, in English or Italian, and in person across the provinces of Varese, Novara and Verbano-Cusio-Ossola and in Milan.",
        "Cosa faccio per aziende e community, e il lavoro che lo dimostra. Lavoro da remoto con team di tutto il mondo, in italiano o in inglese, e in presenza nelle province di Varese, Novara e Verbano-Cusio-Ossola e a Milano.",
    ),
    "area_title": L("Where I work", "Dove lavoro"),
    "area": AREA,
    "what": L("What I do", "Cosa faccio"),
    "proof": L("Where I have done it", "Dove l'ho già fatto"),
    "all": L("All services", "Tutti i servizi"),
    "others": L("Other services", "Altri servizi"),
    "faq": L("Common questions", "Domande frequenti"),
    # For the structured data: the areas served in person, with their Wikidata entries, and the remote work.
    "areas_served": [
        {"name": L("Province of Varese", "Provincia di Varese"), "wikidata": "Q16299"},
        {"name": L("Province of Novara", "Provincia di Novara"), "wikidata": "Q16216"},
        {"name": L("Province of Verbano-Cusio-Ossola", "Provincia del Verbano-Cusio-Ossola"), "wikidata": "Q16312"},
        {"name": L("Metropolitan City of Milan", "Città metropolitana di Milano"), "wikidata": "Q18288155"},
    ],
    "remote": L("Worldwide, remotely", "In tutto il mondo, da remoto"),
    "items": [
        {"slug": "crm-lifecycle", "icon": "briefcase",
         "name": L("CRM & lifecycle marketing", "CRM e lifecycle marketing"),
         "title": L("CRM & lifecycle marketing consultant", "Consulente CRM e lifecycle marketing"),
         "description": L(
             "CRM and lifecycle programs from segments to KPIs: activation, cross-sell and retention, as I built them for Trust Wallet. Remote or around Milan.",
             "Programmi CRM e lifecycle dai segmenti ai KPI: attivazione, cross-sell e retention, come per Trust Wallet. Da remoto o tra Varese, Novara, VCO e Milano."),
         "summary": L("From an empty CRM to a plan your team can run: segments, triggers, messages and KPIs.",
                      "Da un CRM vuoto a un piano che il team può seguire: segmenti, trigger, messaggi e KPI."),
         "what": L([
             "A lifecycle strategy on three pillars, new-user activation, cross-sell and retention, each with its own segments, triggers, messages and KPIs.",
             "Funnel analysis that finds where people drop out, turned into segments you can reach, in Amplitude and Databricks SQL.",
             "A deployment calendar that stops campaigns from colliding, and templates the next person can reuse.",
             "Clean, well-structured customer data in Salesforce or HubSpot.",
         ], [
             "Una strategia lifecycle su tre pilastri, attivazione dei nuovi utenti, cross-sell e retention, ognuno con i suoi segmenti, trigger, messaggi e KPI.",
             "Analisi dei funnel per capire dove le persone si perdono, trasformata in segmenti da raggiungere, con Amplitude e Databricks SQL.",
             "Un calendario delle campagne che evita sovrapposizioni, e modelli che la prossima persona può riusare.",
             "Dati cliente puliti e ben strutturati in Salesforce o HubSpot.",
         ]),
         "faq": [
             {"q": L("Do you work remotely?", "Lavori da remoto?"),
              "a": L("Yes. I work remotely with teams anywhere, in English or Italian, and in person across the provinces of Varese, Novara and Verbano-Cusio-Ossola and in Milan.",
                     "Sì. Lavoro da remoto con team di tutto il mondo, in italiano o in inglese, e in presenza nelle province di Varese, Novara e Verbano-Cusio-Ossola e a Milano.")},
             {"q": L("Where do you start?", "Da dove si parte?"),
              "a": L("From what you already have. I look at the data, the tools and where people drop out, then write the plan: segments, triggers, messages and the KPI for each one.",
                     "Da quello che hai già. Guardo i dati, gli strumenti e i punti in cui le persone si perdono, poi scrivo il piano: segmenti, trigger, messaggi e il KPI di ognuno.")},
             {"q": L("Which tools do you work with?", "Con quali strumenti lavori?"),
              "a": L("Salesforce and HubSpot for customer data, Amplitude and Databricks SQL for funnels and segments. If you use something else, I learn it: the method doesn't change.",
                     "Salesforce e HubSpot per i dati dei clienti, Amplitude e Databricks SQL per funnel e segmenti. Se usi altro lo imparo: il metodo non cambia.")},
         ],
         "proof": [
             {"text": L("Trust Wallet, 2025–2026: I ran CRM and lifecycle for a self-custodial wallet with millions of users.",
                        "Trust Wallet, 2025–2026: ho gestito CRM e lifecycle di un wallet self-custodial con milioni di utenti."),
              "href": "about/#career"},
             {"text": L("Motorola Solutions: cleaner Salesforce data lifted lead conversion by 14% and data accuracy by 28%.",
                        "Motorola Solutions: dati Salesforce più puliti hanno alzato la conversione dei lead del 14% e l'accuratezza dei dati del 28%."),
              "href": "about/#career"},
         ]},
        {"slug": "community", "icon": "users",
         "name": L("Community management", "Gestione community"),
         "title": L("Telegram & Discord community manager", "Community manager Telegram e Discord"),
         "description": L(
             "Telegram and Discord communities that stay useful as they grow: moderation, ambassadors, anti-scam automation. Seven years at Trust Wallet.",
             "Community Telegram e Discord che restano utili mentre crescono: moderazione, ambassador, automazioni anti-truffa. Sette anni in Trust Wallet."),
         "summary": L("Telegram and Discord communities that stay useful as they grow, with moderation, ambassadors and anti-scam automation.",
                      "Community Telegram e Discord che restano utili mentre crescono, con moderazione, ambassador e automazioni anti-truffa."),
         "what": L([
             "Moderation rules, an admin team and a playbook for when things go wrong.",
             "Ambassador programs: recruiting, coordinating and keeping volunteers motivated.",
             "Anti-scam automation and screening for private groups.",
             "Quest campaigns on Zealy and QuestN that bring members back.",
         ], [
             "Regole di moderazione, un team di admin e un playbook per quando le cose vanno storte.",
             "Programmi ambassador: selezione, coordinamento e volontari che restano motivati.",
             "Automazioni anti-truffa e filtri per i gruppi privati.",
             "Campagne a quest su Zealy e QuestN che fanno tornare i membri.",
         ]),
         "faq": [
             {"q": L("Which platforms do you manage?", "Quali piattaforme gestisci?"),
              "a": L("Telegram and Discord. I ran Trust Wallet's global Telegram community for seven years and a network of more than fifteen regional communities.",
                     "Telegram e Discord. Ho gestito per sette anni la community Telegram globale di Trust Wallet e una rete di oltre quindici community regionali.")},
             {"q": L("Do you moderate every day, or set it up for my team?", "Moderi tutti i giorni o prepari il sistema per il mio team?"),
              "a": L("Either. I can run moderation myself, or set up the rules, the admin team and the playbook and hand them over to your people.",
                     "Tutte e due. Posso moderare io, oppure preparare regole, team di admin e playbook e passarli alle tue persone.")},
             {"q": L("How do you deal with scams?", "Come si tengono fuori le truffe?"),
              "a": L("With screening before anyone joins a private group, automation that removes the usual impostors, and a written playbook for the day something goes wrong.",
                     "Con un filtro prima che qualcuno entri nei gruppi privati, automazioni che tolgono di mezzo gli impostori soliti, e un playbook scritto per il giorno in cui qualcosa va storto.")},
         ],
         "proof": [
             {"text": L("Seven years as an admin of Trust Wallet's global Telegram community, coordinating thirty volunteer ambassadors.",
                        "Sette anni da admin della community Telegram globale di Trust Wallet, coordinando trenta ambassador volontari."),
              "href": "about/#career"},
             {"text": L("A network of more than fifteen regional Telegram communities for Trust Wallet.",
                        "Una rete di oltre quindici community Telegram regionali per Trust Wallet."),
              "href": "about/#career"},
             {"text": L("Quest campaigns that lifted participation by 40% for The OGz Club.",
                        "Campagne a quest che hanno alzato la partecipazione del 40% per The OGz Club."),
              "href": "tools/"},
         ]},
        {"slug": "telegram-bots", "icon": "bot",
         "name": L("Custom Telegram bots", "Bot Telegram su misura"),
         "title": L("Custom Telegram bot developer", "Sviluppo di bot Telegram su misura"),
         "description": L(
             "Telegram bots that screen new members, run referral programs or mirror channels, with tests and versioned releases. Built for paying clients.",
             "Bot Telegram che filtrano chi entra, gestiscono programmi referral o copiano canali, con test e release versionate. Nati per clienti paganti."),
         "summary": L("Bots that screen new members, run referral programs or mirror channels, tested and released with versions.",
                      "Bot che filtrano chi entra, gestiscono programmi referral o copiano canali, con test e release versionate."),
         "what": L([
             "Screening questionnaires and fake-account checks before anyone joins a private group.",
             "Referral programs with personal links, points and a leaderboard.",
             "Channel mirroring and scheduled posts across several channels.",
             "Tests, versioned releases and one config file you can edit without touching the code.",
         ], [
             "Questionari di ingresso e controlli sugli account falsi prima che qualcuno entri in un gruppo privato.",
             "Programmi referral con link personali, punti e classifica.",
             "Copia dei post tra canali e invii programmati su più canali.",
             "Test, release versionate e un solo file di configurazione da modificare senza toccare il codice.",
         ]),
         "faq": [
             {"q": L("How long does a bot take?", "In quanto tempo è pronto un bot?"),
              "a": L("It depends on what it has to do. I start from a working minimum version you can try, then add the rest: you see something running early, not at the end.",
                     "Dipende da cosa deve fare. Parto da una versione minima funzionante che puoi già provare, poi aggiungo il resto: vedi qualcosa girare subito, non alla fine.")},
             {"q": L("Is the code mine?", "Il codice è mio?"),
              "a": L("Yes. You get the code, the tests and one configuration file you can change without touching the code, and you can run it wherever you want.",
                     "Sì. Ricevi il codice, i test e un solo file di configurazione da modificare senza toccare il codice, e puoi farlo girare dove vuoi.")},
             {"q": L("Where does the bot run?", "Dove gira il bot?"),
              "a": L("On your own server or on a hosting service. My bots are plain Python and need no database unless the job asks for one.",
                     "Su un tuo server o su un servizio di hosting. I miei bot sono in Python semplice e non hanno bisogno di un database, a meno che il lavoro non lo richieda.")},
         ],
         "proof": [
             {"text": L("Telegram Gatekeeper Bot: screening for private groups, 40 tests, version 3.0.0.",
                        "Telegram Gatekeeper Bot: filtro per i gruppi privati, 40 test, versione 3.0.0."),
              "href": "projects/#gatekeeper"},
             {"text": L("Telegram Referral System: built for a crypto creator's community.",
                        "Telegram Referral System: costruito per la community di un creator crypto."),
              "href": "projects/#referral"},
             {"text": L("Telegram Channel Message Copier: ran for a client posting to six channels.",
                        "Telegram Channel Message Copier: ha lavorato per un cliente che pubblicava su sei canali."),
              "href": "projects/#copier"},
         ]},
        {"slug": "ai-automation", "icon": "code",
         "name": L("AI automation for marketing", "Automazioni AI per il marketing"),
         "title": L("AI automation for marketing teams", "Automazioni con AI per il marketing"),
         "description": L(
             "AI pipelines that take the volume out of localization, reporting and content, with the verification step that makes their output safe to use.",
             "Pipeline di AI che tolgono il lavoro ripetitivo da localizzazione, report e contenuti, con la verifica che rende il risultato sicuro da usare."),
         "summary": L("Pipelines that take the volume out of localization, reporting and content, checked before anything ships.",
                      "Pipeline che tolgono il lavoro ripetitivo da localizzazione, report e contenuti, controllate prima che esca qualsiasi cosa."),
         "what": L([
             "Localization pipelines that keep technical terms intact and respect each channel's character limits.",
             "Analysis and reporting pipelines with a verification step, so numbers are checked before anyone sees them.",
             "Tools that turn long sources, such as a whole YouTube channel, into searchable text.",
             "Agent workflows for code and content, where nothing ships until it has been checked.",
         ], [
             "Pipeline di localizzazione che non stravolgono i termini tecnici e rispettano i limiti di caratteri di ogni canale.",
             "Pipeline di analisi e report con un passaggio di verifica, così i numeri sono controllati prima che qualcuno li veda.",
             "Strumenti che trasformano fonti lunghe, come un intero canale YouTube, in testo da cercare.",
             "Flussi con agenti AI per codice e contenuti, dove niente esce finché non è stato controllato.",
         ]),
         "faq": [
             {"q": L("Doesn't AI make things up?", "L'AI non si inventa le cose?"),
              "a": L("It can, which is why every pipeline I build ends with a verification step: numbers are checked against the source and nothing ships before it passes.",
                     "Può farlo, ed è il motivo per cui ogni flusso che costruisco finisce con una verifica: i numeri si controllano sulla fonte e niente esce prima di passarla.")},
             {"q": L("What is it actually good for?", "Su cosa conviene davvero usarla?"),
              "a": L("Work that is repetitive and has a right answer: localization, reports, drafts, turning long sources into searchable text. Not decisions.",
                     "Il lavoro ripetitivo che ha una risposta giusta: localizzazione, report, bozze, fonti lunghe da trasformare in testo consultabile. Non le decisioni.")},
             {"q": L("Do I need to pay for an AI subscription?", "Serve pagare un abbonamento AI?"),
              "a": L("Usually one, and I tell you which one fits your case and roughly what it will consume before we start.",
                     "Di solito uno, e prima di partire ti dico quale conviene per il tuo caso e più o meno quanto consuma.")},
         ],
         "proof": [
             {"text": L("channel-miner turned 377 hours of video, across 179 episodes, into 237 MB of searchable text.",
                        "channel-miner ha trasformato 377 ore di video, in 179 puntate, in 237 MB di testo da cercare."),
              "href": "projects/#channel-miner"},
             {"text": L("GuardBot includes an MCP server, so AI agents can use it as a tool.",
                        "GuardBot include un server MCP, così anche gli agenti AI possono usarlo come strumento."),
              "href": "projects/#guardbot"},
             {"text": L("How an AI agent and I rebuilt a game from its only surviving build, checking every step.",
                        "Come io e un agente AI abbiamo ricostruito un gioco dall'unica build rimasta, controllando ogni passaggio."),
              "href": "writing/rebuilding-sgamers/"},
         ]},
        {"slug": "multilingual-campaigns", "icon": "send",
         "name": L("Multilingual campaigns", "Campagne multilingua"),
         "title": L("Multilingual campaign operations", "Campagne e localizzazione multilingua"),
         "description": L(
             "Localization workflows, push notifications and in-app banners across languages, with targeting and QA before launch. Ten languages at Trust Wallet.",
             "Localizzazione, notifiche push e banner in app in più lingue, con targeting e controlli prima del lancio. Dieci lingue in Trust Wallet."),
         "summary": L("Localization workflows and campaign setup across languages, with targeting and QA before launch.",
                      "Flussi di localizzazione e campagne in più lingue, con targeting e controlli prima del lancio."),
         "what": L([
             "Localization workflows with a review step, up to ten languages.",
             "Push notifications and in-app banners configured with targeting.",
             "QA before launch and a launch calendar the whole team can follow.",
             "Copy written directly in English and Italian.",
         ], [
             "Flussi di localizzazione con un passaggio di revisione, fino a dieci lingue.",
             "Notifiche push e banner in app configurati con targeting.",
             "Controlli prima del lancio e un calendario che tutto il team può seguire.",
             "Testi scritti direttamente in italiano e in inglese.",
         ]),
         "faq": [
             {"q": L("How many languages can you cover?", "Quante lingue si possono coprire?"),
              "a": L("Up to ten with a review step, as at Trust Wallet. I write English and Italian myself; the rest go through a reviewer.",
                     "Fino a dieci con un passaggio di revisione, come in Trust Wallet. Italiano e inglese li scrivo io, le altre passano da un revisore.")},
             {"q": L("Do you use machine translation?", "Usi la traduzione automatica?"),
              "a": L("As a starting point, never as the final text. Technical terms follow a glossary, and every language gets read by a person before launch.",
                     "Come punto di partenza, mai come testo finale. I termini tecnici seguono un glossario, e ogni lingua viene letta da una persona prima del lancio.")},
             {"q": L("What happens before launch?", "Cosa si controlla prima del lancio?"),
              "a": L("Targeting, character limits for each surface, links, and the calendar: campaigns that collide with each other are the most common avoidable mistake.",
                     "Il targeting, i limiti di caratteri di ogni canale, i link e il calendario: le campagne che si accavallano sono l'errore evitabile più comune.")},
         ],
         "proof": [
             {"text": L("Trust Wallet: announcements in 10 languages and push in 8, for launches such as Cash App Pay and Banxa.",
                        "Trust Wallet: annunci in 10 lingue e push in 8, per lanci come Cash App Pay e Banxa."),
              "href": "about/#career"},
             {"text": L("A weekly crypto market column in English and Italian for Affidaty, in 2024.",
                        "Una rubrica settimanale sul mercato crypto in italiano e in inglese per Affidaty, nel 2024."),
              "href": "writing/"},
         ]},
    ],
}


CONTACT = {
    "title": L("Contact", "Contattami"),
    "description": L(
        "Looking for my next role in CRM, lifecycle or community marketing, remote or around Varese and Milan. Book a call or write to me by email or Telegram.",
        "Cerco un nuovo ruolo in CRM, lifecycle o community marketing, da remoto o tra Varese, Novara, VCO e Milano. Prenota una call o scrivimi: email, Telegram.",
    ),
    "intro": L(
        "I'm looking for my next role in CRM, lifecycle or community marketing, full-time or fractional, remote or in person around Varese, Novara, Verbano-Cusio-Ossola and Milan, in English or Italian. The quickest way to talk is a 30-minute call.",
        "Cerco il mio prossimo ruolo in CRM, lifecycle o community marketing, full-time o part-time, da remoto o in presenza tra Varese, Novara, Verbano-Cusio-Ossola e Milano, in italiano o in inglese. Il modo più veloce per parlarne è una call di 30 minuti.",
    ),
    "cta_call": L("Book a 30-minute call", "Prenota una call di 30 minuti"),
    "cta_email": L("Send an email", "Scrivimi una email"),
    "channels": L("Other ways to reach me", "Altri modi per contattarmi"),
    "cv": L("CV", "CV"),
    "cv_text": L("One page, PDF", "Una pagina, PDF"),
    "whatsapp_text": L("Chat with me", "Scrivimi in chat"),
    "review_title": L("Worked with me?", "Hai lavorato con me?"),
    "review_text": L("A short review on Google helps other people find me.", "Una breve recensione su Google aiuta altre persone a trovarmi."),
    "review_cta": L("Leave me a Google review", "Lasciami una recensione su Google"),
    "help": L("What I can help with", "In cosa posso aiutarti"),
    "offers": [
        {"service": "crm-lifecycle", "title": L("CRM & lifecycle programs", "Programmi CRM e lifecycle"),
         "text": L("From an empty CRM to a plan the team can run: segment definitions, trigger → surface → message → KPI tables for activation, cross-sell and retention, and a deployment calendar that stops campaigns from colliding.",
                   "Da un CRM vuoto a un piano che il team può seguire: definizione dei segmenti, tabelle trigger → canale → messaggio → KPI per attivazione, cross-sell e retention, e un calendario delle campagne che evita sovrapposizioni."),
         "proof": L("I wrote this strategy for Trust Wallet in 2025.", "Ho scritto questa strategia per Trust Wallet nel 2025.")},
        {"service": "multilingual-campaigns", "title": L("Multilingual campaign operations", "Campagne in più lingue"),
         "text": L("Localization workflows that keep crypto terms intact and respect every surface's character limits, plus banner and push configuration with targeting and QA before launch.",
                   "Flussi di localizzazione che non stravolgono i termini crypto e rispettano i limiti di caratteri di ogni canale, più configurazione di banner e notifiche push con targeting e controlli prima del lancio."),
         "proof": L("Announcements in 10 languages and push in 8, for launches such as Cash App Pay and Banxa.", "Annunci in 10 lingue e push in 8, per lanci come Cash App Pay e Banxa.")},
        {"service": "community", "title": L("Crypto community operations", "Gestione di community crypto"),
         "text": L("Telegram and Discord communities that stay useful as they grow: moderation, ambassador programs, anti-scam automation, screening for private groups and a playbook for when things go wrong.",
                   "Community Telegram e Discord che restano utili mentre crescono: moderazione, programmi ambassador, automazioni anti-truffa, filtri per i gruppi privati e un playbook per quando le cose vanno storte."),
         "proof": L("Seven years as an admin of Trust Wallet's global Telegram community.", "Sette anni da admin della community Telegram globale di Trust Wallet.")},
        {"service": "ai-automation", "title": L("AI in marketing operations", "AI nelle operazioni di marketing"),
         "text": L("Pipelines that take the volume out of localization, reporting and content, with the verification step that makes their output safe to use.",
                   "Pipeline che tolgono il lavoro ripetitivo da localizzazione, report e contenuti, con il passaggio di verifica che rende il risultato sicuro da usare."),
         "proof": L("The tools on my Projects page were built this way.", "Gli strumenti della pagina Progetti sono costruiti così.")},
    ],
}
