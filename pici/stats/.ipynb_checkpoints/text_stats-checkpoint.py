from pici.decorators import join_df, as_table
import pandas as pd
from bs4 import BeautifulSoup
import nltk
import numpy as np


class TextStats:
    
    _report_posts_text_stats = {
        "posts_word_occurence": ["words"]
    }
    
    _report_posts_length = {
        "posts_word_length": []
    }
    
    def _count_words(self, t, words):
        if isinstance(t, str):
            bs = BeautifulSoup(t, features="html.parser")
            text = bs.get_text()
            tok = nltk.word_tokenize(text) 
            counts =  nltk.FreqDist(tok)
            return {'occurence of {}'.format(w): counts[w] or 0 for w in words}
        else:
            return {'occurence of {}'.format(w): np.nan for w in words}
        
    def _number_of_words(self, t):
        if isinstance(t, str):
            bs = BeautifulSoup(t, features="html.parser")
            text = bs.get_text()
            tok = nltk.word_tokenize(text) 
            return len(tok)
        else:
            return np.nan    
        
    
    @join_df
    def posts_word_occurence(self, words, normalize=True):
        c = self._community
        p = c.posts[c.text_column]
        
        def countw(t):
            if normalize:
                num_words = self._number_of_words(t)
                return {k:v/num_words if num_words>0 else 0 for k,v in self._count_words(t, words).items()}
            else:
                return self._count_words(t, words)
              
        results =  c.posts[c.text_column].apply(countw).apply(pd.Series)

        return {c: results[c] for c in results.columns}
    
    def posts_word_length(self):
        c = self._community
        p = c.posts[c.text_column]

        return {
            'number of words': c.posts[c.text_column].apply(self._number_of_words)
        }
        