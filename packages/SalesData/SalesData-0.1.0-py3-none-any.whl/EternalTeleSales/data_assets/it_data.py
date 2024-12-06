from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class ItDataClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Transform data to filter for the IT department, join relevant datasets,
        and return the top 100 sales records based on sales amount.

        This method filters the data to include only records from the IT department, joins the
        datasets, orders the resulting data by sales amount in descending order, and limits
        the output to the top 100 rows.

        @param: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one' and 'df_dataset_two'.
        @return: DataFrame: A transformed DataFrame containing the top 100 sales records from the IT department.
        """
        # Filter by IT department before joining
        df = dfs["df_dataset_one"].filter(F.lower(F.col("area")) == "it")
        # Join the dfs
        df = df.join(dfs["df_dataset_two"], on="id", how="inner")
        # Order the dataframe by sales
        df = df.orderBy(F.col("sales_amount").desc())
        # Limit the Dataframe by 100
        df = df.limit(100)

        return super().transform(df)
