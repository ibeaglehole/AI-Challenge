# https://github.com/B4PT0R/streamlit-mic-recorder

import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title('FeelFlow')
st.write('Your AI-powered journaling companion')

my_recorder_output = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    format="webm",
    callback=None,
    args=(),
    kwargs={},
    key=None
)

def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

mic_recorder(key='my_recorder', callback=callback)