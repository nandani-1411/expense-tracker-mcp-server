# Expense Tracker MCP Server

### A remote MCP server for tracking and summarizing expenses.

## Transport

Streamable HTTP

## Available Tools

### add_expense

Add a new expense entry.

Example:

```json
{
  "date": "2026-06-25",
  "amount": 500,
  "category": "Travel",
  "subcategory": "Bus",
  "note": "Office commute"
}
```

### list_expense

Returns all expenses.

### list_expense_month

Returns expenses within a date range.

Example:

```json
{
  "start_date": "2026-06-01",
  "end_date": "2026-06-30"
}
```

### summarize

Summarizes expenses by category.

Example:

```json
{
  "start_date": "2026-06-01",
  "end_date": "2026-06-30"
}
```

## Resources

### expense://categories

Returns available expense categories from categories.json.


## Deployment

Hosted on Render:

https://expense-tracker-mcp-server-o8wr.onrender.com

## MCP Endpoint

Use the following MCP endpoint:

https://expense-tracker-mcp-server-o8wr.onrender.com/mcp