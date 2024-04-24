import conllu

def extract_word_tag_pairs_from_conllu(conllu_text):
    """Parse Universal dependencies dataset and extract
    word/tag pairs out of it
    """
    sentences = conllu.parse(conllu_text)
    word_tag_pairs = []
    for sentence in sentences:
        pairs = [(token['form'], token['upos']) for token in sentence]
        word_tag_pairs.append(pairs)
    return word_tag_pairs

def main():
    # Read CONLLU data from file
    with open("your_conllu_file.conllu", "r", encoding="utf-8") as file:
        conllu_text = file.read()
    
    # Extract word/tag pairs from CONLLU data
    word_tag_pairs = extract_word_tag_pairs_from_conllu(conllu_text)
    
    # Write word/tag pairs to a new file
    with open("word_tag_pairs.txt", "w", encoding="utf-8") as output_file:
        for pairs in word_tag_pairs:
            for pair in pairs:
                output_file.write(f"{pair[0]}/{pair[1]} ")
            output_file.write("\n")

if __name__ == "__main__":
    main()
