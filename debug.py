import codecs
import re 

def remove_test_tags():
    input_file = codecs.open('outputs/incorrectly_predicted.txt', mode = 'r', encoding="utf-8")
    lines = input_file.readlines()
    output_file = codecs.open('outputs/incorrectly_predicted_no_tag.txt', mode = 'w', encoding="utf-8")
    for line in lines:    
        clean = re.sub(r'/[^ \n]*[\s\n]', ' ', line)
        output_file.write(clean[:-1] + '\n')
    input_file.close()
    output_file.close()

remove_test_tags()