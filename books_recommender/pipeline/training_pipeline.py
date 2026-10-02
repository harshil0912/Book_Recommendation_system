from books_recommender.components.stage_00_data_ingestion import DataIngestion
from books_recommender.components.stage_01_data_validation import DataValidation
from books_recommender.components.stage_02_data_transformation import DataTransformation
from books_recommender.components.stage_03_model_trainer import ModelTrainer


class TrainingPipeline:

    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def start_training_pipeline(self):

        # Stage 0: Data Ingestion
        self.data_ingestion.initiate_data_ingestion()

        # Stage 1: Data Validation
        final_ratings = self.data_validation.initiate_data_validation()

        # Stage 2: Data Transformation
        book_pivot, book_sparse = (
            self.data_transformation.initiate_data_transformation(
                final_ratings
            )
        )

        # Stage 3: Model Training
        self.model_trainer.initiate_model_training(
            book_sparse
        )