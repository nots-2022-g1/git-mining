# import these modules
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')

f = open('angular.json')
data = json.load(f)

lemmatizer = WordNetLemmatizer()

messages = []

for i in data:
    messages.append(i['message'])

tokenizedMessages = []

for m in messages:
    tokenizedMessages.append(word_tokenize(m))

print(tokenizedMessages[0])

# for word in tokenizedMessages[0]:
# print(lemmatizer.lemmatize(word))

tokenizedMessages[0] = [lemmatizer.lemmatize(m) for m in tokenizedMessages[0]]


print(tokenizedMessages[0])

print("better :", lemmatizer.lemmatize("better", pos="a"))
