import operator
import jellyfish
import itertools
from metaphone import doublemetaphone

class MatchingScore(object):
  def __init__(self, raw_score, metaphone_score):
    self.raw_score       = raw_score
    self.metaphone_score = metaphone_score

def calculate_similarity_score(query, vocab_word):
  score = MatchingScore(calculate_jaro_winkler_score(vocab_word, query), calculate_jaro_winkler_score(get_metaphone_from_word(vocab_word), get_metaphone_from_word(query)))
  return calculate_matching_score(0.49, 0.51, score) if score.metaphone_score == 1 else calculate_matching_score(0.68, 0.32, score)

def calculate_jaro_winkler_score(word, candidate):
  return jellyfish.jaro_winkler(unicode(word), unicode(candidate))

def calculate_matching_score(multiplier_raw, multiplier_meta, vocab_score):
  return (multiplier_raw * vocab_score.raw_score + multiplier_meta * vocab_score.metaphone_score)

def get_metaphone_from_word(word):
  return doublemetaphone(word)[0] if len(doublemetaphone(word)[0]) > 1 else doublemetaphone(word)[1]
  
def spellcheck(query, wordlist, limit):
  scores     = map(lambda x: calculate_similarity_score(query.lower(), x), wordlist)
  score_list = sorted(dict(itertools.izip(wordlist, scores)).items(), key = operator.itemgetter(1), reverse = True)
  return score_list[0:limit]