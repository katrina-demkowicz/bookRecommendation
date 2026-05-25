DROP TABLE IF EXISTS books;

CREATE TABLE books
(
    id INTEGER PRIMARY KEY NOT NULL,
    book_id INTEGER NOT NULL,
    copy_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    summary TEXT,
    subjects TEXT
);