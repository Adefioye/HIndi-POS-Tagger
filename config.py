synthetic = True

test = 'test_data/test_data.txt'
test_tagged = 'test_data/test_tagged.txt'
train = 'train_data/train_data.txt'

if synthetic:
    test = 'synthetic_test_data/test_data.txt'
    test_tagged = 'synthetic_test_data/test_tagged.txt'
    train = 'synthetic_train_data/train_data.txt'

data = 'data/data.txt'
hmmmodel = 'model/hmmmodel.txt'
hmmoutput = 'outputs/hmmoutput.txt'
unknown_words_out = 'outputs/unknown_words.txt'

test_split_pct = 0.2
train_split_pct = 0.8

data_count = 16630

emission_smoothing = True
smoothing_alpha = 0.08

experiment_out = 'outputs/smoothing_alpha.txt'














        


        
        
        