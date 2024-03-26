class emotion_classifier():
    
    def __init__(self, audio_fp, model_fp = None):
        import joblib, warnings
        from os import getcwd
        
        warnings.filterwarnings("ignore")
        
        if model_fp is None:
            model_fp = getcwd() + '/utils/models/mlp_emotion_classifier.pkl'

        self.file_name = audio_fp
        self.model = joblib.load(model_fp)
        self.possible_emotions = [emotion.split('_')[0] for emotion in self.model.classes_][::2]

    def extract_features(self):
        """Function Extracts Features from WAV file"""
        import librosa, numpy as np

        X, sample_rate = librosa.load(self.file_name)
        stft=np.abs(librosa.stft(X))
        result=np.array([])
        mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
        result=np.hstack((result, mfccs))
        chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        result=np.hstack((result, chroma))
        mel=np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
        result=np.hstack((result, mel))
        return result
    
    def extract_prob_emotions(self):
        import pandas as pd

        features = self.extract_features()
        prob_emotions = pd.Series(self.model.predict_proba(features.reshape(1, -1))[0],
                                  index=self.model.classes_).sort_values(ascending=False)
        return prob_emotions

    def top3emotions(self):
        prob_emotions = self.extract_prob_emotions()
        top3 = []
        for entry in prob_emotions.index:
            emotion = entry.split('_')[0]
            if emotion not in top3 and len(top3) < 3:
                top3.append(emotion)
                
        return top3
    
    def weighted_emotions(self):
        prob_emotions = self.extract_prob_emotions()
        total_prob_emotions = {}
        
        for index, prob in prob_emotions.items():
            emotion = index.split('_')[0]
            if emotion in total_prob_emotions:
                total_prob_emotions[emotion] += prob
            else:
                total_prob_emotions[emotion] = prob

        return total_prob_emotions