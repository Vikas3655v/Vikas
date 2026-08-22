package com.vikas.library;

import java.util.Scanner;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        Library library = new Library();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("\nLibrary Management System");
            System.out.println("1. Add book");
            System.out.println("2. Borrow book");
            System.out.println("3. Return book");
            System.out.println("4. List books");
            System.out.println("5. Exit");
            System.out.print("Choice: ");

            String choice = scanner.nextLine().trim();
            try {
                switch (choice) {
                    case "1" -> addBook(library, scanner);
                    case "2" -> System.out.println(library.borrowBook(readId(scanner)) ? "Book borrowed." : "Book is already borrowed.");
                    case "3" -> System.out.println(library.returnBook(readId(scanner)) ? "Book returned." : "Book is not borrowed.");
                    case "4" -> library.getBooks().forEach(book ->
                            System.out.printf("%d | %s | %s | %s%n", book.getId(), book.getTitle(), book.getAuthor(),
                                    book.isBorrowed() ? "Borrowed" : "Available"));
                    case "5" -> { return; }
                    default -> System.out.println("Invalid choice.");
                }
            } catch (IllegalArgumentException ex) {
                System.out.println("Error: " + ex.getMessage());
            }
        }
    }

    private static int readId(Scanner scanner) {
        System.out.print("Book id: ");
        return Integer.parseInt(scanner.nextLine().trim());
    }

    private static void addBook(Library library, Scanner scanner) {
        int id = readId(scanner);
        System.out.print("Title: ");
        String title = scanner.nextLine();
        System.out.print("Author: ");
        String author = scanner.nextLine();
        library.addBook(new Book(id, title, author));
        System.out.println("Book added.");
    }
}
