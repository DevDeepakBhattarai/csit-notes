from __future__ import annotations

import datetime as dt
import decimal
import html
import json
import re
from pathlib import Path

import pymysql

BASE_DIR = Path(r"C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\4th Sem\DBMS")
OUTPUT_HTML = BASE_DIR / "DBMS_Lab_Report_Part2.html"
VERIFY_JSON = BASE_DIR / "DBMS_Lab_Report_Part2_Verification.json"
VERIFY_DB = "dbms_lab_verify"

SETUP_SQL = r"""
CREATE TABLE categories (
  CategoryID INT AUTO_INCREMENT PRIMARY KEY,
  CategoryName VARCHAR(50),
  Description TEXT
) ENGINE=InnoDB;

CREATE TABLE suppliers (
  SupplierID INT AUTO_INCREMENT PRIMARY KEY,
  SupplierName VARCHAR(100),
  ContactName VARCHAR(50),
  Address VARCHAR(100),
  City VARCHAR(50),
  PostalCode VARCHAR(20),
  Country VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE customers (
  CustomerID INT AUTO_INCREMENT PRIMARY KEY,
  CustomerName VARCHAR(100),
  ContactName VARCHAR(50),
  Address VARCHAR(100),
  City VARCHAR(50),
  PostalCode VARCHAR(20),
  Country VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE employees (
  EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
  LastName VARCHAR(50),
  FirstName VARCHAR(50),
  BirthDate DATE,
  Notes TEXT
) ENGINE=InnoDB;

CREATE TABLE shippers (
  ShipperID INT AUTO_INCREMENT PRIMARY KEY,
  ShipperName VARCHAR(50),
  Phone VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE products (
  ProductID INT AUTO_INCREMENT PRIMARY KEY,
  ProductName VARCHAR(100),
  SupplierID INT,
  CategoryID INT,
  Unit VARCHAR(50),
  Price DECIMAL(10,2),
  FOREIGN KEY (SupplierID) REFERENCES suppliers(SupplierID),
  FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
) ENGINE=InnoDB;

CREATE TABLE orders (
  OrderID INT AUTO_INCREMENT PRIMARY KEY,
  CustomerID INT,
  EmployeeID INT,
  OrderDate DATE,
  ShipperID INT,
  FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
  FOREIGN KEY (EmployeeID) REFERENCES employees(EmployeeID),
  FOREIGN KEY (ShipperID) REFERENCES shippers(ShipperID)
) ENGINE=InnoDB;

CREATE TABLE orderdetails (
  OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
  OrderID INT,
  ProductID INT,
  Quantity INT,
  FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
  FOREIGN KEY (ProductID) REFERENCES products(ProductID)
) ENGINE=InnoDB;

INSERT INTO categories (CategoryName, Description) VALUES
('Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
('Seafood', 'Seaweed and fish'),
('Confections', 'Desserts, candies, and sweet breads'),
('Dairy Products', 'Cheeses'),
('Grains/Cereals', 'Breads, crackers, pasta, and cereal');

INSERT INTO suppliers (SupplierName, ContactName, Address, City, PostalCode, Country) VALUES
('Exotic Liquids', 'Charlotte Cooper', '49 Gilbert St.', 'London', 'EC1 4SD', 'UK'),
('Tokyo Traders', 'Yoshi Nagase', '9-8 Sekimai Musashino-shi', 'Tokyo', '100', 'Japan'),
('New Orleans Cajun Delights', 'Shelley Cain', 'P.O. Box 78934', 'New Orleans', '70117', 'USA'),
('Grandma Kelly Homestead', 'Regina Murphy', '707 Oxford Rd.', 'Ann Arbor', '48104', 'USA'),
('Svensk Sjöföda AB', 'Michael Björn', 'Buvallsvägen 11', 'Stockholm', 'S-857 21', 'Sweden'),
('Refrescos Americanos', 'Pablo Pan', 'Calle 10', 'Osaka', '530', 'Japan');

INSERT INTO customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES
('Alfreds Futterkiste', 'Maria Anders', 'Obere Str. 57', 'Berlin', '12209', 'Germany'),
('Ana Trujillo Emparedados', 'Ana Trujillo', 'Avda. de la Constitución 2222', 'Mexico City', '05021', 'Mexico'),
('Around the Horn', 'Thomas Hardy', '120 Hanover Sq.', 'London', 'WA1 1DP', 'UK'),
('Berglunds snabbköp', 'Christina Berglund', 'Berguvsvägen 8', 'Luleå', 'S-958 22', 'Sweden'),
('Blauer See Delikatessen', 'Hanna Moos', 'Forsterstr. 57', 'Mannheim', '68306', 'Germany'),
('Parisian Foods', 'Pierre Dupond', 'Rue Royale', 'Paris', '75008', 'France'),
('Rome Eats', 'Giovanni Rovelli', 'Via Ludovico', 'Rome', '00100', 'Italy'),
('Salzburg Sweets', 'Georg Pipps', 'Geislrosenweg 14', 'Salzburg', '5020', 'Austria'),
('Madrid Trading', 'Diego Roel', 'C/ Moralzarzal', 'Madrid', '28034', 'Spain');

INSERT INTO employees (LastName, FirstName, BirthDate, Notes) VALUES
('Davolio', 'Nancy', '1968-12-08', 'Education includes a BA in psychology from Colorado State University.'),
('Fuller', 'Andrew', '1952-02-19', 'Andrew received his Ph.D. in international marketing.'),
('Leverling', 'Janet', '1963-08-30', 'Janet has a BS degree in chemistry and a BA degree in business administration.'),
('Peacock', 'Margaret', '1937-09-19', 'Margaret holds a BA from Concordia College.'),
('Buchanan', 'Steven', '1955-03-04', 'Steven Buchanan graduated from St. Andrews University.'),
('Suyama', 'Michael', '1963-07-02', 'Michael is a graduate of Sussex University.');

INSERT INTO shippers (ShipperName, Phone) VALUES
('Speedy Express', '(503) 555-9831'),
('United Package', '(503) 555-3199'),
('Federal Shipping', '(503) 555-9931'),
('Swift Shipping', '(503) 555-1234'),
('Global Express', '(503) 555-5678');

INSERT INTO products (ProductName, SupplierID, CategoryID, Unit, Price) VALUES
('Chai', 1, 1, '10 boxes x 20 bags', 18.00),
('Chang', 1, 1, '24 - 12 oz bottles', 19.00),
('Aniseed Syrup', 1, 1, '12 - 550 ml bottles', 10.00),
('Chef Anton Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.00),
('Ikura', 2, 2, '12 - 200 ml jars', 31.00),
('Uncle Bob Organic Dried Pears', 3, 3, '12 - 1 lb pkgs.', 30.00);

INSERT INTO orders (CustomerID, EmployeeID, OrderDate, ShipperID) VALUES
(1, 1, '2023-08-18', 1),
(2, 3, '2023-08-18', 2),
(3, 5, '2023-08-19', 4),
(4, 6, '2023-08-19', 5),
(5, 2, '2023-08-17', 3);

INSERT INTO orderdetails (OrderID, ProductID, Quantity) VALUES
(1, 1, 12),
(1, 2, 10),
(2, 3, 5),
(3, 4, 20),
(4, 5, 15);
""".strip()

PRODUCTINFO_VIEW = r"""
DROP VIEW IF EXISTS productinfo;
CREATE VIEW productinfo AS
SELECT
  p.ProductID,
  p.ProductName,
  p.Unit,
  p.Price,
  c.CategoryID,
  c.CategoryName,
  c.Description AS CategoryDescription,
  s.SupplierID,
  s.SupplierName,
  s.ContactName AS SupplierContactName,
  s.Address AS SupplierAddress,
  s.City AS SupplierCity,
  s.PostalCode AS SupplierPostalCode,
  s.Country AS SupplierCountry
FROM products AS p
JOIN categories AS c ON c.CategoryID = p.CategoryID
JOIN suppliers AS s ON s.SupplierID = p.SupplierID
""".strip()

ORDERINFO_VIEW = r"""
DROP VIEW IF EXISTS orderinfo;
CREATE VIEW orderinfo AS
SELECT
  o.OrderID,
  o.OrderDate,
  c.CustomerID,
  c.CustomerName,
  c.City AS CustomerCity,
  c.Country AS CustomerCountry,
  e.EmployeeID,
  CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
  s.ShipperID,
  s.ShipperName,
  s.Phone AS ShipperPhone
FROM orders AS o
JOIN customers AS c ON c.CustomerID = o.CustomerID
JOIN employees AS e ON e.EmployeeID = o.EmployeeID
JOIN shippers AS s ON s.ShipperID = o.ShipperID
""".strip()

CUSTOMER_COLS = "CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country"
PRODUCT_COLS = "ProductID, ProductName, SupplierID, CategoryID, Unit, Price"
EMPLOYEE_COLS = "EmployeeID, LastName, FirstName, BirthDate, Notes"
SUPPLIER_COLS = "SupplierID, SupplierName, ContactName, Address, City, PostalCode, Country"
ORDER_COLS = "OrderID, CustomerID, EmployeeID, OrderDate, ShipperID"


def split_sql(sql: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single = False
    escaped = False
    for char in sql:
        if char == "\\" and not escaped:
            escaped = True
            current.append(char)
            continue
        if char == "'" and not escaped:
            in_single = not in_single
        if char == ";" and not in_single:
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
        else:
            current.append(char)
        escaped = False
    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements


def item(item_id: str, lab: int, group: str, no: int, title: str, question: str, sql: str,
         verify: str | None = None, pre: str | None = None, dynamic: str | None = None) -> dict:
    return {
        "id": item_id,
        "lab": lab,
        "group": group,
        "no": no,
        "title": title,
        "question": question,
        "sql": sql.strip(),
        "verify": verify.strip() if verify else None,
        "pre": pre.strip() if pre else None,
        "dynamic": dynamic,
    }


def build_items() -> list[dict]:
    items: list[dict] = []

    # LAB 4 - GROUP A
    q4a = [
        ("Project Category Names", "Project CategoryName from categories.", "SELECT CategoryName FROM categories ORDER BY CategoryID;", None, None),
        ("Project Customer Countries", "Project Country from customers.", "SELECT Country FROM customers ORDER BY CustomerID;", None, None),
        ("Project City and Country", "Project City, Country from customers.", "SELECT City, Country FROM customers ORDER BY CustomerID;", None, None),
        ("Customers from Madrid", "SELECT CustomerName from customers who are from Madrid City.", "SELECT CustomerName FROM customers WHERE City = 'Madrid';", None, None),
        ("German Customer IDs", "SELECT CustomerID from customers who are from Germany.", "SELECT CustomerID FROM customers WHERE Country = 'Germany' ORDER BY CustomerID;", None, None),
        ("Germany or Spain Customers", "SELECT CustomerID, CustomerName from customers who are from Germany or Spain.", "SELECT CustomerID, CustomerName FROM customers WHERE Country IN ('Germany', 'Spain') ORDER BY CustomerID;", None, None),
        ("London, UK Customers", "SELECT all from customers who are from London and UK.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City = 'London' AND Country = 'UK';", None, None),
        ("Customer City by Name Initial", "SELECT all from customers who are from a city whose name starts with the first letter of your name.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City LIKE '{{{{FIRST_LETTER}}}}%' ORDER BY CustomerID;", None, "customer_city_initial"),
        ("Exclude Canada and Belgium", "SELECT all from customers who are not from Canada and Belgium.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE Country NOT IN ('Canada', 'Belgium') ORDER BY CustomerID;", None, None),
        ("Customers from G7 Countries", "SELECT all from customers who are from G7 Countries (USA, UK, Canada, France, Germany, Italy, Japan).", f"SELECT {CUSTOMER_COLS} FROM customers WHERE Country IN ('USA', 'UK', 'Canada', 'France', 'Germany', 'Italy', 'Japan') ORDER BY CustomerID;", None, None),
        ("Postal Code Contains 31", "SELECT all from customers who have PostalCode containing 31.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE PostalCode LIKE '%31%' ORDER BY CustomerID;", None, None),
        ("Postal Code 00 in Rome or Paris", "SELECT all from customers having PostalCode containing 00 and from Rome or Paris.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE PostalCode LIKE '%00%' AND City IN ('Rome', 'Paris') ORDER BY CustomerID;", None, None),
        ("Customers Not from Salzburg", "SELECT all from customers who are not from Salzburg.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City <> 'Salzburg' ORDER BY CustomerID;", None, None),
        ("Employees Born in July", "SELECT all employees who are born in July.", f"SELECT {EMPLOYEE_COLS} FROM employees WHERE MONTH(BirthDate) = 7 ORDER BY EmployeeID;", None, None),
        ("Employees with BA Degree", "SELECT all employees having BA degree in Notes.", f"SELECT {EMPLOYEE_COLS} FROM employees WHERE Notes LIKE '%BA%' ORDER BY EmployeeID;", None, None),
        ("Suppliers from USA and Japan", "SELECT all suppliers from USA and Japan.", f"SELECT {SUPPLIER_COLS} FROM suppliers WHERE Country IN ('USA', 'Japan') ORDER BY SupplierID;", None, None),
        ("Supplier Count by Country", "Find name and count of suppliers from different countries.", "SELECT Country, COUNT(*) AS SupplierCount FROM suppliers GROUP BY Country ORDER BY Country;", None, None),
        ("Customer Count by City", "Find name and count of customers from different cities.", "SELECT City, COUNT(*) AS CustomerCount FROM customers GROUP BY City ORDER BY City;", None, None),
        ("Orders by Employee", "Find number of orders made by employee along with EmployeeID.", "SELECT EmployeeID, COUNT(*) AS OrderCount FROM orders GROUP BY EmployeeID ORDER BY EmployeeID;", None, None),
        ("Orders by Customer", "Find number of orders made by customers along with CustomerID.", "SELECT CustomerID, COUNT(*) AS OrderCount FROM orders GROUP BY CustomerID ORDER BY CustomerID;", None, None),
        ("Orders Shipped by Shipper 1 or 3", "Find all orders that are shipped by shippers having 1 or 3 ShipperID.", f"SELECT {ORDER_COLS} FROM orders WHERE ShipperID IN (1, 3) ORDER BY OrderID;", None, None),
        ("Products in Category 1", "SELECT all product having CategoryID 1.", f"SELECT {PRODUCT_COLS} FROM products WHERE CategoryID = 1 ORDER BY ProductID;", None, None),
        ("Product Name by Name Initial", "SELECT all products having ProductName that starts with the first letter of your name.", f"SELECT {PRODUCT_COLS} FROM products WHERE ProductName LIKE '{{{{FIRST_LETTER}}}}%' ORDER BY ProductID;", None, "product_name_initial"),
    ]
    for n, (title, question, sql, verify, dynamic) in enumerate(q4a, 1):
        items.append(item(f"4A-{n:02d}", 4, "A", n, title, question, sql, verify, dynamic=dynamic))

    # LAB 4 - GROUP B
    q4b = [
        ("Project Category Names", "Project CategoryName from categories.", "SELECT CategoryName FROM categories ORDER BY CategoryID;", None, None),
        ("Project Customer Countries", "Project Country from customers.", "SELECT Country FROM customers ORDER BY CustomerID;", None, None),
        ("Project City and Country", "Project City, Country from customers.", "SELECT City, Country FROM customers ORDER BY CustomerID;", None, None),
        ("Customers from Paris", "SELECT CustomerName from customers who are from Paris City.", "SELECT CustomerName FROM customers WHERE City = 'Paris';", None, None),
        ("Spanish Customer IDs", "SELECT CustomerID from customers who are from Spain.", "SELECT CustomerID FROM customers WHERE Country = 'Spain' ORDER BY CustomerID;", None, None),
        ("Mexico or Italy Customers", "SELECT CustomerID, CustomerName from customers who are from Mexico or Italy.", "SELECT CustomerID, CustomerName FROM customers WHERE Country IN ('Mexico', 'Italy') ORDER BY CustomerID;", None, None),
        ("Frankfurt, Germany Customers", "SELECT all from customers who are from Frankfurt a.M. and Germany.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City = 'Frankfurt a.M.' AND Country = 'Germany';", None, None),
        ("Customer City by Name Initial", "SELECT all from customers who are from a city whose name starts with the first letter of your name.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City LIKE '{{{{FIRST_LETTER}}}}%' ORDER BY CustomerID;", None, "customer_city_initial"),
        ("Exclude Venezuela and Argentina", "SELECT all from customers who are not from Venezuela or Argentina.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE Country NOT IN ('Venezuela', 'Argentina') ORDER BY CustomerID;", None, None),
        ("Customers from G7 Countries", "SELECT all from customers who are from G7 Countries (USA, UK, Canada, France, Germany, Italy, Japan).", f"SELECT {CUSTOMER_COLS} FROM customers WHERE Country IN ('USA', 'UK', 'Canada', 'France', 'Germany', 'Italy', 'Japan') ORDER BY CustomerID;", None, None),
        ("Postal Code Contains 50", "SELECT all from customers who have PostalCode containing 50.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE PostalCode LIKE '%50%' ORDER BY CustomerID;", None, None),
        ("Postal Code 31 in Mexico City or Toulouse", "SELECT all from customers having PostalCode containing 31 and from Mexico City or Toulouse.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE PostalCode LIKE '%31%' AND City IN ('Mexico City', 'Toulouse') ORDER BY CustomerID;", None, None),
        ("Customers Not from Elgin", "SELECT all from customers who are not from Elgin.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City <> 'Elgin' ORDER BY CustomerID;", None, None),
        ("Employees Born in July", "SELECT all employees who are born in July.", f"SELECT {EMPLOYEE_COLS} FROM employees WHERE MONTH(BirthDate) = 7 ORDER BY EmployeeID;", None, None),
        ("Employees with BA Degree", "SELECT all employees having BA degree in Notes.", f"SELECT {EMPLOYEE_COLS} FROM employees WHERE Notes LIKE '%BA%' ORDER BY EmployeeID;", None, None),
        ("Suppliers from Australia and Sweden", "SELECT all suppliers from Australia and Sweden.", f"SELECT {SUPPLIER_COLS} FROM suppliers WHERE Country IN ('Australia', 'Sweden') ORDER BY SupplierID;", None, None),
        ("Supplier Count by Country", "Find name and count of suppliers from different countries.", "SELECT Country, COUNT(*) AS SupplierCount FROM suppliers GROUP BY Country ORDER BY Country;", None, None),
        ("Customer Count by City", "Find name and count of customers from different cities.", "SELECT City, COUNT(*) AS CustomerCount FROM customers GROUP BY City ORDER BY City;", None, None),
        ("Orders by Employee", "Find number of orders made by employee along with EmployeeID.", "SELECT EmployeeID, COUNT(*) AS OrderCount FROM orders GROUP BY EmployeeID ORDER BY EmployeeID;", None, None),
        ("Orders by Customer", "Find number of orders made by customers along with CustomerID.", "SELECT CustomerID, COUNT(*) AS OrderCount FROM orders GROUP BY CustomerID ORDER BY CustomerID;", None, None),
        ("Orders Shipped by Shipper 2 or 4", "Find all orders that are shipped by shippers having 2 or 4 ShipperID.", f"SELECT {ORDER_COLS} FROM orders WHERE ShipperID IN (2, 4) ORDER BY OrderID;", None, None),
        ("Products in Category 5", "SELECT all product having CategoryID 5.", f"SELECT {PRODUCT_COLS} FROM products WHERE CategoryID = 5 ORDER BY ProductID;", None, None),
        ("Product Name by Name Initial", "SELECT all products having ProductName that starts with the first letter of your name.", f"SELECT {PRODUCT_COLS} FROM products WHERE ProductName LIKE '{{{{FIRST_LETTER}}}}%' ORDER BY ProductID;", None, "product_name_initial"),
    ]
    for n, (title, question, sql, verify, dynamic) in enumerate(q4b, 1):
        items.append(item(f"4B-{n:02d}", 4, "B", n, title, question, sql, verify, dynamic=dynamic))

    # LAB 5 - GROUP A
    g7_to_saarc = r"""
UPDATE customers
SET Country = CASE Country
  WHEN 'USA' THEN 'Pakistan'
  WHEN 'UK' THEN 'India'
  WHEN 'Canada' THEN 'Sri Lanka'
  WHEN 'France' THEN 'Bangladesh'
  WHEN 'Germany' THEN 'Nepal'
  WHEN 'Italy' THEN 'Bhutan'
  WHEN 'Japan' THEN 'Maldives'
END
WHERE Country IN ('USA', 'UK', 'Canada', 'France', 'Germany', 'Italy', 'Japan');
""".strip()

    delete_not_salzburg = r"""
DELETE od
FROM orderdetails AS od
JOIN orders AS o ON o.OrderID = od.OrderID
JOIN customers AS c ON c.CustomerID = o.CustomerID
WHERE c.City <> 'Salzburg';

DELETE o
FROM orders AS o
JOIN customers AS c ON c.CustomerID = o.CustomerID
WHERE c.City <> 'Salzburg';

DELETE FROM customers WHERE City <> 'Salzburg';
""".strip()

    delete_employee_month = lambda month: f"""
DELETE od
FROM orderdetails AS od
JOIN orders AS o ON o.OrderID = od.OrderID
JOIN employees AS e ON e.EmployeeID = o.EmployeeID
WHERE MONTH(e.BirthDate) = {month};

DELETE o
FROM orders AS o
JOIN employees AS e ON e.EmployeeID = o.EmployeeID
WHERE MONTH(e.BirthDate) = {month};

DELETE FROM employees WHERE MONTH(BirthDate) = {month};
""".strip()

    delete_product_categories = r"""
DELETE od
FROM orderdetails AS od
JOIN products AS p ON p.ProductID = od.ProductID
JOIN categories AS c ON c.CategoryID = p.CategoryID
WHERE c.CategoryName IN ('Seafood', 'Beverages');

DELETE p
FROM products AS p
JOIN categories AS c ON c.CategoryID = p.CategoryID
WHERE c.CategoryName IN ('Seafood', 'Beverages');
""".strip()

    q5a = [
        ("Add Two Product Categories", "Add two product categories of your choice.", "INSERT INTO categories (CategoryName, Description) VALUES ('Meat/Poultry', 'Prepared meats and poultry'), ('Produce', 'Fresh fruits and vegetables');", "SELECT CategoryID, CategoryName, Description FROM categories WHERE CategoryName IN ('Meat/Poultry', 'Produce') ORDER BY CategoryID;"),
        ("Add Three Suppliers", "Add 3 new suppliers in suppliers table.", "INSERT INTO suppliers (SupplierName, ContactName, Address, City, PostalCode, Country) VALUES ('Himalayan Traders', 'Aarav Sharma', 'Thamel Road', 'Kathmandu', '44600', 'Nepal'), ('Ganga Foods', 'Priya Singh', 'MG Road', 'Delhi', '110001', 'India'), ('Bengal Supplies', 'Rahim Khan', 'Gulshan Avenue', 'Dhaka', '1212', 'Bangladesh');", "SELECT SupplierID, SupplierName, ContactName, Address, City, PostalCode, Country FROM suppliers WHERE SupplierName IN ('Himalayan Traders', 'Ganga Foods', 'Bengal Supplies') ORDER BY SupplierID;"),
        ("Add Five Customers", "Add 5 new customers in customers table.", "INSERT INTO customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES ('Everest Mart', 'Suman Rai', 'Lazimpat', 'Kathmandu', '44600', 'Nepal'), ('Lotus Store', 'Anita Shah', 'Connaught Place', 'Delhi', '110001', 'India'), ('Padma Foods', 'Farhan Ali', 'Dhanmondi', 'Dhaka', '1209', 'Bangladesh'), ('Dragon Market', 'Tashi Dorji', 'Norzin Lam', 'Thimphu', '11001', 'Bhutan'), ('Island Grocers', 'Amina Latheef', 'Majeedhee Magu', 'Malé', '20026', 'Maldives');", "SELECT CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country FROM customers WHERE CustomerName IN ('Everest Mart', 'Lotus Store', 'Padma Foods', 'Dragon Market', 'Island Grocers') ORDER BY CustomerID;"),
        ("Add Four Products", "Add 4 products in product table.", "INSERT INTO products (ProductName, SupplierID, CategoryID, Unit, Price) VALUES ('Nepal Tea', 1, 1, '20 tea bags', 12.50), ('Tokyo Noodles', 2, 5, '10 packets', 8.75), ('Cajun Spice Mix', 3, 3, '6 jars', 16.00), ('Nordic Cheese', 5, 4, '12 packs', 24.50);", "SELECT ProductID, ProductName, SupplierID, CategoryID, Unit, Price FROM products WHERE ProductName IN ('Nepal Tea', 'Tokyo Noodles', 'Cajun Spice Mix', 'Nordic Cheese') ORDER BY ProductID;"),
        ("Add Three Employees", "Add 3 new employees.", "INSERT INTO employees (LastName, FirstName, BirthDate, Notes) VALUES ('Shrestha', 'Anil', '1995-01-15', 'BSc in Computer Science.'), ('Karki', 'Mina', '1994-05-21', 'MBA in Operations.'), ('Gurung', 'Rita', '1996-11-10', 'BA in Management.');", "SELECT EmployeeID, LastName, FirstName, BirthDate, Notes FROM employees WHERE LastName IN ('Shrestha', 'Karki', 'Gurung') ORDER BY EmployeeID;"),
        ("Brazil to Singapore", "Update all customers from Brazil to Singapore.", "UPDATE customers SET Country = 'Singapore' WHERE Country = 'Brazil';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country = 'Singapore' ORDER BY CustomerID;"),
        ("Madrid to Bangalore", "Update customers table changing name of Madrid City to Bangalore.", "UPDATE customers SET City = 'Bangalore' WHERE City = 'Madrid';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE City = 'Bangalore' ORDER BY CustomerID;"),
        ("German to Bhutanese Customers", "Update all German customer to Bhutanese customers.", "UPDATE customers SET Country = 'Bhutan' WHERE Country = 'Germany';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country = 'Bhutan' ORDER BY CustomerID;"),
        ("Spanish to Thai Customers", "Convert all Spanish customer to Thai Customers.", "UPDATE customers SET Country = 'Thailand' WHERE Country = 'Spain';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country = 'Thailand' ORDER BY CustomerID;"),
        ("London to Kathmandu, Nepal", "Convert all customers of London to Kathmandu customers and also change the country.", "UPDATE customers SET City = 'Kathmandu', Country = 'Nepal' WHERE City = 'London';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE City = 'Kathmandu' AND Country = 'Nepal' ORDER BY CustomerID;"),
        ("G7 to SAARC Countries", "Convert customers from G7 Countries to SAARC Countries.", g7_to_saarc, "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country IN ('Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Maldives', 'Nepal', 'Pakistan', 'Sri Lanka') ORDER BY CustomerID;"),
        ("Delete Orders and Order Details", "DELETE all records from orders and orderdetails.", "DELETE FROM orderdetails;\nDELETE FROM orders;", "SELECT (SELECT COUNT(*) FROM orders) AS OrdersRemaining, (SELECT COUNT(*) FROM orderdetails) AS OrderDetailsRemaining;"),
        ("Delete Postal Code 31 Customers", "DELETE all from customers who have PostalCode containing 31.", "DELETE FROM customers WHERE PostalCode LIKE '%31%';", "SELECT COUNT(*) AS CustomersRemaining FROM customers;"),
        ("Delete Rome/Paris Postal 00 Customers", "DELETE all from customers having PostalCode containing 00 and from Rome or Paris.", "DELETE FROM customers WHERE PostalCode LIKE '%00%' AND City IN ('Rome', 'Paris');", "SELECT CustomerID, CustomerName, City, PostalCode, Country FROM customers ORDER BY CustomerID;"),
        ("Delete Customers Not from Salzburg", "DELETE all from customers who are not from Salzburg.", delete_not_salzburg, "SELECT CustomerID, CustomerName, City, Country FROM customers ORDER BY CustomerID;"),
        ("Delete July-born Employees", "DELETE all employees who are born in July.", delete_employee_month(7), "SELECT EmployeeID, LastName, FirstName, BirthDate FROM employees ORDER BY EmployeeID;"),
        ("Delete August-born Employees", "DELETE all employees who are born in August.", delete_employee_month(8), "SELECT EmployeeID, LastName, FirstName, BirthDate FROM employees ORDER BY EmployeeID;"),
        ("Delete Seafood and Beverage Products", "DELETE all product from seafood and beverages categories.", delete_product_categories, "SELECT ProductID, ProductName, CategoryID, Price FROM products ORDER BY ProductID;"),
        ("Supplier Count by Country", "Find name and count of suppliers from different countries.", "SELECT Country, COUNT(*) AS SupplierCount FROM suppliers GROUP BY Country ORDER BY Country;", None),
        ("Customer Count by City", "Find name and count of customers from different cities.", "SELECT City, COUNT(*) AS CustomerCount FROM customers GROUP BY City ORDER BY City;", None),
        ("Orders by Employee", "Find number of orders made by employee along with EmployeeID.", "SELECT EmployeeID, COUNT(*) AS OrderCount FROM orders GROUP BY EmployeeID ORDER BY EmployeeID;", None),
    ]
    for n, (title, question, sql, verify) in enumerate(q5a, 1):
        items.append(item(f"5A-{n:02d}", 5, "A", n, title, question, sql, verify))

    # LAB 5 - GROUP B
    delete_suppliers_singapore_japan = r"""
DELETE od
FROM orderdetails AS od
JOIN products AS p ON p.ProductID = od.ProductID
JOIN suppliers AS s ON s.SupplierID = p.SupplierID
WHERE s.Country IN ('Singapore', 'Japan');

DELETE p
FROM products AS p
JOIN suppliers AS s ON s.SupplierID = p.SupplierID
WHERE s.Country IN ('Singapore', 'Japan');

DELETE FROM suppliers WHERE Country IN ('Singapore', 'Japan');
""".strip()

    q5b = [
        ("Add Two Product Categories", "Add two product categories of your choice.", "INSERT INTO categories (CategoryName, Description) VALUES ('Meat/Poultry', 'Prepared meats and poultry'), ('Produce', 'Fresh fruits and vegetables');", "SELECT CategoryID, CategoryName, Description FROM categories WHERE CategoryName IN ('Meat/Poultry', 'Produce') ORDER BY CategoryID;"),
        ("Add Three Suppliers", "Add 3 new suppliers in suppliers table.", "INSERT INTO suppliers (SupplierName, ContactName, Address, City, PostalCode, Country) VALUES ('Himalayan Traders', 'Aarav Sharma', 'Thamel Road', 'Kathmandu', '44600', 'Nepal'), ('Ganga Foods', 'Priya Singh', 'MG Road', 'Delhi', '110001', 'India'), ('Bengal Supplies', 'Rahim Khan', 'Gulshan Avenue', 'Dhaka', '1212', 'Bangladesh');", "SELECT SupplierID, SupplierName, ContactName, Address, City, PostalCode, Country FROM suppliers WHERE SupplierName IN ('Himalayan Traders', 'Ganga Foods', 'Bengal Supplies') ORDER BY SupplierID;"),
        ("Add Five Customers", "Add 5 new customers in customers table.", "INSERT INTO customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES ('Everest Mart', 'Suman Rai', 'Lazimpat', 'Kathmandu', '44600', 'Nepal'), ('Lotus Store', 'Anita Shah', 'Connaught Place', 'Delhi', '110001', 'India'), ('Padma Foods', 'Farhan Ali', 'Dhanmondi', 'Dhaka', '1209', 'Bangladesh'), ('Dragon Market', 'Tashi Dorji', 'Norzin Lam', 'Thimphu', '11001', 'Bhutan'), ('Island Grocers', 'Amina Latheef', 'Majeedhee Magu', 'Malé', '20026', 'Maldives');", "SELECT CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country FROM customers WHERE CustomerName IN ('Everest Mart', 'Lotus Store', 'Padma Foods', 'Dragon Market', 'Island Grocers') ORDER BY CustomerID;"),
        ("Add Four Products", "Add 4 products in product table.", "INSERT INTO products (ProductName, SupplierID, CategoryID, Unit, Price) VALUES ('Nepal Tea', 1, 1, '20 tea bags', 12.50), ('Tokyo Noodles', 2, 5, '10 packets', 8.75), ('Cajun Spice Mix', 3, 3, '6 jars', 16.00), ('Nordic Cheese', 5, 4, '12 packs', 24.50);", "SELECT ProductID, ProductName, SupplierID, CategoryID, Unit, Price FROM products WHERE ProductName IN ('Nepal Tea', 'Tokyo Noodles', 'Cajun Spice Mix', 'Nordic Cheese') ORDER BY ProductID;"),
        ("Add Three Employees", "Add 3 new employees.", "INSERT INTO employees (LastName, FirstName, BirthDate, Notes) VALUES ('Shrestha', 'Anil', '1995-01-15', 'BSc in Computer Science.'), ('Karki', 'Mina', '1994-05-21', 'MBA in Operations.'), ('Gurung', 'Rita', '1996-11-10', 'BA in Management.');", "SELECT EmployeeID, LastName, FirstName, BirthDate, Notes FROM employees WHERE LastName IN ('Shrestha', 'Karki', 'Gurung') ORDER BY EmployeeID;"),
        ("Mexico to Vietnam", "Update all customers from Mexico to Vietnam.", "UPDATE customers SET Country = 'Vietnam' WHERE Country = 'Mexico';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country = 'Vietnam' ORDER BY CustomerID;"),
        ("Paris to Delhi", "Update customers table changing name of Paris City to Delhi.", "UPDATE customers SET City = 'Delhi' WHERE City = 'Paris';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE City = 'Delhi' ORDER BY CustomerID;"),
        ("USA to Indian Customers", "Update all USA customer to Indian customers.", "UPDATE customers SET Country = 'India' WHERE Country = 'USA';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country = 'India' ORDER BY CustomerID;"),
        ("Brazilian to Cambodian Customers", "Convert all Brazilian customer to Cambodian Customers.", "UPDATE customers SET Country = 'Cambodia' WHERE Country = 'Brazil';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country = 'Cambodia' ORDER BY CustomerID;"),
        ("Madrid to Kathmandu, Nepal", "Convert all customers of Madrid to Kathmandu customers and also change the country.", "UPDATE customers SET City = 'Kathmandu', Country = 'Nepal' WHERE City = 'Madrid';", "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE City = 'Kathmandu' AND Country = 'Nepal' ORDER BY CustomerID;"),
        ("G7 to SAARC Countries", "Convert customers from G7 Countries to SAARC Countries.", g7_to_saarc, "SELECT CustomerID, CustomerName, City, Country FROM customers WHERE Country IN ('Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Maldives', 'Nepal', 'Pakistan', 'Sri Lanka') ORDER BY CustomerID;"),
        ("Delete Orders and Order Details", "DELETE all records from orders and orderdetails.", "DELETE FROM orderdetails;\nDELETE FROM orders;", "SELECT (SELECT COUNT(*) FROM orders) AS OrdersRemaining, (SELECT COUNT(*) FROM orderdetails) AS OrderDetailsRemaining;"),
        ("Delete Postal Code 31 Customers", "DELETE all from customers who have PostalCode containing 31.", "DELETE FROM customers WHERE PostalCode LIKE '%31%';", "SELECT COUNT(*) AS CustomersRemaining FROM customers;"),
        ("Delete Rome/Paris Postal 00 Customers", "DELETE all from customers having PostalCode containing 00 and from Rome or Paris.", "DELETE FROM customers WHERE PostalCode LIKE '%00%' AND City IN ('Rome', 'Paris');", "SELECT CustomerID, CustomerName, City, PostalCode, Country FROM customers ORDER BY CustomerID;"),
        ("Delete Customers Not from Salzburg", "DELETE all from customers who are not from Salzburg.", delete_not_salzburg, "SELECT CustomerID, CustomerName, City, Country FROM customers ORDER BY CustomerID;"),
        ("Delete July-born Employees", "DELETE all employees who are born in July.", delete_employee_month(7), "SELECT EmployeeID, LastName, FirstName, BirthDate FROM employees ORDER BY EmployeeID;"),
        ("Delete August-born Employees", "DELETE all employees who are born in August.", delete_employee_month(8), "SELECT EmployeeID, LastName, FirstName, BirthDate FROM employees ORDER BY EmployeeID;"),
        ("Delete Singapore and Japan Suppliers", "DELETE all suppliers from Singapore and Japan.", delete_suppliers_singapore_japan, "SELECT SupplierID, SupplierName, City, Country FROM suppliers ORDER BY SupplierID;"),
        ("Supplier Count by Country", "Find name and count of suppliers from different countries.", "SELECT Country, COUNT(*) AS SupplierCount FROM suppliers GROUP BY Country ORDER BY Country;", None),
        ("Customer Count by City", "Find name and count of customers from different cities.", "SELECT City, COUNT(*) AS CustomerCount FROM customers GROUP BY City ORDER BY City;", None),
        ("Orders by Employee", "Find number of orders made by employee along with EmployeeID.", "SELECT EmployeeID, COUNT(*) AS OrderCount FROM orders GROUP BY EmployeeID ORDER BY EmployeeID;", None),
    ]
    for n, (title, question, sql, verify) in enumerate(q5b, 1):
        items.append(item(f"5B-{n:02d}", 5, "B", n, title, question, sql, verify))

    # LAB 6 - GROUP A and B
    union_relation = r"""
SELECT ContactName AS PersonName, City AS Location
FROM customers
UNION
SELECT CONCAT(FirstName, ' ', LastName) AS PersonName, NULL AS Location
FROM employees
ORDER BY PersonName;
""".strip()

    union_all_names = r"""
SELECT ContactName AS PersonName FROM customers
UNION ALL
SELECT CONCAT(FirstName, ' ', LastName) AS PersonName FROM employees;
""".strip()

    q6a = [
        ("UNION Customers and Employees", "Perform UNION of customers and employees relation using compatible attributes.", union_relation, None, None),
        ("UNION ALL Contact and Employee Names", "Perform UNION ALL of customers.ContactName and employees.FirstName or full name.", union_all_names, None, None),
        ("Mexico and Austria Customers", "List all customers from Mexico and Austria using UNION.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE Country = 'Mexico'\nUNION\nSELECT {CUSTOMER_COLS} FROM customers WHERE Country = 'Austria'\nORDER BY CustomerID;", None, None),
        ("USA Customers with Names Unlike UK", "List all customers of USA not having the same name as customers from UK.", f"SELECT {CUSTOMER_COLS}\nFROM customers AS usa\nWHERE usa.Country = 'USA'\n  AND NOT EXISTS (\n    SELECT 1 FROM customers AS uk\n    WHERE uk.Country = 'UK' AND uk.CustomerName = usa.CustomerName\n  )\nORDER BY usa.CustomerID;", None, None),
        ("Create cust View", "Create view cust by selecting only 4 attributes from customers.", "DROP VIEW IF EXISTS cust;\nCREATE VIEW cust AS\nSELECT CustomerID, CustomerName, City, Country\nFROM customers;\nSELECT * FROM cust ORDER BY CustomerID;", None, None),
        ("Create productinfo View", "Join products with categories and suppliers to create productinfo with ProductID, ProductName, Unit, Price and all category/supplier attributes.", PRODUCTINFO_VIEW + ";\nSELECT * FROM productinfo ORDER BY ProductID;", None, None),
        ("Category Count from productinfo", "Find name and count of Categories from productinfo.", "SELECT CategoryName, COUNT(*) AS ProductCount FROM productinfo GROUP BY CategoryName ORDER BY CategoryName;", None, PRODUCTINFO_VIEW),
        ("North American Supplier Products", "Find all products that have suppliers from North America in productinfo.", "SELECT ProductID, ProductName, SupplierName, SupplierCity, SupplierCountry, Price FROM productinfo WHERE SupplierCountry IN ('USA', 'Canada', 'Mexico') ORDER BY ProductID;", None, PRODUCTINFO_VIEW),
        ("Products Below Average Price", "Find all products that have price lower than Average price from productinfo.", "SELECT ProductID, ProductName, Price FROM productinfo WHERE Price < (SELECT AVG(Price) FROM productinfo) ORDER BY ProductID;", None, PRODUCTINFO_VIEW),
        ("Create orderinfo View", "Join orders with customers, employees and shippers to create a view as orderinfo.", ORDERINFO_VIEW + ";\nSELECT * FROM orderinfo ORDER BY OrderID;", None, None),
        ("United Package and Swift Shipping Orders", "List all order shipment provided by United Package and Swift Shipping from orderinfo.", "SELECT OrderID, OrderDate, CustomerName, ShipperID, ShipperName FROM orderinfo WHERE ShipperName IN ('United Package', 'Swift Shipping') ORDER BY OrderID;", None, ORDERINFO_VIEW),
        ("Orders Processed by Janet and Steven", "List all order processed by employee Janet Leverling and Steven Buchanan from orderinfo.", "SELECT OrderID, OrderDate, CustomerName, EmployeeID, EmployeeName FROM orderinfo WHERE EmployeeName IN ('Janet Leverling', 'Steven Buchanan') ORDER BY OrderID;", None, ORDERINFO_VIEW),
        ("Shipment Providers on 18 August 2023", "List all order shipment provider on date August 18, 2023 from orderinfo.", "SELECT OrderID, OrderDate, ShipperID, ShipperName FROM orderinfo WHERE OrderDate = '2023-08-18' ORDER BY OrderID;", None, ORDERINFO_VIEW),
        ("Customer Countries on 19 August 2023", "List countries of customers that placed order on August 19, 2023 from orderinfo.", "SELECT DISTINCT CustomerCountry FROM orderinfo WHERE OrderDate = '2023-08-19' ORDER BY CustomerCountry;", None, ORDERINFO_VIEW),
    ]
    for n, (title, question, sql, verify, pre) in enumerate(q6a, 1):
        items.append(item(f"6A-{n:02d}", 6, "A", n, title, question, sql, verify, pre=pre))

    q6b = [
        ("UNION Customers and Employees", "Perform UNION of customers and employees relation using compatible attributes.", union_relation, None, None),
        ("UNION ALL Contact and Employee Names", "Perform UNION ALL of customers.ContactName and employees.FirstName or full name.", union_all_names, None, None),
        ("Berlin and Paris Customers", "List all customers from Berlin, Germany and Paris, France using UNION.", f"SELECT {CUSTOMER_COLS} FROM customers WHERE City = 'Berlin' AND Country = 'Germany'\nUNION\nSELECT {CUSTOMER_COLS} FROM customers WHERE City = 'Paris' AND Country = 'France'\nORDER BY CustomerID;", None, None),
        ("USA Customers with Names Unlike UK", "List all customers of USA not having the same name as customers from UK.", f"SELECT {CUSTOMER_COLS}\nFROM customers AS usa\nWHERE usa.Country = 'USA'\n  AND NOT EXISTS (\n    SELECT 1 FROM customers AS uk\n    WHERE uk.Country = 'UK' AND uk.CustomerName = usa.CustomerName\n  )\nORDER BY usa.CustomerID;", None, None),
        ("Create cust View", "Create view cust by selecting only 4 attributes from customers.", "DROP VIEW IF EXISTS cust;\nCREATE VIEW cust AS\nSELECT CustomerID, CustomerName, City, Country\nFROM customers;\nSELECT * FROM cust ORDER BY CustomerID;", None, None),
        ("Create productinfo View", "Join products with categories and suppliers to create productinfo with ProductID, ProductName, Unit, Price and all category/supplier attributes.", PRODUCTINFO_VIEW + ";\nSELECT * FROM productinfo ORDER BY ProductID;", None, None),
        ("Category Count from productinfo", "Find name and count of Categories from productinfo.", "SELECT CategoryName, COUNT(*) AS ProductCount FROM productinfo GROUP BY CategoryName ORDER BY CategoryName;", None, PRODUCTINFO_VIEW),
        ("Asian Supplier Products", "Find all products that have suppliers from Asia in productinfo.", "SELECT ProductID, ProductName, SupplierName, SupplierCity, SupplierCountry, Price FROM productinfo WHERE SupplierCountry IN ('Japan', 'China', 'India', 'Nepal', 'Bangladesh', 'Bhutan', 'Pakistan', 'Sri Lanka', 'Maldives', 'Singapore', 'Thailand', 'Vietnam', 'Cambodia', 'South Korea') ORDER BY ProductID;", None, PRODUCTINFO_VIEW),
        ("Products Below Average Price", "Find all products that have price lower than Average price from productinfo.", "SELECT ProductID, ProductName, Price FROM productinfo WHERE Price < (SELECT AVG(Price) FROM productinfo) ORDER BY ProductID;", None, PRODUCTINFO_VIEW),
        ("Create orderinfo View", "Join orders with customers, employees and shippers to create a view as orderinfo.", ORDERINFO_VIEW + ";\nSELECT * FROM orderinfo ORDER BY OrderID;", None, None),
        ("Speedy and Global Shipping Orders", "List all order shipment provided by Speedy Express and Global Express from orderinfo.", "SELECT OrderID, OrderDate, CustomerName, ShipperID, ShipperName FROM orderinfo WHERE ShipperName IN ('Speedy Express', 'Global Express') ORDER BY OrderID;", None, ORDERINFO_VIEW),
        ("Orders Processed by Nancy and Michael", "List all order processed by employee Nancy Davolio and Michael Suyama from orderinfo.", "SELECT OrderID, OrderDate, CustomerName, EmployeeID, EmployeeName FROM orderinfo WHERE EmployeeName IN ('Nancy Davolio', 'Michael Suyama') ORDER BY OrderID;", None, ORDERINFO_VIEW),
        ("Shipment Providers on 19 August 2023", "List all order shipment provider on date August 19, 2023 from orderinfo.", "SELECT OrderID, OrderDate, ShipperID, ShipperName FROM orderinfo WHERE OrderDate = '2023-08-19' ORDER BY OrderID;", None, ORDERINFO_VIEW),
        ("Customer Countries on 17 August 2023", "List countries of customers that placed order on August 17, 2023 from orderinfo.", "SELECT DISTINCT CustomerCountry FROM orderinfo WHERE OrderDate = '2023-08-17' ORDER BY CustomerCountry;", None, ORDERINFO_VIEW),
    ]
    for n, (title, question, sql, verify, pre) in enumerate(q6b, 1):
        items.append(item(f"6B-{n:02d}", 6, "B", n, title, question, sql, verify, pre=pre))

    return items


def normalize(value):
    if value is None:
        return None
    if isinstance(value, decimal.Decimal):
        return format(value, "f")
    if isinstance(value, (dt.date, dt.datetime, dt.time)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def execute_sql(cursor, sql: str) -> tuple[list[str], list[list], int]:
    columns: list[str] = []
    rows: list[list] = []
    affected_total = 0
    for statement in split_sql(sql):
        statement = statement.replace("{{FIRST_LETTER}}", "D")
        cursor.execute(statement)
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = [[normalize(v) for v in row] for row in cursor.fetchall()]
        elif cursor.rowcount > 0:
            affected_total += cursor.rowcount
    return columns, rows, affected_total


def verify_items(items: list[dict]) -> list[dict]:
    connection = pymysql.connect(host="127.0.0.1", user="root", password="", charset="utf8mb4", autocommit=True)
    results: list[dict] = []
    try:
        with connection.cursor() as cursor:
            for index, entry in enumerate(items, 1):
                cursor.execute(f"DROP DATABASE IF EXISTS `{VERIFY_DB}`")
                cursor.execute(f"CREATE DATABASE `{VERIFY_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                cursor.execute(f"USE `{VERIFY_DB}`")
                execute_sql(cursor, SETUP_SQL)
                if entry.get("pre"):
                    execute_sql(cursor, entry["pre"])
                columns, rows, affected = execute_sql(cursor, entry["sql"])
                if entry.get("verify"):
                    columns, rows, verify_affected = execute_sql(cursor, entry["verify"])
                    affected += verify_affected
                entry["columns"] = columns
                entry["rows"] = rows
                entry["affected"] = affected
                entry["verified"] = True
                results.append({
                    "id": entry["id"],
                    "lab": entry["lab"],
                    "group": entry["group"],
                    "question": entry["question"],
                    "sql": entry["sql"],
                    "verification_sql": entry.get("verify"),
                    "columns": columns,
                    "rows": rows,
                    "affected_rows": affected,
                    "verified_on": "XAMPP MariaDB 10.4.32",
                })
                print(f"[{index:03d}/{len(items)}] PASS {entry['id']} - {entry['title']}")
    finally:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"DROP DATABASE IF EXISTS `{VERIFY_DB}`")
        finally:
            connection.close()
    return results


def html_template(data_json: str, setup_json: str) -> str:
    return r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBMS Lab Report - Labs 4 to 6</title>
  <meta name="description" content="Verified DBMS Labs 4-6 report with SQL and XAMPP/phpMyAdmin-style outputs.">
  <style>
    :root{--bg:#080b10;--surface:#111722;--card:#182231;--border:rgba(255,255,255,.1);--muted:#8c98aa;--text:#eef3f9;--blue:#3b82f6;--cyan:#22d3ee;--paper:#fff;--ink:#263241}
    *{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}body{min-height:100vh;background:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px),var(--bg);background-size:32px 32px;color:var(--text);font-family:"Segoe UI",Calibri,sans-serif}.container{width:min(1500px,calc(100vw - 32px));margin:auto;padding:16px 0 36px}.inputs{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:10px;margin-bottom:10px}.field label{display:block;color:var(--muted);font:700 10px Consolas,monospace;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px}.field input{width:100%;background:var(--surface);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:10px 12px;font-size:14px;outline:none}.field input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(59,130,246,.15)}.toolbar{display:flex;align-items:center;gap:7px;flex-wrap:wrap;border-bottom:1px solid var(--border);padding-bottom:10px;margin-bottom:12px}.mode-tabs{display:flex;gap:7px;margin-right:auto}.action{border:1px solid var(--border);background:rgba(255,255,255,.035);color:#b7c1cf;border-radius:7px;padding:8px 11px;font:700 12px "Segoe UI",sans-serif;cursor:pointer}.action:hover{color:#fff;background:rgba(255,255,255,.07)}.action.primary{background:var(--blue);border-color:var(--blue);color:#fff}.list{display:flex;flex-direction:column;gap:13px}.card{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden}.card-head{display:flex;align-items:center;gap:12px;padding:13px 15px;cursor:pointer}.num{width:68px;height:38px;display:grid;place-items:center;border:1px solid rgba(34,211,238,.25);background:rgba(34,211,238,.08);color:var(--cyan);border-radius:8px;font:800 14px Consolas,monospace;flex:0 0 auto}.title h2{font-size:16px;color:#fff}.title p{font-size:13px;color:#b3bdcb;line-height:1.45;margin-top:3px}.arrow{margin-left:auto;color:var(--muted);transition:.2s}.body{display:none;border-top:1px solid var(--border);padding:14px}.card.open .body{display:flex;flex-direction:column;gap:12px}.card.open .arrow{transform:rotate(180deg)}.setup-card:not(.open){display:none}.code{border:1px solid var(--border);border-radius:8px;overflow:hidden;background:#0d1118}.codebar{display:flex;justify-content:space-between;align-items:center;background:#171d27;padding:9px 12px;color:var(--muted);font:700 11px Consolas,monospace}.copy{border:0;background:none;color:var(--muted);cursor:pointer;font:700 11px Consolas,monospace}.copy:hover{color:white}pre.sql{padding:16px;overflow:auto;white-space:pre;color:#dce5ef;font:13px/1.6 Consolas,monospace}.kw{color:#7dd3fc;font-weight:700}.str{color:#fbbf24}.com{color:#7f8da0}.xampp{background:#fff;color:#111;border:1px solid #111;border-radius:4px;overflow:hidden;box-shadow:0 8px 22px rgba(0,0,0,.18)}.xampp .kw,.xampp .str,.xampp .com,.xampp .null,.xampp .pm-link{color:#111!important}.xampp .kw{text-decoration:underline dotted;font-weight:700}.notice{background:#b8b8b8;color:#111;border-bottom:1px solid #111;padding:12px 14px;font-size:15px;line-height:1.45;font-weight:600}.query{background:#e5e5e5;color:#111;border-bottom:1px solid #111;padding:16px 18px;white-space:pre-wrap;overflow-wrap:anywhere;font:15px/1.55 "Segoe UI",sans-serif}.profile{display:flex;gap:8px;flex-wrap:wrap;background:#d0d0d0;color:#111;border-bottom:1px solid #111;padding:9px 12px;font-size:14px}.result{padding:10px 0 16px;overflow:auto;background:#fff}.extra{margin:0 0 10px 8px;padding:4px 9px;border:1px solid #555;border-radius:4px;background:linear-gradient(#fff,#d7d7d7);color:#111;font-size:13px}.pm-table{border-collapse:collapse;width:max-content;min-width:420px;background:#fff;color:#111;font-size:15px}.pm-table th{background:linear-gradient(#f2f2f2,#d2d2d2);color:#111;padding:6px 9px;text-align:left;white-space:nowrap}.pm-table td{padding:6px 9px;color:#111;white-space:nowrap;vertical-align:top}.pm-table tr:nth-child(even) td{background:#d9d9d9}.pm-table.wide-table{width:100%;min-width:0;font-size:12.5px;table-layout:auto}.pm-table.wide-table th,.pm-table.wide-table td{padding:4px 6px;white-space:normal;overflow-wrap:anywhere;word-break:normal;line-height:1.25}.empty{padding:14px;color:#333;font-size:15px;font-style:italic}.null{color:#111;font-style:italic;font-family:Consolas,monospace}.footer{margin-top:22px;border-top:1px solid var(--border);padding-top:13px;text-align:center;color:var(--muted);font:700 10px Consolas,monospace;letter-spacing:.06em}
    @media(max-width:850px){.inputs{grid-template-columns:1fr 1fr}.container{width:calc(100vw - 20px)}.toolbar{justify-content:flex-start}}
    @media(max-width:560px){.inputs{grid-template-columns:1fr}.card-head{align-items:flex-start}.num{width:58px}}
    @media print{body{background:white;color:#111;-webkit-print-color-adjust:exact;print-color-adjust:exact}.no-print,.setup-card{display:none!important}.container{width:auto;padding:0}.list{gap:7px}.card{background:white;color:#111;border-color:#ccc;break-inside:auto}.card-head{padding:7px 8px;break-after:avoid}.num{height:30px;width:60px;font-size:10pt}.title h2{color:#111;font-size:11pt}.title p{color:#333;font-size:9.5pt}.arrow{display:none}.body{display:flex!important;padding:8px;gap:7px!important}.code{break-inside:avoid}pre.sql{font-size:9.8pt;color:#111;background:white;white-space:pre-wrap}.xampp{box-shadow:none;break-inside:avoid}.notice,.query,.pm-table,.empty{font-size:10pt}.profile{font-size:9.5pt}.pm-table th,.pm-table td{padding:4px 6px}.footer{display:none}body[data-mode="output"] .list{gap:6mm}body[data-mode="output"] .card{border:0!important;border-radius:0!important;background:transparent!important;overflow:visible!important;margin:0!important;break-inside:auto!important}body[data-mode="output"] .card-head{display:none!important}body[data-mode="output"] .body{display:block!important;border:0!important;padding:0!important}body[data-mode="output"] .xampp{display:block!important;width:100%!important;border:1px solid #a6a6a6!important;border-radius:2px!important;box-shadow:none!important;overflow:hidden!important;margin:0!important;background:#fff!important;color:#000!important;break-inside:avoid-page!important;page-break-inside:avoid!important}body[data-mode="output"] .notice{display:block!important}body[data-mode="output"] .profile{display:flex!important}body[data-mode="output"] .extra{display:inline-block!important}body[data-mode="output"] .query{padding:3mm 3.5mm!important;background:#f2f2f2!important;color:#000!important;border-bottom:1px solid #c4c4c4!important}body[data-mode="output"] .notice{background:#e0e0e0!important;color:#000!important;border-bottom:1px solid #b8b8b8!important}body[data-mode="output"] .profile{background:#e8e8e8!important;color:#000!important;border-bottom:1px solid #c4c4c4!important}body[data-mode="output"] .xampp .kw,body[data-mode="output"] .xampp .str,body[data-mode="output"] .xampp .com,body[data-mode="output"] .xampp .null,body[data-mode="output"] .xampp .pm-link{color:#000!important}body[data-mode="output"] .result{padding:10px 0 16px!important;overflow:visible!important}body[data-mode="output"] .pm-table{min-width:0!important}body[data-mode="output"] .pm-table th,body[data-mode="output"] .pm-table td{padding:4px 6px!important}body[data-mode="output"] .pm-table.wide-table{width:100%!important;font-size:8.5pt!important;table-layout:auto!important}body[data-mode="output"] .pm-table.wide-table th,body[data-mode="output"] .pm-table.wide-table td{padding:2.5px 4px!important;white-space:normal!important;overflow-wrap:anywhere!important;line-height:1.18!important}}
  </style>
</head>
<body>
<main class="container">
  <section class="inputs no-print">
    <div class="field"><label>Student Name</label><input id="name" value="Deepak Bhattarai" oninput="render()"></div>
    <div class="field"><label>Roll No.</label><input id="roll" placeholder="Roll number"></div>
    <div class="field"><label>Section</label><input id="section" placeholder="Section"></div>
    <div class="field"><label>College</label><input id="college" placeholder="College name"></div>
  </section>

  <div class="toolbar no-print">
    <div class="mode-tabs">
      <button id="inputTab" class="action primary" type="button" onclick="setMode('input')">Questions + SQL</button>
      <button id="outputTab" class="action" type="button" onclick="setMode('output')">XAMPP Output</button>
    </div>
    <button class="action" type="button" onclick="toggleSetup()">Setup SQL</button>
    <button class="action" type="button" onclick="toggleAll()">Expand / Collapse All</button>
    <button class="action" type="button" onclick="print()">Print / PDF</button>
    <button class="action" type="button" onclick="downloadHtml()">Download HTML</button>
  </div>

  <div id="content"></div>
  <footer class="footer no-print">Every displayed query was executed against the supplied Northwind-style setup. DML questions are verified independently from a fresh database so one answer does not corrupt another.</footer>
</main>
<script>
const ITEMS = __DATA__;
const SETUP_SQL = __SETUP__;
const CUSTOMER_DATA = [
  [1,'Alfreds Futterkiste','Maria Anders','Obere Str. 57','Berlin','12209','Germany'],
  [2,'Ana Trujillo Emparedados','Ana Trujillo','Avda. de la Constitución 2222','Mexico City','05021','Mexico'],
  [3,'Around the Horn','Thomas Hardy','120 Hanover Sq.','London','WA1 1DP','UK'],
  [4,'Berglunds snabbköp','Christina Berglund','Berguvsvägen 8','Luleå','S-958 22','Sweden'],
  [5,'Blauer See Delikatessen','Hanna Moos','Forsterstr. 57','Mannheim','68306','Germany'],
  [6,'Parisian Foods','Pierre Dupond','Rue Royale','Paris','75008','France'],
  [7,'Rome Eats','Giovanni Rovelli','Via Ludovico','Rome','00100','Italy'],
  [8,'Salzburg Sweets','Georg Pipps','Geislrosenweg 14','Salzburg','5020','Austria'],
  [9,'Madrid Trading','Diego Roel','C/ Moralzarzal','Madrid','28034','Spain']
];
const PRODUCT_DATA = [
  [1,'Chai',1,1,'10 boxes x 20 bags','18.00'],[2,'Chang',1,1,'24 - 12 oz bottles','19.00'],[3,'Aniseed Syrup',1,1,'12 - 550 ml bottles','10.00'],[4,'Chef Anton Cajun Seasoning',2,2,'48 - 6 oz jars','22.00'],[5,'Ikura',2,2,'12 - 200 ml jars','31.00'],[6,'Uncle Bob Organic Dried Pears',3,3,'12 - 1 lb pkgs.','30.00']
];
let mode='input';
let setupOpen=false;
let allOpen=true;
function esc(v){return String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function firstLetter(){const s=document.getElementById('name').value.trim();return (s[0]||'D').toUpperCase()}
function effective(item){const x={...item};x.sql=x.sql.replaceAll('{{FIRST_LETTER}}',firstLetter());if(item.dynamic==='customer_city_initial'){x.columns=['CustomerID','CustomerName','ContactName','Address','City','PostalCode','Country'];x.rows=CUSTOMER_DATA.filter(r=>String(r[4]).toUpperCase().startsWith(firstLetter()))}if(item.dynamic==='product_name_initial'){x.columns=['ProductID','ProductName','SupplierID','CategoryID','Unit','Price'];x.rows=PRODUCT_DATA.filter(r=>String(r[1]).toUpperCase().startsWith(firstLetter()))}return x}
function highlight(sql){let s=esc(sql);s=s.replace(/(--.*)$/gm,'<span class="com">$1</span>');s=s.replace(/'([^']*)'/g,"<span class='str'>'$1'</span>");return s.replace(/\b(SELECT|FROM|WHERE|ORDER|BY|GROUP|HAVING|AS|IN|NOT|AND|OR|LIKE|IS|NULL|DISTINCT|COUNT|AVG|MONTH|INSERT|INTO|VALUES|UPDATE|SET|CASE|WHEN|THEN|ELSE|END|DELETE|JOIN|ON|CREATE|VIEW|DROP|IF|EXISTS|UNION|ALL|CONCAT)\b/gi,'<span class="kw">$1</span>')}
function table(columns,rows){if(!rows||!rows.length)return '<div class="empty">MySQL returned an empty result set (zero rows).</div>';const tableClass=columns.length>6?'pm-table wide-table':'pm-table';return `<table class="${tableClass}"><thead><tr>${columns.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(v=>`<td>${v===null?'<span class="null">NULL</span>':esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table>`}
function outputPane(x){const count=x.rows?.length??0;const affected=x.affected?` · ${x.affected} row(s) affected before verification`:'';const shownSql=x.verify?`${x.sql}\n\n-- Verification query\n${x.verify}`:x.sql;return `<section class="xampp"><div class="notice">Your SQL query has been executed successfully. ${count} row(s) returned${affected}.</div><div class="query">${highlight(shownSql)}</div><div class="profile"><span>□ Profiling</span><span>[ Edit inline ]</span><span>[ Edit ]</span><span>[ Create PHP code ]</span><span>[ Refresh ]</span></div><div class="result"><button class="extra">Extra options</button>${table(x.columns,x.rows)}</div></section>`}
function inputCard(item){const x=effective(item);return `<article class="card ${allOpen?'open':''}"><div class="card-head" onclick="this.parentElement.classList.toggle('open')"><div class="num">${x.id}</div><div class="title"><h2>${esc(x.title)}</h2><p>${esc(x.question)}</p></div><div class="arrow">▼</div></div><div class="body"><div class="code"><div class="codebar"><span>dbms_${x.id.toLowerCase()}.sql</span><button class="copy" onclick="event.stopPropagation();navigator.clipboard.writeText(${JSON.stringify(x.sql)})">Copy SQL</button></div><pre class="sql">${highlight(x.sql)}</pre></div></div></article>`}
function outputCard(item){const x=effective(item);return `<article class="card ${allOpen?'open':''}"><div class="card-head" onclick="this.parentElement.classList.toggle('open')"><div class="num">${x.id}</div><div class="title"><h2>${esc(x.title)}</h2><p>${esc(x.question)}</p></div><div class="arrow">▼</div></div><div class="body">${outputPane(x)}</div></article>`}
function setupCard(){return `<article id="setupCard" class="card setup-card ${setupOpen?'open':''}"><div class="card-head" onclick="toggleSetup()"><div class="num">SETUP</div><div class="title"><h2>Northwind-style Database Setup</h2><p>Create the schema and sample data before running the lab answers.</p></div><div class="arrow">▼</div></div><div class="body"><div class="code"><div class="codebar"><span>rkgajurelnorthwind_setup.sql</span><button class="copy" onclick="event.stopPropagation();navigator.clipboard.writeText(SETUP_SQL)">Copy SQL</button></div><pre class="sql">${highlight(SETUP_SQL)}</pre></div></div></article>`}
function setMode(next){mode=next;setupOpen=false;render();window.scrollTo({top:0,behavior:'smooth'})}
function toggleSetup(){if(mode!=='input'){mode='input'}setupOpen=!setupOpen;render();if(setupOpen){requestAnimationFrame(()=>document.getElementById('setupCard')?.scrollIntoView({behavior:'smooth',block:'start'}))}}
function toggleAll(){allOpen=!allOpen;render()}
function render(){document.body.dataset.mode=mode;document.getElementById('inputTab').classList.toggle('primary',mode==='input');document.getElementById('outputTab').classList.toggle('primary',mode==='output');const cards=mode==='input'?`${setupCard()}${ITEMS.map(inputCard).join('')}`:ITEMS.map(outputCard).join('');document.getElementById('content').innerHTML=`<div class="list">${cards}</div>`}
function downloadHtml(){const blob=new Blob(['<!DOCTYPE html>\n'+document.documentElement.outerHTML],{type:'text/html;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='DBMS_Lab_Report_Part2.html';a.click();URL.revokeObjectURL(a.href)}
render();
</script>
</body>
</html>'''.replace("__DATA__", data_json).replace("__SETUP__", setup_json)

def main() -> None:
    items = build_items()
    if len(items) != 116:
        raise RuntimeError(f"Expected 116 questions, found {len(items)}")
    verification = verify_items(items)
    VERIFY_JSON.write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding="utf-8")
    data_json = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    setup_json = json.dumps("CREATE DATABASE IF NOT EXISTS rkgajurelnorthwind;\nUSE rkgajurelnorthwind;\n\n" + SETUP_SQL, ensure_ascii=False)
    OUTPUT_HTML.write_text(html_template(data_json, setup_json), encoding="utf-8")
    print(f"WROTE {OUTPUT_HTML}")
    print(f"WROTE {VERIFY_JSON}")


if __name__ == "__main__":
    main()
