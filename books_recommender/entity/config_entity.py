from collections import namedtuple


ArtifactsConfig = namedtuple(
    "ArtifactsConfig",
    [
        "artifacts_dir"
    ]
)


DataIngestionConfig = namedtuple(
    "DataIngestionConfig",
    [
        "dataset_dir",
        "books_file",
        "ratings_file",
        "users_file"
    ]
)


DataValidationConfig = namedtuple(
    "DataValidationConfig",
    [
        "books_csv_file",
        "ratings_csv_file",
        "users_csv_file"
    ]
)


DataTransformationConfig = namedtuple(
    "DataTransformationConfig",
    [
        "min_user_ratings",
        "min_book_ratings"
    ]
)


ModelTrainerConfig = namedtuple(
    "ModelTrainerConfig",
    [
        "n_neighbors",
        "algorithm",
        "metric"
    ]
)