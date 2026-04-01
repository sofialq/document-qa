import streamlit as st
from openai import OpenAI
import requests
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# title and description
st.title("Song Recommendation Bot")
st.write("Test different api calls with text, images, and audio")
st.write(" ")

# initialize session state
if "text_response" not in st.session_state:
    st.session_state.text_response = None

if "url_response" not in st.session_state:
    st.session_state.url_response = None

if "uploaded_response" not in st.session_state:
    st.session_state.uploaded_response = None

if "audio_response" not in st.session_state:
    st.session_state.audio_response = None

st.subheader("Text Only Input")
st.write("Click the button for a random song recommendation")

# button for api call
if st.button("Recommend me a song"):
    text_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": "Recommend a random song- "
            "avoid popular choices. Describe the artist and genre. "
            "Provide one or two sentences on why you recommended this song. "
            "Keep consistent formatting."}
        ]
    )
    st.session_state.text_response = text_response.choices[0].message.content

# -------

# write response
if st.session_state.text_response:
    st.write(st.session_state.text_response)

st.subheader("Image URL Input")
st.write("Input an image url for a random song recommendation based off the analyzed vibe.")
url = st.text_input("Image URL", value="https://i.pinimg.com/736x/2c/93/17/2c93174ec1297a1cc460491c99c70ca8.jpg")

# button for api call
if st.button("Analyze URL Image + Recommend Song"):
    url_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": url, "detail": "auto"}},
                {"type": "text", "text": "Describe this image. Recommend a random song "
                "to match the image's vibe-avoid popular choices. "
                "Describe the artist and genre. "
            "Provide one or two sentences on why you recommended this song. "
            "Keep consistent formatting."}
            ]
        }]
    )
    st.session_state.url_response = url_response.choices[0].message.content

# write response
if st.session_state.url_response:
    st.write(st.session_state.url_response)

# -------

st.subheader("Image Upload Input")
st.write("Upload an image for a random song recommendation based off the analyzed vibe.")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "gif"])

if st.button("Analyze Uploaded Image +  Recommend Song") and uploaded:
    b64 = base64.b64encode(uploaded.read()).decode("utf-8")
    mime = uploaded.type  # e.g. "image/png"
    data_uri = f"data:{mime};base64,{b64}"

    uploaded_response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}},
                {"type": "text", "text": "Describe this image. Recommend a random song to match the image's vibe- " \
            "avoid popular choices. Describe the artist and genre. "
            "Provide one or two sentences on why you recommended this song. "
            "Keep consistent formatting."}
            ]
        }]
    )
    st.session_state.uploaded_response = uploaded_response.choices[0].message.content

# write response
if st.session_state.uploaded_response:
    st.write(st.session_state.uploaded_response)

# -----

st.subheader("Audio Input")
st.write("Input an audio file and have the bot describe it's vibe and provide similar song recommendations.")

uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if st.button("Analyze Uploaded Audio + Recommend Song") and uploaded_audio:
    uploaded_audio.seek(0)  # reset pointer before reading
    audio_b64 = base64.b64encode(uploaded_audio.read()).decode("utf-8")
    fmt = "mp3" if uploaded_audio.type == "audio/mpeg" else "wav"

    audio_response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "input_audio", "input_audio": {"data": audio_b64, "format": fmt}},
                {"type": "text", "text": "Describe what you hear in this audio. Recommend a random song to match. "
                 "Avoid popular choices. Describe the artist and genre. "
                 "Provide one or two sentences on why you recommended this song. "
                 "Keep consistent formatting."}
            ]
        }]
    )
    st.session_state.audio_response = audio_response.choices[0].message.content

# write response
if st.session_state.audio_response:
    st.write(st.session_state.audio_response)
