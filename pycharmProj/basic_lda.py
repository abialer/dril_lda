from gensim import corpora,models
import pyLDAvis.gensim

def lda():
    corpus = corpora.MmCorpus("tweet_corpus.mm")
    d = corpora.Dictionary.load("tweet_dict.dict")
    lda = models.ldamodel.LdaModel(corpus, num_topics = 3, id2word=d)
    lda.save("lda.ginsem")

def print_topics(topic_list):
    for topic in topic_list:
        topic_num = topic[0]
        word_probs = topic[1]
        wp = word_probs.split(" + ")
        s = "Topic " + str(topic_num) + ":\t"
        for w in wp:
            word = w.split("*")
            s += str(word[1]) + ": " + str(word[0]) + "\t"
        print s

def visualize(lda, corpus, dictionary):
    pyLDAvis.gensim.prepare(lda, corpus, dictionary)

#lda()
#lda_results = models.ldamodel.LdaModel.load("lda.ginsem")
#print_topics(lda_results.show_topics())
visualize(models.ldamodel.LdaModel.load("lda.ginsem"), corpora.MmCorpus("tweet_corpus.mm"), corpora.Dictionary.load("tweet_dict.dict"))
