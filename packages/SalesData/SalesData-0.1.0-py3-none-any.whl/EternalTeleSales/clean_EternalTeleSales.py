import os
from typing import Dict, List

from pyspark.sql import DataFrame, SparkSession

from logger import Logger


class CleanTaskEternalTeleSales:
    """
    A class to handle the ETL (Extract, Transform, Load) tasks for the EternalTeleSales data source.

    Attributes:
        logger (Logger): An instance of the Logger class for logging task progress.
        spark (SparkSession): A SparkSession instance used for handling data processing tasks.
        file_path (List[str]): List of file paths to be processed.
        out_path (str): The output path for saving transformed data.
    """

    def __init__(self, logger: Logger, app_name: str, file_path: List[str]) -> None:
        self.spark = (
            SparkSession.builder.appName(app_name).master("local[*]").getOrCreate()
        )
        self.logger = logger
        self.file_path = file_path
        self.out_path = app_name

    def extract(self) -> Dict[str, DataFrame]:
        """
        Extract data from CSV files into a dictionary of DataFrames, where each key represents
        a dataset name and each value is a DataFrame.

        Returns:
            @return: Dict[str, DataFrame]: Dictionary with dataset names as keys and DataFrames as values.
        """

        file_path_dict = dict()
        for path in self.file_path:
            dataset = os.path.splitext(os.path.basename(path))[0]
            file_path_dict[f"df_{dataset}"] = self.spark.read.csv(path, header=True)
        return file_path_dict

    def write_file(self, df: DataFrame) -> None:
        """
        Load the transformed DataFrame into a specified output folder as a CSV file.

        Args:
            @params: df (DataFrame): The DataFrame to be saved.
        """
        df.coalesce(1).write.csv(header=True, path=self.out_path, mode="overwrite")

    def transform(self, dfs: Dict[str, DataFrame]) -> DataFrame:
        """
        Transform the extracted data. This function applies necessary transformations to all
        extracted datasets.

        @params: dfs (Dict[str, DataFrame]): A dictionary of DataFrames to be transformed.
        @return: DataFrame: A transformed DataFrame ready for loading.
        """
        # Placeholder transformation logic; implement specific transformations for the data source
        return dfs

    def run(self) -> None:
        """
        Execute the ETL process: extract data, transform it, and load the final result.
        """

        self.logger.log_message("INFO", "Start Loading Data")
        dfs = self.extract()

        self.logger.log_message("INFO", "Transform Data")
        df = self.transform(dfs)

        self.logger.log_message("INFO", "Loading data into a file")
        self.write_file(df)

        self.spark.stop()
