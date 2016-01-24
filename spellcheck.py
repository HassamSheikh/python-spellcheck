import operator
import jellyfish
from metaphone import doublemetaphone

class MatchingScore(object):
  def __init__(self, raw_score, metaphone_score):
    self.raw_score       = raw_score
    self.metaphone_score = metaphone_score

def calculate_similarity_score(word, candidate):
  return jellyfish.jaro_winkler(unicode(word), unicode(candidate))

def calculate_matching_score(multiplier_raw, multiplier_meta, vocab_score):
  return (multiplier_raw * vocab_score.raw_score + multiplier_meta * vocab_score.metaphone_score)

def SimilarityRaw(AddressArray, Suggestion, metaphone_list, limit):
  score_list                  = {}
  AddressMeta                 = get_metaphone_from_word(AddressArray)
  for y in xrange(len(Suggestion)):
    score                     = MatchingScore(calculate_similarity_score(Suggestion[y], AddressArray), calculate_similarity_score(metaphone_list[y], AddressMeta))
    score_list[Suggestion[y]] = calculate_matching_score(0.49, 0.51, score) if score.metaphone_score == 1 else calculate_matching_score(0.68, 0.32, score) 
  score_list                  = sorted(score_list.items(), key=operator.itemgetter(1), reverse = True)
  return score_list[0:limit]

def get_metaphone_from_word(word):
  return doublemetaphone(word)[0] if len(doublemetaphone(word)[0]) > 1 else doublemetaphone(word)[1]
  
def SpellCheck(query, wordlist, limit):
  wordlist       = map(lambda s: s.strip(), wordlist)
  metaphone_list = map(get_metaphone_from_word, wordlist)
  AllScore       = SimilarityRaw(query.lower(), wordlist, metaphone_list, limit)
  return AllScore