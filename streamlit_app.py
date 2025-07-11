import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from transformers import BlipProcessor, BlipForConditionalGeneration
import random

st.set_page_config(page_title="Generatore di prompt musicali basati su immagini by Loop507")

st.title("Generatore di prompt musicali basati su immagini by Loop507")

uploaded_file = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])

# Liste di atmosfere per i prompt musicali
electronic_atmospheres = [
    "soft minimal electronic, filtered textures",
    "warm ambient pads, subtle granular motion",
    "glitchy rhythms with deep bass pulses",
    "muted techno with evolving patterns",
    "analog noise, slow distortion, shimmering delay",
    "breathing synths, tape-saturated loops",
    "modular bleeps and lo-fi sequences",
    "crystalline glitches with airy drones",
    "dreamy synth layers with pulsating beats",
    "textured digital soundscapes with mellow rhythms",
    "abstract electronic waves with subtle modulation"
]

classical_atmospheres = [
    "modern string quartet with emotional nuance",
    "solo piano, intimate and contemplative",
    "orchestral swells with cinematic tension",
    "baroque-inspired textures with minimalist pulse",
    "chamber music with ambient overlays",
    "neo-romantic harmonies with subtle dissonance",
    "dramatic string ensemble with dynamic phrasing",
    "lush cello melodies with soft violin harmonies",
    "elegant harp arpeggios and gentle flute lines",
    "expressive woodwinds with a pastoral feel"
]

natural_atmospheres = [
    "field recordings with distant animal calls",
    "soft wind textures with forest ambience",
    "acoustic guitar with natural reverb",
    "water drips and leaf rustling in slow rhythm",
    "birdsong over gentle drone",
    "minimal flute motifs with river textures",
    "organic loops and earthy percussive tones",
    "morning dew sounds with gentle breeze",
    "crackling fire sounds mixed with night insects",
    "rustling grass and soft rain with distant thunder"
]

def generate_atmospheres():
    atm1 = random.choice(electronic_atmospheres)
    atm2 = random.choice(classical_atmospheres)
    atm3 = random.choice(natural_atmospheres)
    return atm1, atm2, atm3

@st.cache_resource(show_spinner=False)
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption="Immagine caricata", use_container_width=True)

        processor, model = load_model()

        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)
        st.markdown("### Descrizione immagine:")
        st.write(description)

        atm1, atm2, atm3 = generate_atmospheres()

        st.markdown("### Prompt musicali generati:")
        st.write(f"Atmosfera 1: {atm1}")
        st.write(f"Atmosfera 2: {atm2}")
        st.write(f"Atmosfera 3: {atm3}")

        hashtags = "#musica #soundscape #ambient #electronic #classical #nature"
        st.markdown("### Hashtag suggeriti:")
        st.write(hashtags)

    except Exception as e:
        st.error(f"Errore durante l'analisi dell'immagine: {e}")

else:
    st.info("Carica un'immagine per generare descrizione e prompt musicali.")
