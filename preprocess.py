import codecs 
import random
import re 
import config 
import sys
import os

if config.synthetic == False:
    print ('This file should only be run when working with synthetic data')
    sys.exit()

def random_sample_vocab():
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
    unknown_words = random.sample(sorted(vocab), 50)
    input_file.close()
    return set(unknown_words)

def test_train_split():
    sample = random_sample_vocab()
    fin = config.data
    input_file = codecs.open(fin, mode = 'r', encoding="utf-8")
    test = set()
    train = set()
    lines = input_file.readlines()
    for line in lines:
        oline = line
        line = line.strip('\n')
        data = line.split(" ")
        for s in data:
            i = s.index('/')
            s = s[:i]
            if s in sample:
                test.add(oline)
                break
        if oline not in test:
            train.add(oline)
    write_set_to_file(config.test_tagged, test)
    write_set_to_file(config.train, train)

def write_set_to_file(file_path, input_set):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with codecs.open(file_path, mode = 'w', encoding="utf-8") as file:
        for item in input_set:
            file.write(str(item))

def remove_test_tags():
    input_file = codecs.open(config.test_tagged, mode = 'r', encoding="utf-8")
    lines = input_file.readlines()
    output_file = codecs.open(config.test, mode = 'w', encoding="utf-8")
    for line in lines:    
        clean = re.sub(r'/[^ \n]*[\s\n]', ' ', line)
        output_file.write(clean[:-1] + '\n')
    input_file.close()
    output_file.close()


test_train_split()
remove_test_tags()