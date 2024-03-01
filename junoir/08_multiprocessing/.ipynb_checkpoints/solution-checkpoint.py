import re
from string import punctuation

import pandas as pd
from joblib import delayed, Parallel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def clear_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")
    text = str(text)
    text = re.sub(r"https?://[^,\s]+,?", "", text)
    text = re.sub(r"@[^,\s]+,?", "", text)
    transform_text = text.translate(str.maketrans("", "", punctuation))
    transform_text = re.sub(" +", " ", transform_text)
    text_tokens = word_tokenize(transform_text)
    lemma_text = [lemmatizer.lemmatize(word.lower()) for word in text_tokens]
    cleaned_text = " ".join([str(word) for word in lemma_text if word not in stop_words])
    return cleaned_text
    
def clear_data(source_path: str, target_path: str, n_jobs: int):
    """Parallel process dataframe

    Parameters
    ----------
    source_path : str
        Path to load dataframe from

    target_path : str
        Path to save dataframe to

    n_jobs : int
        Count of job to process
    """
    # Функция для очистки текста

    
    # Загрузка данных
    data = pd.read_parquet(source_path)
    data = data.copy().dropna().reset_index(drop=True)
    # Применение очистки текста к каждому текстовому столбцу параллельно
    cleaned_text_list = Parallel(n_jobs=n_jobs, backend='multiprocessing')(
        delayed(clear_text)(text) for text in data["text"]
    )
    
    # Добавление очищенных текстов в DataFrame
    data["cleaned_text"] = cleaned_text_list
    
    # Сохранение DataFrame в файл
    data.to_parquet(target_path)
