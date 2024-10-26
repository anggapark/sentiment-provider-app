import importlib
import os.path
from typing import Dict, Any, Optional
import pandas as pd
from kedro_datasets.pandas import SQLTableDataset
from kedro_datasets.pandas.sql_dataset import (
    _get_missing_module_error,
    _get_sql_alchemy_missing_error,
)
from sqlalchemy.exc import NoSuchModuleError


class DTypedSqlTableDataSet(SQLTableDataset):
    """
    https://github.com/kedro-org/kedro/discussions/898#discussioncomment-1451139
    """

    def __init__(
        self,
        table_name: str,
        credentials: Dict[str, Any],
        load_args: Optional[Dict[str, Any]] = None,
        save_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            table_name=table_name,
            credentials=credentials,
            load_args=load_args,
            save_args=save_args,
        )
        self._credentials = credentials

    def _save(self, data: pd.DataFrame) -> None:
        self._modify_save_args_dtype()
        try:
            conn = self._credentials.get("con")
            data.to_sql(**self._save_args, con=conn)
        except ImportError as import_error:
            raise _get_missing_module_error(import_error) from import_error
        except NoSuchModuleError as exc:
            raise _get_sql_alchemy_missing_error() from exc

    def _modify_save_args_dtype(self) -> None:
        new_dtype = {}
        if self._save_args == None:
            return

        dtype = self._save_args.get("dtype")

        if dtype == None:
            return

        for key, value in list(dtype.items()):
            mod_list = value.split(".")
            mod_name = ".".join(mod_list[:-1])
            class_name = "".join(mod_list[-1:])

            module = importlib.import_module(mod_name)
            actual_class = getattr(module, class_name)
            new_dtype[key] = actual_class

        self._save_args["dtype"] = new_dtype
