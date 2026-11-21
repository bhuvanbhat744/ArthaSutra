from database.db import get_connection


def add_token(symbol, quantity):
    connection = get_connection()
    cursor = connection.cursor()

    symbol = symbol.upper().strip()

    cursor.execute("""
        INSERT INTO portfolio (token_symbol, quantity)
        VALUES (?, ?)
        ON CONFLICT(token_symbol)
        DO UPDATE SET quantity = excluded.quantity
    """, (symbol, quantity))

    connection.commit()
    connection.close()

def delete_token(symbol):
    connection = get_connection()
    cursor = connection.cursor()

    symbol = symbol.upper().strip()

    cursor.execute(
        "DELETE FROM portfolio WHERE token_symbol = ?",
        (symbol,)
    )

    connection.commit()
    connection.close()

def get_portfolio():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT token_symbol, quantity
        FROM portfolio
    """)

    portfolio = cursor.fetchall()

    connection.close()

    return portfolio