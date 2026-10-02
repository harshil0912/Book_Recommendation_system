# Book Recommendation System

A content-based-on-user-ratings book recommendation web app built with Python and Streamlit. It uses the Book-Crossing dataset and scikit-learn's nearest-neighbor search to find books with similar rating patterns.

## Overview

This project applies item-item collaborative filtering. It represents each book by the ratings it received from users, then finds nearby book vectors using cosine distance. Select a book in the Streamlit app to see five similar books and their cover images.

The current processed dataset contains approximately **862 books**, **888 users**, and **65,402 ratings**. These counts describe the processed data snapshot and may change if the source dataset or filtering thresholds change.

## Recommendation Pipeline

```text
Book-Crossing CSV files
        ↓
Load and validate source files
        ↓
Keep users with more than 200 ratings
        ↓
Join ratings with book metadata
        ↓
Keep books with more than 45 ratings
        ↓
Remove duplicate user/book pairs
        ↓
Build a book-by-user rating pivot table
        ↓
Convert the table to a CSR sparse matrix
        ↓
Fit scikit-learn NearestNeighbors
        ↓
Recommend the five nearest books in Streamlit
```

Missing ratings in the pivot table are filled with zero. The model uses `NearestNeighbors` with `algorithm="brute"`, `metric="cosine"`, and `n_neighbors=6`. The selected book itself is the closest result, so the app skips it and displays the next five neighbors.

## Project Structure

```text
Book_Recommendation_system/
├── app.py                         # Streamlit recommendation interface
├── main.py                        # Starts the training pipeline
├── config/
│   └── config.yaml                # Dataset paths and model/filter settings
├── books_recommender/
│   ├── components/                # Ingestion, validation, transformation, training
│   ├── config/                    # Configuration loading
│   ├── entity/                    # Configuration entities
│   ├── exception/                 # Exception handling
│   ├── logger/                    # Logging setup
│   ├── pipeline/                  # Training pipeline orchestration
│   └── utils/                     # Shared utilities
├── Book_Dataset/
│   ├── BX-Books.csv               # Book metadata
│   ├── BX-Book-Ratings.csv        # User ratings
│   └── BX-Users.csv               # User metadata
├── artifacts/                     # Generated model and processed data
│   ├── book_pivot.pkl
│   ├── final_ratings.pkl
│   └── model.pkl
├── requirements.txt
├── setup.py
└── Dockerfile
```

The dataset files are expected in `Book_Dataset/`. The project archive also contains generated artifacts; if you start from a clean checkout without them, generate them using the training steps below.

## Dataset

The project expects the Book-Crossing CSV files with their original semicolon-delimited format and Latin-1 encoding:

- `BX-Books.csv`
- `BX-Book-Ratings.csv`
- `BX-Users.csv`

Place them in the `Book_Dataset/` directory. The data files are not reproduced in this README. Use a legitimate copy of the Book-Crossing dataset and follow its applicable terms of use.

The current pipeline selects book metadata fields needed for display, filters to users who have rated more than 200 books, and retains books with more than 45 ratings. The thresholds are configured in `config/config.yaml`.

## Requirements

- Python 3.10 or newer
- pip
- The three Book-Crossing CSV files in `Book_Dataset/`

Dependencies are listed in `requirements.txt`: scikit-learn, pandas, NumPy, SciPy, PyYAML, and Streamlit. The project is installed in editable mode through `-e .`.

## Installation

From the project root, create and activate a virtual environment.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure the dataset folder has this structure before training:

```text
Book_Dataset/
├── BX-Books.csv
├── BX-Book-Ratings.csv
└── BX-Users.csv
```

## Train the Model

Run the training pipeline from the project root:

```bash
python main.py
```

The pipeline reads and filters the dataset, creates the book-user pivot table and CSR matrix, trains the nearest-neighbor model, and writes these files under `artifacts/`:

- `book_pivot.pkl` — book-by-user rating table used by the app
- `final_ratings.pkl` — processed ratings and book metadata, including cover URLs
- `model.pkl` — fitted scikit-learn nearest-neighbor model

Training requires the source CSV files. Keep the artifacts together with the code because the app loads them from `artifacts/` at startup.

## Run the App

After the artifacts have been generated, start Streamlit from the project root:

```bash
streamlit run app.py
```

Choose a title from the selector and click **Recommend**. The app shows five recommended titles with cover images when the dataset provides image URLs.

## Configuration

Edit `config/config.yaml` to adjust the dataset filenames and filtering/model settings. The current settings are:

```yaml
data_transformation_config:
  min_user_ratings: 200
  min_book_ratings: 45

model_trainer_config:
  n_neighbors: 6
  algorithm: brute
  metric: cosine
```

The implementation applies strict greater-than filters: users must have more than 200 ratings, and books must have more than 45 ratings.

## Technologies

- **Python** for the application and training pipeline
- **Pandas** and **NumPy** for data processing
- **SciPy CSR sparse matrices** for efficient storage of the book-user rating matrix
- **scikit-learn NearestNeighbors** for cosine-distance neighbor search
- **Streamlit** for the interactive web interface
- **PyYAML** for configuration

## KNN Learning Notes

The conceptual KNN learning notes are kept in the separate [`ml_from_scratch`](https://github.com/harshil0912/ml_from_scratch) repository. This README documents how KNN is configured and used in this book recommendation project; it is not a replacement for those learning notes.

## Troubleshooting

- **Missing dataset file:** Check that all three CSV files are in `Book_Dataset/` and that their names match `config/config.yaml`.
- **Missing artifact:** Run `python main.py` before starting Streamlit.
- **App cannot find an artifact:** Start Streamlit from the project root so relative paths such as `artifacts/model.pkl` resolve correctly.
- **A book is not selectable:** The title may not remain after the configured user and book rating filters.

## License

See the repository's `LICENSE` file for licensing information.
