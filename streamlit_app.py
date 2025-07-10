import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Caricamento modello e processor BLIP (meglio caricarli fuori funzione per efficienza)
@st.cache_resource(show_spinner=False)
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_model()

st.set_page_config(page_title="Generatore di prompt musicali by Loop507", layout="centered")

st.title("Generatore di prompt musicali basati su immagini by Loop507")

uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])

def generate_description(image):
    # Prepara l'immagine per il modello
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Immagine caricata", use_column_width=True)

    with st.spinner("Analisi in corso..."):
        description = generate_description(image)
    
    st.subheader("Descrizione immagine:")
    st.write(description)

    # Prompt musicali distinti, senza ripetere la descrizione nel testo, ma usandola solo come riferimento finale
    prompt_styles = [
        "drone ipnotico, atmosfera sospesa",
        "soundscape naturale, suoni ambientali (vento, acqua, foglie)",
        "musica elettronica glitch sperimentale, ritmo frastagliato"
    ]

    st.subheader("Prompt musicali generati:")

    for i, style in enumerate(prompt_styles, start=1):
        prompt = f"Prompt {i}: Componi un brano in stile {style}, basato sulla scena descritta."
        st.write(prompt)

    # Hashtag suggeriti statici ma coerenti
    hashtags = "#musica #soundscape #drone #glitch #ambient"
    st.subheader("Hashtag suggeriti:")
    st.write(hashtags)
