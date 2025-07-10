import streamlit as st
from PIL import Image
import random
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Titolo
st.title("ImageToMusicPrompt by Loop507")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Immagine caricata", use_column_width=True)

    # Caricamento modello BLIP
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Generazione descrizione immagine
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    st.markdown("### Descrizione immagine:")
    st.write(description)

    # Set ampio di atmosfere musicali
    atmosphere_templates = [
        "Drone ipnotico, texture ambient e lente trasformazioni sonore",
        "Soundscape naturale, vento tra gli alberi, acqua che scorre, suoni di foglie",
        "Glitch elettronico sperimentale, ritmo frastagliato e suoni distorti",
        "Classica minimale, piano delicato e silenzi contemplativi",
        "Noise pulsante, caos controllato e distorsione ritmica",
        "Synthwave nostalgica, con toni retrò e malinconia luminosa",
        "Ambient scuro, rumori profondi e riverberi avvolgenti",
        "Techno astratta, pattern ripetitivi e struttura liquida",
        "Jazz liquido, basso rotondo e fiati leggeri",
        "Cinematica, archi sospesi e senso di attesa"
    ]

    # Scelta casuale di 3 atmosfere diverse
    atmospheres = random.sample(atmosphere_templates, 3)

    # Mostra le 3 atmosfere
    st.markdown("### Atmosfere musicali generate:")
    for mood in atmospheres:
        st.markdown(f"- {mood}")

    # Hashtag
    st.markdown("### Hashtag suggeriti:")
    st.code("#musica #atmosfera #sounddesign #AIart #musicprompt #image2music")
