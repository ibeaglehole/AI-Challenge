import streamlit as st
import os
import pickle
import matplotlib.pyplot as plt

path = 'C:/Users/Work/OneDrive - University of Bath/ART-AI MRes Modules/CM50304 AI Challenge/AI-Challenge/user_interface/'

# Load data from a pickle file
def load_data(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return(data)

def get_available_dates(directory):
    available_dates = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.pkl'):
            date = file_name.split('_')[-1].split('.')[0]
            available_dates.append(date)
            available_dates = sorted(available_dates)
            available_dates.reverse()
    return available_dates

def main():
    # Set the page title and icon
    st.set_page_config(
    page_title = "Welcome to FeelFlow!",
    page_icon = path + '/images/FeelFlow_logo.png'
    )

    st.image(path + '/images/FeelFlow.png')
    st.write('## View your previous journal entries here')
    st.write('Use the selection box in the left hand column to select your journal entries from past dates.')

    data_dir = path + 'history'
    dates = get_available_dates(data_dir)

    date = st.sidebar.selectbox("Select Date", dates)

    data_file_path = os.path.join(data_dir, f"emotions_data_{date}.pkl")
    if os.path.exists(data_file_path):
        data = load_data(data_file_path)
        st.write("**Data for", date + "**")
        st.write(data['summary'])

        top_emotions = data['top_emotions']
        emotion_prob = data['emotion_prob']

        st.write("**Your top three emotions based on your audio:**")
        emotions_html = ""
        for emotion in top_emotions:
            color = emotion_colours[emotion]
            emotions_html += f'<div style="background-color: {color}; width: 200px; height: 50px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center; margin-right: 20px; text-align: centre;"><h2>{emotion}</h2></div>'

        st.markdown(emotions_html, unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(4, 3))

        ax.clear()

        emotions = [emotion.capitalize() for emotion in top_emotions]
        probabilities = [emotion_prob[emotion] for emotion in top_emotions]
        colors = [emotion_colours[emotion] for emotion in top_emotions]

        ax.bar(emotions, probabilities, color=colors)
        ax.set_ylabel('Probability')
        ax.set_title('Top Three Emotions and Their Probabilities')

        st.pyplot(fig)

    else:
        st.write('No data available for', date)

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

if __name__ == '__main__':
    main()


