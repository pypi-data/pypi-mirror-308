import sqlite3
from typing import Any, List, Tuple, Dict, Optional, Union

class DB:
    def __init__(self, db_name: str):
        """Initialize the database connection."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row  # Allows row access by column name
        self.cursor = self.conn.cursor()

    def __execute(self, query: str, params: Tuple[Any, ...] = ()) -> Union[List[Dict[str, Any]], None]:
        """Private method to execute a query and handle both SELECT and non-SELECT queries."""
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                rows = self.cursor.fetchall()
                return [dict(row) for row in rows]
            else:
                self.conn.commit()
        except sqlite3.Error as e:
            return {"error": str(e)}
        return None

    def create_table(self, table: str, columns: Dict[str, str]) -> Union[None, Dict[str, str]]:
        """Create a table with specified columns if it does not already exist."""
        column_definitions = ', '.join([f"{col} {data_type}" for col, data_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table} ({column_definitions})"
        return self.__execute(query)

    def insert(self, table: str, data: Dict[str, Any]) -> Union[None, Dict[str, str]]:
        """Insert a row into the specified table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.__execute(query, tuple(data.values()))

    def update(self, table: str, data: Dict[str, Any], where: str, where_params: Tuple[Any, ...]) -> Union[None, Dict[str, str]]:
        """Update rows in the specified table with a WHERE clause."""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        return self.__execute(query, tuple(data.values()) + where_params)

    def delete(self, table: str, where: str, where_params: Tuple[Any, ...]) -> Union[None, Dict[str, str]]:
        """Delete rows from the specified table with a WHERE clause."""
        query = f"DELETE FROM {table} WHERE {where}"
        return self.__execute(query, where_params)

    def read_all(self, table: str) -> Union[List[Dict[str, Any]], Dict[str, str]]:
        """Read all rows from the specified table."""
        query = f"SELECT * FROM {table}"
        return self.__execute(query)

    def read_one(self, table: str, where: str, params: Tuple[Any, ...]) -> Union[Dict[str, Any], None, Dict[str, str]]:
        """Read a single row from the specified table with a WHERE clause."""
        query = f"SELECT * FROM {table} WHERE {where}"
        result = self.__execute(query, params)
        return result[0] if result else None

    def custom_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Union[List[Dict[str, Any]], None, Dict[str, str]]:
        """
        Execute a custom query with optional parameters.

        Args:
            query (str): The custom SQL query to execute.
            params (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            Union[List[Dict[str, Any]], None, Dict[str, str]]: Rows if a SELECT query, else None.
        """
        if params is None:
            params = ()
        return self.__execute(query, params)

    def join(self, table1: str, table2: str, on_condition: str, join_type: str = "INNER", columns: Optional[List[str]] = None) -> Union[List[Dict[str, Any]], Dict[str, str]]:
        """Perform a JOIN operation."""
        columns = ', '.join(columns) if columns else "*"
        query = f"SELECT {columns} FROM {table1} {join_type} JOIN {table2} ON {on_condition}"
        return self.__execute(query)

    def group_by(self, table: str, columns: List[str], having: Optional[str] = None) -> Union[List[Dict[str, Any]], Dict[str, str]]:
        """Perform GROUP BY operation with an optional HAVING clause."""
        group_by_clause = ', '.join(columns)
        query = f"SELECT {group_by_clause}, COUNT(*) FROM {table} GROUP BY {group_by_clause}"
        if having:
            query += f" HAVING {having}"
        return self.__execute(query)

    def transaction(self, queries: List[str]) -> Union[None, Dict[str, str]]:
        """Execute a set of queries as a transaction."""
        try:
            self.conn.begin()
            for query in queries:
                self.__execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            return {"error": str(e)}
        return None

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()

