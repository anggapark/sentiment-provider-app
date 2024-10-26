"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.19.9
"""

import os
from tqdm import tqdm
import unicodedata

import pandas as pd
import numpy as np

import re
import nltk

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
from nltk import ngrams
from nltk.corpus import stopwords

# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from mpstemmer import MPStemmer


############################
# Combine dataset
############################
def combine_dataset(
    telkom_df: pd.DataFrame,
    xl_df: pd.DataFrame,
    indosat_df: pd.DataFrame,
    smartfren_df: pd.DataFrame,
) -> pd.DataFrame:
    # add provider before mergine for analysis
    telkom_df["provider"] = "telkomsel"
    xl_df["provider"] = "xl"
    indosat_df["provider"] = "indosat"
    smartfren_df["provider"] = "smartfren"

    all_df = pd.concat(
        [telkom_df, xl_df, indosat_df, smartfren_df], axis=0
    ).reset_index(drop=True)
    all_df["content"] = all_df["content"].astype("object")
    return all_df


############################
# Data Preprocessing
############################
def remove_missing_value(df: pd.DataFrame) -> pd.DataFrame:
    nan_idx = df[(df["sentiment"].isnull()) | (df["content"].isnull())].index
    # drop the index
    df = df.drop(nan_idx, axis=0).reset_index(drop=True)
    return df


def remove_emoji(df: pd.DataFrame) -> pd.DataFrame:
    # https://en.wikipedia.org/wiki/List_of_emoticons
    emoji_pattern = re.compile(
        r"^[\U0001F600-\U0001F64F"  # emoticons
        r"\U0001F300-\U0001F5FF"  # misc Symbols and Pictographs
        r"\U0001F680-\U0001F6FF"  # transport and Map Symbols
        r"\U0001F700-\U0001F77F"  # alchemical Symbols
        r"\U0001F780-\U0001F7FF"  # geometric Shapes Extended
        r"\U0001F800-\U0001F8FF"  # supplemental Arrows-C
        r"\U0001F900-\U0001F9FF"  # supplemental Symbols and Pictographs
        r"\U0001FA00-\U0001FA6F"  # chess Symbols
        r"\U0001FA70-\U0001FAFF"  # symbols and Pictographs Extended-A
        r"\U00002700-\U000027BF"  # dingbats
        r"\U000024C2-\U0001F251"  # enclosed characters
        r"]+$"
    )

    # get index containing emoji-only reviews
    emoji_idx = df[df["content"].apply(lambda x: bool(emoji_pattern.match(x)))].index

    # drop the index
    return df.drop(emoji_idx, axis=0).reset_index(drop=True)


def lowercase(texts: str):
    """Converts all characters in the input text to lowercase.

    Args:
        texts (str): A string of text to be converted to lowercase.
    Returns:
        str: The input text with all characters converted to lowercase.
    Example:
        >>> lowercase("Ini Adalah Teks")
        'ini adalah teks'
    """
    words = texts.split()
    words = [word.lower() for word in words]
    return " ".join(words)


def remove_stopwords(texts: str):
    """Removes stopwords from the input text based on a predefined list of stopwords in Indonesian.

    Args:
        texts (str): A string of text from which stopwords will be removed.
    Returns:
        str: The text with stopwords removed.
    Example:
        >>> remove_stopwords("ini adalah sebuah contoh teks")
        'contoh teks'
    """
    words = texts.split()
    words = [word for word in words if word not in stopwords.words("indonesian")]
    return " ".join(words)


def add_space_after_punctuation(text: str):
    """Add space after punctuations so it can be removed using remove_punctuation.
    preventing word to combine after punctuation removal

    Args:
        texts (str): A string of text from which stopwords will be removed.
    Returns:
        str: The text with added space after punctuation.
    Example:
        >>> add_space_after_punctuation("Aplikasi yang sangat buruk,jelek,pembohong")
        'Aplikasi yang sangat buruk, jelek, pembohong'
    """
    text = re.sub(r"([.,!?;:])([^\s])", r"\1 \2", text)
    return text


def remove_punctuation(texts: str):
    """Removes punctuation characters from the input text.

    Args:
        texts (str): A string of text from which punctuation will be removed.
    Returns:
        str: The text without any punctuation.
    Example:
        >>> remove_punctuation("Halo! Ini, adalah: contoh.")
        'Halo Ini adalah contoh'
    """
    texts = re.sub(r"[^\w\s]", " ", texts)
    return texts


def remove_non_ascii(texts: str):
    """Removes non-ASCII characters from the input text.

    Args:
        texts (str): A string of text from which non-ASCII characters will be removed.
    Returns:
        str: The text with non-ASCII characters removed.
    Example:
        >>> remove_non_ascii("café naïve résumé")
        'cafe naive resume'
    """
    words = texts.split()
    words = [
        unicodedata.normalize("NFKD", word)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
        for word in words
    ]
    return " ".join(words)


def remove_urls(texts: str):
    """Removes URLs from the input texts.

    Args:
        texts (str): A string of texts from which URLs will be removed.
    Returns:
        str: The texts without any URLs.
    Example:
        >>> remove_urls("Check this out: https://example.com")
        'Check this out:'
    """
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    return url_pattern.sub(r"", texts)


def stemmer(texts: str):
    """Reduces words to their root form using a stemming algorithm for Indonesian.

    Args:
        texts (str): A string of text to be stemmed.
    Returns:
        str: The text with words reduced to their root forms.
    Example:
        >>> stemmer("makanan minuman berjalan")
        'makan minum jalan'
    """
    #     stem = StemmerFactory()
    stemmer = MPStemmer()
    words = texts.split()
    texts = [stemmer.stem_kalimat(word) for word in words]
    return " ".join(words)


def load_kamus_alay():
    slang_df = pd.read_csv("colloquial-indonesian-lexicon-v3.csv")
    return slang_df[["slang", "formal"]].drop_duplicates()


def replace_slang(texts: str):
    """Replaces slang words in the input texts with their formal equivalents using
    a slang dictionary.

    Args:
        texts (str): A string of texts containing slang words.
    Returns:
        str: The texts with slang words replaced by their formal equivalents.
    Example:
        >>> replace_slang("gw mau makan")
        'saya mau makan'
    """
    slang_df = load_kamus_alay()
    slang_dict = dict(zip(slang_df["slang"], slang_df["formal"]))
    words = texts.split()
    normalized_words = [slang_dict.get(word.lower(), word) for word in words]
    return " ".join(normalized_words)


def remove_irrelevant_words(texts: str):
    """Removes specific irrelevant words from the input text if they stand alone.
    (for some reason, "nya" are one of most used word after preprocessing, so
    remove that word)
    Args:
        texts (str): A string of text from which irrelevant words will be removed.
    Returns:
        str: The text with irrelevant standalone words removed.
    Example:
        >>> remove_irrelevant_words("Aplikasi ini lebih bagus dari Telkomsel myTelkomsel")
        'Aplikasi ini lebih bagus dari myTelkomsel'
    """
    irrelevant_words = [
        "my",
        "telkomsel",
        "indihome",
        "telkom",
        "mytelkomsel",
        "mytelkom",
        "xl",
        "xi",
        "axis",
        "myxl",
        "indosat",
        "im3",
        "myim3",
        "smartfren",
        "sf",
        "mysf",
        "smarfren",
        "nya",
        "myindihome",
        "sih",
        "telsel",
    ]
    # Compile a regex pattern to match whole words
    pattern = r"\b(?:" + "|".join(re.escape(word) for word in irrelevant_words) + r")\b"
    # Replace matched standalone words with an empty string
    cleaned_text = re.sub(pattern, "", texts, flags=re.IGNORECASE)
    # Remove extra spaces
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text


def normalize_repeated_characters(texts: str):
    """fix letter repetition
    Args:
        texts (str): A string of texts from which repeated letter in word will be removed.
    Returns:
        str: The texts with repeated letter removed.
    Example:
        "mmantap" -> "mantap",
        "mannntap" -> "mantap",
        "mantapp" -> "mantap"
    """
    texts = re.sub(r"(.)\1+", r"\1", texts)
    return texts


def remove_review_less_than_n_words(texts: str, n: int = 2):
    words = texts.split()
    words = [word for word in words if len(words) > n]
    return " ".join(words)


def encode_label(label):
    """Applied encoding on label data to 1 if label is positif,
    0 otherwise

    """
    if label == "positif":
        return 1
    else:
        return 0


# Preprocessing function
def preprocessing_texts(df: pd.DataFrame) -> pd.DataFrame:
    """Applies a preprocessing text pipeline to clean the texts in a DataFrame.

    Args:
        df (pd.DataFrame): The original DataFrame containing a 'content' column with
        the text data.
    Returns:
        pd.DataFrame: The DataFrame with an additional 'clean_text' column containing
        the cleaned texts.
    """
    df = remove_missing_value(df)
    df = remove_emoji(df)

    tqdm.pandas(desc="remove_urls")
    df["clean_text"] = df["content"].progress_apply(lambda x: remove_urls(x))
    tqdm.pandas(desc="lowercase")
    df["clean_text"] = df["clean_text"].progress_apply(lambda x: lowercase(x))
    tqdm.pandas(desc="remove_non_ascii")
    df["clean_text"] = df["clean_text"].progress_apply(lambda x: remove_non_ascii(x))
    tqdm.pandas(desc="add_space_after_punctuation")
    df["clean_text"] = df["clean_text"].progress_apply(
        lambda x: add_space_after_punctuation(x)
    )
    tqdm.pandas(desc="remove_punctuation")
    df["clean_text"] = df["clean_text"].progress_apply(lambda x: remove_punctuation(x))
    tqdm.pandas(desc="replace_slang")
    df["clean_text"] = df["clean_text"].progress_apply(lambda x: replace_slang(x))
    tqdm.pandas(desc="stemmer")
    df["clean_text"] = df["clean_text"].progress_apply(lambda x: stemmer(x))
    #     tqdm.pandas(desc="remove_stopwords")
    #     df["clean_text"] = df["clean_text"].progress_apply(lambda x: remove_stopwords(x))
    tqdm.pandas(desc="remove_brand_name")
    df["clean_text"] = df["clean_text"].progress_apply(
        lambda x: remove_irrelevant_words(x)
    )
    tqdm.pandas(desc="normalize_repeated_characters")
    df["clean_text"] = df["clean_text"].progress_apply(
        lambda x: normalize_repeated_characters(x)
    )
    tqdm.pandas(desc="remove_review_less_than_n_words")
    df["clean_text"] = df["clean_text"].progress_apply(
        lambda x: remove_review_less_than_n_words(x, 2)
    )

    # because review less than 2 words were replaced by empty string
    # get the index of empty review
    empty_str_idx = df[df["clean_text"] == ""].index
    # drop the index
    df = df.drop(empty_str_idx, axis=0).reset_index(drop=True)

    # encode labels
    df["sentiment"] = df["sentiment"].apply(encode_label)

    return df


# Preprocessing function
def preprocessing_sentence(texts: str) -> str:
    """Applies a preprocessing text pipeline to clean input sentence for deploy.

    Args:
        texts (str): The original texts user input
    Returns:
        str: clean texts input ready for as model input
    """

    texts = remove_urls(texts)
    texts = lowercase(texts)
    texts = remove_non_ascii(texts)
    texts = add_space_after_punctuation(texts)
    texts = remove_punctuation(texts)
    texts = replace_slang(texts)
    texts = stemmer(texts)
    texts = remove_irrelevant_words(texts)
    texts = normalize_repeated_characters(texts)
    texts = remove_review_less_than_n_words(texts, 2)

    return texts
