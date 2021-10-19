import pandas as pd
# import nltk

import langdetect as ld

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('words')

# To Display all Columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 700)

date_cols = ['timestamp']
dtypes = {'text': str, 'timestamp': str, 'user': str}
df_raw = pd.read_csv(r'C:\Users\Ryan\Desktop\tweets.csv',
                     encoding='UTF-8',
                     usecols=["text", "timestamp", "user"],
                     dtype=dtypes,
                     parse_dates=date_cols,
                     low_memory='false',
                     sep=";")


counter = 0
length = len(df_raw['text'])


def is_english(text):
    global counter
    counter += 1

    if counter % 10000 == 0:
        print("Completed: " + str(counter) + "/" + str(length))

    try:
        return ld.detect(text) == 'en'
    except:
        return False


# Removing non-English Tweets
df_english = df_raw[df_raw['text'].apply(is_english)]

# Creating a column named date of data type date time
df_english['date'] = pd.to_datetime(df_english['timestamp'], format='%Y-%m-%d').dt.date
df_english = df_english.sort_values(by='date')

# Setting an index
df_english = df_english.set_index('date')

# Cutting off tweets which are out of range - df['Date'].date.year > '2017'
startDate = pd.to_datetime("2017-01-01").date()
df_english = df_english.loc[startDate:]

print(df_english.isnull().sum())
df_english.dropna(how='any', inplace=True)

print("Size: " + str(df_english['text'].size))
print("Length: " + str(len(df_english['text'])))

print(df_english)

df_english.to_csv(r'C:\Users\Ryan\Desktop\english_tweets_no_duplicates.csv')


