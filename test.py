import sys
from decimal import *
import codecs
import config
import matplotlib.pyplot as plt
import numpy as np

tag_set = set()
word_set = set()
unknown_words_set = set()
if config.synthetic:
    unknown_words = codecs.open(config.unknown_words_out, mode='r', encoding="utf-8")
    for line in unknown_words.readlines():
        unknown_words_set.add(line.strip())

def parse_traindata():
    fin = config.hmmmodel
    output_file = config.hmmoutput
    transition_prob = {}
    emission_prob = {}
    tag_list = []
    tag_count ={}
    global tag_set
    try:
        input_file = codecs.open(fin,mode ='r', encoding="utf-8")
        lines = input_file.readlines()
        flag = False
        for line in lines:
            line = line.strip('\n')
            if line != "Emission Model":
                i = line[::-1]
                key_insert = line[:-i.find(":")-1]
                value_insert = line.split(":")[-1]

                # for transition probabilities #
                if flag == False:
                    transition_prob[key_insert] = value_insert
                    if (key_insert.split("~tag~")[0] not in tag_list) and (key_insert.split("~tag~")[0] != "start"):
                        tag_list.append(key_insert.split("~tag~")[0])

                else:
                    # for emission probabilities #
                    emission_prob[key_insert] = value_insert
                    val = key_insert.split("/")[-1]
                    j = key_insert[::-1]
                    word = key_insert[:-j.find("/")-1].lower()
                    word_set.add(word)
                    if val in tag_count:
                        tag_count[val] +=1
                    else:
                        tag_count[val] = 1
                    tag_set.add(val)

            else:
                flag = True
                continue

        input_file.close()
        return tag_list, transition_prob, emission_prob, tag_count, word_set

    except IOError:
        fo = codecs.open(output_file, mode='w',encoding="utf-8")
        fo.write("File not found: {}".format(fin))
        fo.close()
        sys.exit()

absent_word_set = set()

def viterbi_algorithm(sentence, tag_list, transition_prob, emission_prob,tag_count, word_set):
    global tag_set
    # Get words from each sentence #
    sentence = sentence.strip("\n")
    word_list = sentence.split(" ")
    current_prob = {}
    for tag in tag_list:
        # transition probability #
        tp = Decimal(0)
        # Emission probability #
        em = Decimal(0)
        # Storing the probability of every tag to be starting tag #
        if "start~tag~"+tag in transition_prob:
            tp = Decimal(transition_prob["start~tag~"+tag])
        # Check for word in training data. If present, check the probability of the first word to be of given tag#
        if word_list[0].lower() in word_set:
            if (word_list[0].lower()+"/"+tag) in emission_prob:
                em = Decimal(emission_prob[word_list[0].lower()+"/"+tag])
                # Storing probability of current combination of tp and em #
                current_prob[tag] = tp * em
         # Check for word in training data. If absent then probability is just tp# 
        else:
            absent_word_set.add(word_list[0])
            em = Decimal(1) /(tag_count[tag] +len(word_set))
            current_prob[tag] = tp

    if len(word_list) == 1:
        # Return max path if only one word in sentence #
        max_path = max(current_prob, key=current_prob.get)
        return max_path
    else:
        # Tracking from second word to last word #
        for i in range(1, len(word_list)):
            previous_prob = current_prob
            current_prob = {}
            locals()['dict{}'.format(i)] = {}
            previous_tag = ""
            for tag in tag_list:
                if word_list[i].lower() in word_set:
                    if word_list[i].lower()+"/"+tag in emission_prob:
                        em = Decimal(emission_prob[word_list[i].lower()+"/"+tag])
                        # Find the maximum probability using previous node's(tp*em)[i.e probability of reaching to the previous node] * tp * em (Bigram Model) #
                        max_prob, previous_state = max((Decimal(previous_prob[previous_tag]) * Decimal(transition_prob[previous_tag + "~tag~" + tag]) * em, previous_tag) for previous_tag in previous_prob)
                        current_prob[tag] = max_prob
                        locals()['dict{}'.format(i)][previous_state + "~" + tag] = max_prob
                        previous_tag = previous_state
                else:
                    absent_word_set.add(word_list[i])
                    em = Decimal(1) /(tag_count[tag] +len(word_set))
                    max_prob, previous_state = max((Decimal(previous_prob[previous_tag]) * Decimal(transition_prob[previous_tag+"~tag~"+tag]) * em, previous_tag) for previous_tag in previous_prob)
                    current_prob[tag] = max_prob
                    locals()['dict{}'.format(i)][previous_state + "~" + tag] = max_prob
                    previous_tag = previous_state

            # if last word of sentence, then return path dicts of all words #
            if i == len(word_list)-1:
                max_path = ""
                last_tag = max(current_prob, key=current_prob.get)
                max_path = max_path + last_tag + " " + previous_tag
                for j in range(len(word_list)-1,0,-1):
                    for key in locals()['dict{}'.format(j)]:
                        data = key.split("~")
                        if data[-1] == previous_tag:
                            max_path = max_path + " " +data[0]
                            previous_tag = data[0]
                            break
                result = max_path.split()
                result.reverse()
                return " ".join(result)



tag_list, transition_model, emission_model, tag_count, word_set = parse_traindata()

fin = config.test
input_file = codecs.open(fin, mode='r', encoding="utf-8")
fout = codecs.open(config.hmmoutput,mode='w',encoding="utf-8")
for sentence in input_file.readlines():
    path = viterbi_algorithm(sentence, tag_list, transition_model, emission_model,tag_count, word_set)
    sentence = sentence.strip("\n")
    word = sentence.split(" ")
    tag = path.split(" ")
    for j in range(0,len(word)):
        if j == len(word)-1:
            fout.write(word[j] + "/" + tag[j]+ u'\n')
        else:
            fout.write(word[j] + "/" + tag[j] + " ")

if (config.synthetic):
    print ("Absent words ", len(absent_word_set))
    print ("Unknown words ", len(unknown_words_set))
    print ("Intersection count between the above two ", len(absent_word_set.intersection(unknown_words_set)))

predicted = codecs.open(config.hmmoutput, mode ='r', encoding="utf-8")
expected = codecs.open(config.test_tagged, mode ='r', encoding="utf-8")

c = 0
total = 0
unknown_words_incorrectly_predicted = 0
unknown_words_instances = 0
classified_as = dict()
correctly_classified_as = dict()
tag_count_test = dict()

for line in expected.readlines():
    u = line.split(" ")
    for i in range(len(u)):
        tag = u[i]
        tag = tag[u[i].find('/') + 1:].strip(' /\n\t')
        if len(tag) > 0 and tag in tag_count_test:
            tag_count_test[tag] += 1 
        elif len(tag) > 0:
            tag_count_test[tag] = 1  

expected.seek(0)

for line in predicted.readlines():
    u = line.split(" ")
    total += len(u)
    a = expected.readline().split(" ")
    for i in range(len(u)):
        word = u[i]
        word =word[:u[i].find('/')]
        if word in unknown_words_set:
            unknown_words_instances += 1 
        tag = u[i]
        tag = tag[max(u[i].find('/') + 1, u[i].find('//') + 1):].strip(' /\n\t')
        if len(tag) > 0 and tag in classified_as:
             classified_as[tag] += 1
        elif len(tag) > 0:
           classified_as[tag] = 1
        if(a[i]!=u[i]):
            c+=1
            if config.synthetic and word in unknown_words_set:
                unknown_words_incorrectly_predicted += 1 
        else: 
            if len(tag) > 0 and tag in correctly_classified_as:
                correctly_classified_as[tag] += 1
            elif len(tag) > 0:
                correctly_classified_as[tag] = 1

print("Wrong Predictions = ",c)
print("Total Predictions = ",total)
print("Accuracy is = ",100 - (c/total * 100),"%")

for tag in sorted(classified_as):
    print ("Precision for tag ", tag, " = ", (correctly_classified_as[tag]/classified_as[tag]) * 100, '%')

for tag in sorted(tag_count_test):
    print ("Recall for tag ", tag, " = ", (correctly_classified_as[tag]/tag_count_test[tag]) * 100, '%')


if config.synthetic:
    print("Total number of induced unknown words", len(unknown_words_set))
    print("Total number of unknown word instances", unknown_words_instances)
    print("Total instances where unknown words were incorrectly predicted", unknown_words_incorrectly_predicted)
    print("Model accuracy when it comes to tackling unknown words is = ",100 - (unknown_words_incorrectly_predicted/unknown_words_instances * 100),"%")
    print("Model accuracy when it comes to tackling known words is = ",100 - ((c-unknown_words_incorrectly_predicted)/(total-unknown_words_instances) * 100),"%")

plt.style.use('Solarize_Light2')

# Calculating precision and recall
precision_data = {tag: (correctly_classified_as[tag], classified_as[tag]) for tag in sorted(classified_as)}
recall_data = {tag: (correctly_classified_as[tag], tag_count_test[tag]) for tag in sorted(tag_count_test)}

# Extracting tag names, precision/recall values, and tag counts
tags = sorted(classified_as.keys())
precisions = [val[0] / val[1] for val in precision_data.values()]
recalls = [val[0] / val[1] for val in recall_data.values()]
tag_counts = [tag_count_test[tag] for tag in tags]

# Plotting both precision and recall on the same bar chart
bar_width = 0.35
index = np.arange(len(tags))

plt.figure(figsize=(20, 7))
bar1 = plt.bar(index, precisions, bar_width, label='Precision', color='blue')
bar2 = plt.bar(index + bar_width, recalls, bar_width, label='Recall', color='green')

# Creating custom x-axis labels with tag names and counts
x_labels = [f'{tag}\n({count})' for tag, count in zip(tags, tag_counts)]
plt.xlabel('Tags', fontsize=14)  # Increase font size for better readability
plt.ylabel('Percentage', fontsize=14)  # Increase font size for better readability
plt.title('Precision and Recall vs Tags', fontsize=16)  # Increase font size for better readability
plt.xticks(index + bar_width / 2, x_labels, rotation=90)  # Adjust x-axis labels and rotation
plt.legend()  # Add legend to distinguish between precision and recall

plt.tight_layout()
plt.show()