import streamlit as st
from PIL import Image
import random

# Titolo dell'app
st.set_page_config(page_title="Image to Music Prompt")
st.title("🎵 Generatore di Prompt Musicali basati su Immagini")
st.write("Carica una foto e ottieni ispirazione musicale!")

# Caricamento immagine
uploaded_file = st.file_uploader("📷 Carica un'immagine", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Immagine caricata", use_column_width=True)

    # Simulazione di analisi immagine
    st.subheader("🎼 Descrizione del suono suggerito")

    categorie = [
        {
            "tipo": "Suono naturale",
            "descrizione": "🌿 Ambienti sonori naturali come vento, pioggia o foglie che si muovono.",
            "prompt": [
                "ambient forest soundscape with gentle wind and leaves",
                "natural sound of flowing water with distant thunder",
                "minimalist bird calls in an open field, atmospheric"
            ]
        },
        {
            "tipo": "Elettronica",
            "descrizione": "🎛️ Ritmi sintetici, texture digitali, vibrazioni urbane.",
            "prompt": [
                "glitchy electronic loop with reverb and distortion",
                "slow techno beat with deep bass and modular synths",
                "experimental ambient noise with granular textures"
            ]
        },
        {
            "tipo": "Classica / Orchestrale",
            "descrizione": "🎻 Armonie cinematiche, strumenti acustici, atmosfera emotiva.",
            "prompt": [
                "melancholic piano with soft strings, cinematic mood",
                "orchestral crescendo with brass and violins",
                "solo cello with reverb, nostalgic ambient feel"
            ]
        },
        {
            "tipo": "Noise / Sperimentale",
            "descrizione": "⚡ Rumori astratti, texture crude, suoni destrutturati.",
            "prompt": [
                "white noise burst with crackles and broken rhythm",
                "industrial ambience with metallic scraping and hums",
                "chaotic synth stabs and distorted textures"
            ]
        }
    ]

    scelta = random.choice(categorie)
    st.markdown(f"**Tipo di suono:** {scelta['tipo']}")
    st.markdown(f"**Descrizione:** {scelta['descrizione']}")
    st.markdown("**🎧 Prompt suggeriti per generare musica:**")

    for i, prompt in enumerate(scelta['prompt'], 1):
        st.code(f"{i}. {prompt}", language="text")

else:
    st.info("Carica un'immagine per iniziare.")
