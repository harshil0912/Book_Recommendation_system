import os
import sys
import pandas as pd

from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class DataValidation:

    def __init__(self, app_config=AppConfiguration()):
        try:
            logging.info(
                f"{'=' * 20} Data Validation log started. {'=' * 20}"
            )

            self.data_ingestion_config = (
                app_config.get_data_ingestion_config()
            )

            self.data_validation_config = (
                app_config.get_data_validation_config()
            )

            self.data_transformation_config = (
                app_config.get_data_transformation_config()
            )

        except Exception as e:
            raise AppException(e, sys) from e

    def preprocess_data(self):
        try:

            # -------------------------------
            # 1. Get dataset paths
            # -------------------------------

            dataset_dir = self.data_ingestion_config.dataset_dir

            books_path = os.path.join(
                dataset_dir,
                self.data_validation_config.books_csv_file
            )

            ratings_path = os.path.join(
                dataset_dir,
                self.data_validation_config.ratings_csv_file
            )

            users_path = os.path.join(
                dataset_dir,
                self.data_validation_config.users_csv_file
            )

            logging.info(f"Books path: {books_path}")
            logging.info(f"Ratings path: {ratings_path}")
            logging.info(f"Users path: {users_path}")

            # -------------------------------
            # 2. Read the CSV files
            # -------------------------------

            books = pd.read_csv(
                books_path,
                sep=";",
                encoding="latin-1",
                on_bad_lines="skip"
            )

            ratings = pd.read_csv(
                ratings_path,
                sep=";",
                encoding="latin-1",
                on_bad_lines="skip"
            )

            users = pd.read_csv(
                users_path,
                sep=";",
                encoding="latin-1",
                on_bad_lines="skip"
            )

            logging.info("All CSV files loaded successfully.")

            # -------------------------------
            # 3. Select required book columns
            # -------------------------------

            books = books[
                [
                    "ISBN",
                    "Book-Title",
                    "Book-Author",
                    "Year-Of-Publication",
                    "Publisher",
                    "Image-URL-L"
                ]
            ]

            # -------------------------------
            # 4. Find active users
            # -------------------------------

            min_user_ratings = (
                self.data_transformation_config.min_user_ratings
            )

            x = ratings["User-ID"].value_counts() > min_user_ratings

            y = x[x].index

            ratings = ratings[
                ratings["User-ID"].isin(y)
            ]

            logging.info(
                f"Ratings after user filtering: {ratings.shape}"
            )

            # -------------------------------
            # 5. Merge ratings with books
            # -------------------------------

            users_with_books = ratings.merge(
                books,
                on="ISBN"
            )

            logging.info(
                f"Ratings + books shape: {users_with_books.shape}"
            )

            # -------------------------------
            # 6. Count ratings for each book
            # -------------------------------

            number_ratings = (
                users_with_books
                .groupby("Book-Title")["Book-Rating"]
                .count()
                .reset_index(name="num_ratings")
            )

            # -------------------------------
            # 7. Merge rating counts
            # -------------------------------

            final_ratings = users_with_books.merge(
                number_ratings,
                on="Book-Title"
            )

            # -------------------------------
            # 8. Keep popular books
            # -------------------------------

            min_book_ratings = (
                self.data_transformation_config.min_book_ratings
            )

            final_ratings = final_ratings[
                final_ratings["num_ratings"] > min_book_ratings
            ]

            # -------------------------------
            # 9. Remove duplicate user-book pairs
            # -------------------------------

            final_ratings.drop_duplicates(
                ["User-ID", "Book-Title"],
                inplace=True
            )

            logging.info(
                f"Final cleaned dataset shape: "
                f"{final_ratings.shape}"
            )

            return final_ratings

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_validation(self):
        try:
            final_ratings = self.preprocess_data()

            logging.info(
                "Data validation and preprocessing completed successfully."
            )

            return final_ratings

        except Exception as e:
            raise AppException(e, sys) from e