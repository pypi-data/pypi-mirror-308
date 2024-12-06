from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame
from pyspark.sql.window import Window

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class BestSalespersonClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Perform transformations to identify the top-performing salesperson in each country.

        This function joins three datasets, aggregates sales data by salesperson and country,
        ranks salespeople within each country, and filters the DataFrame to keep only the top
        salesperson per country.

        @params:dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one', 'df_dataset_two', and 'df_dataset_three'.
        @return: A DataFrame with the top-performing salesperson for each country, including columns for the salesperson's name, country, and total sales amount.
        """
        # Join dataframes
        df = dfs["df_dataset_one"].join(dfs["df_dataset_two"], on="id", how="inner")
        df = df.join(
            dfs["df_dataset_three"], df.id == dfs["df_dataset_three"].caller_id, "inner"
        )
        # Group
        df = df.groupBy(["name", "country"]).agg(
            F.sum(F.col("sales_amount")).alias("total_sales_amount")
        )
        # Define window to rank salespeople within each country by total sales amount
        window_spec = Window.partitionBy("country").orderBy(
            F.col("total_sales_amount").desc()
        )

        # Rank and filter the top performer per country
        df = (
            df.withColumn("rank", F.rank().over(window_spec))
            .filter(F.col("rank") == 1)
            .drop("rank")
        )

        return super().transform(df)
