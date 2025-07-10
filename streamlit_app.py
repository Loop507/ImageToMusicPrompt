import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Funzione fittizia per simulare descrizione dall'immagine (sostituisci con la tua API o modello)
def get_image_description(image):
    # Questa è una simulazione, nella realtà userai un modello o API di analisi immagine
    # Esempio con descrizione ripetuta da correggere:
    return "a microwave with a bowl of fruit and a bowl of fruit"

def clean_description(text):
    words = text.split()
    for i in range(len(words) - 1):
        if words[i] == words[i+1]:
            return " ".join(words[:i+1])
    return text

def generate_prompts(description):
    # Pulisce la descrizione da ripetizioni
    clean_desc = clean_description(description)

    prompt1 = f"Componi un brano ispirato a questa scena, stile drone ipnotico, atmosfera sospesa, ambientato in un paesaggio simile a: {clean_desc}"
    prompt2 = f"Immagina una soundscape naturale, con suoni ambientali (vento, acqua, foglie), ispirata a: {clean_desc}"
    prompt3 = f"Genera musica elettronica glitch sperimentale, con ritmo frastagliato, basata sulla scena: {clean_desc}"

    return clean_desc, [prompt1, prompt2, prompt3]

st.title("Generatore di prompt musicali basati su immagini by Loop507")

uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Immagine caricata', use_column_width=True)

    if st.button("Genera descrizione e prompt musicali"):
        with st.spinner('Analizzando immagine e generando prompt...'):
            description = get_image_description(image)
            description, prompts = generate_prompts(description)

            st.subheader("Descrizione immagine:")
            st.write(description)

            st.subheader("Prompt musicali generati:")
            for i, prompt in enumerate(prompts, 1):
                st.write(f"Prompt {i}: {prompt}")

            # opzionale: generazione riga hashtag sintetici
            hashtags = " ".join(["#musica", "#soundscape", "#drone", "#glitch", "#ambient"])
            st.write(f"Hashtag suggeriti: {hashtags}")
