# 📚 Library Management System

A small Java console application demonstrating object-oriented design for common library workflows.

## Features

- Add books
- Borrow available books
- Return borrowed books
- List current books and availability
- Input validation for basic invalid operations

## Technologies

- Java
- Object-Oriented Programming
- Java Collections
- JUnit 5 for service tests

## Structure

```text
library-management-system/
├── pom.xml
├── README.md
└── src/
    ├── main/java/com/vikas/library/
    └── test/java/com/vikas/library/
```

## Run

Requires Java 17+ and Maven.

```bash
mvn test
mvn package
java -cp target/classes com.vikas.library.Main
```

## Interview Discussion

The project demonstrates interfaces, encapsulation, domain modelling, collection usage, validation, separation of concerns, and unit testing. It is intentionally small so the design can be explained clearly in an interview.

## Status

Working implementation committed to this portfolio workspace. Packaging and tests should be run locally before claiming a release/deployment.
