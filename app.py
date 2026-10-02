import pickle
import streamlit as st


# Load trained model
model = pickle.load(
    open("artifacts/model.pkl", "rb")
)

# Load book-user pivot table
book_pivot = pickle.load(
    open("artifacts/book_pivot.pkl", "rb")
)

# Load final ratings/data
final_ratings = pickle.load(
    open("artifacts/final_ratings.pkl", "rb")
)


class Recommendation:

    def __init__(self):
        self.model = model
        self.book_pivot = book_pivot
        self.final_ratings = final_ratings

    def recommend_books(self, book_name):

        # Find the row number of the selected book
        book_id = self.book_pivot.index.get_loc(book_name)

        # Find the 6 nearest books
        distances, indices = self.model.kneighbors(
            self.book_pivot.iloc[book_id, :].values.reshape(1, -1),
            n_neighbors=6
        )

        recommendations = []
        poster_urls = []

        # Skip the first result because it is the selected book itself
        for index in indices[0][1:]:

            # Get book title
            book_title = self.book_pivot.index[index]

            recommendations.append(book_title)

            # Find book information
            book_data = self.final_ratings[
                self.final_ratings["Book-Title"] == book_title
            ].iloc[0]

            # Get image URL
            poster_urls.append(
                book_data["Image-URL-L"]
            )

        return recommendations, poster_urls


# Create recommendation object
recommendation = Recommendation()


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("📚 Book Recommendation System")

selected_book = st.selectbox(
    "Select a book",
    book_pivot.index
)

if st.button("Recommend"):

    books, posters = recommendation.recommend_books(
        selected_book
    )

    st.write("### Recommended Books")

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            st.image(
                posters[i],
                use_container_width=True
            )

            st.write(books[i])