package com.vikas.library;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class LibraryTest {
    @Test
    void bookCanBeBorrowedAndReturned() {
        Library library = new Library();
        library.addBook(new Book(1, "Clean Code", "Robert C. Martin"));

        assertTrue(library.borrowBook(1));
        assertTrue(library.findBook(1).isBorrowed());
        assertTrue(library.returnBook(1));
        assertFalse(library.findBook(1).isBorrowed());
    }

    @Test
    void duplicateBookIdsAreRejected() {
        Library library = new Library();
        library.addBook(new Book(1, "A", "Author"));
        assertThrows(IllegalArgumentException.class,
                () -> library.addBook(new Book(1, "B", "Author")));
    }

    @Test
    void missingBooksAreRejected() {
        Library library = new Library();
        assertThrows(IllegalArgumentException.class, () -> library.borrowBook(99));
    }
}
