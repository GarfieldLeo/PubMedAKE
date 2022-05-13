import json


def read_pubmedake(filename):
    with open(filename) as f:
        data = json.load(f)
        f.close()
    return data


def write_extracted(outputfile, keywords):
    with open(outputfile, 'w') as f:
        json.dump(keywords, f, indent=4)
        f.close()