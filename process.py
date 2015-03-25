import os
import re
import sys
import glob
import parser
import numpy
from scipy.cluster.vq import kmeans,vq
from gensim.utils import simple_preprocess
from gensim.corpora.bleicorpus import BleiCorpus
from gensim.corpora.textcorpus import TextCorpus
from gensim.models.ldamodel import LdaModel
from nltk.corpus import stopwords
from Stemmer import Stemmer

stop = open('stopwords.txt')
stoplist = [word.rstrip('\n') for word in stop if word]
stoplist += stopwords.words('english')
stoplist = set(stoplist)

def read_text(stream):
    '''
    get text from a stream, override this function for different application.
    '''
    try:
        s = ''
        title = ''
        conversation_cnt = 0
        post_cnt = 0
        for line in stream:
            line = line.strip()
            if not line:
                continue
            if '@INFINITYTEAMBIGTHREAD' in line:
                conversation_cnt += 1
                if conversation_cnt != 1:
                    post_cnt = 0
                continue
            if '@INFINITYTEAMSMALLPOST' in line:
                post_cnt += 1
                if post_cnt != 1:
                    yield s
                    s = ''
                else:
                    pass
            else:
                if post_cnt == 0:
                    title = line
                    s += line
                else:
                    s += line
            #yield line
    finally:
        stream.close()

def read_conver(stream):
    '''
    get text from a stream, override this function for different application.
    '''
    try:
        s = ''
        title = ''
        conversation_cnt = 0
        for line in stream:
            line = line.strip()
            if not line:
                continue
            if '@INFINITYTEAMBIGTHREAD' in line:
                conversation_cnt += 1
                if conversation_cnt != 1:
                    yield s
                    s = ''
            if '@INFINITYTEAMSMALLPOST' in line:
                s+=line+"\n"
            else:
                if conversation_cnt == 0:
                    title = line
                    s += line+"\n"
                else:
                    s += line+"\n"
            #yield line
    finally:
        stream.close()

def process_text(s):
    s = re.sub('<[^>]+>', '', s)
    s = re.sub('&.*?;', '', s)
    words = simple_preprocess(s, deacc=True, max_len=99)
    words = [word for word in words if word not in stoplist]
    stemmer = Stemmer('english')
    words = stemmer.stemWords(words)
    #print words
    #print stoplist
    #raw_input()
    return words

class StackExchangeCorpus(TextCorpus):
    def __init__(self, input=None):
        super(self.__class__, self).__init__(input)

    def get_texts(self):
        for post in read_text(self.getstream()):
            yield process_text(post)

def make_corpus(file, path, file_name):
    try:
        os.mkdir(os.path.join(path, 'corpus'))
    except OSError:
        pass
    corpus = StackExchangeCorpus(file)
    BleiCorpus.serialize(os.path.join(path, 'corpus', file_name + '.cor'), corpus=corpus, id2word=corpus.dictionary)
    corpus.dictionary.save(os.path.join(path, 'corpus', file_name + '.dict'))

def load_corpus(file, path, file_name):
    corpus = BleiCorpus(os.path.join(path, 'corpus', file_name + '.cor'))
    return corpus

def make_lda_model(corpus, num_topics, fname, **kwargs):
    kwargs = dict({'alpha': 'auto', 'passes': 1}, **kwargs)
    lda = LdaModel(corpus, num_topics, id2word=corpus.id2word, **kwargs)
    lda.save(fname)
    return lda

def make_multiple_lda_models(path, file_name, corpus, num_topics_list=[], **kwargs):
    try:
        os.mkdir(os.path.join(path, 'models'))
    except OSError:
        pass
    for k in num_topics_list:
        fname = os.path.join(path, 'models', file_name + '_k=%03d' % k)
        make_lda_model(corpus, k, fname, **kwargs)


def save_top_words(model_file, output_file):
    lda = LdaModel.load(model_file)
    topics = lda.show_topics(-1, topn=20, formatted=False)

    topics = [[word for (_, word) in topic] for topic in topics]
    with open(output_file, 'w') as fp:
        for i, topic in enumerate(topics):
            #print topic
            line = 'Topic %d: %s\n' % (i + 1, ', '.join(topic))
            fp.write(line)
    return topics

def save_top_words_for_models(path, file_name):
    models = glob.glob(os.path.join(path, 'models', file_name + '_k=???'))
    models_topics_list= []
    try:
        os.mkdir(os.path.join(path, 'topics'))
    except OSError:
        pass
    for m in models:
        k = int(m[-3:], 10)
        models_topics_list.append( save_top_words(m, os.path.join(path, 'topics', file_name + '_lda_%d_topics.txt' % k)) )
    return models_topics_list    

def contains(topics, filetext):
    topics_to_file = []
    for topic in topics:
        if filetext.lower().find(topic.lower()) >= 0:
            topics_to_file.append(1);
        else:
            topics_to_file.append(0);    
    return topics_to_file;




def create_matrix(topics, files):
    topics_to_files= []
    corpus = StackExchangeCorpus(files)

    for filetext in read_conver(corpus.getstream()):
        topics_to_files.append(contains(topics, filetext))

    topics_to_files=numpy.array(zip (*topics_to_files))
    '''
    for k in topics_to_files:
        print k   
    '''
    return topics_to_files



def extract_topics(keyword,rebuild):
    keywordstr =""    
    for k in keyword:
        #print "k is"+ k    
        keywordstr += k +" "
    keywordstr = keywordstr[0:-1]    
    print keywordstr
    path = os.path.join('.', 'data', str(keywordstr))
    txtFilePath = os.path.join(path, str(keywordstr) + '.txt')
    csvFilePath = os.path.join(path, str(keywordstr) + '.csv')
    try:
        os.mkdir(path)
    except OSError:
        pass
    if rebuild == 1:
        try:
            line_tuple = parser.create_corpus(keyword, None, txtFilePath)
            parser.create_csv(line_tuple, csvFilePath)
        except Exception, e:
            print >>sys.stderr, e, Exception
            return 2
    
    print "start LDA"
    (path, file_name) = os.path.split(txtFilePath)
    (file_name, file_ext) = os.path.splitext(file_name)
    #print "path is"+ path
    #print "file_name is "+file_name
    make_corpus(txtFilePath, path, file_name)
    corpus = load_corpus(txtFilePath, path, file_name)
    make_multiple_lda_models(path, file_name, corpus, [2])



def group_topics(file_name, topics):
    path = os.path.join('.', 'data', file_name)
    txtFilePath = os.path.join(path, file_name + '.txt')
    result = []
    m = create_matrix(topics, txtFilePath)
    # computing K-Means with K = 2 (2 clusters)
    groups,_ = kmeans(m,2)
    # assign each sample to a cluster
    idx,_ = vq(m,groups)
    #print idx
    topic1=[]
    topic2=[]
    count =0;
    for i in idx:
        if i == 0:
            topic1.append(topics[count])
        else:   
            topic2.append(topics[count])

        count+=1   

    result.append(topic1)
    result.append(topic2)
    return result        

def update_corpus(txtFilePath, topics):
    match = 0
    with open(txtFilePath+'~', 'w') as txt:
        try:
            corpus = StackExchangeCorpus(txtFilePath)
            for filetext in read_conver(corpus.getstream()):
                if 1 in contains(topics, filetext):
                    match+=1
                    txt.write(filetext+"\n")
            txt.write(str(match))
            print "the total documents updates to "+str(match)
        except Exception, e:
            print >>sys.stderr, "still out sync"
            raise Exception(e); 
        finally:
            os.remove(txtFilePath)
            os.rename(txtFilePath+'~', txtFilePath)
            #os.remove(txtFilePath+'~')
            txt.close()              