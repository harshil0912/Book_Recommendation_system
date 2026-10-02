import sys
import os
import pickle

from sklearn.neighbors import NearestNeighbors

from books_recommender.logger.log import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class ModelTrainer:

    def __init__(self, app_config=AppConfiguration()):
        try:
            logging.info(
                f"{'=' * 20} Model Trainer log started. {'=' * 20}"
            )

            self.model_trainer_config = (
                app_config.get_model_trainer_config()
            )

            self.artifacts_config = (
                app_config.get_artifacts_config()
            )

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_model_training(self, book_sparse):

        try:

            # Create KNN model
            model = NearestNeighbors(
                n_neighbors=self.model_trainer_config.n_neighbors,
                algorithm=self.model_trainer_config.algorithm,
                metric=self.model_trainer_config.metric
            )

            # Train KNN
            model.fit(book_sparse)

            logging.info(
                "KNN model training completed successfully."
            )

            # Create artifacts directory
            artifacts_dir = self.artifacts_config.artifacts_dir

            os.makedirs(
                artifacts_dir,
                exist_ok=True
            )

            # Save trained model
            model_path = os.path.join(
                artifacts_dir,
                "model.pkl"
            )

            with open(model_path, "wb") as file:
                pickle.dump(model, file)

            logging.info(
                f"KNN model saved at: {model_path}"
            )

            return model

        except Exception as e:
            raise AppException(e, sys) from e