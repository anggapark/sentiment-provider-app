"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import combine_dataset, preprocessing_texts

# def create_pipeline(**kwargs) -> Pipeline:
#     return pipeline([])


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=combine_dataset,
                inputs=["telkom_df", "xl_df", "indosat_df", "smartfren_df"],
                outputs="app_review_df",
                name="combine_dataset",
            ),
            node(
                func=preprocessing_texts,
                inputs="app_review_df",
                outputs="preprocessed_df",
                name="preprocess_texts",
            ),
        ]
    )
