from pathlib import Path
import matplotlib.pyplot as plt

import pandas as pd
import glob

from italia.extract.batch import hello

def extract(str):
    pass

def density(str):
    lines = str.split("\n")
    sums = sum(len(l) for l in lines)
    return sums / len(lines)

raw = [Path(path).read_text() for path in glob.glob("./fratelli/*.html")]

df = pd.DataFrame(raw, columns=["text"])
df["density"] = df["text"].apply(density)
df.to_csv("./dataset.csv", index=None)


