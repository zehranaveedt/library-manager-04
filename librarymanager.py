import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    library.append({
        "title": title,
        "author": author,
        "publication_year": int(year),
        "genre": genre,
        "read_status": read_status,
    })
    save_library(library)
    st.success("Book added successfully!")

def remove_book(library, title):
    library[:] = [book for book in library if book["title"].lower() != title.lower()]
    save_library(library)
    st.success("Book removed successfully!")

def search_books(library, query, search_by):
    return [book for book in library if query.lower() in book[search_by].lower()]

def display_books(library):
    if library:
        for book in library:
            st.write(f"**{book['title']}** by {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
    else:
        st.warning("No books found.")

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book['read_status'])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

# Streamlit UI
st.title("📚 Personal Library Manager")
library = load_library()
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"])

if menu == "Add Book":
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    if st.button("Add Book"):
        add_book(library, title, author, year, genre, read_status)

elif menu == "Remove Book":
    title = st.text_input("Enter book title to remove")
    if st.button("Remove Book"):
        remove_book(library, title)

elif menu == "Search Book":
    search_by = st.radio("Search by", ["title", "author"])
    query = st.text_input("Enter search query")
    if st.button("Search"):
        results = search_books(library, query, search_by)
        display_books(results)

elif menu == "Display All Books":
    display_books(library)

elif menu == "Statistics":
    display_statistics(library)
