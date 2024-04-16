import codecs 
import random
import re 
import config 
import sys
import os

def random_sample_vocab():
    """
    This helps to randomly sample a dataset and select 100
    unique words from the dataset
    """
    fin = config.data
    vocab = set()
    input_file = codecs.open(fin, mode = 'r', encoding="utf-8")
    lines = input_file.readlines()
    for line in lines:
        line = line.strip('\n')
        data = line.split(" ")
        for s in data:
            i = s.index('/')
            s = s[:i]
            if (s != '|'):
                vocab.add(s)
    unknown_words = random.sample(sorted(vocab), 100)
    input_file.close()
    return set(unknown_words)

def test_train_split():
    """
    This helps to split data into `train` and `test` categories.
    For synthetic data
    """
    sample = random_sample_vocab()
    write_sample_to_file(sample)
    fin = config.data
    input_file = codecs.open(fin, mode = 'r', encoding="utf-8")
    test = set()
    train = set()
    test_count = 0
    lines = input_file.readlines()
    for line in lines:
        oline = line
        line = line.strip('\n')
        data = line.split(" ")
        for s in data:
            i = s.index('/')
            s = s[:i]
            if config.synthetic and s in sample:
                test.add(oline)
                break
            if not config.synthetic and test_count < int(config.test_split_pct * config.data_count):
                test.add(oline)
                test_count +=1 
                break
        if oline not in test:
            train.add(oline)
    write_set_to_file(config.test_tagged, test)
    write_set_to_file(config.train, train)
    print ('Total test points ', len(test))
    print ('Total train points ', len(train))
    return len(test), len(train)

def write_set_to_file(file_path, input_set):
    """
    This helps to write `input_set` to `file_path`
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with codecs.open(file_path, mode = 'w', encoding="utf-8") as file:
        for item in input_set:
            file.write(str(item))

def remove_test_tags():
    """Removing tags in test data to generate `test_tagged.txt`.
    This dataset is useful for computing evaluation metrics like
    accuracy, precision, recall and F1-score
    """
    input_file = codecs.open(config.test_tagged, mode = 'r', encoding="utf-8")
    lines = input_file.readlines()
    output_file = codecs.open(config.test, mode = 'w', encoding="utf-8")
    for line in lines:    
        clean = re.sub(r'/[^ \n]*[\s\n]', ' ', line)
        output_file.write(clean[:-1] + '\n')
    input_file.close()
    output_file.close()

def write_sample_to_file(random_sample_vocab):
    """This writes randomly sampled vocabulary to a file"""
    output_file = codecs.open(config.unknown_words_out, mode = 'w', encoding="utf-8")
    for s in random_sample_vocab:
        output_file.write(s + '\n')
    output_file.close()

split = test_train_split()  
if config.synthetic == True:
    iteration = 1   
    while (config.test_split_pct * config.data_count > split[0]):
        split = test_train_split()
        print ("---- Iteration number ", iteration, " ----")
        iteration += 1 
remove_test_tags()