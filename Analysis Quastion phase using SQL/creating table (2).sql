-- Create Customers Table
CREATE TABLE Customers (
    CustomerID VARCHAR(50) PRIMARY KEY,
    CustomerName VARCHAR(100),
    Segment VARCHAR(50)
);

-- Create Products Table
CREATE TABLE Products (
    ProductID VARCHAR(50) PRIMARY KEY,
    ProductName VARCHAR(255),
    Category VARCHAR(50),
    SubCategory VARCHAR(50)
);

-- Create Geography Table
CREATE TABLE Geography (
    PostalCode VARCHAR(10) PRIMARY KEY,
    City VARCHAR(100),
    State VARCHAR(50),
    Country VARCHAR(50),
    Region VARCHAR(50)
);

-- Create Orders Table
CREATE TABLE Orders (
    OrderID VARCHAR(50) PRIMARY KEY,
    OrderDate DATE,
    ShipDate DATE,
    ShipMode VARCHAR(50),
    CustomerID VARCHAR(50),
    PostalCode VARCHAR(10),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (PostalCode) REFERENCES Geography(PostalCode)
);

-- Create OrderDetails Table
CREATE TABLE OrderDetails (
    OrderID VARCHAR(50),
    ProductID VARCHAR(50),
    Sales DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);




