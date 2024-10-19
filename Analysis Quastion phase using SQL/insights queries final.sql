--1 top 10 customer by total sale 
SELECT TOP 10 Customers.CustomerID, SUM(OrderDetails.Sales) AS TotalSales
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
GROUP BY Customers.CustomerID
ORDER BY TotalSales DESC;


--2  customer segment generate highiset sales 

SELECT Customers.Segment, SUM(OrderDetails.Sales) AS TotalSales
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
GROUP BY Customers.Segment
ORDER BY TotalSales DESC;

--3 Regions with the highest customer count

SELECT Geography.Region, COUNT(DISTINCT Customers.CustomerID) AS CustomerCount
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN Geography ON Orders.PostalCode = Geography.PostalCode
GROUP BY Geography.Region
ORDER BY CustomerCount DESC;

--4 Unique customers who placed orders in each year

SELECT YEAR(Orders.OrderDate) AS OrderYear, COUNT(DISTINCT Customers.CustomerID) AS UniqueCustomers
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY YEAR(Orders.OrderDate)
ORDER BY OrderYear;
 
 --5  most sold product categories by total revenue

 SELECT  Products.Category, SUM(OrderDetails.Sales) AS TotalRevenue
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
GROUP BY Products.Category
ORDER BY TotalRevenue DESC

--6  Highest sales products in each region:

SELECT top 10 Geography.Region, Products.ProductName, SUM(OrderDetails.Sales) AS TotalSales
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
JOIN Geography ON Orders.PostalCode = Geography.PostalCode
GROUP BY Geography.Region, Products.ProductName
ORDER BY Geography.Region, TotalSales DESC

 --6 Percentage of sales contributed by each product sub-category

 SELECT Products.SubCategory, 
       SUM(OrderDetails.Sales) * 100.0 / (SELECT SUM(Sales) FROM OrderDetails) AS PercentageOfSales
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
GROUP BY Products.SubCategory


--8 Average time between order date and ship date by ship mode

SELECT ShipMode, AVG(DATEDIFF(DAY, Orders.OrderDate, Orders.ShipDate)) AS AvgShippingTime
FROM Orders
GROUP BY ShipMode

--9 Orders placed each month and trend over time:

SELECT top 15 YEAR(OrderDate) AS Year, MONTH(OrderDate) AS Month, COUNT(OrderID) AS OrdersCount
FROM Orders
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY Year, Month DESC

--10  Percentage of sales per region over total sales

SELECT Geography.Region, 
       SUM(OrderDetails.Sales) * 100.0 / (SELECT SUM(Sales) FROM OrderDetails) AS SalesPercentage
FROM Geography
JOIN Orders ON Geography.PostalCode = Orders.PostalCode
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
GROUP BY Geography.Region

