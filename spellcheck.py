import re
import operator
import re, collections
from jellyfish import jaro_distance
from jellyfish import levenshtein_distance
import jellyfish
import numpy
from metaphone import doublemetaphone

def SimilarityRaw(AddressArray,Suggestion):
  score_raw=[]
  word_area=[]
  score_meta=[]
  if(len(AddressArray)>1):
    answer = doublemetaphone(AddressArray)
    if (len(answer[0])>1):
      AddressMeta=answer[0]
    else:
      AddressMeta=answer[1]
    for y in xrange(len(Suggestion)):
      try:
        answer = doublemetaphone(Suggestion[y])
        if (len(answer[0])>1):
          SuggestMeta=answer[0]
        else:
          SuggestMeta=answer[1]
        score_meta.append(jellyfish.jaro_winkler(SuggestMeta,AddressMeta))
        score_raw.append(jellyfish.jaro_winkler(Suggestion[y],AddressArray))
        word_area.append(Suggestion[y])
      except:
        print "There was a problem matching"
  zipped= zip (word_area,score_raw,score_meta)
  finalAnswer =sorted(zipped, key=operator.itemgetter(0))
  return finalAnswer

def RelevantWord(Query,limit):
  score_final=[]
  word_final=[]
  for x in xrange(len(Query)):
    if (Query[x][2]==1.0):
      score_final.append(0.49*Query[x][1]+0.51*Query[x][2])
    else:
      score_final.append(0.68*Query[x][1]+0.32*Query[x][2])
    word_final.append(str(Query[x][0]))
  zipped= zip(word_final,score_final)
  final_Answer =sorted(zipped, key=operator.itemgetter(1),reverse=True) 
  final_Answer = numpy.array(final_Answer)
  return (final_Answer[0:limit])
  
def SpellCheck(query,wordlist,limit):
  wordlist = map(lambda s: s.strip(), wordlist)
  AllScore= SimilarityRaw(query.ToLower(),wordlist)
  Answer = RelevantWord(AllScore,limit)
  return Answer
