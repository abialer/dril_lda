#!/usr/bin/env
from gensim import corpora
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from enchant.checker import SpellChecker
from string import punctuation
import pickle

chkr = SpellChecker("en_US")
p_stemmer = PorterStemmer()

""" returns raw tweet text from html """
def getTweetTextFromHTML():
    f = open('coolTweetsDrilHtml.txt', 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()
    return [li.find('div', class_ = 'text').string for li in soup.find_all(lambda tag:
                            tag.name == 'li' and tag.get('class') == ['t'])]

""" spell checks word """
def spell_check(word):
    if chkr.check(word):
        return word
    else:
        suggestion = chkr.suggest(word)
        return suggestion[0] if suggestion else word

""" porter stems word """
def p_stem(word):
    return p_stemmer.stem(word) or word

""" returns true if stopword """
def isStopWord(word):
    return word in stopwords.words('english')

""" removes all punctuation from string """
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

"""

1. Removes stopwords
2. Porter stems
3. Spell checks
4. Lowers case
5. Removes tweets with links
6. Strips punctuation
 
"""
def formListOfTweets(tweets):
    final_tweets = []

    for tweet in tweets:

        if tweet is None or "http://" in tweet.lower():
            continue

        final_tweet = []

        for word in tweet.split():
            punc_stripped = strip_punctuation(word)
            if not punc_stripped: continue
            low = punc_stripped.lower()
            spell_checked = spell_check(low)
            p_stemmed = p_stem(spell_checked)
            if isStopWord(p_stemmed) or isStopWord(spell_checked): continue
            final_tweet.append(p_stemmed)

        final_tweets.append(final_tweet)

    return final_tweets

def saveAsList(tweets):
    f = open('tweetList.txt', 'w')
    pickle.dump(tweets, f)
    f.close()

def loadAsList():
    f = open('tweetList.txt', 'r')
    return pickle.load(f)

def saveAsCorpus(tweets):
    d = corpora.Dictionary(tweets)
    d.save("tweet_dict.dict")
    corpus = [d.doc2bow(tweet) for tweet in tweets]
    corpora.MmCorpus.serialize("tweet_corpus.mm", corpus)

def saveForDMM(tweets):
    f = open('tweetsForDMM.txt', 'w')
    for tweet in tweets:
        for word in tweet:
            f.write("%s " % word)
        f.write("\n")

def removeWeirdUnicode(tweets):
    clean_tweets = []
    for tweet in tweets:
        clean_tweet = []
        for word in tweet:
            word = word.encode('ascii', 'ignore')
            if word:
                clean_tweet.append(word)
        clean_tweets.append(clean_tweet)
    return clean_tweets

def removeMi(tweets):
    clean_tweets = []
    for tweet in tweets:
        clean_tweet = []
        for word in tweet:
            if word != 'mi':
                clean_tweet.append(word)
        clean_tweets.append(clean_tweet)
    return clean_tweets

#saveAsList(removeWeirdUnicode(formListOfTweets(getTweetTextFromHTML())))
saveAsList(removeMi(loadAsList()))
saveAsCorpus(loadAsList())
print loadAsList()
saveForDMM(loadAsList())
