import re

stopword_file = open("stopwords_minimal.txt")
all_words =  stopword_file.readline()
stop_words = all_words.strip().split(",")

punct_list_file  = open("punct_list.txt")
punct_list = punct_list_file.readline().strip().split(",")


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def tokenize_twitter(s):
    return tokens_re.findall(s)

def removehash (s):
    if s[0]=="#":
       return s[1:]
    else:
        return s 
 
def get_preprocessed_twitter_tokens(s):
    global stop_words
    s =  re.sub(r"http\S+", "", s)
    tokens = tokenize_twitter(s) 
    tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    tokens = [removehash(token)  for token in tokens if token not in stop_words and token not in 
        punct_list and not(is_number(token))]
    return tokens
