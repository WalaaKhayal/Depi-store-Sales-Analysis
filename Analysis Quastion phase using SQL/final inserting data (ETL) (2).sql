INSERT INTO Customers (CustomerID, CustomerName, Segment)
SELECT DISTINCT Customer_ID, Customer_Name, Segment
FROM Clean_11


INSERT INTO Geography (PostalCode, City, State, Country, Region)
SELECT DISTINCT Postal_Code, City, State, Country, Region
FROM Clean_11

INSERT INTO Products (ProductID, ProductName, Category, SubCategory)
SELECT DISTINCT Product_ID, Product_Name, Category, Sub_Category
FROM Clean_11

INSERT INTO Orders (OrderID, OrderDate, ShipDate, ShipMode, CustomerID, PostalCode)
SELECT DISTINCT Order_ID, Order_Date, Ship_Date, Ship_Mode, Customer_ID, Postal_Code
FROM Clean_1


INSERT INTO OrderDetails (OrderID, ProductID, ProductName, Sales)
SELECT DISTINCT Order_ID, Product_ID, Product_Name, Sales
FROM Clean_11