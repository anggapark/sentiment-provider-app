"""
This is a boilerplate pipeline 'machine_learning'
generated using Kedro 0.19.9
"""

import logging
from typing import Tuple, Any

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import f1_score


def split_data(data: pd.DataFrame, parameters: dict[str, Any]) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters_machine_learning.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data[parameters["labels"]]

    train_df, X_test, train_label, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    X_train, X_val, y_train, y_val = train_test_split(
        train_df, train_label, test_size=0.2, random_state=0
    )
    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


def train_model(
    X_train: pd.Series, y_train: pd.Series, parameters: dict[str, Any]
) -> SVC:
    """Trains the linear classification model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for labels.
        parameters: Parameters defined in parameters_machine_learning.yml.

    Returns:
        Trained model.
    """
    classification_model = SVC(
        C=parameters["C"], gamma=parameters["gamma"], kernel=parameters["kernel"]
    )

    # create train pipeline
    trained_model = Pipeline(
        [("word_embedding", TfidfVectorizer()), ("clf_model", classification_model)]
    )
    # vectorizer = TfidfVectorizer()
    # X_train = vectorizer.fit_transform(X_train)

    trained_model.fit(X_train.squeeze(), np.ravel(y_train))
    return trained_model


def predict(classification_model: SVC, X_test: pd.Series) -> pd.Series:
    """Calculates and logs the coefficient of determination.

    Args:
        classification_model: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = classification_model.predict(X_test.squeeze())
    return y_pred


def evaluate_model(y_pred: pd.Series, y_test: pd.Series):
    """Calculates and logs the F1-Score on test data.

    Args:
        classification_model: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for sentiment labels.
    """
    score = f1_score(y_test.squeeze(), y_pred)
    logger = logging.getLogger(__name__)
    logger.info(f"Model has a F1-Score of {score*100:.3f} % on test data.")

    return score
