from fastmcp import FastMCP
import os
import aiosqlite
import asyncio
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Expense Tracker MCP Server")

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
        """)
        await db.commit()


@mcp.tool()
async def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    note: str = ""
):
    """Add a new expense entry."""

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO expenses
            (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (date, amount, category, subcategory, note)
        )
        await db.commit()

        return {
            "status": "ok",
            "id": cursor.lastrowid
        }


@mcp.tool()
async def list_expense():
    """List all expenses."""

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT
                id,
                date,
                amount,
                category,
                subcategory,
                note
            FROM expenses
            ORDER BY id ASC
            """
        )

        rows = await cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


@mcp.tool()
async def list_expense_month(
    start_date: str,
    end_date: str
):
    """List expenses within a date range."""

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT
                id,
                date,
                amount,
                category,
                subcategory,
                note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )

        rows = await cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


@mcp.tool()
async def summarize(
    start_date: str,
    end_date: str,
    category: str | None = None
):
    """Summarize expenses by category."""

    query = """
    SELECT
        category,
        SUM(amount) AS total_amount
    FROM expenses
    WHERE date BETWEEN ? AND ?
    """

    params = [start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += """
    GROUP BY category
    ORDER BY category ASC
    """

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(query, params)

        rows = await cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


@mcp.resource(
    "expense://categories",
    mime_type="application/json"
)
async def categories():
    """Return categories.json."""

    with open(
        CATEGORIES_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


if __name__ == "__main__":
    

    asyncio.run(init_db())

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )