def program(exp_no):
    if exp_no == 1:
        print("""\
pip install nltk
import nltk

# Check the NLTK version
print(nltk.__version__)

# Download the 'brown' corpus and access some data
nltk.download('brown')
from nltk.corpus import brown

# Print first 10 words from the 'brown' corpus
print(brown.words()[:10])

# Get all categories and total number of categories
categories = brown.categories()
total_categories = len(categories)

print(f"Total number of categories in the Brown Corpus: {total_categories}")
print(f"Categories: {categories}")

# Get sentences and tagged sentences from the 'government' category
government_sentences = brown.sents(categories='government')
print(government_sentences)

tagged_word = brown.tagged_sents(categories='government')
print(tagged_word)

# Display the first 5 sentences from the 'government' category
for i in range(5):
    sentence = ' '.join(government_sentences[i])
    print(f"Sentence {i + 1}: {sentence}")

# Get tagged words from the 'government' category
tagged_words = brown.tagged_words(categories='government')
print(tagged_words)

# Print all file IDs and the government category file IDs
all_file_ids = brown.fileids()
print("All file IDs:", all_file_ids)

government_file_ids = brown.fileids(categories='government')
print("Government file IDs:", government_file_ids)

# Display the first 10 words from a specific file
words = brown.words(fileids=['ch22'])
print(words[:10])

# Frequency distribution for modal verbs in the 'government' category
from nltk import FreqDist

text = brown.words(categories='government')
fdist = FreqDist(w.lower() for w in text)

modals = ['can', 'could', 'may', 'might', 'must', 'will']

for m in modals:
    print(f"{m}: {fdist[m]}")

# POS tagging of 'news' text
from nltk import pos_tag
news_text = brown.words(categories='news')
nltk.download('averaged_perceptron_tagger')

tagged_words = pos_tag(news_text)
nouns = [word for word, pos in tagged_words if pos in ['NN', 'NNS']]
print(nouns[:10])

# Working with Reuters corpus
from nltk.corpus import reuters
nltk.download('reuters')

print(reuters.fileids())
print(reuters.categories())
print(len(reuters.categories()))

# Named Entity Recognition
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

text = "Barack Obama was born in Hawaii."
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
named_entities = nltk.chunk.ne_chunk(tagged)
print(named_entities)

# Get raw document text from a specific file in Reuters corpus
file_id = 'test/15017'
document_text = reuters.raw(file_id)
tokens = nltk.word_tokenize(document_text)
tagged = pos_tag(tokens)
named_entities = nltk.chunk.ne_chunk(tagged)
print(named_entities)

# Synsets and definitions for a word using WordNet
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

def get_synsets(word):
    synsets = wn.synsets(word)
    return synsets

word = "economy"
synsets = get_synsets(word)

print(f"Synsets for the word '{word}':")
for synset in synsets:
    print(f"{synset.name()}: {synset.definition()}")
""")
    elif exp_no == 2:
        print("""\
# Simple string concatenation
simple_string = 'hello' + " I'm a simple string"
print(simple_string)

# Multi-line string
multi_line_string = '''Hello I'm
a multi-line
string!'''
print(multi_line_string)

# Multi-line string using concatenation
multi_line_string = "Hello I'm\n" + \
                    "a multi-line\n" + \
                    "string!"
print(multi_line_string)

# Raw string
raw_string = r'D:\\2023-24 Even\\NLP Lab\\file.txt'
print(raw_string)

# String concatenation
print('Hello' + ' and welcome ' + 'to AI!')
print('Hello' ' and welcome ' 'to AI-ML!')

s1 = 'AI!'
print('Hello ' + s1)

# String repetition
s2 = '--Machine Learning--'
print((s1 + s2) * 3)

# Concatenating several strings using parentheses
s3 = ('This '
      'is another way '
      'to concatenate '
      'several strings!')
print(s3)

# Checking substring existence
print('way' in s3)
print('python' in s3)
print('ve' in s3)

# String length and indexing
print(len(s3))
s = 'PYTHON'
for index, character in enumerate(s):
    print('Character', character + ':', 'has index:', index)

print(s[0], s[1], s[2], s[3], s[4], s[5])
print(s[-1], s[-2], s[-3], s[-4], s[-5], s[-6])

# Slicing
print(s[:])
print(s[1:4])
print(s[:3])
print(s[3:])
print(s[-3:])
print(s[:3] + s[3:])
print(s[:3] + s[-3:])

# String transformations
s = 'python is great'
print(s.capitalize())
print(s.upper())
print(s.replace('python', 'analytics'))

# Splitting and joining strings
s = 'I,am,a,comma,separated,string'
print(s.split(','))
print(' '.join(s.split(',')))

# Stripping spaces
s = '   I am surrounded by spaces    '
print(s)
print(s.strip())

# Title case
s = 'this is in lower case'
print(s.title())

# Regular expressions
import re
print(re.findall(r'\\w+', s))

# Unicode string
s = u'H\\u00e8llo'
print(re.findall(r'\\w+', s, re.UNICODE))

# Regex match, search, findall, and substitution examples
pattern = 'Python'
s1 = 'Python is an excellent language'
s2 = 'I love the Python language. I also use Python to build applications at work!'

# match only returns a match if regex match is found at the beginning of the string
print(re.match(pattern, s1))
print(re.match(pattern, s2))
print(re.match(pattern, s1, flags=re.IGNORECASE))

# search returns the first match anywhere in the string
print(re.search(pattern, s2, re.IGNORECASE))
print(re.findall(pattern, s2, re.IGNORECASE))

# NLTK treebank corpus example
import nltk
nltk.download('treebank')
from nltk.corpus import treebank

# Accessing sentences from the treebank corpus
sentences = treebank.sents()
print(sentences[0])

# Accessing tagged words
tagged_words = treebank.tagged_words()
print(tagged_words[:10])

# Accessing parsed trees
parsed_trees = treebank.parsed_sents()
print(parsed_trees[0])

# More regex examples
text = "The quick brown fox jumps over the lazy dog. The fox is quick and clever."

# Find all occurrences of the word 'fox'
pattern = r'fox'
matches = re.findall(pattern, text)
print("Find all 'fox':", matches)

# Search for the first occurrence of the word 'quick'
search_result = re.search(r'quick', text)
print("Search for 'quick':", search_result.group() if search_result else "Not found")

# Match the word 'The' at the beginning of the string
match_result = re.match(r'The', text)
print("Match 'The' at the beginning:", match_result.group() if match_result else "Not found")

# Substitute all occurrences of 'fox' with 'cat'
substituted_text = re.sub(r'fox', 'cat', text)
print("Substitute 'fox' with 'cat':", substituted_text)

# Find all numbers in the text
text = "The 1 quick brown fox jumped over 2 lazy dogs."
numbers = re.findall(r'\\d+', text)
print("Find all numbers:", numbers)

# Find all words with letters only (no numbers)
words = re.findall(r'[a-zA-Z]+', text)
print("Find all words:", words)

# Find all emails and URLs in a sample string
text = "Email me at example.email@domain.com or visit http://example.com."

# Find all email addresses
emails = re.findall(r'\\b[\\w\\.-]+@[\\w\\.-]+\\.\\w+\\b', text)
print("Find all emails:", emails)

# Find all URLs
urls = re.findall(r'http://[\\w\\./]+', text)
print("Find all URLs:", urls)
""")
    elif exp_no ==3:
        print("""\
import nltk
nltk.download("gutenberg")
nltk.download("punkt")
from nltk.corpus import gutenberg
from pprint import pprint
alice = gutenberg.raw(fileids='carroll-alice.txt')
sample_text = 'We will discuss briefly about the basic syntax,\
 structure and design philosophies. \
 There is a defined hierarchical syntax for Python code which you should remember \
 when writing code! Python is a really powerful programming language!'
default_st = nltk.sent_tokenize
alice_sentences = default_st(text=alice)
sample_sentences = default_st(text=sample_text)
print ('Total sentences in sample_text:', len(sample_sentences))
print ('Sample text sentences :-')
pprint(sample_sentences)
print ('\nTotal sentences in alice:', len(alice_sentences))
print ('First 5 sentences in alice:-')
pprint(alice_sentences[0:5])
sentence = "The brown fox wasn't that quick and he couldn't win the race"
default_wt = nltk.word_tokenize
words = default_wt(sentence)
print (words)
treebank_wt = nltk.TreebankWordTokenizer()
words = treebank_wt.tokenize(sentence)
print (words)
TOKEN_PATTERN = r'\w+'        
regex_wt = nltk.RegexpTokenizer(pattern=TOKEN_PATTERN,
                                gaps=False)
words = regex_wt.tokenize(sentence)
print (words)
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
tokens = nltk.word_tokenize(sentence)
tagged_sent = nltk.pos_tag(tokens, tagset='universal')
print (tagged_sent)
from nltk.corpus import treebank
nltk.download('treebank')
data = treebank.tagged_sents()
train_data = data[:3500]
test_data = data[3500:]
print (train_data[0])
from nltk.tag import DefaultTagger
dt = DefaultTagger('NN')
print (dt.evaluate(test_data))
print (dt.tag(tokens))
import nltk
import re
import string
from pprint import pprint
corpus = ["The brown fox wasn't that quick and he couldn't win the race",
          "Hey that's a great deal! I just bought a phone for $199",
          "@@You'll (learn) a **lot** in the book. Python is an amazing language!@@"]
def tokenize_text(text):
    sentences = nltk.sent_tokenize(text)
    word_tokens = [nltk.word_tokenize(sentence) for sentence in sentences] 
    return word_tokens
    
token_list = [tokenize_text(text) 
              for text in corpus]
pprint(token_list)
print
def remove_characters_after_tokenization(tokens):
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens])
    return filtered_tokens
    
filtered_list_1 =  [filter(None,[remove_characters_after_tokenization(tokens) 
                                for tokens in sentence_tokens]) 
                    for sentence_tokens in token_list]
print (filtered_list_1)
print 
print (corpus[0].lower())
print (corpus[0].upper())
nltk.download('stopwords')
def remove_stopwords(tokens):
    stopword_list = nltk.corpus.stopwords.words('english')
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    return filtered_tokens
    cleaned_corpus_tokens = [tokenize_text(text)
                          for text in corpus]    
filtered_list_3 =  [[remove_stopwords(tokens) 
                        for tokens in sentence_tokens] 
                        for sentence_tokens in corpus]
print (filtered_list_3)
print 
from nltk.stem import PorterStemmer
ps = PorterStemmer()
print (ps.stem('jumping'), ps.stem('jumps'), ps.stem('jumped'))
print (ps.stem('lying'))
print (ps.stem('strange'))
CONTRACTION_MAP = { 
"isn't": "is not", 
"aren't": "are not", 
"can't": "cannot", 
"can't've": "cannot have", 
"you'll've": "you will have", 
"you're": "you are", 
"you've": "you have" 
}
import contractions

def expand_contractions(sentence):
    return contractions.fix(sentence)

# Example usage:
cleaned_corpus = ["I'm going to the store.", "You're amazing!"]
expanded_corpus = [expand_contractions(sentence) for sentence in cleaned_corpus]
print(expanded_corpus)
pip install contractions
import re

CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
}

def expand_contractions(sentence, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), flags=re.IGNORECASE | re.DOTALL)
    
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction
    
    expanded_sentence = contractions_pattern.sub(expand_match, sentence)
    return expanded_sentence

cleaned_corpus = ["I'm going to the store.", "You're amazing!"]
expanded_corpus = [expand_contractions(sentence, CONTRACTION_MAP) for sentence in cleaned_corpus]
print(expanded_corpus)                            
""")
    elif exp_no == 4:
        print("""\
CORPUS = [
'the sky is blue',
'sky is blue and sky is beautiful',
'the beautiful sky is so blue',
'i love blue cheese'
]
new_doc = ['loving this blue sky today']
pip install scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
vectorizer
CORPUS = [
'the sky is blue',
'sky is blue and sky is beautiful',
'the beautiful sky is so blue',
'love blue cheese'
]
X = vectorizer.fit_transform(CORPUS)
X
vocabulary=vectorizer.get_feature_names_out()
print (vocabulary)
X.toarray()
vectorizer.vocabulary_.get('beautiful')

bigram_vectorizer = CountVectorizer(ngram_range=(1, 2))
analyze = bigram_vectorizer.build_analyzer()
analyze('the sky is blue')

X1= bigram_vectorizer.fit_transform(CORPUS).toarray()
X1
feature_index = bigram_vectorizer.vocabulary_.get('is blue')
feature_index

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
pipe = Pipeline([('count', CountVectorizer(vocabulary=vocabulary)),('tfid', TfidfTransformer())]).fit(CORPUS)
pipe['count'].transform(CORPUS).toarray()
pipe['tfid'].idf_
from sklearn.feature_extraction.text import TfidfVectorizer
corpus = [
     'This is the first document.',
     'This document is the second document.',
     'And this is the third one.',
     'Is this the first document?',
 ]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print (X)

print (vectorizer.get_feature_names_out())
print(X.shape)
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample corpus
corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?'
]

# Create a TfidfVectorizer that considers both unigrams and bigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # (1, 2) means unigrams and bigrams
X = vectorizer.fit_transform(corpus)

# Print the feature names (unigrams and bigrams)
print(vectorizer.get_feature_names_out())

# Print the TF-IDF matrix
print(X.toarray())
corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?'
]
vectorizer_trigrams = TfidfVectorizer(ngram_range=(1, 3))  # unigrams, bigrams, and trigrams
X_trigrams = vectorizer_trigrams.fit_transform(corpus)
print("Unigrams, Bigrams, and Trigrams:")
print(vectorizer_trigrams.get_feature_names_out())
print(X_trigrams.toarray())
print("\n")
vectorizer_min_df = TfidfVectorizer(min_df=2)  # Terms must appear in at least 2 documents
X_min_df = vectorizer_min_df.fit_transform(corpus)
print("Min DF (terms appear in at least 2 documents):")
print(vectorizer_min_df.get_feature_names_out())
print(X_min_df.toarray())
print("\n")
vectorizer_stop_words = TfidfVectorizer(stop_words='english')  # Removing common English stop words
X_stop_words = vectorizer_stop_words.fit_transform(corpus)
print("Stop Words Removed:")
print(vectorizer_stop_words.get_feature_names_out())
print(X_stop_words.toarray())
print("\n")
vectorizer_max_df = TfidfVectorizer(max_df=0.8)  # Terms appear in no more than 80% of documents
X_max_df = vectorizer_max_df.fit_transform(corpus)
print("Max DF (terms appear in no more than 80% of documents):")
print(vectorizer_max_df.get_feature_names_out())
print(X_max_df.toarray())
print("\n")
# 6. Limiting Vocabulary Size (Top 5 terms by frequency)
vectorizer_limited_vocab = TfidfVectorizer(max_features=5)  # Use only the top 5 terms by frequency
X_limited_vocab = vectorizer_limited_vocab.fit_transform(corpus)
print("Top 5 Terms by Frequency:")
print(vectorizer_limited_vocab.get_feature_names_out())
print(X_limited_vocab.toarray())
print("\n")                                                                                    
""")
    elif exp_no == 5:
        print("""\
import pandas as pd
data = pd.read_csv('spam.csv', encoding='latin-1')
data.head()
data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
data.columns = ['label', 'text']
data.head()
data.isna().sum()
data.shape
import nltk
nltk.download('all')
text = list(data['text'])                            
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
corpus = []
for i in range(len(text)):
    r = re.sub('[^a-zA-Z]', ' ', text[i])
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    corpus.append(r)
data['text'] = corpus
data.head()
X = data['text']
y = data['label']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)
print('Training Data :', X_train.shape)
print('Testing Data : ', X_test.shape)              
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)
X_train_cv.shape
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train_cv, y_train)
X_test_cv = cv.transform(X_test)
predictions = lr.predict(X_test_cv)
predictions
import pandas as pd
from sklearn import metrics
df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions), index=['ham','spam'], columns=['ham','spam'])
df
import pandas as pd
data = pd.read_csv('Tweets.csv', encoding='latin-1')
data.head()
print(data.columns)
data.drop(['negativereason_confidence', 'airline', 'airline_sentiment_gold', 'name', 
           'negativereason_gold', 'retweet_count', 'tweet_coord', 'tweet_created', 
           'tweet_location', 'user_timezone'], axis=1, inplace=True, errors='ignore')
data.columns = ['airline_sentiment', 'text']
data.head()
data.isna().sum()
data.shape
pip install matplotlib
import matplotlib.pyplot as plt
data['airline_sentiment'].value_counts(normalize = True).plot.bar()
plt.show()
text = list(data['text'])
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
corpus = []
for i in range(len(text)):
    r = re.sub('[^a-zA-Z]', ' ', text[i])
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    corpus.append(r)
data['text'] = corpus
data.head()
X = data['text']
y = data['airline_sentiment']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)
print('Training Data :', X_train.shape)
print('Testing Data : ', X_test.shape)
print('Training Label:',y_train.shape)
print('Test Label:',y_test.shape)
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)
X_train_cv.shape
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train_cv, y_train)
X_test_cv = cv.transform(X_test)
predictions = lr.predict(X_test_cv)
predictions                                                                                                                                                                        
import pandas as pd
from sklearn import metrics
df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['neutral','positive','negative'], columns=['neutral','positive','negative'])
df
from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, predictions, target_names=['neutral','positive','negative']))
print(confusion_matrix(y_test, predictions))              
""")
    elif exp_no == 6:
        print("""\
#EXP 6 Perform text summarization for sample dataset
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
text = '''he Elder Scrolls V: Skyrim is an open world action role-playing video game
developed by Bethesda Game Studios and published by Bethesda Softworks.
It is the fifth installment in The Elder Scrolls series, following
The Elder Scrolls IV: Oblivion. Skyrim&#39;s main story revolves around
the player character and their effort to defeat Alduin the World-Eater,
a dragon who is prophesied to destroy the world.
The game is set two hundred years after the events of Oblivion
and takes place in the fictional province of Skyrim. The player completes quests
and develops the character by improving skills.
Skyrim continues the open world tradition of its predecessors by allowing the
player to travel anywhere in the game world at any time, and to
ignore or postpone the main storyline indefinitely. The player may freely roam
over the land of Skyrim, which is an open world environment consisting

of wilderness expanses, dungeons, cities, towns, fortresses and villages.
Players may navigate the game world more quickly by riding horses,
or by utilizing a fast-travel system which allows them to warp to previously
Players have the option to develop their character. At the beginning of the game,
players create their character by selecting one of several races,
including humans, orcs, elves and anthropomorphic cat or lizard-like creatures,
and then customizing their character&#39;s appearance.discovered locations. Over the
course of the game, players improve their character&#39;s skills, which are numerical
representations of their ability in certain areas. There are eighteen skills
divided evenly among the three schools of combat, magic, and stealth.
Skyrim is the first entry in The Elder Scrolls to include Dragons in the game&#39;s
wilderness. Like other creatures, Dragons are generated randomly in the world
and will engage in combat.'''

import nltk
nltk.download('stopwords')
nltk.download('punkt')
# Tokenizing the text
stopWords = set(stopwords.words('english'))
words = word_tokenize(text)
# Creating a frequency table to keep the score of each word

freqTable = dict()
for word in words:
 word = word.lower()
 if word in stopWords:
  continue
 if word in freqTable:

  freqTable[word] += 1
 else:
  freqTable[word] = 1

sentences = sent_tokenize(text)
sentenceValue = dict()

for sentence in sentences:
 for word, freq in freqTable.items():

    if word in sentence.lower():

        if sentence in sentenceValue:

           sentenceValue[sentence] += freq
        else:
                 sentenceValue[sentence] = freq
sumValues = 0
for sentence in sentenceValue:
 sumValues += sentenceValue[sentence]

average = int(sumValues / len(sentenceValue))

summary=''
for sentence in sentences:
  if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
   summary += "" + sentence

print(summary)
""")

    elif exp_no == 7:
        print("""\
#EXP 7 Work with topic modelling
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample documents
doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

doc_complete = [doc1, doc2, doc3, doc4, doc5]

# Preprocessing
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

# Convert documents into document-term matrix for LDA and LSI
# Here, `doc_clean` is a list of strings, each representing a cleaned document
doc_clean_tokenized = [doc.split() for doc in doc_clean]
dictionary = corpora.Dictionary(doc_clean_tokenized)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean_tokenized]

# LDA Model
lda_model = gensim.models.LdaModel(doc_term_matrix, num_topics=3, id2word=dictionary, passes=50)
print("\nLDA Model Topics:\n")
for idx, topic in lda_model.print_topics(num_topics=3, num_words=3):
    print(f"Topic {idx + 1}: {topic}")

# LSI Model
lsi_model = gensim.models.LsiModel(doc_term_matrix, num_topics=3, id2word=dictionary)
print("\nLSI Model Topics:\n")
for idx, topic in lsi_model.print_topics(num_topics=3, num_words=3):
    print(f"Topic {idx + 1}: {topic}")

# NMF Model
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(doc_clean)
nmf_model = NMF(n_components=3, random_state=1)
nmf_model.fit(tfidf)
tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()

print("\nNMF Model Topics:\n")
for topic_idx, topic in enumerate(nmf_model.components_):
    print(f"Topic {topic_idx + 1}: ", " ".join([tfidf_feature_names[i] for i in topic.argsort()[:-4:-1]]))

# Comparison of Topics
print("\nComparison of LDA, LSI, and NMF Topics:\n")
for i in range(3):
    lda_topic = lda_model.print_topic(i, 3)
    lsi_topic = lsi_model.print_topic(i, 3)
    nmf_topic = " ".join([tfidf_feature_names[j] for j in nmf_model.components_[i].argsort()[:-4:-1]])
    print(f"Topic {i + 1} (LDA): {lda_topic}")
    print(f"Topic {i + 1} (LSI): {lsi_topic}")
    print(f"Topic {i + 1} (NMF): {nmf_topic}")


""")    
        
    elif exp_no == 8:
        print('''\
#EXP 8 Analyze text similarity using various measures
def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two lists """
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)
sentences = ["The bottle is empty",
"There is nothing in the bottle"]
sentences = [sent.lower().split(" ")
             for sent in sentences]
jaccard_similarity(sentences[0], sentences[1])
print(jaccard_similarity(sentences[0], sentences[1]))



import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
X ="I love horror movies"
Y ="Lights out is a horror movie"
nltk.download('punkt_tab')
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)

# sw contains the list of stopwords
sw = stopwords.words('english')
l1 =[];l2 =[]

X_set = {w for w in X_list if not w in sw}
Y_set = {w for w in Y_list if not w in sw}

rvector = X_set.union(Y_set)
for w in rvector:
    if w in X_set: l1.append(1)
    else: l1.append(0)
    if w in Y_set: l2.append(1)
    else: l2.append(0)
c = 0

for i in range(len(rvector)):
        c+= l1[i]*l2[i]
cosine = c / float((sum(l1)*sum(l2))**0.5)
print("similarity: ", cosine)

def overlapping_coefficient(text1, text2):
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    intersection = len(set1.intersection(set2))
    return intersection / min(len(set1), len(set2))

text1 = "I love programming in Python"
text2 = "Python is my favorite programming language"
print("Overlapping Coefficient:", overlapping_coefficient(text1, text2))

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def manhattan_distance(text1, text2):
    vectorizer = CountVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([text1, text2]).toarray()
    return np.sum(np.abs(vectors[0] - vectors[1]))

text1 = "I love programming in Python"
text2 = "Python is my favorite programming language"
print("Manhattan Distance:", manhattan_distance(text1, text2))

''')    

    elif exp_no == 9:
        print('''\
def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two lists """
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)
sentences = ["The bottle is empty",
"There is nothing in the bottle"]
sentences = [sent.lower().split(" ")
for sent in sentences]
jaccard_similarity(sentences[0], sentences[1])
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
X ="I love horror movies"
Y ="Lights out is a horror movie"
#tokenization
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)

# sw contains the list of stopwords
sw = stopwords.words('english')
l1 =[];l2 =[]

# remove stop words from the string
X_set = {w for w in X_list if not w in sw}
Y_set = {w for w in Y_list if not w in sw}

# form a set containing keywords of both strings
rvector = X_set.union(Y_set)
for w in rvector:
    if w in X_set: l1.append(1)
    else: l1.append(0)
    if w in Y_set: l2.append(1)
    else: l2.append(0)
c = 0

# cosine formula
for i in range(len(rvector)):
        c+= l1[i]*l2[i]
cosine = c / float((sum(l1)*sum(l2))**0.5)
print("similarity: ", cosine)
                                                        
''')            
    else:
        print("No experiment Code found ,Please check your question paper or ask someone else and find the question number \n All the best for your exam and cheat well... ")