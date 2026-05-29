import streamlit as st
from PIL import Image
import random
from colorsys import rgb_to_hsv

st.set_page_config(page_title="Generatore di Prompt Musicali - Loop507", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Space Mono', monospace; background-color: #0a0a0a; color: #e8e8e0; }
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3 { font-family: 'Syne', sans-serif; }
    .prompt-block { background: #111; border: 1px solid #2a2a2a; border-left: 3px solid #c8ff00; padding: 1.5rem; margin: 1rem 0; font-family: 'Space Mono', monospace; font-size: 0.78rem; line-height: 1.8; white-space: pre-wrap; color: #e8e8e0; }
    .section-header { color: #c8ff00; font-family: 'Syne', sans-serif; font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.3rem; }
    .tag-chip { display: inline-block; background: #1a1a1a; border: 1px solid #333; color: #c8ff00; padding: 2px 10px; margin: 3px; font-size: 0.75rem; font-family: 'Space Mono', monospace; }
    .stButton > button { background: #c8ff00; color: #0a0a0a; border: none; font-family: 'Syne', sans-serif; font-weight: 700; letter-spacing: 0.05em; padding: 0.5rem 1.5rem; }
    .stButton > button:hover { background: #dfff4f; color: #0a0a0a; }
    .profile-pill { display: inline-block; background: #c8ff00; color: #0a0a0a; padding: 3px 12px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 0.7rem; letter-spacing: 0.15em; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 15 PROFILI x 3 VARIANTI = 45 COMBINAZIONI UNICHE
# ═══════════════════════════════════════════════════════

PROFILES = {
    "urban_night": {
        "title_adj": ["Notti", "Pulse", "Frequenze", "Riflessi", "Circuito", "Asfalto"],
        "genre": "Electronic / IDM / Glitch",
        "bpm_range": (88, 122),
        "keywords": ["night", "dark", "city", "street", "neon", "rain", "urban", "building", "road", "lamp"],
        "variants": [
            {"style": "Elettronica urbana con ritmiche glitch e basso sub pulsante", "instruments": ["sintetizzatori modulari", "beat glitch", "basso sub", "pad atmosferici"], "mood": "alienato, notturno, ipnotico", "structure_note": "Struttura ciclica e ipnotica. Tensione continua senza risoluzione netta.", "ai_parts": ["slow IDM", "glitch drum beat", "deep sub bass", "modular synth", "urban nocturnal", "hypnotic loop", "filtered pad"], "sections": {"intro": "Rumore urbano filtrato, kick singolo ogni due battute", "strofa": "Beat glitch rarefatto con basso sub in sottofondo", "pre_rit": "Apertura del filtro, sintetizzatori emergenti", "ritornello": "Densita elettronica piena, modulare in primo piano", "bridge": "Breakdown minimale, solo texture urbane", "outro": "Fade out con eco lontano e rumore di pioggia"}, "analysis": "La palette urbana notturna guida verso timbri metallici e freddi. Il basso sub crea radicamento fisico mentre il glitch destabilizza.", "uso": "Scene di solitudine metropolitana, night drive, alienazione urbana", "tags": ["#GlitchElectronic", "#UrbanNight", "#IDM", "#SubBass", "#Hypnotic"]},
            {"style": "Techno minimale con microritmi e pad nebbiosi", "instruments": ["drum machine 909", "pad lunghi nebbiosi", "arpeggiatore lento", "effetti metallici"], "mood": "freddo, geometrico, immersivo", "structure_note": "Struttura a loop progressivo. Ogni sezione aggiunge o rimuove un elemento.", "ai_parts": ["minimal techno", "909 drums", "long atmospheric pad", "slow arpeggio", "metallic fx", "cold and precise", "loop-based progressive"], "sections": {"intro": "Hi-hat secco e singolo pad lungo, nessun basso ancora", "strofa": "Kick 909, pad nebbiosi, arpeggiatore in lontananza", "pre_rit": "Aggiunta del basso, filtro in apertura graduale", "ritornello": "Tutti gli elementi, massima pulizia geometrica", "bridge": "Solo hi-hat e pad, azzeramento ritmico", "outro": "Elementi che scompaiono uno ad uno fino al silenzio"}, "analysis": "Il minimalismo freddo riflette la geometria urbana notturna. Ogni elemento sonoro e essenziale e non decorativo.", "uso": "Club ambience, scene notturne astratte, architettura sonora", "tags": ["#MinimalTechno", "#909Drums", "#ColdElectronic", "#LoopBased", "#Geometric"]},
            {"style": "Drum and bass lento con jazz samples e distorsione analogica", "instruments": ["break beat rallentato", "contrabbasso jazzato", "pianoforte campionato", "rumore analogico"], "mood": "torbido, notturno, noir", "structure_note": "Struttura jazz-pop reinterpretata in chiave downtempo. Swing distorto e rotto.", "ai_parts": ["slow drum and bass", "jazz piano sample", "upright bass", "analog distortion", "nocturnal noir", "broken swing", "lo-fi texture"], "sections": {"intro": "Campione jazz filtrato, crackle di vinile", "strofa": "Breakbeat lento, contrabbasso pulsante", "pre_rit": "Piano jazzato che emerge, tensione armonica", "ritornello": "Tutto insieme in un groove torbido e sincopato", "bridge": "Solo contrabbasso e rumore, nessun ritmo", "outro": "Il campione jazz che sfuma nel silenzio notturno"}, "analysis": "L'ibridazione jazz-elettronica crea un senso di familiarita distorta. Il noir sonoro rispecchia la palette visiva urbana.", "uso": "Scene noir, detective story, bar notturni, flashback urbani", "tags": ["#NocturnalJazz", "#SlowDnB", "#UrbanNoir", "#LoFiJazz", "#BrokenGroove"]},
        ]
    },
    "nature_calm": {
        "title_adj": ["Respiro", "Radici", "Acqua", "Foresta", "Terra", "Foglie"],
        "genre": "Ambient / Nature / Folk",
        "bpm_range": (48, 72),
        "keywords": ["forest", "tree", "grass", "field", "river", "lake", "mountain", "beach", "flower", "garden", "leaf", "nature", "green", "wood"],
        "variants": [
            {"style": "Ambient organico con field recordings e chitarra acustica fingerpicking", "instruments": ["chitarra acustica fingerpicking", "field recordings", "flauto minimale", "pad di archi leggeri"], "mood": "sereno, contemplativo, radicato", "structure_note": "Struttura aperta e respirante. Nessun climax forzato, crescita organica naturale.", "ai_parts": ["acoustic guitar fingerpicking", "field recordings", "forest ambience", "minimal flute", "slow ambient", "natural reverb", "meditative", "organic"], "sections": {"intro": "Field recordings puri, vento tra le foglie", "strofa": "Chitarra in fingerpicking con riverbero naturale", "pre_rit": "Flauto che si inserisce delicatamente", "ritornello": "Sovrapposizione di chitarra, flauto e natura", "bridge": "Solo field recording, nessuno strumento", "outro": "Chitarra che sfuma nei suoni naturali"}, "analysis": "L'ambiente naturale guida verso timbri organici e non processati. La chitarra in fingerpicking mima il ritmo naturale.", "uso": "Scene di natura, meditazione, introspezione, trekking", "tags": ["#NatureAmbient", "#AcousticGuitar", "#FieldRecording", "#Meditative", "#Organic"]},
            {"style": "Folk minimalista con dulcimer e percussioni tribali leggere", "instruments": ["dulcimer", "percussioni tribali leggere", "voce campionata lontana", "archi frullati"], "mood": "antico, rituale, mistico", "structure_note": "Struttura rituale e ciclica. Ogni ripetizione e una trasformazione.", "ai_parts": ["dulcimer", "light tribal percussion", "distant sampled voice", "flutter strings", "ancient folk", "ritual", "mystical", "cyclic"], "sections": {"intro": "Dulcimer solo, melodia antica", "strofa": "Percussioni tribali leggere, dulcimer continua", "pre_rit": "Voce campionata lontana emerge", "ritornello": "Tutti gli elementi in rituale sonoro", "bridge": "Solo voce campionata, quasi inudibile", "outro": "Dulcimer che rallenta fino a note singole isolate"}, "analysis": "Il folk minimalista evoca radici culturali ancestrali. Il dulcimer porta una qualita di tempo sospeso.", "uso": "Documentari etnografici, spiritualita, rituali, natura selvaggia", "tags": ["#FolkMinimal", "#Dulcimer", "#TribalPercussion", "#Ancient", "#Ritual"]},
            {"style": "Drone ambient con armoniche naturali e canto degli uccelli", "instruments": ["drone di corde", "armoniche naturali", "canto degli uccelli registrato", "campane tibetane"], "mood": "immobile, eterno, vasto", "structure_note": "Nessuna struttura tradizionale. Il suono esiste senza inizio ne fine.", "ai_parts": ["natural drone", "string harmonics", "bird song recordings", "Tibetan bowls", "vast", "eternal", "still", "no rhythm"], "sections": {"intro": "Silenzio, poi drone emerge lentissimamente", "strofa": "Drone pieno, uccelli in distanza", "pre_rit": "Campane tibetane, armoniche che si moltiplicano", "ritornello": "Massima apertura sonora e spaziale", "bridge": "Solo campane e silenzio", "outro": "Drone che scompare nel nulla"}, "analysis": "Il drone ambient naturale dissolve il tempo. La vastita sonora riflette la vastita visiva del paesaggio.", "uso": "Meditazione profonda, yoga, paesaggi naturali vasti, alba", "tags": ["#DroneAmbient", "#NaturalHarmonics", "#TibetanBowls", "#Vast", "#Timeless"]},
        ]
    },
    "melancholy": {
        "title_adj": ["Frammenti", "Memoria", "Cenere", "Distanza", "Eco", "Ombra"],
        "genre": "Downtempo / Experimental / Cinematic",
        "bpm_range": (52, 72),
        "keywords": ["alone", "person", "window", "room", "chair", "empty", "still", "old", "abandoned", "fog", "grey"],
        "variants": [
            {"style": "Downtempo malinconico con pianoforte riverberato e saturazione nastro", "instruments": ["pianoforte feltrato", "archi da camera", "sine wave synth lontano", "rumori di vinile"], "mood": "malinconico, nostalgico, introspettivo", "structure_note": "Struttura Pop dilatata e svuotata. Familiarita emotiva con arrangiamenti minimali.", "ai_parts": ["felt piano", "tape saturation", "vinyl crackle", "melancholic", "slow downtempo", "chamber strings", "introspective", "vast cinematic space"], "sections": {"intro": "Rumore di vinile, accordi lenti di pianoforte filtrato", "strofa": "Piano isolato con leggeri archi, massimo spazio", "pre_rit": "Apertura degli archi, crescita dinamica lenta", "ritornello": "Armonia completa, sine wave in lontananza", "bridge": "Sospensione ritmica, solo droni e rumore bianco", "outro": "Nastro magnetico che rallenta fino a fermarsi"}, "analysis": "La saturazione del nastro e i rumori di vinile trasformano la malinconia in oggetto fisico. Il pianoforte feltrato abbraccia l'intimita.", "uso": "Flashback cinematografici, momenti di rivelazione emotiva, perdita", "tags": ["#MelancholicPiano", "#Downtempo", "#TapeSaturation", "#Introspective", "#CinematicAmbient"]},
            {"style": "Post-rock strumentale con chitarra pulita e costruzione lenta", "instruments": ["chitarra elettrica pulita con riverbero", "basso profondo", "batteria spazzolata", "violino solista"], "mood": "nostalgico, epico nei silenzi, fragile", "structure_note": "Struttura post-rock classica: piccolo poi grande poi dissoluzione. L'emozione arriva in ritardo.", "ai_parts": ["post-rock", "clean electric guitar", "reverb guitar", "slow build", "brushed drums", "solo violin", "nostalgic", "cinematic build-up"], "sections": {"intro": "Chitarra pulita sola, melodia fragile", "strofa": "Basso entra, batteria spazzolata leggera", "pre_rit": "Violino che emerge, tensione crescente", "ritornello": "Tutto insieme, costruzione epica", "bridge": "Dissoluzione improvvisa, solo chitarra e violino", "outro": "Ritorno al tema iniziale, ancora piu fragile"}, "analysis": "Il post-rock usa la struttura della canzone pop per costruire emozioni cinematografiche senza parole. Il violino porta umanita al muro elettrico.", "uso": "Documentari, finali emotivi, time-lapse, paesaggi urbani grigi", "tags": ["#PostRock", "#CleanGuitar", "#SlowBuild", "#Cinematic", "#EpicFragile"]},
            {"style": "Ambient minimale con note di pianoforte isolate e silenzio come elemento", "instruments": ["pianoforte preparato", "silenzio come elemento compositivo", "risonanza di stanza", "micro-suoni"], "mood": "vuoto, presente, sospeso nel tempo", "structure_note": "Il silenzio e parte della composizione. Le pause sono lunghe quanto le note.", "ai_parts": ["prepared piano", "minimal isolated notes", "silence as composition", "room resonance", "micro sounds", "suspended", "timeless", "empty"], "sections": {"intro": "Silenzio. Una nota sola dopo 8 secondi", "strofa": "Note isolate, lunghe pause tra ognuna", "pre_rit": "Le pause si accorciano leggermente", "ritornello": "Tre note insieme, massima densita di questo brano", "bridge": "Silenzio assoluto per 16 battute", "outro": "Un'ultima nota, poi il silenzio definitivo"}, "analysis": "Il minimalismo estremo usa il silenzio come elemento compositivo attivo. Ogni nota e evento raro e prezioso.", "uso": "Installazioni d'arte, teatro sperimentale, contemplazione, lutto", "tags": ["#PreparedPiano", "#Minimalism", "#SilenceAsMusic", "#Suspended", "#ContemporaryClassical"]},
        ]
    },
    "energetic": {
        "title_adj": ["Impatto", "Forza", "Collisione", "Adrenalina", "Tensione", "Esplosione"],
        "genre": "Electronic / Industrial / Techno",
        "bpm_range": (122, 150),
        "keywords": ["fire", "crowd", "sport", "run", "fast", "bright", "explosion", "energy", "power", "fight"],
        "variants": [
            {"style": "Techno industriale con percussioni potenti e synth taglienti", "instruments": ["drum machine industriale", "synth lead tagliente", "basso distorto", "effetti metallici industriali"], "mood": "aggressivo, potente, inesorabile", "structure_note": "Struttura a build continuo. Tensione crescente con drop esplosivo senza rilascio.", "ai_parts": ["industrial techno", "aggressive drums", "distorted bass", "sharp synth lead", "high energy", "driving rhythm", "intense", "relentless"], "sections": {"intro": "Rumore industriale, kick singolo che accelera", "strofa": "Beat pieno con synth lead affilato", "pre_rit": "Build up percussivo, filtro in apertura totale", "ritornello": "Drop pieno, massima densita energetica", "bridge": "Breakdown industriale, solo effetti metallici", "outro": "Decelerazione progressiva, metallo che raffredda"}, "analysis": "L'industrial techno usa la macchina come strumento espressivo. L'aggressivita e forma, non contenuto.", "uso": "Scene d'azione, sport estremo, tensione narrativa, fight scenes", "tags": ["#Industrial", "#Techno", "#HighEnergy", "#AggressiveElectronic", "#Drop"]},
            {"style": "Drum and bass neurofunk con bassi evolutivi e breaks complessi", "instruments": ["breaks complessi", "basso neurofunk modulare", "synth glitch", "sub bass profondo"], "mood": "teso, tecnico, futuristico", "structure_note": "Struttura neurofunk: complessita ritmica massima, basso come melodia.", "ai_parts": ["neurofunk drum and bass", "complex breaks", "modular neuro bass", "glitch synth", "deep sub bass", "tense", "technical", "futuristic"], "sections": {"intro": "Sub bass solo, beat che costruisce", "strofa": "Breaks complessi, basso neurofunk pulsante", "pre_rit": "Accelerazione dei breaks, basso piu aggressivo", "ritornello": "Massima complessita ritmica e basso dominante", "bridge": "Half-time breakdown, solo sub bass", "outro": "Breaks che si frammentano, dissoluzione"}, "analysis": "Il neurofunk porta la complessita algoritmica nella danza. Il basso modulare e la voce di una macchina che pensa.", "uso": "Gaming, sci-fi, chase scenes, tecnologia avanzata", "tags": ["#Neurofunk", "#DnB", "#NeuroBase", "#ComplexBreaks", "#Futuristic"]},
            {"style": "Big beat con influenze punk e attitude ribelle", "instruments": ["big beat drums pesanti", "chitarra distorta punk", "sample rock", "basso aggressivo"], "mood": "ribelle, diretto, senza compromessi", "structure_note": "Struttura punk-elettronica. Diretta, breve, senza fronzoli.", "ai_parts": ["big beat", "punk influence", "distorted guitar", "rock sample", "aggressive bass", "rebellious", "direct", "no compromise", "raw energy"], "sections": {"intro": "Sample rock, poi drums che esplodono", "strofa": "Big beat pieno, chitarra punk in sottofondo", "pre_rit": "Chitarra distorta che sale", "ritornello": "Tutto insieme, energia massima senza filtri", "bridge": "Solo drum break, nient'altro", "outro": "Hard stop, fine brutale"}, "analysis": "Il big beat punk porta l'estetica del DIY nella produzione elettronica. L'energia grezza e la qualita, non il difetto.", "uso": "Skateboarding, extreme sports, ribellione, pubblicita energetiche", "tags": ["#BigBeat", "#PunkElectronic", "#RawEnergy", "#Rebellious", "#DistortedGuitar"]},
        ]
    },
    "dreamy": {
        "title_adj": ["Deriva", "Nebbia", "Soglia", "Sospensione", "Galassia", "Velo"],
        "genre": "Dream Pop / Ambient / Shoegaze",
        "bpm_range": (62, 92),
        "keywords": ["fog", "mist", "light", "sun", "water", "reflection", "blur", "soft", "dream", "sky", "cloud", "haze"],
        "variants": [
            {"style": "Shoegaze etereo con muro di chitarre riverberanti", "instruments": ["chitarra con delay e riverbero infinito", "voce campionata come strumento", "batteria morbida", "pad di synth"], "mood": "etereo, sognante, avvolgente", "structure_note": "Struttura fluttuante. Le sezioni sfumano l'una nell'altra senza confini netti.", "ai_parts": ["shoegaze guitar", "infinite reverb", "dreamy atmosphere", "sampled voice texture", "soft drums", "lush synth pad", "ethereal", "wall of sound"], "sections": {"intro": "Pad synth che emerge dal silenzio", "strofa": "Chitarra con delay, melodia che galleggia", "pre_rit": "Stratificazione progressiva, tutto si infittisce", "ritornello": "Muro di suono etereo, voce campionata perduta", "bridge": "Dissoluzione totale, solo riverbero che decade", "outro": "Ritorno al pad iniziale, poi silenzio"}, "analysis": "Lo shoegaze usa l'eccesso come strumento di perdita del se. Il muro di suono e rifugio e dissoluzione simultanea.", "uso": "Sequenze oniriche, introspezione, amore, scene di distanza emotiva", "tags": ["#Shoegaze", "#DreamPop", "#EtherealGuitar", "#WallOfSound", "#Onirico"]},
            {"style": "Ambient elettronica con sintesi granulare e texture fluttuanti", "instruments": ["synth shimmer granulare", "chitarra con pitch shift", "basso leggero", "micro-percussioni"], "mood": "sospeso, curioso, leggero", "structure_note": "Struttura come viaggio. Si parte e non si sa dove si arriva.", "ai_parts": ["granular shimmer synth", "pitch shifted guitar", "light bass", "micro percussion", "floating", "curious", "weightless", "textural journey"], "sections": {"intro": "Shimmer granulare, note che nascono dal nulla", "strofa": "Chitarra con pitch shift, melodia curiosa", "pre_rit": "Micro-percussioni che appaiono", "ritornello": "Texture piena, leggerezza massima", "bridge": "Granulare solo, micro-suoni", "outro": "Le texture si rarefanno e scompaiono"}, "analysis": "La sintesi granulare trasforma il suono in nuvola di particelle sonore. La leggerezza e la qualita principale.", "uso": "Animazione, sogni ad occhi aperti, creativita, esplorazione", "tags": ["#GranularSynth", "#TexturalAmbient", "#Weightless", "#FloatingDream", "#Shimmer"]},
            {"style": "Hypnagogic pop con nostalgia distorta e estetica VHS", "instruments": ["synth lo-fi anni 80", "beat drum machine detuned", "basso synthwave", "coro campionato e pitchato"], "mood": "nostalgico-distorto, onirico-retro, familiar-straniante", "structure_note": "Pop degli anni 80 visto in sogno. Familiare ma irraggiungibile.", "ai_parts": ["hypnagogic pop", "lo-fi 80s synth", "detuned drum machine", "synthwave bass", "pitched choir sample", "nostalgic", "VHS aesthetic", "dreamlike retro"], "sections": {"intro": "Synth anni 80 detuned, come un nastro VHS che parte", "strofa": "Beat drum machine leggermente fuori tempo, basso synthwave", "pre_rit": "Coro campionato che emerge", "ritornello": "Pop onirico pieno, massima nostalgia distorta", "bridge": "Solo synth, glitch del nastro", "outro": "VHS che si riavvolge, fine del sogno"}, "analysis": "L'hypnagogic pop usa la nostalgia come materia prima distorta. Il passato non e ricordato, e sognato.", "uso": "Ricordi d'infanzia, nostalgia, estetica vaporwave, lost places", "tags": ["#HypnagogicPop", "#80sSynth", "#VHSAesthetic", "#NostalgicDream", "#Synthwave"]},
        ]
    },
    "tension": {
        "title_adj": ["Soglia", "Precipizio", "Attesa", "Vuoto", "Rottura", "Confine"],
        "genre": "Cinematic / Dark Ambient / Suspense",
        "bpm_range": (55, 100),
        "keywords": ["dark", "shadow", "abandoned", "broken", "storm", "danger", "threat", "horror", "fear"],
        "variants": [
            {"style": "Score cinematografico con archi dissonanti e percussioni irregolari", "instruments": ["archi dissonanti in tremolo", "percussioni orchestrali irregolari", "droni bassi", "effetti sonori tesi"], "mood": "teso, oscuro, irrisolvibile", "structure_note": "Struttura a tensione crescente. Nessuna risoluzione vera, tutto rimane sospeso.", "ai_parts": ["dissonant strings tremolo", "irregular orchestral percussion", "dark drone", "cinematic tension", "suspenseful", "eerie", "no resolution", "dark score"], "sections": {"intro": "Drone basso, silenzio quasi totale", "strofa": "Archi in tremolo, percussioni sporadiche", "pre_rit": "Densificazione degli archi, ritmo che accelera", "ritornello": "Climax dissonante, massima tensione orchestrale", "bridge": "Silenzio improvviso, poi note isolate", "outro": "Ritorno al drone, senza risoluzione"}, "analysis": "Gli archi dissonanti sono lo strumento classico del pericolo cinematografico. L'assenza di risoluzione lascia il pubblico in stato di allerta.", "uso": "Thriller, horror, suspense, scene di pericolo, boss fight", "tags": ["#DarkCinematic", "#DissonantStrings", "#Suspense", "#FilmScore", "#NoResolution"]},
            {"style": "Dark ambient con field recordings minacciosi e basso pulsante", "instruments": ["field recordings modificati e inquietanti", "basso pulsante lento", "synth pad oscuro", "micro-rumori"], "mood": "minaccioso, claustrofobico, presente", "structure_note": "Struttura basata sulla presenza. La minaccia e sempre li, mai esplode.", "ai_parts": ["dark ambient", "threatening field recordings", "slow pulsing bass", "dark synth pad", "micro-noises", "menacing", "claustrophobic", "present danger"], "sections": {"intro": "Field recording ambiguo, non identificabile", "strofa": "Basso pulsante, suoni ambientali inquietanti", "pre_rit": "I micro-rumori aumentano di frequenza", "ritornello": "Pad oscuro pieno, basso dominante", "bridge": "Solo field recording, nessuno strumento sintetico", "outro": "Basso che scompare, rimane solo l'ambiente"}, "analysis": "Il dark ambient usa l'ambiente sonoro reale come fonte di inquietudine. La minaccia e nel conosciuto reso sconosciuto.", "uso": "Horror psicologico, documentari true crime, ambienti post-apocalittici", "tags": ["#DarkAmbient", "#ThreateningSound", "#Claustrophobic", "#SlowPulse", "#PsychologicalHorror"]},
            {"style": "Musique concrete con suoni quotidiani trasformati in paesaggio alieno", "instruments": ["suoni quotidiani processati", "oggetti come strumenti", "manipolazione del nastro", "feedback controllato"], "mood": "disorientante, alieno, inquietante", "structure_note": "Nessuna struttura musicale tradizionale. E un paesaggio sonoro in evoluzione.", "ai_parts": ["musique concrete", "processed everyday sounds", "objects as instruments", "tape manipulation", "controlled feedback", "disorienting", "alien soundscape", "avant-garde"], "sections": {"intro": "Suono quotidiano irriconoscibile, processato al limite", "strofa": "Paesaggio sonoro alieno in evoluzione", "pre_rit": "Feedback che cresce, tensione aumenta", "ritornello": "Caos organizzato, massima densita", "bridge": "Silenzio improvviso, un suono quotidiano riconoscibile", "outro": "Ritorno al paesaggio alieno, poi silenzio"}, "analysis": "La musique concrete trasforma il familiare in inquietante. Il riconoscimento e il disorientamento avvengono simultaneamente.", "uso": "Arte sperimentale, installazioni sonore, horror avant-garde", "tags": ["#MusiqueConcrète", "#SoundArt", "#AvantGarde", "#AlienSoundscape", "#Experimental"]},
        ]
    },
    "jazz_noir": {
        "title_adj": ["Fumo", "Bourbon", "Pioggia", "Lampione", "Mezzanotte", "Tromba"],
        "genre": "Jazz / Noir / Cool Jazz",
        "bpm_range": (70, 110),
        "keywords": ["jazz", "saxophone", "trumpet", "smoke", "bar", "vintage", "classic", "elegant", "noir"],
        "variants": [
            {"style": "Cool jazz notturno con tromba sordinata e contrabbasso", "instruments": ["tromba sordinata", "contrabbasso pizzicato", "pianoforte jazz", "spazzole su rullante"], "mood": "raffinato, notturno, malinconico-elegante", "structure_note": "Forma jazz AABA con improvvisazione. L'eleganza e nella semplicita.", "ai_parts": ["muted trumpet", "pizzicato upright bass", "jazz piano", "brushed snare", "cool jazz", "nocturnal", "smoky", "elegant melancholy"], "sections": {"intro": "Tromba sordinata sola, tema principale", "strofa": "Sezione ritmica entra, groove jazz lento", "pre_rit": "Piano che improvvisa sopra la struttura", "ritornello": "Tema completo, tutti insieme", "bridge": "Solo di contrabbasso, tromba silenziosa", "outro": "Tema senza il ritmo, solo tromba che sfuma"}, "analysis": "Il cool jazz usa la sobrieta come massima espressione. La sordina e distanza emotiva che paradossalmente avvicina.", "uso": "Bar e lounge, scene romantiche, noir cinematografico, notti pluviose", "tags": ["#CoolJazz", "#MutedTrumpet", "#NocturnalJazz", "#SmokyBar", "#Noir"]},
            {"style": "Bebop riarrangiato per ensemble elettroacustico moderno", "instruments": ["sax alto", "vibrafono", "basso elettrico", "drum kit jazz moderno"], "mood": "energico-sofisticato, urbano-jazz, contemporaneo", "structure_note": "Bebop con influenze moderne. Velocita e complessita armonica.", "ai_parts": ["bebop alto sax", "vibraphone", "electric bass", "modern jazz drums", "sophisticated", "fast harmonic changes", "urban jazz", "contemporary"], "sections": {"intro": "Tema bebop al sax, veloce e sinuoso", "strofa": "Ritmo jazz completo, vibrafono in controcanto", "pre_rit": "Accelerazione armonica, tensione bebop", "ritornello": "Tutti improvvisano insieme, massima energia jazz", "bridge": "Solo vibrafono, poi sax risponde", "outro": "Tema principale al sax, fine in fade"}, "analysis": "Il bebop moderno usa la complessita come linguaggio emotivo. La velocita armonica crea eccitazione intellettuale e fisica.", "uso": "Scene urbane dinamiche, documentari musicali, creativita in movimento", "tags": ["#Bebop", "#AltoSax", "#Vibraphone", "#ModernJazz", "#UrbanSophisticated"]},
            {"style": "Jazz modale meditativo con influenze africane e mediorientali", "instruments": ["sax tenore modale", "oud o kora", "percussioni africane", "basso tenuto lungo"], "mood": "spirituale, ipnotico, universale", "structure_note": "Modale, senza risoluzione tonica. Il viaggio e la destinazione.", "ai_parts": ["modal tenor sax", "oud", "African percussion", "long sustained bass", "spiritual jazz", "hypnotic", "universal", "modal improvisation", "world jazz"], "sections": {"intro": "Oud solo, scala modale orientale", "strofa": "Sax tenore entra in dialogo con l'oud", "pre_rit": "Percussioni africane che si aggiungono", "ritornello": "Tutti insieme in improvvisazione modale", "bridge": "Solo percussioni, ritmo puro", "outro": "Sax e oud, poi solo oud, poi silenzio"}, "analysis": "Il jazz modale abbandona la risoluzione armonica per abbracciare l'ipnosi del modo. L'influenza africana e mediorientale porta nuovi centri tonali.", "uso": "Spiritualita, world music, meditazione attiva, festival culturali", "tags": ["#ModalJazz", "#SpiritualJazz", "#WorldJazz", "#Oud", "#AfricanPercussion"]},
        ]
    },
    "post_rock": {
        "title_adj": ["Orizzonte", "Vastita", "Macerie", "Sopravvissuto", "Oltre", "Parete"],
        "genre": "Post-Rock / Cinematic / Instrumental",
        "bpm_range": (65, 105),
        "keywords": ["vast", "landscape", "horizon", "empty", "ruin", "journey", "epic", "wide", "sky"],
        "variants": [
            {"style": "Post-rock epico con build monumentale e chitarre stratificate", "instruments": ["chitarre elettriche stratificate", "basso post-rock", "batteria dinamica", "synth orchestrale"], "mood": "epico, malinconico, trascendente", "structure_note": "Build classico post-rock: 8 minuti, piccolo poi enorme poi silenzio.", "ai_parts": ["post-rock", "layered electric guitars", "dynamic drums", "orchestral synth", "epic build", "melancholic", "transcendent", "cinematic climax"], "sections": {"intro": "Chitarra pulita sola, tema fragile", "strofa": "Basso entra, batteria leggera, costruzione lenta", "pre_rit": "Chitarre che si stratificano, synth in fondo", "ritornello": "Climax totale, muro sonoro epico", "bridge": "Dissoluzione, tutto si smonta", "outro": "Solo chitarra pulita, come all'inizio"}, "analysis": "Il post-rock usa il tempo come strumento compositivo. La pazienza del listener e parte dell'esperienza emotiva.", "uso": "Finali emotivi, documentari, paesaggi, in memoriam", "tags": ["#PostRock", "#EpicBuild", "#LayeredGuitars", "#CinematicClimax", "#Transcendent"]},
            {"style": "Math rock con poliritmia e cambi di tempo improvvisi", "instruments": ["chitarra con poliritmia complessa", "basso tecnico", "batteria math rock", "effetti tap delay"], "mood": "teso, tecnico, sorprendente", "structure_note": "Struttura imprevedibile. I cambi di tempo sono la narrazione.", "ai_parts": ["math rock", "polyrhythmic guitar", "technical bass", "odd time signatures", "tap delay guitar", "tense", "surprising", "technical precision"], "sections": {"intro": "Riff math rock, 7/8 o 5/4", "strofa": "Basso tecnico in dialogo con chitarra", "pre_rit": "Cambio di tempo improvviso", "ritornello": "Unisono tecnico, massima precisione", "bridge": "Solo chitarra con tap delay, pattern complesso", "outro": "Riff iniziale, poi stop improvviso"}, "analysis": "Il math rock usa l'asimmetria ritmica come emozione. La sorpresa e la melodia.", "uso": "Gaming, scene tecniche, documentari scientifici, creativita analitica", "tags": ["#MathRock", "#Polyrhythm", "#OddTime", "#TechnicalGuitar", "#Surprising"]},
            {"style": "Post-rock ambientale con loop pedal e drone", "instruments": ["chitarra elettrica con loop pedal", "synth drone", "batteria minimalista", "basso profondo"], "mood": "meditativo-epico, vasto, lento bruciore", "structure_note": "Ibrido post-rock/ambient. Il loop costruisce la struttura dall'interno.", "ai_parts": ["post-rock ambient", "loop pedal guitar", "synth drone", "minimal drums", "deep bass", "meditative epic", "slow burn", "vast", "loop-based build"], "sections": {"intro": "Loop di chitarra, drone synth che inizia", "strofa": "Loop si stratifica, batteria minimale entra", "pre_rit": "Drone cresce, loop piu denso", "ritornello": "Tutto insieme, vasto e pesante", "bridge": "Solo drone, loop si ferma", "outro": "Loop singolo, drone sfuma"}, "analysis": "L'ibridazione post-rock/ambient usa il loop come meditazione in tempo reale. La costruzione e lento bruciore, non esplosione.", "uso": "Meditazione attiva, paesaggi, documentari natura, contemplazione", "tags": ["#PostRockAmbient", "#LoopGuitar", "#DroneRock", "#SlowBurn", "#Meditative"]},
        ]
    },
    "lofi_hiphop": {
        "title_adj": ["Caffe", "Studio", "3AM", "Nebbia", "Tazza", "Lampada"],
        "genre": "Lo-Fi Hip Hop / Chillhop / Study Music",
        "bpm_range": (70, 95),
        "keywords": ["coffee", "study", "room", "indoor", "book", "desk", "window", "rain", "cozy", "warm", "interior"],
        "variants": [
            {"style": "Lo-fi hip hop classico con jazz samples e pioggia in background", "instruments": ["drums lo-fi con crackle", "piano jazz campionato", "basso morbido", "pioggia registrata"], "mood": "accogliente, concentrato, nostalgico", "structure_note": "Loop con variazioni minime. Il comfort della ripetizione.", "ai_parts": ["lo-fi hip hop", "jazz piano sample", "soft lo-fi drums", "gentle rain", "warm bass", "cozy atmosphere", "focused", "nostalgic", "vinyl crackle"], "sections": {"intro": "Pioggia, poi piano jazz campionato", "strofa": "Loop lo-fi completo, groove morbido", "pre_rit": "Variazione quasi impercettibile", "ritornello": "Loop leggermente piu ricco, piu caldo", "bridge": "Solo pioggia e basso", "outro": "Loop che sfuma lentamente nella pioggia"}, "analysis": "Il lo-fi hip hop usa l'imperfezione del suono come conforto. Il crackle del vinile e la firma dell'umano.", "uso": "Studio, lavoro creativo, chill time, caffe, notti tranquille", "tags": ["#LoFiHipHop", "#StudyMusic", "#JazzSample", "#CozyVibes", "#Chillhop"]},
            {"style": "Chillhop con marimba, vibrafono e groove solare", "instruments": ["marimba", "vibrafono", "chitarra funky leggera", "drums groove rilassato"], "mood": "solare, rilassato, positivo senza sforzo", "structure_note": "Groove leggero con melodia gioiosa. Comfort senza malinconia.", "ai_parts": ["chillhop", "marimba", "vibraphone", "light funky guitar", "relaxed groove", "sunny", "positive", "easygoing", "warm"], "sections": {"intro": "Marimba sola, melodia semplice e allegra", "strofa": "Groove completo, vibrafono in dialogo", "pre_rit": "Chitarra funky che si inserisce", "ritornello": "Tutto insieme, leggerezza massima", "bridge": "Solo vibrafono, quasi improvvisazione", "outro": "Marimba sola, ritorno al tema iniziale"}, "analysis": "Il chillhop solare usa timbri legnosi e metallici per evocare calore diurno senza peso emotivo.", "uso": "Mattine creative, estate, buon umore di fondo, lavoro leggero", "tags": ["#Chillhop", "#Marimba", "#Vibraphone", "#SunnyGroove", "#Easygoing"]},
            {"style": "Boom bap rallentato con sample soul anni 70 e vinile pesante", "instruments": ["boom bap drums pesanti", "sample soul anni 70", "basso pesante", "crackle vinile marcato"], "mood": "pesante, nostalgico-soul, radicato", "structure_note": "Boom bap classico rallentato. Il peso e il groove sono la priorita.", "ai_parts": ["slow boom bap", "70s soul sample", "heavy drums", "thick bass", "loud vinyl crackle", "heavy groove", "golden era hip hop", "nostalgic soul"], "sections": {"intro": "Crackle forte, sample soul anni 70", "strofa": "Boom bap pesante, basso in primo piano", "pre_rit": "Sample che si stratifica, tensione sale", "ritornello": "Massimo peso ritmico, groove dominante", "bridge": "Solo sample soul, drums via", "outro": "Crackle finale, fade out analogico"}, "analysis": "Il boom bap rallentato porta il peso della storia hip hop nel presente. Il vinile e memoria fisica e culturale.", "uso": "Hip hop, cypher, golden era vibes, documentari culturali", "tags": ["#SlowBoomBap", "#SoulSample", "#HeavyDrums", "#GoldenEra", "#VinylCrackle"]},
        ]
    },
    "neoclassical": {
        "title_adj": ["Elegia", "Sonetto", "Adagio", "Lacrimosa", "Requiem", "Notturno"],
        "genre": "Neoclassical / Modern Classical / Contemporary",
        "bpm_range": (42, 78),
        "keywords": ["elegant", "formal", "architecture", "museum", "classical", "art", "refined", "sculpture"],
        "variants": [
            {"style": "Piano solo neoclassico con influenze romantiche", "instruments": ["pianoforte da concerto Steinway", "risonanza naturale della sala da concerto"], "mood": "elegiaco, raffinato, commovente", "structure_note": "Forma libera con reminiscenze della sonata romantica. L'emozione guida la struttura.", "ai_parts": ["neoclassical piano solo", "concert grand piano", "romantic influence", "elegiac", "refined", "moving", "intimate concert hall reverb", "Satie influence"], "sections": {"intro": "Tema principale enunciato con semplicita", "strofa": "Variazioni emotive sul tema", "pre_rit": "Tensione armonica che cresce", "ritornello": "Climax emotivo, massima espressione pianistica", "bridge": "Sezione contemplativa quasi improvvisata", "outro": "Ripresa variata del tema, risoluzione serena"}, "analysis": "Il neoclassico per piano solo usa la semplicita apparente per nascondere profondita emotiva. Ogni nota e scelta con economia assoluta.", "uso": "Film d'autore, scene emotive, gallerie d'arte, cerimonie", "tags": ["#NeoclassicalPiano", "#ModernClassical", "#Elegiac", "#PianoSolo", "#Contemplative"]},
            {"style": "Quartetto d'archi con dissonanze contemporanee e risoluzione romantica", "instruments": ["violino I", "violino II", "viola", "violoncello"], "mood": "conflittuale, sofisticato, risolutivo", "structure_note": "Forma quartetto con tensioni contemporanee e risoluzioni romantiche. Il conflitto e la narrazione.", "ai_parts": ["string quartet", "contemporary dissonance", "romantic resolution", "chamber music", "sophisticated", "conflicted", "modern classical string writing"], "sections": {"intro": "Tutti insieme, dissonanza iniziale", "strofa": "Dialogo tra violino I e violoncello", "pre_rit": "Tensione armonica tra le voci", "ritornello": "Risoluzione romantica inaspettata", "bridge": "Solo viola, voce di mezzo dimenticata", "outro": "Riconciliazione di tutte le voci"}, "analysis": "Il quartetto d'archi usa quattro voci come quattro personaggi in conflitto. La risoluzione finale e catarsi.", "uso": "Film d'autore, dramma emotivo, documentari, teatro", "tags": ["#StringQuartet", "#ChamberMusic", "#ModernClassical", "#DissonanceResolution", "#Sophisticated"]},
            {"style": "Orchestra da camera minimalista nello stile di Philip Glass", "instruments": ["archi d'arco ripetuti", "fiati minimalisti", "pianoforte arpeggiato", "patterns ostinato"], "mood": "meditativo-matematico, spirituale, in trasformazione", "structure_note": "Struttura minimalista: piccoli cambiamenti in pattern ripetuti creano grande trasformazione.", "ai_parts": ["minimalist chamber orchestra", "Philip Glass style", "repetitive strings", "arpeggiated piano", "ostinato patterns", "meditative", "mathematical", "spiritual transformation"], "sections": {"intro": "Pattern ostinato al pianoforte, semplice", "strofa": "Archi entrano, pattern si stratificano", "pre_rit": "Fiati aggiungono melodia sopra i pattern", "ritornello": "Massima stratificazione, trasformazione evidente", "bridge": "Riduzione progressiva, ritorno al pattern base", "outro": "Solo pianoforte, pattern iniziale"}, "analysis": "Il minimalismo orchestrale usa la ripetizione come meditazione. I piccoli cambiamenti nel tempo diventano grandi trasformazioni emotive.", "uso": "Installazioni d'arte, meditazione attiva, documentari natura, sacralita laica", "tags": ["#Minimalism", "#PhilipGlassStyle", "#ChamberOrchestra", "#Ostinato", "#SpiritualMinimal"]},
        ]
    },
    "folk_intimista": {
        "title_adj": ["Focolare", "Soglia", "Pane", "Radici", "Voce", "Casa"],
        "genre": "Folk / Indie Folk / Singer-Songwriter",
        "bpm_range": (60, 95),
        "keywords": ["home", "fire", "family", "warm", "cozy", "rural", "simple", "wooden", "hearth"],
        "variants": [
            {"style": "Folk acustico intimo con voce parlata e fingerpicking", "instruments": ["chitarra acustica fingerpicking", "voce come strumento principale", "banjo leggero", "armonica a bocca"], "mood": "intimo, onesto, caldo", "structure_note": "Struttura canzone folk tradizionale. La semplicita e la forza.", "ai_parts": ["intimate acoustic folk", "fingerpicking guitar", "spoken word feel", "light banjo", "harmonica", "honest", "warm", "storytelling", "simple and true"], "sections": {"intro": "Fingerpicking solo, melodia familiare", "strofa": "Chitarra e voce, nient'altro", "pre_rit": "Banjo che si aggiunge delicatamente", "ritornello": "Armonica e tutto insieme, calore massimo", "bridge": "Chitarra sola, pausa narrativa", "outro": "Come l'intro, cerchio chiuso"}, "analysis": "Il folk intimo non nasconde nulla. La voce e la chitarra sono sufficienti perche l'onesta emotiva e la melodia.", "uso": "Scene domestiche, storie personali, campagna, serenita", "tags": ["#IntimateFolk", "#AcousticFingerPicking", "#Storytelling", "#Warm", "#Honest"]},
            {"style": "Indie folk con arrangiamento orchestrale camera e nostalgia autunnale", "instruments": ["chitarra acustica", "violoncello", "glockenspiel", "voce femminile campionata"], "mood": "autunnale, malinconico-dolce, crepuscolare", "structure_note": "Indie folk con cuore orchestrale. L'autunno come stato d'animo permanente.", "ai_parts": ["indie folk", "acoustic guitar", "cello", "glockenspiel", "sampled female voice", "autumnal", "bittersweet", "twilight", "orchestral chamber folk"], "sections": {"intro": "Glockenspiel solo, tema autunnale", "strofa": "Chitarra entra, violoncello in sottofondo", "pre_rit": "Voce femminile campionata emerge", "ritornello": "Tutto insieme, malinconia dolce", "bridge": "Solo violoncello, tristezza elegante", "outro": "Glockenspiel ritorna, come foglie che cadono"}, "analysis": "L'indie folk orchestrale usa l'autunno come metafora visiva permanente. Il glockenspiel porta leggerezza che contrasta il violoncello.", "uso": "Autunno, nostalgia stagionale, coming-of-age, fine estate", "tags": ["#IndieFolk", "#AutumnalMood", "#Cello", "#Glockenspiel", "#Bittersweet"]},
            {"style": "Folk nordico con nyckelharpa e risonanze medievali", "instruments": ["nyckelharpa", "flauto di canna", "percussioni frame drum", "voce in armonico"], "mood": "antico, nordico, mistico-terrestre", "structure_note": "Struttura basata su forme melodiche folk nordiche. La circolarita e la legge.", "ai_parts": ["nyckelharpa", "Nordic folk", "reed flute", "frame drum", "throat singing influence", "ancient", "Nordic mystical", "circular melody", "medieval folk"], "sections": {"intro": "Nyckelharpa sola, melodia circolare", "strofa": "Flauto di canna in dialogo", "pre_rit": "Frame drum entra, ritmo nordico", "ritornello": "Tutti insieme, danza antica", "bridge": "Voce in armonico, solo", "outro": "Nyckelharpa sola, melodia circolare che riprende"}, "analysis": "Il folk nordico porta con se paesaggi di foreste e fjord. La nyckelharpa e strumento di confine tra umano e natura.", "uso": "Paesaggi nordici, storia medievale, fantasy, spiritualita pagana", "tags": ["#NordicFolk", "#Nyckelharpa", "#MedievalFolk", "#NorthernMystic", "#AncientMelody"]},
        ]
    },
    "world_ethnic": {
        "title_adj": ["Caravan", "Deserto", "Spezie", "Seta", "Confine", "Horizonte"],
        "genre": "World Music / Ethnic / Fusion",
        "bpm_range": (75, 115),
        "keywords": ["desert", "market", "spice", "exotic", "travel", "culture", "ethnic", "world", "foreign", "journey", "sand"],
        "variants": [
            {"style": "Musica mediorientale con oud, qanun e ritmi asimmetrici", "instruments": ["oud", "qanun", "darbuka", "nay flauto"], "mood": "esotico, malinconico-solare, antico", "structure_note": "Struttura maqam mediorientale. Le scale modali creano emozioni irraggiungibili con la tonalita occidentale.", "ai_parts": ["oud", "qanun", "darbuka rhythm", "nay flute", "Middle Eastern maqam", "exotic", "melancholic and sunny", "ancient trade routes"], "sections": {"intro": "Oud solo, scale maqam", "strofa": "Darbuka entra, ritmo 9/8", "pre_rit": "Qanun che si aggiunge, armonia ricca", "ritornello": "Tutti insieme, massima energia mediorientale", "bridge": "Nay solo, melodia antica", "outro": "Oud solo, ritorno all'origine"}, "analysis": "Il maqam mediorientale usa scale con quarti di tono che creano emozioni impossibili nella tonalita occidentale. Il darbuka porta poliritmia.", "uso": "Documentari culturali, Medio Oriente, rotte della seta, mercati spezie", "tags": ["#Oud", "#MiddleEastern", "#Maqam", "#Darbuka", "#WorldMusic"]},
            {"style": "Afrobeat con poliritmia west-africana e fiati funk", "instruments": ["percussioni west-africane poliritmiche", "basso funky", "fiati funk", "chitarra afrobeat"], "mood": "gioioso, energico, comunitario", "structure_note": "Struttura afrobeat: groove ciclico dove ogni strumento e una voce nella conversazione.", "ai_parts": ["afrobeat", "West African polyrhythm", "funky bass", "funk horns", "afrobeat guitar", "joyful", "high energy", "communal", "cyclic groove"], "sections": {"intro": "Percussioni sole, poliritmia iniziale", "strofa": "Basso e chitarra entrano, groove afrobeat", "pre_rit": "Fiati funk si aggiungono", "ritornello": "Tutto insieme, danza comunitaria", "bridge": "Solo percussioni, ritmo puro", "outro": "Groove che si riduce a percussioni sole"}, "analysis": "L'afrobeat usa la poliritmia come democrazia musicale. Ogni strumento ha voce uguale nel dialogo ritmico.", "uso": "Festival, scene africane, documentari, energia positiva", "tags": ["#Afrobeat", "#WestAfrican", "#Polyrhythm", "#FunkHorns", "#Communal"]},
            {"style": "Cumbia elettronica con sintetizzatori e percussioni latinoamericane", "instruments": ["accordeon campionato", "percussioni cumbia", "basso synth", "marimba elettronica"], "mood": "festivo, sensuale, nostalgico-moderno", "structure_note": "Cumbia tradizionale con production elettronica moderna. La festa e nel DNA.", "ai_parts": ["electronic cumbia", "sampled accordion", "cumbia percussion", "synth bass", "electronic marimba", "festive", "sensual", "nostalgic-modern", "Latin dance"], "sections": {"intro": "Accordeon campionato, melodia cumbia", "strofa": "Percussioni cumbia, basso synth", "pre_rit": "Marimba elettronica che entra", "ritornello": "Tutto insieme, danza latina elettronica", "bridge": "Solo accordeon con effetti synth", "outro": "Fade out festivo"}, "analysis": "La cumbia elettronica porta la tradizione latinoamericana nel futuro digitale senza perdere l'anima della danza.", "uso": "Feste, estate, celebrazioni, scene latinoamericane, fusione culturale", "tags": ["#ElectronicCumbia", "#LatinElectronic", "#Accordion", "#CumbiaGroove", "#FestiveDance"]},
        ]
    },
    "drone_industrial": {
        "title_adj": ["Macchina", "Ruggine", "Fonderia", "Buco Nero", "Entropia", "Ferro"],
        "genre": "Drone / Industrial / Dark Ambient",
        "bpm_range": (0, 55),
        "keywords": ["factory", "metal", "rust", "machine", "industrial", "abandoned", "concrete", "steel", "dark", "massive"],
        "variants": [
            {"style": "Drone industriale con field recordings di fabbrica e basso infinito", "instruments": ["drone di basso sintetico", "field recordings industriali", "metalli percossi", "feedback lento"], "mood": "massiccio, oppressivo, catartico", "structure_note": "Nessun ritmo tradizionale. Il drone e la struttura. La durata e la forma.", "ai_parts": ["industrial drone", "factory field recordings", "percussive metal", "slow feedback", "massive", "oppressive", "cathartic", "no rhythm", "infinite bass"], "sections": {"intro": "Silenzio, poi il drone emerge lentamente", "strofa": "Drone pieno, field recordings industriali", "pre_rit": "Metalli che cominciano a percuotersi", "ritornello": "Massima densita, catarsi sonora", "bridge": "Solo field recording, drone si abbassa", "outro": "Drone che sfuma in cinque minuti"}, "analysis": "Il drone industriale usa il peso fisico del suono come catarsi. L'oppressione e l'abbraccio.", "uso": "Installazioni industriali, horror, meditazione estrema, arte contemporanea", "tags": ["#IndustrialDrone", "#DarkAmbient", "#FactorySound", "#Cathartic", "#Massive"]},
            {"style": "Power electronics con noise wall e struttura nascosta", "instruments": ["noise sintetico", "feedback estremo", "ritmo nascosto sotto il noise", "distorsione totale"], "mood": "estremo, fisico, confrontazionale", "structure_note": "Il noise e la forma. Sotto il caos c'e ordine. Trovalo.", "ai_parts": ["power electronics", "noise wall", "extreme feedback", "hidden rhythm", "total distortion", "extreme", "physical confrontation", "cathartic chaos"], "sections": {"intro": "Noise puro, impatto immediato", "strofa": "Ritmo che emerge nel noise", "pre_rit": "Ritmo dominante, noise sfondo", "ritornello": "Noise e ritmo alla pari, massima violenza sonora", "bridge": "Solo noise, ritmo scomparso", "outro": "Ritmo scompare di nuovo nel noise"}, "analysis": "Il power electronics usa l'aggressione sonora come linguaggio diretto. Non c'e bellezza, c'e onesta brutale.", "uso": "Arte estrema, performance, protesta, esperienza limite", "tags": ["#PowerElectronics", "#NoiseWall", "#Extreme", "#Confrontational", "#Cathartic"]},
            {"style": "Ambient computazionale con algoritmi generativi e granulare", "instruments": ["granulare processato", "algoritmi generativi", "sintesi FM", "texture computazionale"], "mood": "algoritmico, evolutivo, non-umano", "structure_note": "Struttura generativa. La composizione si scrive da sola seguendo regole matematiche.", "ai_parts": ["computational ambient", "generative algorithm", "granular synthesis", "FM synthesis", "evolving texture", "algorithmic composition", "non-human", "mathematical"], "sections": {"intro": "Algoritmo che inizia, prime texture granulari", "strofa": "Evoluzione granulare lenta e imprevedibile", "pre_rit": "FM synthesis che emerge dalle texture", "ritornello": "Massima complessita computazionale", "bridge": "Reset algoritmico, silenzio computazionale", "outro": "L'algoritmo che si spegne lentamente"}, "analysis": "La musica computazionale riflette la natura algoritmica del digitale. Non c'e intenzione umana diretta, solo regole che interagiscono.", "uso": "Installazioni tecnologiche, AI art, sperimentazione pura, futuro", "tags": ["#Computational", "#Generative", "#GranularSynthesis", "#Algorithmic", "#AIMusic"]},
        ]
    },
    "synthwave": {
        "title_adj": ["Neon", "Chrome", "Autostrada", "Retrowave", "Arcade", "Prisma"],
        "genre": "Synthwave / Retrowave / Outrun",
        "bpm_range": (100, 128),
        "keywords": ["neon", "retro", "80s", "chrome", "sunset", "highway", "arcade", "cyberpunk"],
        "variants": [
            {"style": "Synthwave classico outrun con arpeggiatori e drum machine anni 80", "instruments": ["synth arpeggiatore", "drum machine LinnDrum", "basso synth portamento", "synth pad retro"], "mood": "nostalgico-futuristico, cinematico, solitario-epico", "structure_note": "Struttura pop anni 80 con estetica cinema action. Il tramonto e la durata.", "ai_parts": ["classic synthwave", "outrun", "arpeggiator synth", "LinnDrum", "portamento synth bass", "retro pad", "nostalgic futurism", "cinematic sunset", "driving"], "sections": {"intro": "Arpeggiatore synth, tema outrun", "strofa": "LinnDrum entra, basso synth", "pre_rit": "Pad retro che si stratifica", "ritornello": "Tutto insieme, sunset highway", "bridge": "Solo arpeggiatore, accelerazione", "outro": "Dissolvenza outrun, tramonto terminato"}, "analysis": "Il synthwave usa la nostalgia degli anni 80 come utopia retrofuturistica. Il tramonto e sempre alle spalle.", "uso": "Anni 80 revival, cyberpunk, guida notturna, nostalgia futuristica", "tags": ["#Synthwave", "#Outrun", "#Retrowave", "#80sNostalgia", "#NeonSunset"]},
            {"style": "Darksynth con influenze metal e estetica horror anni 80", "instruments": ["synth pesante distorto", "drum machine aggressiva", "basso distorto", "arpeggiatore oscuro"], "mood": "oscuro, pericoloso, eccitante", "structure_note": "Synthwave portato nel buio. Il pericolo e l'estetica.", "ai_parts": ["darksynth", "heavy distorted synth", "aggressive drum machine", "distorted bass", "dark arpeggio", "80s horror aesthetic", "dangerous", "thrilling"], "sections": {"intro": "Arpeggiatore oscuro, tema di pericolo", "strofa": "Drum machine aggressiva, basso distorto", "pre_rit": "Sintetizzatori che si stratificano nel buio", "ritornello": "Massima oscurita sonora", "bridge": "Solo arpeggiatore oscuro", "outro": "Dissolvenza nel buio"}, "analysis": "Il darksynth porta l'estetica horror degli anni 80 nella produzione elettronica moderna. Il pericolo e il fascino.", "uso": "Horror anni 80, videogiochi dark, villain cinematografici, notte", "tags": ["#Darksynth", "#HorrorSynth", "#80sHorror", "#DangerousGroove", "#DarkAesthetic"]},
            {"style": "Lo-fi synthwave con synth detuned e nostalgia VHS", "instruments": ["synth detuned vintage", "drum machine lo-fi", "basso caldo analogico", "chorus e delay analogico"], "mood": "nostalgico-malinconico, sfocato, delicato", "structure_note": "Synthwave portato nel lo-fi. La perfezione e nell'imperfezione.", "ai_parts": ["lo-fi synthwave", "detuned vintage synth", "lo-fi drum machine", "warm analog bass", "analog chorus and delay", "nostalgic melancholy", "blurry VHS", "delicate"], "sections": {"intro": "Synth detuned, melodia sfocata", "strofa": "Lo-fi drums, basso caldo", "pre_rit": "Chorus analogico che si stratifica", "ritornello": "Tutto insieme, nostalgia massima", "bridge": "Solo synth detuned, quasi intonato", "outro": "Fade analogico, nastro che sfuma"}, "analysis": "Il lo-fi synthwave usa l'imperfezione del vintage come emozione. Il detuning e ricordo che non torna mai perfetto.", "uso": "Nostalgia anni 80-90, estetica vaporwave, memorie d'infanzia, malinconia solare", "tags": ["#LoFiSynthwave", "#DetunedSynth", "#VHSNostalgia", "#AnalogWarm", "#BlurryDream"]},
        ]
    },
    "cinematic_epic": {
        "title_adj": ["Battaglia", "Destino", "Alba", "Impero", "Sacrificio", "Gloria"],
        "genre": "Cinematic / Epic / Orchestral",
        "bpm_range": (80, 140),
        "keywords": ["epic", "war", "battle", "hero", "journey", "powerful", "monumental", "dramatic"],
        "variants": [
            {"style": "Score orchestrale epico con coro e percussioni massive", "instruments": ["orchestra completa", "coro epico", "percussioni massive", "ottoni eroici"], "mood": "epico, eroico, monumentale", "structure_note": "Struttura score cinematografico. Build verso il climax e tutto.", "ai_parts": ["epic orchestral score", "full orchestra", "epic choir", "massive percussion", "heroic brass", "cinematic epic", "monumental", "heroic journey"], "sections": {"intro": "Ottoni soli, tema eroico", "strofa": "Orchestra completa in costruzione", "pre_rit": "Coro che entra, tensione massima", "ritornello": "Tutto insieme, apice epico", "bridge": "Silenzio, poi solo percussioni", "outro": "Tema eroico agli ottoni, fine maestosa"}, "analysis": "Lo score epico usa la massa orchestrale come forza emotiva. Il coro porta dimensione umana collettiva all'eroismo individuale.", "uso": "Trailer film, videogiochi epici, sport, documentari storici", "tags": ["#EpicOrchestral", "#Cinematic", "#EpicChoir", "#HeroicBrass", "#Monumental"]},
            {"style": "Score emotivo intimo con archi e pianoforte per scene drammatiche", "instruments": ["archi da camera", "pianoforte solo", "oboe solista", "tappeto orchestrale leggero"], "mood": "drammatico-intimo, commovente, umano", "structure_note": "Score emotivo non epico. La grandezza e nell'intimita, non nel volume.", "ai_parts": ["intimate dramatic score", "chamber strings", "solo piano", "solo oboe", "light orchestral bed", "emotionally dramatic", "moving", "human scale"], "sections": {"intro": "Piano solo, tema emotivo", "strofa": "Archi in sottofondo, piano continua", "pre_rit": "Oboe solista emerge", "ritornello": "Archi e oboe insieme, climax intimo", "bridge": "Solo oboe, massima solitudine", "outro": "Piano solo, risoluzione"}, "analysis": "Lo score intimo usa la vulnerabilita come forza. L'oboe solista e la voce umana della fragilita.", "uso": "Drammi, perdite, scene madri, cinema d'autore", "tags": ["#IntimateScore", "#ChamberStrings", "#SoloOboe", "#EmotionalDrama", "#MovingCinema"]},
            {"style": "Score ibrido orchestrale-elettronico per fantascienza epica", "instruments": ["orchestra con elettronica integrata", "synth orchestrali", "percussioni ibride", "coro processato"], "mood": "futuristico-epico, tecnologico-umano, vasto", "structure_note": "Ibrido che non sceglie tra passato e futuro. Entrambi sono presenti.", "ai_parts": ["hybrid orchestral electronic", "electronic orchestra", "orchestral synths", "hybrid percussion", "processed choir", "sci-fi epic", "futuristic and human", "vast space"], "sections": {"intro": "Synth orchestrali, spazio cosmico", "strofa": "Orchestra e elettronica in dialogo", "pre_rit": "Coro processato che emerge", "ritornello": "Unione totale, epica futuristica", "bridge": "Solo elettronica, poi solo orchestra", "outro": "I due mondi che si fondono definitivamente"}, "analysis": "Lo score ibrido riflette la condizione umana nel futuro tecnologico. L'emozione e il punto di incontro tra macchina e natura.", "uso": "Sci-fi, space opera, videogiochi fantascientifici, futuro", "tags": ["#HybridScore", "#SciFiEpic", "#OrchestraElectronic", "#FuturisticEpic", "#CosmicScale"]},
        ]
    },
}


# ═══════════════════════════════════════════════════════
# FUNZIONI
# ═══════════════════════════════════════════════════════

def analyze_colors(image):
    img_small = image.resize((100, 100))
    pixels = list(img_small.getdata())
    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)
    brightness = (avg_r + avg_g + avg_b) / 3
    h, s, v = rgb_to_hsv(avg_r/255, avg_g/255, avg_b/255)
    return {"brightness": brightness, "hue": h * 360, "saturation": s}

def select_profile(description, color_data):
    desc_lower = description.lower()
    brightness = color_data["brightness"]
    hue = color_data["hue"]
    sat = color_data["saturation"]
    scores = {k: 0 for k in PROFILES}
    for profile_key, profile in PROFILES.items():
        for kw in profile.get("keywords", []):
            if kw in desc_lower:
                scores[profile_key] += 2
    if brightness < 70:
        scores["tension"] += 3; scores["drone_industrial"] += 2; scores["melancholy"] += 2
    elif brightness < 120:
        scores["urban_night"] += 3; scores["jazz_noir"] += 2; scores["melancholy"] += 2
    elif brightness > 180:
        scores["energetic"] += 2; scores["cinematic_epic"] += 2; scores["lofi_hiphop"] += 1
    if sat < 0.2:
        scores["neoclassical"] += 2; scores["melancholy"] += 2; scores["drone_industrial"] += 1
    elif sat > 0.6:
        scores["energetic"] += 2; scores["world_ethnic"] += 2; scores["synthwave"] += 2
    if 60 <= hue <= 160:
        scores["nature_calm"] += 3; scores["folk_intimista"] += 2
    if 200 <= hue <= 280:
        scores["dreamy"] += 2; scores["urban_night"] += 2; scores["synthwave"] += 2
    if 0 <= hue <= 30 or hue >= 340:
        scores["energetic"] += 2; scores["cinematic_epic"] += 2
    return max(scores, key=scores.get)

def generate_title(profile):
    adj = random.choice(profile["title_adj"])
    nouns = ["di Luce","Perduta","Notturna","del Tempo","Invisibile","Sospesa",
             "Digitale","nell'Aria","Silenziosa","Frantumata","Antica","Futura",
             "di Pietra","del Vuoto","Remota","Crescente","Spezzata","Intatta"]
    return f"{adj} {random.choice(nouns)}"

def generate_prompt(description, profile_key, profile, seed=None):
    if seed is not None:
        random.seed(seed)
    variant = random.choice(profile["variants"])
    title = generate_title(profile)
    bpm_lo, bpm_hi = profile["bpm_range"]
    bpm = random.randint(bpm_lo if bpm_lo > 0 else 40, bpm_hi)
    ai_parts = variant["ai_parts"].copy()
    random.shuffle(ai_parts)
    ai_prompt = f"Instrumental, {bpm} BPM, " + ", ".join(ai_parts) + ", no vocals, background music"
    instruments_str = ", ".join(variant["instruments"])
    s = variant["sections"]
    sep = "=" * 64
    output = "\n".join([
        f"TITLE: {title}", "",
        f"STYLE/GENRE: {variant['style']} / {profile['genre']}",
        f"BPM: {bpm}",
        f"KEY INSTRUMENTS: {instruments_str}",
        f"MOOD: {variant['mood']}", "",
        f"STRUCTURE NOTE: {variant['structure_note']}", "",
        sep, "AI GENERATION PROMPT (English)", sep,
        ai_prompt, "",
        sep, "IMAGE DESCRIPTION (BLIP)", sep,
        description, "",
        sep, "STRUCTURE / GUIDE (Italian)", sep,
        f"[INTRO] ({s['intro']})", "",
        f"[STROFA 1] ({s['strofa']})", "",
        f"[PRE-RITORNELLO] ({s['pre_rit']})", "",
        f"[RITORNELLO] ({s['ritornello']})", "",
        "[STROFA 2] (Variazione della strofa 1, leggera evoluzione timbrica)", "",
        "[PRE-RITORNELLO] (Nuova apertura armonica, piu intensa)", "",
        "[RITORNELLO] (Massima espressione emotiva strumentale)", "",
        f"[BRIDGE] ({s['bridge']})", "",
        "[RITORNELLO FINALE] (Ripresa del tema con intensita aumentata)", "",
        f"[OUTRO] ({s['outro']})", "",
        sep, "CRITICAL ANALYSIS", sep,
        variant['analysis'], "",
        f"Profilo: {profile_key.upper().replace('_', ' ')} | Variante casuale tra 3.", "",
        sep, "DETAILS", sep,
        f"Usage: {variant['uso']}",
        f"Tags: {' '.join(variant['tags'])}"
    ])
    return output, title, variant["tags"]


# ═══════════════════════════════════════════════════════
# UI
# ═══════════════════════════════════════════════════════

st.markdown("<h1 style='font-size:2rem; letter-spacing:-0.02em; margin-top:-1rem;'>GENERATORE DI PROMPT MUSICALI<br><span style='color:#c8ff00;font-size:1rem;letter-spacing:0.2em;'>BY LOOP507</span></h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown('<div class="section-header">Carica immagine</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, use_container_width=True)
        color_data = analyze_colors(image)
        b, h, s = color_data["brightness"], color_data["hue"], color_data["saturation"]
        st.markdown('<div class="section-header">Dati cromatici</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Luminosita", f"{b:.0f}/255")
        c2.metric("Tonalita", f"{h:.0f}deg")
        c3.metric("Saturazione", f"{s:.2f}")
        st.markdown('<div class="section-header">15 profili x 3 varianti</div>', unsafe_allow_html=True)
        for pk in PROFILES:
            st.caption(f"· {pk.replace('_',' ').title()} — {PROFILES[pk]['genre']}")

with col2:
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        color_data = analyze_colors(image)
        description = ""
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            @st.cache_resource(show_spinner=False)
            def load_model():
                p = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                m = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
                return p, m
            with st.spinner("Analisi visiva in corso..."):
                processor, model = load_model()
                inputs = processor(image, return_tensors="pt")
                out = model.generate(**inputs)
                description = processor.decode(out[0], skip_special_tokens=True)
            st.markdown(f"**BLIP:** `{description}`")
        except Exception:
            description = "image"
            st.info("BLIP non disponibile - uso solo analisi colori.")

        if "forced_profile" not in st.session_state:
            st.session_state.forced_profile = None
        profile_key = st.session_state.forced_profile or select_profile(description, color_data)
        profile = PROFILES[profile_key]

        st.markdown('<div class="section-header">Profilo rilevato</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="profile-pill">{profile_key.replace("_"," ").upper()}</span>', unsafe_allow_html=True)
        st.caption(f"{profile['genre']} · BPM {profile['bpm_range'][0]}-{profile['bpm_range'][1]}")
        st.markdown("---")

        if "seed" not in st.session_state:
            st.session_state.seed = random.randint(0, 99999)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Rigenera Prompt"):
                st.session_state.seed = random.randint(0, 99999)
                st.session_state.forced_profile = None
        with col_b2:
            if st.button("Profilo Casuale"):
                st.session_state.forced_profile = random.choice(list(PROFILES.keys()))
                st.session_state.seed = random.randint(0, 99999)

        prompt_text, title, tags = generate_prompt(description, profile_key, profile, seed=st.session_state.seed)

        st.markdown('<div class="section-header">Prompt musicale strutturato</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="prompt-block">{prompt_text}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Tags</div>', unsafe_allow_html=True)
        tags_html = " ".join([f'<span class="tag-chip">{t}</span>' for t in tags])
        st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-header">Copia testo completo</div>', unsafe_allow_html=True)
        st.text_area("", value=prompt_text, height=220, label_visibility="collapsed")
    else:
        st.markdown("""
        <div style='padding: 3rem 1rem; color: #444; font-size: 0.82rem; line-height: 2.2;'>
        Carica un'immagine per generare il prompt musicale strutturato.<br><br>
        <span style='color:#c8ff00;'>15 profili x 3 varianti = 45 output unici</span><br><br>
        Profili: Urban Night, Nature Calm, Melancholy, Energetic, Dreamy,<br>
        Tension, Jazz Noir, Post Rock, Lo-Fi Hip Hop, Neoclassical,<br>
        Folk Intimista, World Ethnic, Drone Industrial, Synthwave, Cinematic Epic
        </div>
        """, unsafe_allow_html=True)
