from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame
from pyspark.sql.window import Window

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class Top3MostSoldPerDepartmentNetherlandsClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Transform the data by ranking products within each department based on the quantity sold,
        specifically for the Netherlands.

        This method filters the data to only include records from the Netherlands, joins relevant datasets,
        groups by department and product to calculate the total quantity sold, and ranks the top 3 products
        by quantity within each department.

        @param: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one', 'df_dataset_three'.
        @return: DataFrame: A transformed DataFrame containing the department, product, and total quantity sold, with only the top 3 products per department.
        """
        # Filter the country before joining
        df = dfs["df_dataset_three"].filter(F.lower(F.col("country")) == "netherlands")
        # Join
        df = dfs["df_dataset_one"].join(
            df, dfs["df_dataset_one"].id == df.caller_id, "inner"
        )
        # Groupby the Department and Product to get the sold number
        df = df.groupBy(["area", "product_sold"]).agg(
            F.sum(F.col("quantity")).alias("total_quantity_sold")
        )

        # Define window to rank products within each department by quantity sold
        window_spec = Window.partitionBy("area").orderBy(
            F.col("total_quantity_sold").desc()
        )

        # Rank and filter top 3 products per department
        df = (
            df.withColumn("rank", F.rank().over(window_spec))
            .filter(F.col("rank") <= 3)
            .drop("rank")
        )

        return super().transform(df)
