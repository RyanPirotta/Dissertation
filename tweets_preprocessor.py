import pandas as pd
import re
import nltk
import contractions

from nltk.corpus import stopwords, words
from nltk import TweetTokenizer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer

nltk.download('stopwords')
nltk.download('punkt')
# nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')

# To Display all Columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 700)

# Setting Stop Words and Words from nltk.corpus
stop_words = set(stopwords.words('english'))
word_set = set(words.words())

# analyzer = SentimentIntensityAnalyzer()
tokenizer = TweetTokenizer()
detokenizer = TreebankWordDetokenizer()
lemmatizer = nltk.WordNetLemmatizer()


def remove_punctuation(words):
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def lemmatize_text(text):
    return [(lemmatizer.lemmatize(w)) for w in tokenizer.tokenize(text)]


def detokenize_text(tokenized):
    return detokenizer.detokenize(tokenized)


def remove_URL(sample):
    return re.sub("(?P<url>https?://[^\s]+)", "", sample)


def get_hashtag_text(word):
    global word_set
    if not word.startswith("#"):
        return word

    # remove hashtag
    word = word[1:]
    return word if word in word_set else ""


# function to remove numbers
def remove_numbers(text):
    # define the pattern to keep
    pattern = r'[^a-zA-z.,!?/:;\"\'\s]'
    return re.sub(pattern, '', text)


def preprocess_tweets(text):
    global counter
    counter += 1

    if counter % 10000 == 0:
        print("Completed: " + str(counter) + "/" + str(length))

    # Capitalisation
    text = text.lower()

    # Remove non-alphanumeric
    text = remove_numbers(text)

    # Substituting multiple spaces with single space
    text = re.sub(r'\s+', ' ', text, flags=re.I)

    # Remove picture URL
    text = re.sub(r'pic.twitter.com/[\w]*', "", text)

    # remove url
    text = remove_URL(text)

    # Fix Contractions
    expanded_words = []
    for word in text.split():
        # using contractions.fix to expand the shortened words
        expanded_words.append(contractions.fix(word))
    text = ' '.join(expanded_words)

    # lemmatize
    tokenized = lemmatize_text(text)

    # keep only hashtags in english dictionary
    tokenized = [get_hashtag_text(word) for word in tokenized if get_hashtag_text(word) != '']

    # remove stop words
    tokenized = [word for word in tokenized if word not in stop_words]

    # for each token
    for index, word in enumerate(tokenized):
        # if mentions
        if word.startswith("@"):
            tokenized[index] = "USER"

    # remove punctuation
    tokenized = remove_punctuation(tokenized)

    return detokenize_text(tokenized)


def count_words(sentence):
    sentence = str(sentence)
    return len(sentence.split())


if __name__ == "__main__":

    df_english = pd.read_csv(r'C:\Users\Ryan\Desktop\english_tweets_no_duplicates.csv',
                             encoding='UTF-8',
                             low_memory='false')

    counter = 0
    length = len(df_english['text'])

    print(length)

    # Pre-processing Tweets
    df_english['text'] = df_english['text'].apply(preprocess_tweets)

    # Dropping Duplicates tweets by the same user since numbers were removed - THIS IS THE PREFERRED APPROACH
    df_english = df_english.drop_duplicates(subset=['text', 'user']).reset_index()

    # Removing words with less than 3 letters
    df_english = df_english[df_english['text'].map(count_words) > 3]

    print(df_english)

    # Removing Tweets not containing the word 'bitcoin' or 'btc'
    df_english.drop(df_english[df_english['text'].str.contains('btc|bitcoin') == False].index, axis=0, inplace=True)

    print(df_english)

    df_english = df_english[['user', 'timestamp', 'text']]

    print(df_english)

    df_english.to_csv(r'C:\Users\Ryan\Desktop\preprocessed_tweets.csv')


