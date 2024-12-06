# SQLite DB Class

A simple and flexible SQLite database wrapper class to simplify common database operations like `INSERT`, `UPDATE`, `DELETE`, `SELECT`, and more. Supports complex queries including `JOIN`, `GROUP BY`, `HAVING`, and transactions, with easy-to-use methods and error handling.

## Key Features

- **Create Tables**: Create tables with automatic checks for existing tables.
- **Insert, Update, Delete**: Perform basic CRUD operations with minimal syntax.
- **Custom Queries**: Execute any custom SQL query with optional parameters.
- **Join Support**: Easily join tables using `INNER`, `LEFT`, `RIGHT`, and `FULL OUTER` joins.
- **Group By and Aggregations**: Perform `GROUP BY` queries with optional `HAVING` clauses.
- **Transactions**: Execute a set of queries as a transaction for consistency.
- **Error Handling**: Returns error messages instead of raising exceptions.

## Installation

You can install this package from PyPI:

```bash
pip install sqlite-db-wrapper
```

## Usage Examples

1. Creating a Table

    Create a table with specified columns if it does not already exist.

    ```python
    from db_wrapper import DB

    # Initialize database connection
    db = DB("example.db")

    # Define table columns and types
    columns = {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "age": "INTEGER"
    }

    # Create the table
    db.create_table("users", columns)
    ```

2. Inserting Data

    Insert data into the table.

    ```python
    # Insert a single user
    db.insert("users", {"name": "John Doe", "age": 30})

    # Insert another user
    db.insert("users", {"name": "Jane Smith", "age": 25})
    ```

3. Selecting Data

    Select data from the table.

    ```python
    # Fetch all users
    users = db.read_all("users")
    print(users)

    # Fetch user by name
    user = db.read_one("users", "name = ?", ("John Doe",))
    print(user)
    ```

4. Updating Data

    Update data in the table.

    ```python
    # Update the age of a user
    db.update("users", {"age": 31}, "name = ?", ("John Doe",))
    ```

5. Deleting Data

    Delete data from the table.

    ```python
    # Delete a user by name
    db.delete("users", "name = ?", ("John Doe",))
    ```

6. Performing Joins

    Join two tables with a specified condition.

    ```python
    # Assuming there are two tables: 'users' and 'orders'
    # Perform an INNER JOIN between 'users' and 'orders'
    join_condition = "orders.user_id = users.id"
    result = db.join("users", "orders", join_condition, join_type="INNER", columns=["users.name", "orders.total"])
    print(result)
    ```

7. Using Group By and Aggregations

    Perform GROUP BY operations with an optional HAVING clause.

    ```python
    # Group by age and filter groups with more than 1 user
    result = db.group_by("users", ["age"], having="COUNT(*) > 1")
    print(result)
    ```

8. Running Custom Queries

    Execute any custom query with parameters.

    ```python
    # Run a custom SELECT query with a parameter
    result = db.custom_query("SELECT name, age FROM users WHERE age > ?", (30,))
    print(result)
    ```

9. Running Transactions

    Execute a set of queries as a single transaction.

    ```python
    queries = [
        "INSERT INTO users (name, age) VALUES ('Alice', 22)",
        "UPDATE users SET age = 23 WHERE name = 'Alice'"
    ]

    # Execute the queries as a transaction
    db.transaction(queries)
    ```

## Methods Overview

* `create_table(table: str, columns: dict)`: Creates a table if it does not already exist.

* `insert(table: str, data: dict)`: Inserts a row into the specified table.

* `update(table: str, data: dict, where: str, where_params: tuple)`: Updates rows in the table with a WHERE clause.

* `delete(table: str, where: str, where_params: tuple)`: Deletes rows from the table with a WHERE clause.

* `read_all(table: str)`: Retrieves all rows from the specified table.

* `read_one(table: str, where: str, params: tuple)`: Retrieves a single row from the table using a WHERE clause.

* `custom_query(query: str, params: tuple)`: Executes a custom SQL query with optional parameters.

* `join(table1: str, table2: str, on_condition: str, join_type: str, columns: list)`: Performs a JOIN operation between two tables.

* `group_by(table: str, columns: list, having: str)`: Performs a GROUP BY operation with an optional HAVING clause.

* `transaction(queries: list)`: Executes a set of queries as a transaction.
close(): Closes the database connection.

## Error Handling

Instead of raising exceptions, all methods return a dictionary with an "error" key in case of an error, e.g.:

```python
{
    "error": "Error message"
}
```