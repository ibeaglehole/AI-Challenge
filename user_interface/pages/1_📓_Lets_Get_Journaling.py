import wave
import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder, speech_to_text
from utils.api_keys import openai_api
from utils.audio_to_emotion import emotion_classifier
from utils.transcript_analysis import transcript_analysis, prompt1

path = 'C:/Users/Work/OneDrive - University of Bath/ART-AI MRes Modules/CM50304 AI Challenge/AI-Challenge/'

# Preamble
st.image('FeelFlow.png')
st.write("""Whenever you're ready to record your journal entry, just click the button to start recording. 
         Once you're done, click the button again to finish the recording.""")

audio_data = None

# Set up a callback function that will save the audio journal recording.
def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

        audio_sampwidth = st.session_state.my_recorder_output['sample_width']
        audio_framerate = st.session_state.my_recorder_output['sample_rate']

        r = sr.Recognizer()
        audio_data = sr.AudioData(audio_bytes, sample_rate=audio_framerate, sample_width=audio_sampwidth)

        text = r.recognize_google(audio_data)
        st.write(text)

        audio_to_analyse = transcript_analysis(openai_api, audio_data)
        output = audio_to_analyse.prompt_gpt(prompt1)

        st.write(output)

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

