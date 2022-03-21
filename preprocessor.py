# import these modules
import json
import string
import pandas as pd
import regex as re
import argparse

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=argparse.FileType('r', encoding='UTF-8'),
                    required=True, help="specify the input json containing parsed git log output")
parser.add_argument('--output', required=False, default="output.csv", help="specify the output csv, default is output.csv")
args = parser.parse_args()

# Download required assets (will skip if already downloaded)
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
# Load JSON from file
f = open(args.input.name)
data = json.load(f)

args.input.close()

lemmatizer = WordNetLemmatizer()

# Get git commit messages from raw data by querying key 'message' for each entry in JSON data
messages = [i['message'] for i in data]

messagesWithoutUrls = [re.sub(r'http\S+', '', m) for m in messages]

# Remove punctuation from message strings
# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
messagesWithoutPunctuation = [m.translate(str.maketrans('', '', string.punctuation)) for m in messagesWithoutUrls]

# Remove numbers from message strings
messagesWithoutNumPunctuation = [m.translate(str.maketrans('', '', string.digits)) for m in messagesWithoutPunctuation]

# Normalize message strings (lowercase)
messagesWithoutNumPunctuationNormalized = [m.lower() for m in messagesWithoutNumPunctuation]


# Tokenize message strings, word by word
tokenizedMessages = [word_tokenize(m) for m in messagesWithoutNumPunctuationNormalized]

lemmatizedTokenizedMessages = []

for message in tokenizedMessages:
    lemmatizedTokenizedMessage = [lemmatizer.lemmatize(word) for word in message]
    lemmatizedTokenizedMessages.append(lemmatizedTokenizedMessage)

# allTokens = [word for message in tokenizedMessages for word in message]

restoredMessages = []
for tokenizedMessage in lemmatizedTokenizedMessages:
    message = ""
    for token in tokenizedMessage:
        message += f'{token} '
    restoredMessages.append(message)

df = pd.DataFrame(messages)
df.to_csv(args.output)
