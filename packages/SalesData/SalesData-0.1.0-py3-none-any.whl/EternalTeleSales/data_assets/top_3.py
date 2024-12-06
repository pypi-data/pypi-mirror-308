from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame
from pyspark.sql.window import Window

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class Top3Clean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Transform the data by calculating the call success rate and ranking employees
        within their department by sales amount, filtering for those with a success rate above 75%.

        This method joins two datasets, calculates the call success rate, filters employees
        with a success rate above 75%, ranks the top employees by sales amount within each department,
        and rounds the success rate for readability.

        @param: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one' and 'df_dataset_two'.
        @return: DataFrame: A transformed DataFrame containing the department, employee rank, sales amount, and rounded call success rate for the top employees.
        """
        # Join the dfs
        df = dfs["df_dataset_one"].join(dfs["df_dataset_two"], on="id", how="inner")
        # Calculate success rate
        df = df.withColumn(
            "calls_success_rate",
            (F.col("calls_successful") / F.col("calls_made")) * 100,
        )
        # Filter by 75
        df = df.filter(F.col("calls_success_rate") > 75)
        # Define window specification to rank employees within each department by sales_amount
        window_spec = Window.partitionBy("area").orderBy(F.col("sales_amount").desc())

        # Rank and filter top 3 by department
        df = (
            df.withColumn("rank", F.rank().over(window_spec))
            .filter(F.col("rank") <= 3)
            .drop("rank")
        )

        # Round the success rate for readability
        df = df.withColumn(
            "calls_success_rate", F.round(F.col("calls_success_rate"), 2)
        )

        return super().transform(df)
