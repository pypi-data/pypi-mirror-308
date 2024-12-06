from typing import Dict

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from EternalTeleSales.clean_EternalTeleSales import CleanTaskEternalTeleSales


class MarketingAddressInfoClean(CleanTaskEternalTeleSales):

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Transform the data by extracting zip codes from the 'address' field in the Marketing department's dataset.

        This method filters the data for records from the Marketing department, joins the relevant datasets,
        extracts the zip code from the address using a regular expression, and separates the zip code from the
        address field. It then cleans up the address field by removing any extra commas and spaces.

        @params: dfs (Dict[str, DataFrame]): Dictionary of input DataFrames with keys 'df_dataset_one' and 'df_dataset_two'.
        @returns: DataFrame: A transformed DataFrame containing only the 'address' and 'zip_code' columns.
        """
        # Define regex pattern to capture the zip code format (4 digits followed by optional whitespace and two letters)
        zip_code_pattern = r"\b(\d{4}\s?[A-Z]{2})\b"

        # Filter by Marketing department before joining
        df = dfs["df_dataset_one"].filter(F.lower(F.col("area")) == "marketing")
        # Join the dfs
        df = df.join(dfs["df_dataset_two"], on="id", how="inner")

        df = df.withColumn(
            "zip_code", F.trim(F.regexp_extract(F.col("address"), zip_code_pattern, 1))
        )
        df = (
            df.withColumn(
                "address", F.regexp_replace(F.col("address"), zip_code_pattern, ",")
            )
            .withColumn("address", F.regexp_replace(F.col("address"), r",\s*,*", ","))
            .withColumn(
                "address", F.trim(F.regexp_replace("address", r"(^,)|(,$)", ""))
            )
        )
        df = df.select(F.col("address"), F.col("zip_code"))

        return super().transform(df)
