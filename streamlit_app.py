import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

@st.cache_resource(show_spinner=False)
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def get_image_description(image, processor, model):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    if image.mode != "RGB":
        image = image.convert("RGB")

    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

def generate_prompts(description):
    prompt1 = f"Componi un brano ispirato a questa scena, stile drone ipnotico, atmosfera sospesa, ambientato in un paesaggio simile a: {description}"
    prompt2 = f"Immagina una soundscape naturale, con suoni ambientali (vento, acqua, foglie), ispirata a: {description}"
    prompt3 = f"Genera musica elettronica glitch sperimentale, con ritmo frastagliato, basata sulla scena: {description}"

    return description, [prompt1, prompt2, prompt3]

st.title("Generatore di prompt musicali basati su immagini by Loop507")

uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Immagine caricata', use_column_width=True)

    if st.button("Genera descrizione e prompt musicali"):
        with st.spinner('Analizzando immagine e generando prompt...'):
            processor, model = load_model()
            description = get_image_description(image, processor, model)
            description, prompts = generate_prompts(description)

            st.subheader("Descrizione immagine:")
            st.write(description)

            st.subheader("Prompt musicali generati:")
            for i, prompt in enumerate(prompts, 1):
                st.write(f"Prompt {i}: {prompt}")

            hashtags = " ".join(["#musica", "#soundscape", "#drone", "#glitch", "#ambient"])
            st.write(f"Hashtag suggeriti: {hashtags}")
