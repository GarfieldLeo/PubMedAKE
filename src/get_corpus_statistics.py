import argparse
from nltk.tokenize import word_tokenize, sent_tokenize
import pubmedake
import tqdm
import string


def count_words(x):
    words = 0
    punct = set(string.punctuation)
    sentences = sent_tokenize(x)
    for sent in sentences:
        sent_tokens = word_tokenize(sent)
        # remove the punctuation
        for token in sent_tokens:
            if token not in punct:
                words += 1
    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
                        help='Constructed JSON file')
    args = parser.parse_args()
    # read the corpus
    corpus = pubmedake.read_pubmedake(args.infile)
    # things to calculate
    total_kwds = 0
    ext_kwds = 0
    abs_kwds = 0
    title_words = 0
    abstract_words = 0
    n_articles = len(corpus)
    for pmid, body in tqdm.tqdm(corpus.items()):
        kwds_in = body['keywords_in']
        kwds_not_in = body['keywords_not_in']
        # calculate keywords statistics
        ext_kwds += len(kwds_in)
        abs_kwds += len(kwds_not_in)
        total_kwds += len(kwds_in) + len(kwds_not_in)
        # calculate words statistics
        title_words += count_words(body['title'])
        abstract_words += count_words(body['abstract'])
    stats = {"avg_kwds": total_kwds / n_articles,
             "avg_ext": ext_kwds / n_articles,
             "avg_abs": abs_kwds / n_articles,
             "avg_title": title_words / n_articles,
             "avg_abstract": abstract_words / n_articles
    }
    print(stats)
    
