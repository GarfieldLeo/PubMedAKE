from nltk.stem.porter import PorterStemmer
import numpy as np
import re


stemmer = PorterStemmer()


def exact_match(extracted, ground):
    """
    Given 2 list of keyphrases, find the exact match.
    """
    same = set(extracted).intersection(set(ground))
    return len(same)


def stem_keyphrases(keyphrase_list):
    processed_keyphrases = set()
    for keyphrase in keyphrase_list:
        phr = ''
        # convert to lower case and split
        words = keyphrase.lower().split()
        for tkn in words:
            stmd = stemmer.stem(tkn)
            phr = phr + " " + stmd
        # try to decode it using utf
        if type(phr) == str:
            try:
                phr = phr.decode('utf-8')
            except:
                pass
        # check that its only valid characters in the string
        if bool(re.compile('^[a-zA-Z0-9_\-\s*]+$').match(phr)):    
            processed_keyphrases.add(phr.strip())
        
    return processed_keyphrases


def porter_match(extracted, ground):
    '''
    '''
    extracted_texts = stem_keyphrases(extracted)
    ground_texts = stem_keyphrases(ground)     
    return len(extracted_texts.intersection(ground_texts))


def partial_match(extracted, ground):
    '''
    Calculate the partial match with stems
    '''
    extracted_texts = stem_keyphrases(extracted)
    ground_texts = stem_keyphrases(ground)
    score = 0
    for ex in ground_texts:
        tempList = [0]
        # split the extracted kwds into pieces
        tempC = list(re.split(' ', ex))        
        # for each word, loop through the groundtruth list to calculate score
        for act in extracted_texts:
            # split ground truth into pieces
            cc = list(re.split(' ', act))
            matched = len([w for w in cc if w in tempC])
            ss = 2*matched/(len(tempC)+len(cc))
            tempList.append(ss)
        ss = max(tempList)
        score += ss
    return score


def evaluate_model(candidates, pubmedake,
                   match_fun=porter_match,
                   ext_key="keywords_in"):
    # figure out how many keywords
    first_value = next(iter(candidates.items()))[1]
    max_k = len(first_value)
    # initialize it to loop through the extracted keywords
    actual = np.zeros(max_k)
    extracted = np.zeros(max_k)
    matched = np.zeros(max_k)

    for idx, ex in candidates.items():
        kwds_in = pubmedake[idx][ext_key]
        k = 0
        for _, extracted_kwds in ex.items():
            score = match_fun(extracted_kwds, kwds_in)
            actual[k] += len(kwds_in)
            extracted[k] += len(extracted_kwds)
            matched[k] += score
            k += 1
    precision = np.divide(matched, extracted)
    recall = np.divide(matched, actual)
    f1 = np.zeros(len(actual))
    if np.all(precision+recall > 0):
        f1 = 2 * np.divide((np.multiply(precision, recall)), precision + recall)
    # here put it into a single map
    perf = {}
    perf['precision'] = dict(zip(ex.keys(), precision))
    perf['recall'] = dict(zip(ex.keys(), recall))
    perf['f1'] = dict(zip(ex.keys(), f1))
    return perf

