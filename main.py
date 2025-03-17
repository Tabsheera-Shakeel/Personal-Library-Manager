import streamlit as st
import json
import os
from PIL import Image
import pandas as pd

# all libaray data will save in library.json
LIBRARY_FILE = "library.json"

# Initialize session state for the library
if "library" not in st.session_state:
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            st.session_state.library = json.load(file)
    else:
        st.session_state.library = []

def save_library():
    with open(LIBRARY_FILE, "w") as file:
        json.dump(st.session_state.library, file)

# Function to add a book
def add_book(title, author, year, genre, read_status, rating, cover_image):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status,
        "rating": rating,
        "cover_image": cover_image
    }
    st.session_state.library.append(book)
    save_library()
    st.success("Book added successfully!")

# Function to remove a book
def remove_book(title):
    for book in st.session_state.library:
        if book["title"].lower() == title.lower():
            st.session_state.library.remove(book)
            save_library()
            st.success("Book removed successfully!")
            return
    st.error("Book not found!")

# Function to search for books
def search_books(query, search_by, genre_filter, year_filter, read_filter):
    results = []
    for book in st.session_state.library:
        matches_search = (
            (search_by == "title" and query.lower() in book["title"].lower()) or
            (search_by == "author" and query.lower() in book["author"].lower())
        )
        matches_genre = genre_filter == "All" or book["genre"].lower() == genre_filter.lower()
        matches_year = year_filter == "All" or book["year"] == year_filter
        matches_read = read_filter == "All" or book["read_status"] == (read_filter == "Read")
        if matches_search and matches_genre and matches_year and matches_read:
            results.append(book)
    return results

# Function to display books in a card layout
def display_books(books):
    if not books:
        st.write("No books found.")
    else:
        cols = st.columns(3)  
        for i, book in enumerate(books):
            with cols[i % 3]:
                st.image(book.get("cover_image", "https://via.placeholder.com/150"), width=150)
                st.write(f"**{book['title']}**")
                st.write(f"by {book['author']} ({book['year']})")
                st.write(f"Genre: {book['genre']}")
                st.write(f"Rating: {'⭐' * book['rating']}")
                st.write(f"Status: {'Read' if book['read_status'] else 'Unread'}")

# Function to display statistics
def display_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read_status"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"**Total books:** {total_books}")
    st.write(f"**Percentage read:** {percentage_read:.1f}%")
    st.progress(percentage_read / 100)

# Function to export library to CSV
def export_library():
    df = pd.DataFrame(st.session_state.library)
    csv = df.to_csv(index=False)
    st.download_button("Export Library to CSV", csv, "library.csv", "text/csv")

# Streamlit App
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")
st.title("📚 Personal Library Manager")

# Sidebar Navigation
st.sidebar.header("Menu")
menu_option = st.sidebar.radio(
    "Choose an option:",
    ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Export Library"]
)

# Add a Book
if menu_option == "Add a Book":
    st.header("Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    rating = st.slider("Rating (1-5 stars)", 1, 5)
    cover_image = st.text_input("Cover Image URL (optional)", "https://via.placeholder.com/150")
    if st.button("Add Book"):
        if title and author and genre:
            add_book(title, author, year, genre, read_status, rating, cover_image)
        else:
            st.error("Please fill in all fields.")

# Remove a Book
elif menu_option == "Remove a Book":
    st.header("Remove a Book")
    title = st.text_input("Enter the title of the book to remove:")
    if st.button("Remove Book"):
        if title:
            remove_book(title)
        else:
            st.error("Please enter a title.")

# Search for a Book
elif menu_option == "Search for a Book":
    st.header("Search for a Book")
    search_by = st.radio("Search by:", ["Title", "Author"])
    query = st.text_input(f"Enter the {search_by.lower()}:")
    genre_filter = st.selectbox("Filter by Genre", ["All"] + list(set(book["genre"] for book in st.session_state.library)))
    year_filter = st.selectbox("Filter by Year", ["All"] + list(set(book["year"] for book in st.session_state.library)))
    read_filter = st.selectbox("Filter by Read Status", ["All", "Read", "Unread"])
    if st.button("Search"):
        if query:
            results = search_books(query, search_by.lower(), genre_filter, year_filter, read_filter)
            display_books(results)
        else:
            st.error("Please enter a search term.")

# Display All Books
elif menu_option == "Display All Books":
    st.header("Your Library")
    display_books(st.session_state.library)

# Display Statistics
elif menu_option == "Display Statistics":
    st.header("Library Statistics")
    display_statistics()

# Export Library
elif menu_option == "Export Library":
    st.header("Export Library")
    export_library()

# Save library on exit
st.sidebar.write("---")
if st.sidebar.button("Exit"):
    save_library()
    st.sidebar.write("Library saved. Goodbye!")
    st.stop()

st.markdown("---")
st.markdown("**Built by Tabsheera Shakeel**")