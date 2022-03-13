import pandas as pd
from nltk.corpus import stopwords

import settings
from wordcloud import WordCloud


def generate_wordcloud(df: pd.DataFrame, column: str) -> str:
    filename = f'{settings.IMG_DIR}{column}_wordcloud.png'

    text = ' '.join([val for val in df[column].values])
    wordcloud = WordCloud(
        width=800,
        height=800,
        stopwords=stopwords.words('english'),
        background_color='rgba(255, 255, 255, 1)',
        mode='RGBA',
        min_font_size=10).generate(text)
    wordcloud.to_file(filename)
    return f'/{filename}'
