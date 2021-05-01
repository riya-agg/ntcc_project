from nltk.corpus import stopwords, wordnet
from nltk.parse.stanford import StanfordParser
from nltk.stem import WordNetLemmatizer
from nltk.tree import *
from nltk import pos_tag
import os

os.environ['STANFORD_PARSER'] = 'E:\\NTCC Minor-Major Project\\Major Project - 8th Sem\\jars'
os.environ['STANFORD_MODELS'] = 'E:\\NTCC Minor-Major Project\\Major Project - 8th Sem\\jars'

def filter_stop_words(words):
    stopwords_set = ['is', 'am', 'are', 'a', 'an', 'the']
    #stopwords_set = set(stopwords.words("english"))
    print(stopwords_set)
    words = list(filter(lambda x: x not in stopwords_set, words))
    return words


def lemmatize_tokens(token_list):
    lemmatizer = WordNetLemmatizer()
    #pos_tagger_list    = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'R': wordnet.ADV, 'N': wordnet.NOUN} 
    
    def pos_tagger(nltk_tag):
        if nltk_tag == 'J':
            return wordnet.ADJ
        elif nltk_tag == 'V':
            return wordnet.VERB
        elif nltk_tag == 'N':
            return wordnet.NOUN
        elif nltk_tag == 'R':
            return wordnet.ADV
        else:          
            return None    
            
    lemmatized_words = []
    
    for token, tag in pos_tag(token_list):
        lemmatized_words.append(lemmatizer.lemmatize(token, pos_tagger(tag[0])))

    return lemmatized_words
    

def label_parse_subtrees(parent_tree):
    tree_traversal_flag = {}

    for sub_tree in parent_tree.subtrees():
        tree_traversal_flag[sub_tree.treeposition()] = 0
    return tree_traversal_flag


def handle_noun_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree):
    if tree_traversal_flag[sub_tree.treeposition()] == 0 and tree_traversal_flag[sub_tree.parent().treeposition()] == 0:
        tree_traversal_flag[sub_tree.treeposition()] = 1
        modified_parse_tree.insert(i, sub_tree)
        i = i + 1
    return i, modified_parse_tree


def handle_verb_prop_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree):
    for child_sub_tree in sub_tree.subtrees():
        if child_sub_tree.label() == "NP" or child_sub_tree.label() == 'PRP':
            if tree_traversal_flag[child_sub_tree.treeposition()] == 0 and tree_traversal_flag[child_sub_tree.parent().treeposition()] == 0:
                tree_traversal_flag[child_sub_tree.treeposition()] = 1
                modified_parse_tree.insert(i, child_sub_tree)
                i = i + 1
    return i, modified_parse_tree


def modify_tree_structure(parent_tree):
    tree_traversal_flag = label_parse_subtrees(parent_tree)

    modified_parse_tree = Tree('ROOT', [])
    i = 0
    for sub_tree in parent_tree.subtrees():
        if sub_tree.label() == "NP":
            i, modified_parse_tree = handle_noun_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree)
        if sub_tree.label() == "VP" or sub_tree.label() == "PRP":
            i, modified_parse_tree = handle_verb_prop_clause(i, tree_traversal_flag, modified_parse_tree, sub_tree)

    for sub_tree in parent_tree.subtrees():
        for child_sub_tree in sub_tree.subtrees():
            if len(child_sub_tree.leaves()) == 1: 
                if tree_traversal_flag[child_sub_tree.treeposition()] == 0 and tree_traversal_flag[child_sub_tree.parent().treeposition()] == 0:
                    tree_traversal_flag[child_sub_tree.treeposition()] = 1
                    modified_parse_tree.insert(i, child_sub_tree)
                    i = i + 1

    return modified_parse_tree


def convert_eng_to_isl(input_string):

    if len(list(input_string.split(' '))) == 1:
        return list(input_string.split(' '))

    parser = StanfordParser(model_path='E:\\NTCC Minor-Major Project\\Major Project - 8th Sem\\englishparser\\englishPCFG.ser.gz')
    possible_parse_tree_list = [tree for tree in parser.parse(input_string.split())]

    parse_tree = possible_parse_tree_list[0]
    print(parse_tree)
    # output = '(ROOT
    #               (S
    #                   (PP (IN As) (NP (DT an) (NN accountant)))
    #                   (NP (PRP I))
    #                   (VP (VBP want) (S (VP (TO to) (VP (VB make) (NP (DT a) (NN payment))))))
    #                )
    #             )'

    parent_tree = ParentedTree.convert(parse_tree)

    modified_parse_tree = modify_tree_structure(parent_tree)

    parsed_sent = modified_parse_tree.leaves()
    return parsed_sent


def pre_process(sentence):
    words = list(sentence.split())
    f = open('words.txt', 'r')
    eligible_words = f.read()
    f.close()
    final_string = ""

    for word in words:
        if word not in eligible_words:
            for letter in word:
                final_string += " " + letter
        else:
            final_string += " " + word

    return final_string