from typing import List, Tuple, Any, Optional
from . import db


def get_databases() -> List[str]:
    """
    Returns a list of database names from DBC.DatabasesV.

    :return: A list of database names.
    """
    query = "SELECT DatabaseName FROM DBC.DatabasesV ORDER BY 1"
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute(query)
        # Flatten list of tuples [(db1,), (db2,)] -> [db1, db2]
        return [row[0] for row in cur.fetchall()]


def get_tables(
    database_name: str,
) -> List[Tuple[str, str, Optional[str]]]:
    """
    Returns a list of tables for a given database.

    :param database_name: The name of the database to query.
    :return: A list of tuples containing (TableName, TableKind, CommentString).
    """
    query = """
    SELECT TableName, TableKind, CommentString 
    FROM DBC.TablesV 
    WHERE DatabaseName = ? 
    ORDER BY 1
    """
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute(query, (database_name,))
        return cur.fetchall()


def get_table_sample(
    database_name: str,
    table_name: str,
    limit: int = 100,
    offset: int = 0,
) -> Tuple[List[str], List[Tuple[Any, ...]]]:
    """
    Returns (columns, rows) for a given table using SAMPLE.

    :param database_name: The name of the database.
    :param table_name: The name of the table.
    :param limit: Number of rows to return (default 100).
    :param offset: Warning: Not used with SAMPLE syntax. Kept for signature compatibility.
    :return: A tuple containing a list of column names and a list of row tuples.
    """
    safe_db = f'"{database_name}"'
    safe_table = f'"{table_name}"'

    # User requested SAMPLE syntax.
    # SAMPLE n returns n random rows.
    # We cannot use OFFSET with simple SAMPLE.
    query = f"""
    SELECT * 
    FROM {safe_db}.{safe_table} 
    SAMPLE {limit}
    """

    # SAMPLE usually doesn't take parameters for the count in standard SQL prepared statements
    # consistently across all TD drivers/versions, but teradatasql might support it.
    # However, since limit is internal int, f-string is safe enough here.

    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return columns, rows


def get_record(
    database_name: str,
    table_name: str,
    key_column: str,
    key_value: str,
) -> Tuple[List[str], Optional[Tuple[Any, ...]]]:
    """
    Fetch a single record from a table based on a specific column and value.

    :param database_name: The name of the database.
    :param table_name: The name of the table.
    :param key_column: The column to search on (e.g., Primary Key).
    :param key_value: The value to match.
    :return: A tuple of (column_names, first_row, total_count). Row is None if not found.
    """
    safe_db = f'"{database_name}"'
    safe_table = f'"{table_name}"'
    safe_col = f'"{key_column}"'

    query = f"SELECT * FROM {safe_db}.{safe_table} WHERE {safe_col} = ?"

    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute(query, (key_value,))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []

        total_count = len(rows)
        first_row = rows[0] if rows else None

        return columns, first_row, total_count
