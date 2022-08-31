"""
Streamlit app - NLLB-200 translation demo for lyrics.
"""

import pandas as pd
import streamlit as st
from pathlib import Path

st.title("NLLB-200 translator for lyrics")

st.markdown("## What is this demo? 🤔")
st.markdown("> __*Translate your favorite songs in 200 languages with the NLLB-200 model!*__")

st.markdown("""
This demo lets you check how the NLLB-200 research model performs at translating lyrics. 
You can translate the lyrics in 200 languages, including low-resource languages. 

All translations were pre-generated using the NLLB-200 research model. Base lyrics are from Musixmatch.
"""
            )

st.markdown("## Translate a song 🎶")

# ====== load songs dataset from file ======
path_music_choice = "data/music_to_translate.txt"
df_music = pd.read_csv(path_music_choice, encoding='utf-8', delimiter=";", header=0, index_col=None)
df_music["title_formatted"] = df_music["title"] + ", by " + df_music["artist"]
# df_music

# select songs
song_titles = df_music["title"]
song_choices = df_music["title_formatted"].values.tolist()
select_song = st.selectbox(
    'Select a song',
    song_choices,
)
index_song = song_choices.index(select_song)
select_img_url = df_music["url_image"][index_song]

# show picture from selected url
col1_img, col2_img, col3_img = st.columns([1, 3, 1])
with col1_img:
    st.write(' ')
with col2_img:
    st.image(select_img_url)
with col3_img:
    st.write(' ')

# ====== load languages ======
df_lang = pd.read_csv("data/nllb-languages.txt", sep="|", encoding="latin-1", )
df_lang["language_formatted"] = df_lang["language"] + " [" + df_lang["code"] + "]"
lang_choices = df_lang["language_formatted"].values.tolist()

# select language
select_lang = st.selectbox(
    'Select a translation language',
    lang_choices,
    index=56,
)
index_lang = lang_choices.index(select_lang)

# ===== load right translations =====

# open right translation file
selected_title = df_music["title"][index_song]
selected_artist = df_music["artist"][index_song]
selected_lc = df_lang["code"][index_lang]
file_tr = f"data/translation/{selected_title}/{selected_artist}_{selected_title}_{selected_lc}.txt"
try:
    lyrics_translated = Path(file_tr).read_text()
except:
    print("Can't load the translation file.")
    lyrics_translated = "Sorry. Translation is not available. 😕"

# open right source file
file_src = f"data/source/{selected_artist}_{selected_title}.txt"
lyrics_src = Path(file_src).read_text()

# show lyrics
selected_tf = df_music["title_formatted"][index_song]
select_lf = df_lang["language_formatted"][index_lang]
src_lf = "English [eng_Latn]"
st.markdown(f"## {selected_tf} lyrics translation 🔁")

col1_lyrics, col2_lyrics = st.columns(2)
with col1_lyrics:
    st.markdown(f"### {src_lf}")
    st.text(lyrics_src)
with col2_lyrics:
    st.markdown(f"### {select_lf}")
    st.text(lyrics_translated)
