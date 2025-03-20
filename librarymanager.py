import streamlit as st
import json
import time
from datetime import datetime
import plotly.express as px
import pandas as pd

data_file = "library.json"

def load_library():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library():
    with open(data_file, "w") as file:
        json.dump(st.session_state.library, file, indent=4)

def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

def get_library_states():
    total_books = len(st.session_state.library)
    genres = {}
    decades = {}
    read_count = 0
    
    for book in st.session_state.library:
        genres[book['genre']] = genres.get(book['genre'], 0) + 1
        decade = (book['publication_year'] // 10) * 10
        decades[decade] = decades.get(decade, 0) + 1
        if book['read_status']:
            read_count += 1
    
    return total_books, genres, decades, read_count

def update_read_status(index):
    st.session_state.library[index]['read_status'] = not st.session_state.library[index]['read_status']
    save_library()
    st.rerun()

def delete_book(index):
    del st.session_state.library[index]
    save_library()
    st.rerun()

st.set_page_config(page_title="Personal Library", layout="wide")
st.title("📚 Personal Library Management System")

if "library" not in st.session_state:
    st.session_state.library = load_library()

st.sidebar.header("Add New Book")
title = st.sidebar.text_input("Title")
author = st.sidebar.text_input("Author")
publication_year = st.sidebar.number_input("Publication Year", min_value=1800, max_value=2025, step=1)
genre = st.sidebar.text_input("Genre")
read_status = st.sidebar.checkbox("Read")
if st.sidebar.button("Add Book"):
    add_book(title, author, publication_year, genre, read_status)

st.header("📖 Your Book Collection")
total_books, genres, decades, read_count = get_library_states()

st.write(f"Total Books: {total_books} | Read Books: {read_count}")

for index, book in enumerate(st.session_state.library):
    with st.expander(f"{book['title']} by {book['author']}"):
        st.write(f"**Publication Year:** {book['publication_year']}")
        st.write(f"**Genre:** {book['genre']}")
        status_label = "Mark as Read" if not book['read_status'] else "Mark as Unread"
        if st.button(status_label, key=f"read_{index}"):
            update_read_status(index)
        if st.button("Delete", key=f"del_{index}"):
            delete_book(index)

if total_books > 0:
    df_genres = pd.DataFrame({"Genre": list(genres.keys()), "Count": list(genres.values())})
    fig_genres = px.bar(df_genres, x="Genre", y="Count", title="Books by Genre", labels={"Count": "Number of Books"})
    st.plotly_chart(fig_genres)
    
    df_decades = pd.DataFrame({"Decade": list(decades.keys()), "Count": list(decades.values())})
    fig_decades = px.bar(df_decades, x="Decade", y="Count", title="Books by Publication Decade", labels={"Count": "Number of Books"})
    st.plotly_chart(fig_decades)

st.markdown(
    """
    <style>
    .stButton>button {background-color: #3B82F6; color: white; padding: 8px; border-radius: 5px;}
    </style>
    """,
    unsafe_allow_html=True
)
