import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import random

# Titolo
st.set_page_config(page_title="Generatore di Prompt Musicali – by Loop507", layout="centered")
st.title("🎶 Generatore di Prompt Musicali basati su immagini – by Loop507")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Immagine caricata", use_column_width=True)

    # Caricamento modello di captioning
    with st.spinner("Analisi dell'immagine..."):
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)

    st.subheader("📝 Descrizione visiva")
    st.write(description)

    # Tipologie musicali random in base alla descrizione
    generi = ["musica elettronica glitch", "soundscape naturale", "ambient sperimentale", "melodia classica malinconica", "rumore industriale", "drone ipnotico"]
    selezionati = random.sample(generi, 3)

    # Generazione prompt musicali
    st.subheader("🎼 Prompt Musicali Generati")
    for i, g in enumerate(selezionati, 1):
        st.markdown(f"**Prompt {i}:** Componi un brano ispirato a questa scena, stile: _{g}_, ambientato in un paesaggio simile a: _{description}_")

    # Hashtag generici + dinamici
    base_tags = ["#musicgenerator", "#aigenerated", "#sounddesign", "#loop507", "#visualsound"]
    descr_tags = [f"#{w.lower()}" for w in description.split() if w.isalpha() and len(w) > 3][:5]
    all_tags = base_tags + descr_tags

    st.subheader("🔖 Hashtag suggeriti")
    st.code(" ".join(all_tags), language="markdown")
