prompt1=f"Summarise the following journal transcript into a few sentences. Give your answer by addressing the reader directly, \
    e.g. with language like 'In today's journal entry, you...'."

prompt2=f"Repeat the text I have just inputted. If there are any spelling/grammar mistakes, please correct these. Do not output any additonal text."

prompt3=f"Extract three tags from the following transcript which are not emotions. The output should be a list of single keywords \
    regarding what the user is talking about. For example, if the user was talking about a time when they went skiing, holiday \
        and skiing might be two of the keywords returned."

class transcript_analysis():

    def __init__(self, openai_api_key, audio_file):
        from openai import OpenAI

        self.audio_file = audio_file

        self.client = OpenAI(api_key=openai_api_key)

        journal = open(self.audio_file, 'rb')
        self.transcription = self.client.audio.transcriptions.create(
        model="whisper-1", 
        file=journal, 
        response_format="text"
        )
    
    def prompt_gpt(self, prompt):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, analysing journal entries to help users understand \
            feelings they might be experiencing."},
            {"role": "user", "content": f"{prompt} : {self.transcription}"}
        ]
        )
        return response.choices[0].message.content