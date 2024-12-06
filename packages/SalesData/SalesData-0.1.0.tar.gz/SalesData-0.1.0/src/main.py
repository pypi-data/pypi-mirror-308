import argparse
import importlib
from timeit import default_timer as timer

from logger import Logger


def main() -> None:
    """
    Main entry point for executing data asset tasks. This function parses command-line
    arguments for the data asset name and file paths, initializes logging, dynamically loads
    the specified data asset module and class, and runs its `run()` method.

    It also tracks and logs the task duration, handling any exceptions that occur during task
    execution.
    """

    start = timer()

    # Argument parser setup for command-line arguments
    parser = argparse.ArgumentParser(description="ABN Outputs")
    parser.add_argument("--data_asset", type=str, dest="data_asset", required=True)
    parser.add_argument(
        "--file_path", type=str, nargs="+", dest="file_path", required=True
    )

    # Parse the arguments from the command line
    args = parser.parse_args()
    data_asset = args.data_asset
    file_path = args.file_path

    # Initialize a logger instance with the data asset name
    logger = Logger(data_asset)
    try:

        logger.log_message("INFO", f"Starting task: {data_asset.upper()}")
        logger.log_message("INFO", f"Task Input Files: {file_path}")
        logger.log_message("INFO", f"Task Output Location: {data_asset}")

        # Dynamically import the data asset module based on the provided name
        data_asset_module = importlib.import_module(
            f"EternalTeleSales.data_assets.{data_asset}"
        )
        # Dynamically get the class within the module and instantiate it with logger, data_asset, and file_path
        data_asset_class = getattr(
            data_asset_module, f"{data_asset.title().replace('_', '')}Clean"
        )(logger, data_asset, file_path)

        # Run the primary task method within the data asset class
        data_asset_class.run()

        end = timer()
        logger.log_message(
            logging_level="INFO",
            message=f"Completed task: {data_asset.upper()}; task_duration: {end-start}",
        )

    except Exception as exc:
        # Handle any exception that occurs and log error details
        end = timer()

        logger.log_message(
            logging_level="ERROR",
            message=f" - Error occurred during execution of the action. Error message: {exc}; \n - task_duration: {end-start}",
        )

        logger.clear_handlers()

        raise Exception(exc)


if __name__ == "__main__":
    main()
