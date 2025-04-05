import streamlit as st
import json
import os

data_file = "library.json"

def load_library():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file)

def add_book(library):
    st.subheader("Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read the book?")

    if st.button("Add Book"):
        new_book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read
        }
        library.append(new_book)
        save_library(library)
        st.success(f"Book '{title}' added successfully!")

def remove_book(library):
    st.subheader("Remove a Book")
    title_to_remove = st.text_input("Enter the title to remove")
    if st.button("Remove Book"):
        updated_library = [book for book in library if book['title'].lower() != title_to_remove.lower()]
        if len(updated_library) < len(library):
            save_library(updated_library)
            st.success(f"Book '{title_to_remove}' removed successfully!")
        else:
            st.warning("Book not found!")
        return updated_library
    return library

def search_library(library):
    st.subheader("Search the Library")
    search_by = st.selectbox("Search by", ["title", "author"])
    term = st.text_input(f"Enter the {search_by}")
    if st.button("Search"):
        results = [book for book in library if term.lower() in book[search_by].lower()]
        if results:
            for book in results:
                status = "Read" if book['read'] else "Unread"
                st.write(f"📖 **{book['title']}** by *{book['author']}* - {book['year']} - {book['genre']} - **{status}**")
        else:
            st.warning("No matching books found!")
            
def display_all_books(library):
    if library:
        for book in library:
            status = "Read" if book['read_status'] else "Unread"
            st.write(f"📘 **{book['title']}** by *{book['author']}* - {book['publication_year']} - {book['genre']} - **{status}**")
    else:
        st.write("The library is empty.")

def display_statistics(library):
    st.subheader("Statistics")
    total_books = len(library)
    read_books = len([book for book in library if book['read_status']])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    st.metric("Total Books", total_books)
    st.metric("Books Read", read_books)
    st.metric("Read Percentage", f"{percentage_read:.2f}%")

def main():
    st.title("📚 Library Manager")
    library = load_library()

    menu = ["Add Book", "Remove Book", "Search Book", "View All Books", "View Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Book":
        add_book(library)
    elif choice == "Remove Book":
        library = remove_book(library)
    elif choice == "Search Book":
        search_library(library)
    elif choice == "View All Books":
        display_all_books(library)
    elif choice == "View Statistics":
        display_statistics(library)

if __name__ == '__main__':
    main()
