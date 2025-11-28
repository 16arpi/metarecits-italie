import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spacy.lang.it import Italian
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = Italian()
stopwords = nlp.Defaults.stop_words

custom_stopwords = {"italia", "italiani", "italiano", "italiana","fratelli", "fdi", "meloni", "giorgia","centrodestra", "alleanza", "partito","rampelli", "cirielli", "renzi", "francesco","fabio",
"camera", "commissione", "parlamento","deputato", "deputati", "presidente", "capogruppo","regione", "regionale", "dichiara", "politica","legge", "decreto", "nota", "interrogazione","proposta", "politiche", "parlamentare",
"senato", "aula", "repubblica", "sistema","maggioranza", "elettorale", "elezioni", "voto", "8217", "far", "sopratutto"}

all_stopwords = stopwords | custom_stopwords

df = pd.read_csv("../extract/textes/corpus_reduit/corpus_reduit.csv")

def tokeniser(text):
    tokens = re.findall(r"\b\w+\b", str(text).lower())
    tokens = [t for t in tokens if t not in all_stopwords and len(t) > 2]
    return " ".join(tokens)

df["clean_text"] = df["text"].astype(str).apply(tokeniser)

vectorizer = TfidfVectorizer(
    max_df=0.85,    
    min_df=5,     
    ngram_range=(1, 2),
)

X = vectorizer.fit_transform(df["clean_text"])

scores = {}
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=0)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    scores[k] = score

best_k = max(scores, key=scores.get)


kmeans = KMeans(n_clusters=best_k, n_init="auto", random_state=0)
labels = kmeans.fit_predict(X)
df["cluster"] = labels


terms = vectorizer.get_feature_names_out()
centers = kmeans.cluster_centers_


for cluster_id in range(best_k):
    print(f"\nCluster {cluster_id}:")
    top_idx = np.argsort(centers[cluster_id])[::-1][:15]
    print(", ".join(terms[i] for i in top_idx))

