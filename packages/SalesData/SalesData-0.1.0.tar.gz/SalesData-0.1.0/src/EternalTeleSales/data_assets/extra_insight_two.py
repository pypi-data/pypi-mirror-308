from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class ExtraInsightTwoClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Transform data to classify employees by call success rate into performance categories,
        and calculate metrics such as employee count and average sales per category.

        This method joins datasets, computes call success rates, classifies employees into
        performance categories based on success rates, and calculates the number of employees
        and average sales in each category.

        @params: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one', 'df_dataset_two', and 'df_dataset_three'.
        @return: DataFrame: A transformed DataFrame with employee count and average sales amount by performance category.
        """
        # Join dataframes
        df = dfs["df_dataset_one"].join(dfs["df_dataset_two"], on="id", how="inner")

        # Calculate call success rate
        df = df.withColumn(
            "success_rate", F.col("calls_successful") / F.col("calls_made") * 100
        )

        # Classify employees into performance categories
        df = df.withColumn(
            "performance_category",
            F.when(F.col("success_rate") >= 75, "High")
            .when(
                (F.col("success_rate") >= 50) & (F.col("success_rate") < 75), "Medium"
            )
            .otherwise("Low"),
        )

        # Count employees in each performance category and calculate avg sales
        df = (
            df.groupBy("performance_category")
            .agg(
                F.count("id").alias("employee_count"),
                F.round(F.avg("sales_amount"), 2).alias("avg_sales_amount"),
            )
            .orderBy("performance_category", ascending=False)
        )

        return super().transform(df)
