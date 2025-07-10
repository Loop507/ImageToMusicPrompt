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

    # Generazione descrizione
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    st.markdown("### Descrizione immagine:")
    st.write(description)

    # Set di atmosfere musicali possibili
    atmosphere_templates = [
        "Atmosfera drone ipnotico, texture ambient e lente trasformazioni sonore",
        "Atmosfera soundscape naturale, vento tra gli alberi, acqua che scorre, suoni di foglie",
        "Atmosfera glitch elettronica sperimentale, ritmo frastagliato e suoni distorti",
        "Atmosfera classica minimale, piano delicato e silenzi contemplativi",
        "Atmosfera noise pulsante, caos controllato e distorsione ritmica",
        "Atmosfera synthwave nostalgica, con toni retrò e malinconia luminosa",
        "Atmosfera ambient scura, rumori profondi e riverberi avvolgenti",
        "Atmosfera techno astratta, pattern ripetitivi e struttura liquida",
        "Atmosfera jazz liquido, basso rotondo e fiati leggeri",
        "Atmosfera cinematica, archi sospesi e senso di attesa"
    ]

    # Scelta random di 3 atmosfere diverse
    atmospheres = random.sample(atmosphere_templates, 3)

    # Mostra le 3 atmosfere
    st.markdown("### Prompt musicali generati:")
    for i, prompt in enumerate(atmospheres, 1):
        st.markdown(f"**Atmosfera {i}:** {prompt}")

    # Hashtag finali
    hashtags = "#musica #atmosfera #sounddesign #AIart #musicprompt #image2music"
    st.markdown("### Hashtag suggeriti:")
    st.code(hashtags)
