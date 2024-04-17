import io
import wave
import streamlit as st
import speech_recognition as sr
import pickle
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from streamlit_mic_recorder import mic_recorder, speech_to_text
from utils.api_keys import openai_api
from utils.audio_to_emotion import emotion_classifier
from utils.transcript_analysis import transcript_analysis, prompt1, prompt2

path = 'C:/Users/Work/OneDrive - University of Bath/ART-AI MRes Modules/CM50304 AI Challenge/AI-Challenge/user_interface/'
entry_recorded = False

# Set the page title and icon
st.set_page_config(
    page_title="Welcome to FeelFlow!",
    page_icon=path + '/images/FeelFlow_logo.png'
)

# Preamble
st.image(path + '/images/FeelFlow.png')
st.write("""Whenever you're ready to record your journal entry, just click the button to start recording. 
         Once you're done, click the button again to finish the recording.""")

audio_data = None

def save_as_wav(audio_bytes, filepath, sample_width, sample_rate, num_channels):
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

# Set up a callback function that will save the audio journal recording.
def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

        audio_sampwidth = st.session_state.my_recorder_output['sample_width']
        audio_framerate = st.session_state.my_recorder_output['sample_rate']

        # r = sr.Recognizer()
        # audio_data = sr.AudioData(audio_bytes, sample_rate=audio_framerate, sample_width=audio_sampwidth)

        # text = r.recognize_google(audio_data)
        # st.write(text)

        today_date = datetime.now().strftime('%Y-%m-%d')
        audio_f = path + f'history/audio_{today_date}.wav'

        save_as_wav(audio_bytes, audio_f, audio_sampwidth, audio_framerate, 1)
        audio_wav = audio_f

        audio_to_prompt = transcript_analysis(openai_api, audio_wav)

        transcript = audio_to_prompt.prompt_gpt(prompt2)
        st.write('**Here is the transcript of your journal entry:**')
        st.write(transcript)

        summary = audio_to_prompt.prompt_gpt(prompt1)
        st.write("**Here is a summary of today's journal entry:**")
        st.write(summary)

        emotion_model = path + '/utils/models/mlp_emotion_classifier.pkl'
        audio_to_emotion = emotion_classifier(audio_wav, emotion_model)
        top_emotions = audio_to_emotion.top3emotions()
        emotion_prob = audio_to_emotion.weighted_emotions()

        emot_f = path + f'history/emotions_data_{today_date}.pkl'

        data_to_store = {'transcript': transcript, 'summary': summary, 'top_emotions': top_emotions, 'emotion_prob': emotion_prob}

        with open(emot_f, 'wb') as f:
            pickle.dump(data_to_store, f)

        st.write("**Your top three emotions based on your audio:**")
        emotions_html = ""
        for emotion in top_emotions:
            color = emotion_colours[emotion]
            emotions_html += f'<div style="background-color: {color}; width: 200px; height: 50px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center; margin-right: 20px; text-align: centre;"><h2>{emotion}</h2></div>'

        st.markdown(emotions_html, unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.clear()

        emotions = [emotion.capitalize() for emotion in top_emotions]
        probabilities = [emotion_prob[emotion] for emotion in top_emotions]
        colors = [emotion_colours[emotion] for emotion in top_emotions]

        ax.bar(emotions, probabilities, color=colors)
        ax.set_ylabel('Probability')
        ax.set_title('Top Three Emotions and Their Probabilities')

        st.pyplot(fig)

        st.write("**If you'd like, you can view some of your old journal content from the page below.**")

        if st.button("View My Past Journal Entries"):
            st.switch_page("pages/2_🗃️_Previous_Journal_Entries.py")
    
emotion_colours = {
    'sad': '#ADD8E6',       # Light blue (Pastel)
    'calm': '#98FB98',      # Light green (Pastel)
    'neutral': '#FFFFE0',   # Light yellow (Pastel)
    'angry': '#FFA07A',     # Light salmon (Pastel)
    'disgust': '#E6E6FA',   # Lavender (Pastel)
    'fearful': '#FFD700',   # Gold (Pastel)
    'happy': '#00FFFF',     # Light cyan (Pastel)
    'surprised': '#FFC0CB'  # Pink (Pastel)
}

# Implement the mic_recorder function. This appears as a button on the webpage. 
audio = mic_recorder(
    start_prompt="Record journal entry",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    format="wav",
    callback=callback,
    args=(),
    kwargs={},
    key='my_recorder'
)

    