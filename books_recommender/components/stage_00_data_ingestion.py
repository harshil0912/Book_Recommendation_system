import sys

from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class DataIngestion:

    def __init__(self, app_config=AppConfiguration()):

        """
        Data Ingestion Initialization
        """

        try:

            logging.info(
                f"{'=' * 20} Data Ingestion log started. {'=' * 20}"
            )

            self.data_ingestion_config = (
                app_config.get_data_ingestion_config()
            )

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_ingestion(self):

        try:

            logging.info(
                f"Dataset directory: "
                f"{self.data_ingestion_config.dataset_dir}"
            )

            logging.info(
                f"Books file: "
                f"{self.data_ingestion_config.books_file}"
            )

            logging.info(
                f"Ratings file: "
                f"{self.data_ingestion_config.ratings_file}"
            )

            logging.info(
                f"Users file: "
                f"{self.data_ingestion_config.users_file}"
            )

            return self.data_ingestion_config

        except Exception as e:
            raise AppException(e, sys) from e