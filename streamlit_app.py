import streamlit as st
import re

st.title("Generatore di prompt musicali basati su immagini by Loop507")
st.write("Carica una foto e ricevi descrizioni e prompt musicali ispirati all'immagine.")

uploaded_file = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])

def analyze_image(file):
    # Placeholder analisi immagine
    return "Auto sportiva rossa su strada asfaltata in una giornata soleggiata."

def generate_music_prompts(description, genre="Varied"):
    prompts = [
        f"Suono ambientale naturale ispirato a {description} - suoni di vento, foglie, acqua",
        f"Musica elettronica con vibe futuristica e glitch, ispirata a {description}",
        f"Composizione classica con archi e pianoforte che riflette {description}"
    ]
    return prompts

def generate_hashtags(prompts):
    hashtags = set()
    for prompt in prompts:
        # Estrae parole chiave rimuovendo punteggiatura e parole troppo corte
        words = re.findall(r'\b\w{4,}\b', prompt.lower())
        for word in words:
            hashtags.add(f"#{word}")
    return " ".join(sorted(hashtags))

if uploaded_file:
    st.image(uploaded_file, caption='Immagine caricata', use_column_width=True)
    description = analyze_image(uploaded_file)
    
    st.subheader("Descrizione generata:")
    st.info(description)
    
    prompts = generate_music_prompts(description)
    
    st.subheader("Prompt musicali generati:")
    for i, prompt in enumerate(prompts, 1):
        st.code(f"{i}. {prompt}", language=None)
    
    hashtags = generate_hashtags(prompts)
    st.subheader("Hashtag suggeriti:")
    st.write(hashtags)
    
    all_prompts = "\n".join(prompts)
    st.download_button("Scarica i prompt generati", all_prompts, file_name="music_prompts.txt", mime="text/plain")
else:
    st.warning("Carica un'immagine per iniziare.")
