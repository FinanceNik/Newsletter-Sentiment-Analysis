import pandas as pd

df = pd.read_csv('data/movie.csv')


def get_data():
    df_cleaned = df.dropna()
    df_cleaned['label'] = df_cleaned['label'].astype(int)
    df_cleaned['text'] = df_cleaned['text'].astype(str)
    return df_cleaned


