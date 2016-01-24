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

def SimilarityRaw(AddressArray,Suggestion):
  score_list = {}
  AddressMeta = get_metaphone_from_word(AddressArray)
  for y in xrange(len(Suggestion)):
    SuggestMeta = get_metaphone_from_word(Suggestion[y])
    score = MatchingScore(calculate_similarity_score(Suggestion[y], AddressArray), calculate_similarity_score(SuggestMeta, AddressMeta))
    score_list[Suggestion[y]] = score 
  return score_list

def get_metaphone_from_word(word):
  return doublemetaphone(word)[0] if len(doublemetaphone(word)[0]) > 1 else doublemetaphone(word)[1]

def RelevantWord(query,limit):
  final_score = {}
  for key in query:
    final_score[key] = calculate_matching_score(0.49, 0.51, query[key]) if query[key].metaphone_score == 1 else calculate_matching_score(0.68, 0.32, query[key])
  final_score = sorted(final_score.items(), key=operator.itemgetter(1), reverse = True)
  return final_score[0:limit]
  
def SpellCheck(query,wordlist,limit):
  wordlist = map(lambda s: s.strip(), wordlist)
  AllScore = SimilarityRaw(query.lower(),wordlist)
  Answer   = RelevantWord(AllScore,limit)
  return Answer