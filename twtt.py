# -*- coding: utf-8 -*-
import sys
import os
import re
import string
import NLPlib
 

word_list_dir = "/u/cs401/Wordlists/"
char_codes = {
    '&quot;' : '"',
    '&amp;'  : '&',
    '&gt;'   : '>',
    '&lt;'   : '<'
}


def read_word_list(filepath):
    with open(filepath) as f:
        return [line.rstrip('\n') for line in f.readlines()]

# 1. Remove all html tags and attributes
def remove_tags_and_attr (line):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', line)
 
# 2. Remove HTML character codes
def remove_char_codes(tweet):
    pattern = re.compile(r'(' + '|'.join(char_codes.keys()) + r')')
    return pattern.sub(lambda x: char_codes[x.group()], tweet)
 
# 3. Remove all of the URL
def remove_URL (line):
    return re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', line)
 
# 4. Remove '@' before user names and '#' before hash tags
def process_username_hashtag(tweet):
    pattern = re.compile(r"(^|\s)(@|#)\S")
    return pattern.sub(lambda x: x.group().replace(x.group(2), '') , tweet)
 
# 7. Insert space around punctuations and clitics
def insert_spacing (sent):
    sent = re.sub(r"((^|\s)'|'(\s|$))", r" ' ", sent)
    sent =  non_EoS_pattern.sub(lambda x: (' ' + x.group().strip() + ' '), sent)
    return apost_pattern.sub(lambda x : x.group()[0] + ' ' + x.group()[1:], sent)
 
# 5. Return a list of sentences from a tweet
def seperate_sentences (tweet):
    # assume '.' is used in abbreviations
    ignore_indexes = set()
    sents = []
    puncts = []
    # find a list of abbreviations
    abbrevs_matches = abbrevs_pattern.finditer(tweet)
    if abbrevs_matches:
        for match in abbrevs_matches:
            abbrev = match.group(2)
            for i in range(len(abbrev)):
                if abbrev[i] == '.':
                    ignore_indexes.add(i + match.start() + len(match.group(1)))
    # find a list of sentence separator indices
    # skip the ones that are part of the abbreviation, for example 'e.g.'
    # 6. Consecutive punctuations are not split
    separator_matches = separator_pattern.finditer(tweet)
    if separator_pattern:
        for match in separator_matches:
            punct = match.group()
            break_pos = match.group()
            i = len(punct) - 1
            while i >= 0:
                if punct[i] == '.' and (i + match.start()) in ignore_indexes:
                    break
                i -= 1
            punct = punct[(i + 1):]
            if punct.strip():
                puncts.append((match.start() + i + 1, punct))
    i = 0
    sents.append('')
    # separate string into sentences
    for index, punct in puncts:
        punct_clean = punct.replace(' ', '')
        sents[-1] += tweet[i:index] + ' ' + punct_clean + ' '
        # ellipsis does not end a sentence
        if not re.match(r'\.\.\.+', punct_clean):
            sents.append('')
        i = index + len(punct)
    sents[-1] += tweet[i:].strip()
    if not sents[-1]:
        del sents[-1]   
    return sents
 
# 8. Tag each token in a sentence with part of speech
def tag_sentence_tokens(sent):
    tokens = sent.split()
    tags = tagger.tag(tokens)
    for i in range(len(tokens)):
        lc_token = tokens[i].lower()
        if ((lc_token in female_first_name) or (lc_token in male_first_name)) and (tags[i] == "NN"):
            tokens[i] += '/' + "NNP"
        # ellipsis
        elif re.match(r'\.\.\.+', tokens[i]):
            tokens[i] += '/' + ":"
        # end of sentence punctuation
        elif separator_pattern.match(tokens[i]):
            tokens[i] += '/' + "."
        else:
            tokens[i] += '/' + tags[i]
    return ' '.join(tokens)
 
# process a list of tweets from belonging to a class
def process_class (class_list, train_fd):
    for item in class_list:
        tweet_content = item.split("\",\"") # The fifth item is the tweet
        tweet_num = "<A=" + tweet_content[0][1:] + ">"
        if len(tweet_content) > 6:
            for i in range(6, len(tweet_content)):
                tweet_content[5] += tweet_content[i]
        tweet = (tweet_content[5])[:-2]
        tweet = remove_char_codes(tweet)
        tweet = remove_tags_and_attr(tweet)
        tweet = remove_URL (tweet)
        tweet = process_username_hashtag(tweet)
        train_fd.write (tweet_num + "\n")
        sentence_list = seperate_sentences (tweet)
        for sentence in sentence_list:
            sentence = insert_spacing (sentence)
            sentence = tag_sentence_tokens(sentence)
            train_fd.write (sentence + "\n")

def create_feature_category (file_name):
    file_name = word_list_dir + file_name
    file_fd = open (file_name)
    PoS_list = file_fd.readlines ()
    PoS_list = [pos.strip('\n') for pos in PoS_list if pos != '\n']
    return PoS_list
 


if __name__ == "__main__":

    ### GLOBAL VARIABLES ###

    abbrevs = read_word_list(word_list_dir + 'abbrev.english') + \
    read_word_list(word_list_dir + 'pn_abbrev.english')
    abbrevs = [re.escape(abbrev) for abbrev in abbrevs]
    abbrevs_pattern = re.compile(r'(\s)(' + '|'.join(abbrevs) + r')')

    EoS_puncts = r'.?!'
    other_puncts = r',;:-()[]{}"+^%$#@*'
    # apostrophe is handled separately
        
    EoS_puncts = [re.escape(EoS_punct) for EoS_punct in EoS_puncts]
    separator_pattern = re.compile(r'(\s*(' + '|'.join(EoS_puncts) + r')\s*)+')
    other_puncts = [re.escape(other_punct) for other_punct in other_puncts]
    non_EoS_pattern = re.compile(r'\s*(' + '|'.join(other_puncts) + r')\s*')
    apost_pattern = re.compile(r"\Sn?'\S")

    tagger = NLPlib.NLPlib()

    ### END OF GLOBAL VARIABLES ###


    train_data = sys.argv[2]
    csv_file = sys.argv[1]
    group_ID = -1
    if len(sys.argv) == 4:
        group_ID = int(sys.argv[2])
        train_data = sys.argv[3]

    csv_fd = open (csv_file, "r")
    train_fd = open (train_data, "w")
    lines = []
    lines = csv_fd.readlines()
    last_name = create_feature_category ("lastNames.txt")
    male_first_name = create_feature_category ("maleFirstNames.txt")
    female_first_name = create_feature_category ("femaleFirstNames.txt")

    # Use all data if group ID is -1 
    if group_ID != -1:
        class_4_start = 800000
        class_0_lower = group_ID * 5500
        class_0_upper = (group_ID + 1) * 5500
        class_4_lower = class_4_start + group_ID * 5500
        class_4_upper = class_4_start + (group_ID + 1) * 5500
        class_0 = lines[class_0_lower: class_0_upper]
        class_4 = lines[class_4_lower: class_4_upper]
        process_class (class_0, train_fd)
        process_class (class_4, train_fd)
    else: 
        process_class (lines, train_fd)

    csv_fd.close()
    train_fd.close()
