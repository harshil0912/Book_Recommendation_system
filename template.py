import os
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s:'
)


project_name = "books_recommender"


list_of_files = [

    f"{project_name}/__init__.py",

    # Components
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/stage_00_data_ingestion.py",
    f"{project_name}/components/stage_01_data_validation.py",
    f"{project_name}/components/stage_02_data_transformation.py",
    f"{project_name}/components/stage_03_model_trainer.py",

    # Config
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/configuration.py",

    # Constant
    f"{project_name}/constant/__init__.py",

    # Entity
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",

    # Exception
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/exception_handler.py",

    # Logger
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/log.py",

    # Pipeline
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",

    # Utils
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    "config/config.yaml",
    # Root files
    "template/index.html",
    ".dockerignore",
    ".gitignore",
    "app.py",
    "Dockerfile",
    "LICENSE",
    "README.md",
    "requirements.txt",
    "setup.py"
]


for filepath in list_of_files:

    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    # Create directory
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(
            f"Creating directory: {filedir} for the file {filename}"
        )

    # Create file if it doesn't exist or is empty
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:

        with open(filepath, "w") as f:
            pass

        logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filepath} is already created")