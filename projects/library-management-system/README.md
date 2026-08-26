# 📚 Library Management System

A small Java console application demonstrating clean object-oriented design for common library workflows.

## ✨ Features

- Add books with validation
- Borrow available books
- Return borrowed books
- List books and availability
- Reject duplicate IDs and missing books
- JUnit 5 tests for core behaviour

## 🧰 Technologies

Java 17+ • Maven • Java Collections • JUnit 5 • OOP

## 📁 Structure

```text
library-management-system/
├── src/
│   ├── main/java/com/vikas/library/
│   │   ├── Book.java
│   │   ├── Library.java
│   │   └── Main.java
│   └── test/java/com/vikas/library/
│       └── LibraryTest.java
├── pom.xml
└── README.md
```

## ▶️ Run Tests

Requires Java 17+ and Maven.

```bash
mvn test
```

## 📦 Build

```bash
mvn package
```

## ▶️ Run Application

```bash
java -cp target/classes com.vikas.library.Main
```

## 🧠 What this demonstrates

The project focuses on encapsulation, domain modelling, collection usage, input validation, state transitions and unit testing. It is intentionally small so the design and implementation can be explained clearly in an interview.

## 📌 Status

Working portfolio implementation. Tests should be run locally before claiming a release or deployment.
