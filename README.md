# PubMedAKE Dataset

## Introduction to PubMedAKE

PubMedAKE is a large, author-assigned keyphrase extraction dataset that contains the non-commerical use articles from the PubMed Open Access Subset. The dataset contains 843,629 articles and stores the title, abstract, PubMedID, and both the extractive and abstractive keywords (see example image below). The dataset is randomly split into three files: train, validation, and test. A selected version of the dataset, PubMedAKE_{small} contains articles that contain 5 to 25 extractive (keywords_in) keywords. All 6 data files can be found on [Zenodo](https://doi.org/10.5281/zenodo.6330817). To facilitate usage, a small sample with 1000 articles is available in the `data` folder.

[![data-extract.png](https://i.postimg.cc/Kz61vVp5/data-extract.png)](https://postimg.cc/S2GSgZhX)


This toolkit allows for easy benchmarking of state-of-the-art keyphrase extraction models such as `pke` on PubMedAKE. The tookit can be used to replicate the results of several baseline models, assess new models using the same performance metrics (exact match, match with stemming, and partial match with stemming).

## Installation

To pip install `pubmedake` from Github:
```
pip install git+https://github.com/GarfieldLeo/PubMedAKE
```

pubmedake relies on `pke`, `nltk`, `numpy` to be installed.


## Minimal Examples

A sample on reading the data and using the dataset:
```
import pubmedake

data = pubmedake.read_pubmedake("data/sample_1000.json")

# data is a dictionary with all of the data 
for pmid, body in data.items():
    abstract    = body['abstract']
    title       = body['title']
    kwds_in     = body['keywords_in']
    kwds_not_in = body['keywords_not_in']
```

The `example` folder contains code to run the abstractive and extractive baselines reported in the paper on the small data sample. 
To evaluate the extracted phrases against the ground truth for a single article, three methods have been created: `exact_match`, `porter_match`, and `partial_match`. An additional method, `evaluate_model` has also been developed
to evaluate a corpus of extracted keywords that are stored as a nested dictionary {pmid, {#extracted, extracted_keywords}}. A sample of using this method on an extracted sample from running YAKE on the small data sample:
```
import pubmedake

gt = pubmedake.read_pubmedake("data/sample_1000.json")
yake = pubmedake.read_pubmedake("results/sample_yakekwds.json")

pubmedake.evaluate_model(yake, gt, pubmedake.porter_match)
```

The `results` folder contains a Python script that can be used to print the evaluation results from the command line by passing in appropriate arguments.

The `src` folder contains the original code for creating the dataset from the XML files.

## Dataset Statistics

| Sample Name    | # Articles    | # KP (Ext)  |  # KP (Abs)  | # words (Title) | # words (Abstract) |
| -------------  | ------------- | ----------- | ------------ | --------------- | ------------------ |
| small_train    | 82,011        | 5.58        | 1.44         | 14.08           | 239.53             |
| small_validate | 27,336        | 5.57        | 1.41         | 14.81           | 237.50             |
| small_validate | 27,336        | 3.01        | 2.15         | 14.16           | 216.54             |
| train          | 505,959       | 3.01        | 2.15         | 14.16           | 216.54             |
| validate       | 168,653       | 3.01        | 2.15         | 14.14           | 215.73             |
| test           | 168,653       | 3.01        | 2.15         | 14.15           | 218.94             |

