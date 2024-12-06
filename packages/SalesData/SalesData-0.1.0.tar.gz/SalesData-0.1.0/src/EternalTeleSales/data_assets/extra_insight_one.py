from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class ExtraInsightOneClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Perform transformations to calculate the sum of product quantity sold for each country and department.

        This function joins datasets on the "id" field, groups data by country and department,
        calculates the quantity sum, and orders the result by country and quantity.

        @params: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one' and 'df_dataset_three'.
        @return: DataFrame: A DataFrame with the quantity sum per department within each country, ordered by country and quantity.
        """
        # Filter out country
        df_3 = dfs["df_dataset_three"].select("caller_id", "country", "quantity")

        # Join dataframes
        df = dfs["df_dataset_one"].join(
            df_3, dfs["df_dataset_one"].id == df_3.caller_id, "inner"
        )

        # Group by country and department, calculating the average sales amount
        df = (
            df.groupBy("country", "area")
            .agg(F.sum("quantity").alias("sum_quantity_amount"))
            .orderBy("country", "sum_quantity_amount", ascending=False)
        )

        return super().transform(df)
