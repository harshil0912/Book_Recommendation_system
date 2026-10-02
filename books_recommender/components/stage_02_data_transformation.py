import sys
import os
import pickle

from scipy.sparse import csr_matrix

from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class DataTransformation:

    def __init__(self, app_config=AppConfiguration()):
        try:
            logging.info(
                f"{'=' * 20} Data Transformation log started. {'=' * 20}"
            )

            self.data_transformation_config = (
                app_config.get_data_transformation_config()
            )

            self.artifacts_config = (
                app_config.get_artifacts_config()
            )

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_transformation(self, final_ratings):

        try:

            # --------------------------------
            # 1. Create book-user pivot table
            # --------------------------------

            book_pivot = final_ratings.pivot_table(
                columns="User-ID",
                index="Book-Title",
                values="Book-Rating"
            )

            logging.info(
                f"Book pivot shape: {book_pivot.shape}"
            )

            # --------------------------------
            # 2. Fill missing ratings with 0
            # --------------------------------

            book_pivot.fillna(0, inplace=True)

            # --------------------------------
            # 3. Convert pivot table to sparse matrix
            # --------------------------------

            book_sparse = csr_matrix(book_pivot)

            logging.info(
                f"Book sparse matrix shape: {book_sparse.shape}"
            )

            # --------------------------------
            # 4. Create artifacts directory
            # --------------------------------

            artifacts_dir = self.artifacts_config.artifacts_dir

            os.makedirs(
                artifacts_dir,
                exist_ok=True
            )

            # --------------------------------
            # 5. Save final_ratings
            # --------------------------------

            final_ratings_path = os.path.join(
                artifacts_dir,
                "final_ratings.pkl"
            )

            with open(final_ratings_path, "wb") as file:
                pickle.dump(final_ratings, file)

            # --------------------------------
            # 6. Save book_pivot
            # --------------------------------

            book_pivot_path = os.path.join(
                artifacts_dir,
                "book_pivot.pkl"
            )

            with open(book_pivot_path, "wb") as file:
                pickle.dump(book_pivot, file)

            logging.info(
                f"Saved final_ratings at: {final_ratings_path}"
            )

            logging.info(
                f"Saved book_pivot at: {book_pivot_path}"
            )

            logging.info(
                "Data transformation completed successfully."
            )

            return book_pivot, book_sparse

        except Exception as e:
            raise AppException(e, sys) from e