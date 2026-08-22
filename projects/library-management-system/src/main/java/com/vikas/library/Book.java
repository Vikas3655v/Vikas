package com.vikas.library;

public final class Book {
    private final int id;
    private final String title;
    private final String author;
    private boolean borrowed;

    public Book(int id, String title, String author) {
        if (id <= 0) throw new IllegalArgumentException("Book id must be positive");
        if (title == null || title.isBlank()) throw new IllegalArgumentException("Title is required");
        if (author == null || author.isBlank()) throw new IllegalArgumentException("Author is required");
        this.id = id;
        this.title = title.trim();
        this.author = author.trim();
    }

    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public boolean isBorrowed() { return borrowed; }

    boolean borrow() {
        if (borrowed) return false;
        borrowed = true;
        return true;
    }

    boolean returnToLibrary() {
        if (!borrowed) return false;
        borrowed = false;
        return true;
    }
}
