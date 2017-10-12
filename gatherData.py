import string
import nltk
import pickle

pos = []
neg = []

lines = []
with open("train.csv") as data:
    for line in data:
        tok_line = string.split(line, ',')
        message = tok_line[5].replace('\"', '').strip("\n")
        rating = int(tok_line[0].replace('\"', ''))
        tweet = (message, rating)

        if rating == 4:
            pos.append(tweet)
        elif rating == 0:
            neg.append(tweet)


# to use a subset of the data
# /1000 indicated 1/1000 of the data is used
# del pos[len(pos)/1000:]
# del neg[len(neg)/1000:]


tweets = []
for (words, sentiment) in pos + neg:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

print len(tweets)



def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = nltk.classify.apply_features(extract_features, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)
# For saving the classifier
# f = open('nbc.pickle', 'wb')
# pickle.dump(classifier, f)
# f.close()
print classifier.show_most_informative_features(32)
