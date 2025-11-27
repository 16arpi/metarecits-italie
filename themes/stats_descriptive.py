import re
import random
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from spacy.lang.it import Italian 

nlp = Italian()
stopwords = nlp.Defaults.stop_words

custom_stopwords = {"italia", "italiani", "italiano", "italiana","fratelli", "fdi", "meloni", "giorgia","centrodestra", "alleanza", "partito","rampelli", "cirielli", "renzi", "francesco","fabio",
"camera", "commissione", "parlamento","deputato", "deputati", "presidente", "capogruppo","regione", "regionale", "dichiara", "politica","legge", "decreto", "nota", "interrogazione","proposta", "politiche", "parlamentare",
"senato", "aula", "repubblica", "sistema","maggioranza", "elettorale", "elezioni", "voto", "8217", "far", "sopratutto"}

all_stopwords = stopwords | custom_stopwords

df = pd.read_csv("metarecits-italie/extract/textes/corpus_reduit/corpus_reduit.csv")

def tokeniser(text):
    tokens = re.findall(r"\b\w+\b", str(text).lower())
    tokens = [
        tok for tok in tokens
        if tok not in all_stopwords and len(tok) > 2
    ]
    return tokens

all_tokens = []
for t in df["text"]:
    all_tokens.extend(tokeniser(t))

freq = Counter(all_tokens)

for word, count in freq.most_common(50):
    print(word, count)

def italian_color_func(*args, **kwargs):
    return random.choice(["#008C45", "#F4F5F0", "#CD212A"])

freq_dict = dict(freq)
wc = WordCloud(
    width=1200,
    height=600,
    background_color="black",
    max_words=200,
).generate_from_frequencies(freq_dict)
wc.recolor(color_func=italian_color_func)

plt.figure(figsize=(15, 7))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
