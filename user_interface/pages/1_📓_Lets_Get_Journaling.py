import wave
import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder, speech_to_text
from transcript_analysis import 

path = 'C:/Users/Work/OneDrive - University of Bath/ART-AI MRes Modules/CM50304 AI Challenge/project/'

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

        # with wave.open('output.wav', 'wb') as wf:
        #     wf.setnchannels(1)
        #     wf.setsampwidth(audio_sampwidth)
        #     wf.setframerate(audio_framerate)
        #     wf.writeframes(audio_bytes)

        # r = sr.Recognizer()
        # with sr.AudioFile('output.wav') as source:
        #     audio_data = r.record

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

