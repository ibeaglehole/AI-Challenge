import io
import wave
import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder, speech_to_text
from pages.utils.api_keys import openai_api
from pages.utils.audio_to_emotion import emotion_classifier
from pages.utils.transcript_analysis import transcript_analysis, prompt1

path = 'C:/Users/Work/OneDrive - University of Bath/ART-AI MRes Modules/CM50304 AI Challenge/AI-Challenge/user_interface/'

# Preamble
st.image(path + 'FeelFlow.png')
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

        r = sr.Recognizer()
        audio_data = sr.AudioData(audio_bytes, sample_rate=audio_framerate, sample_width=audio_sampwidth)

        text = r.recognize_google(audio_data)
        st.write(text)

        filepath = path + 'audio.wav'

        save_as_wav(audio_bytes, filepath, audio_sampwidth, audio_framerate, 1)
        audio_wav = filepath

        audio_to_prompt = transcript_analysis(openai_api, audio_wav)
        output = audio_to_prompt.prompt_gpt(prompt1)

        st.write(output)

        emotion_model = path + 'pages/utils/models/mlp_emotion_classifier.pkl'
        audio_to_emotion = emotion_classifier(audio_wav, emotion_model)
        top_emotions = audio_to_emotion.top3emotions()
        emotion_prob = audio_to_emotion.weighted_emotions()

        st.write(top_emotions)
        st.write(emotion_prob)

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

