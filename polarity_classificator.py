import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')

# To Display all Columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 700)

df_cleaned = pd.read_csv(r'C:\Users\Ryan\Desktop\preprocessed_tweets.csv',
                         encoding='UTF-8',
                         low_memory='false')

print(df_cleaned)

analyzer = "vader"
# analyzer = "textBlob"

# Polarity using Vader Analyzer
if analyzer == "vader":
    vader = SentimentIntensityAnalyzer()
    df_cleaned['neg'] = df_cleaned['text'].apply(lambda x: vader.polarity_scores(x)['neg'])
    df_cleaned['neu'] = df_cleaned['text'].apply(lambda x: vader.polarity_scores(x)['neu'])
    df_cleaned['pos'] = df_cleaned['text'].apply(lambda x: vader.polarity_scores(x)['pos'])
    df_cleaned["compound"] = df_cleaned['text'].apply(lambda x: vader.polarity_scores(x)['compound'])
    df_cleaned['comp_score'] = df_cleaned['compound'].apply(lambda c: 1 if c >= 0.05 else (-1 if c <= -0.05 else 0))

elif analyzer == "textBlob":

    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity


    def get_polarity(text):
        return TextBlob(text).sentiment.polarity


    def get_analysis(text):
        testimonial = TextBlob(text)
        return testimonial.sentiment


    # Create two new columns ‘Subjectivity’ & ‘Polarity’
    df_cleaned['Subjectivity'] = df_cleaned['text'].apply(get_subjectivity)
    df_cleaned['Polarity'] = df_cleaned['text'].apply(get_polarity)
    df_cleaned['score'] = df_cleaned['Polarity'].apply(lambda c: 1 if c >= 0.05 else (-1 if c <= -0.05 else 0))

print(df_cleaned)

df_cleaned.to_csv(r'C:\Users\Ryan\Desktop\classified_tweets.csv')
