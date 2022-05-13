from collections import defaultdict
from nltk.corpus import stopwords
import pke
import string

from pubmedake import write_extracted


def run_yake(abstract, window=2, use_stems=False):
    extractor = pke.unsupervised.YAKE()
    stoplist = stopwords.words('english')
    extractor.load_document(input=abstract,
                            language='en',
                            normalization=None,
                            stoplist=stoplist)
    extractor.candidate_selection(n=3)
    extractor.candidate_weighting(window=window,
                                  use_stems=use_stems)
    return extractor


def run_textrank(abstract, window=2, top_percent=0.33):
    pos = {'NOUN', 'PROPN', 'ADJ'}
    extractor = pke.unsupervised.TextRank()
    extractor.load_document(input=abstract,
                            language='en',
                            normalization=None)
    extractor.candidate_weighting(window=window,
                                  pos=pos,
                                  top_percent=top_percent)
    return extractor


def run_singlerank(abstract, window=10):
    pos = {'NOUN', 'PROPN', 'ADJ'}
    extractor = pke.unsupervised.SingleRank()
    extractor.load_document(input=abstract,
                            language='en',
                            normalization=None)
    extractor.candidate_selection(pos=pos)
    extractor.candidate_weighting(window=window, pos=pos)
    return extractor


def run_topicrank(abstract, thr=0.74, method="average"):
    pos = {'NOUN', 'PROPN', 'ADJ'}

    extractor = pke.unsupervised.TopicRank()
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')

    extractor.load_document(input=abstract, stoplist=stoplist)
    extractor.candidate_selection(pos=pos)
    extractor.candidate_weighting(threshold=thr, method=method)
    return extractor


def run_positionrank(abstract, max_word=3, window=10):
    pos = {'NOUN', 'PROPN', 'ADJ'}
    grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"
    extractor = pke.unsupervised.PositionRank()
    extractor.load_document(input=abstract,
                            language='en',
                            normalization=None)
    extractor.candidate_selection(grammar=grammar,
                                  maximum_word_number=max_word)
    extractor.candidate_weighting(window=window, pos=pos)
    return extractor


def run_multirank(abstract, alpha=1.1, thr=0.74, method='average'):
    extractor = pke.unsupervised.MultipartiteRank()
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')
    extractor.load_document(input=abstract, stoplist=stoplist)

    pos = {'NOUN', 'PROPN', 'ADJ'}
    extractor.candidate_selection(pos=pos)

    extractor.candidate_weighting(alpha=alpha,
                                  threshold=thr,
                                  method=method)
    return extractor


def run_pke_model(corpus, top_k_list,
                  run_func, output_file):
    extracted_map = defaultdict(dict)
    for idx, body in corpus.items():
        abstract = body['abstract']
        # apply the model that we're running
        extractor = run_func(abstract)
        for nn in top_k_list:
            keyphrases = extractor.get_n_best(n=nn)
            keyphrases = [i[0] for i in keyphrases]
            extracted_map[idx][nn] = keyphrases
    # write the outputfile
    write_extracted(output_file, extracted_map)
    return extracted_map

