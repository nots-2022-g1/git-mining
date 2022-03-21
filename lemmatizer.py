# import these modules
import json
import string
import pandas as pd
import regex as re

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required assets (will skip if already downloaded)
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

# Load JSON from file
f = open('angular.json')
data = json.load(f)

lemmatizer = WordNetLemmatizer()

# Get git commit messages from raw data by querying key 'message' for each entry in JSON data
messages = [i['message'] for i in data]

# Remove punctuation from message strings
# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
messagesWithoutUrls = [re.sub(r'http\S+', '', m) for m in messages]
messagesWithoutPunctuation = [m.translate(str.maketrans('', '', string.punctuation)) for m in messagesWithoutUrls]
messagesWithoutNumPunctuation = [m.translate(str.maketrans('', '', string.digits)) for m in messagesWithoutPunctuation]
messagesWithoutNumPunctuationNormalized = [m.lower() for m in messagesWithoutNumPunctuation]

# Remove numbers from message strings since we won't be using them for now
# messagesWithoutPunctuationAndNumbers = ''.join(i for i in messagesWithoutPunctuation if not i.isdigit())

# Tokenize message strings, word by word
tokenizedMessages = [word_tokenize(m) for m in messagesWithoutNumPunctuationNormalized]

lemmatizedTokenizedMessages = []

for message in tokenizedMessages:
    lemmatizedTokenizedMessage = [lemmatizer.lemmatize(word) for word in message]
    lemmatizedTokenizedMessages.append(lemmatizedTokenizedMessage)
# Lemmatize tokenized message strings
# lemmatizedMessages = [word for message in tokenizedMessages for word in message]

restoredMessages = []
for tokenizedMessage in lemmatizedTokenizedMessages:
    message = ""
    for token in tokenizedMessage:
        message += f'{token} '
    restoredMessages.append(message)

df = pd.DataFrame(messages)
df.to_csv('angular.original.csv')

# print(restoredMessages[0])
