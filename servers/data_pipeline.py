"""
Data Pipeline & ETL MCP Server for NATO1000
Tools for data loading, cleaning, transformation, and feature engineering.
"""
from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json
import csv
from io import StringIO

mcp = FastMCP(name="NATO1000 Data Pipeline Tools")

@mcp.tool()
def load_csv_preview(csv_content: str, max_rows: int = 5) -> Dict[str, Any]:
    """Preview the first rows of CSV content and return schema info."""
    reader = csv.DictReader(StringIO(csv_content))
    rows = []
    for i, row in enumerate(reader):
        if i >= max_rows:
            break
        rows.append(row)
    columns = reader.fieldnames or []
    return {
        "columns": columns,
        "preview_rows": rows,
        "n_columns": len(columns),
        "note": "Full data not loaded — use for schema inspection"
    }

@mcp.tool()
def clean_missing_values(data: List[Dict], strategy: str = "drop", fill_value: Optional[str] = None) -> List[Dict]:
    """Clean missing/null values in a list of dict records. Strategies: drop, fill."""
    cleaned = []
    for record in data:
        if strategy == "drop":
            if all(v not in (None, "", "null", "NULL") for v in record.values()):
                cleaned.append(record)
        elif strategy == "fill" and fill_value is not None:
            filled = {k: (fill_value if v in (None, "", "null", "NULL") else v) for k, v in record.items()}
            cleaned.append(filled)
        else:
            cleaned.append(record)
    return cleaned

@mcp.tool()
def extract_features(text_records: List[str]) -> List[Dict[str, Any]]:
    """Simple feature extraction from text: length, word count, has_number."""
    features = []
    for text in text_records:
        features.append({
            "length": len(text),
            "word_count": len(text.split()),
            "has_number": any(c.isdigit() for c in text),
            "text_preview": text[:50] + "..." if len(text) > 50 else text
        })
    return features

if __name__ == "__main__":
    mcp.run()
