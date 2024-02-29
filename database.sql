CREATE TABLE Services (
    ServiceID INT PRIMARY KEY,
    ServiceType VARCHAR(255),
    Price DECIMAL(10, 2),
    Date DATE,
    Amount INT,
    Performer VARCHAR(255),
    PaymentMethod VARCHAR(50)
);

CREATE TABLE Expenses (
    ExpenseID INT PRIMARY KEY,
    Amount DECIMAL(10, 2),
    Date DATE,
    PaymentMethod VARCHAR(50)
);

CREATE TABLE ProductsInStock (
    ProductID INT PRIMARY KEY,
    Name VARCHAR(255),
    Amount INT
);
