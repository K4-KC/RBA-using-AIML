import nltk
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize, sent_tokenize

corpus = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget"

print(sent_tokenize(corpus))
print(word_tokenize(corpus))