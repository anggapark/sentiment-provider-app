"""
This is a boilerplate pipeline 'machine_learning'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import split_data, train_model, predict, evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=[
                    "preprocessed_df",
                    "params:splitting_options",
                ],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train", "params:model_params"],
                outputs="classification_model",
                name="train_model_node",
            ),
            node(
                func=predict,
                inputs=["classification_model", "X_test"],
                outputs="y_pred",
                name="prediction",
            ),
            node(
                func=evaluate_model,
                inputs=["y_pred", "y_test"],
                outputs="classification_score",
                name="evaluate_model_node",
            ),
        ]
    )
