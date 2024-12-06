from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class DepartmentBreakdownClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Perform transformations to calculate the sales amount and call success rate for each department.

        This function joins datasets on the "id" field, groups data by department, calculates the total sales amount,
        and computes the percentage of successful calls per department.

        @params: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one' and 'df_dataset_two'.
        @return: DataFrame: A DataFrame with aggregated metrics for each department, including sales amount and call success rate, rounded to two decimal places.
        """
        # Join the dfs
        df = dfs["df_dataset_one"].join(dfs["df_dataset_two"], on="id", how="inner")
        # Aggregation between each department
        df = (
            df.groupBy(F.col("area"))
            .agg(
                F.sum(F.col("sales_amount")).alias("sales_amount"),
                (
                    F.sum(F.col("calls_successful")) / F.sum(F.col("calls_made")) * 100
                ).alias("calls_success_rate"),
            )
            .withColumn("calls_success_rate", F.round(F.col("calls_success_rate"), 2))
        )

        return super().transform(df)
