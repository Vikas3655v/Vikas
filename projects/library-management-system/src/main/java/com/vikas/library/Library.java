package com.vikas.library;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;

public final class Library {
    private final Map<Integer, Book> books = new LinkedHashMap<>();

    public void addBook(Book book) {
        if (books.containsKey(book.getId())) {
            throw new IllegalArgumentException("A book with this id already exists");
        }
        books.put(book.getId(), book);
    }

    public Book findBook(int id) {
        return books.get(id);
    }

    public boolean borrowBook(int id) {
        Book book = requireBook(id);
        return book.borrow();
    }

    public boolean returnBook(int id) {
        Book book = requireBook(id);
        return book.returnToLibrary();
    }

    public Collection<Book> getBooks() {
        return books.values();
    }

    private Book requireBook(int id) {
        Book book = books.get(id);
        if (book == null) throw new IllegalArgumentException("Book not found: " + id);
        return book;
    }
}
