"""
Feature Engineering MCP Server for NATO1000
Tools for scaling, encoding, and basic feature creation.
"""
from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import statistics

mcp = FastMCP(name="NATO1000 Feature Engineering")

@mcp.tool()
def scale_features(data: List[List[float]], method: str = "minmax") -> Dict[str, Any]:
    """Scale numeric features. Methods: minmax, standard."""
    if not data or not data[0]:
        return {"error": "Empty data"}
    n_features = len(data[0])
    scaled = [[0.0] * n_features for _ in data]
    stats = []
    for j in range(n_features):
        col = [row[j] for row in data]
        if method == "minmax":
            mn, mx = min(col), max(col)
            rng = mx - mn if mx != mn else 1
            for i, val in enumerate(col):
                scaled[i][j] = (val - mn) / rng
            stats.append({"min": mn, "max": mx})
        elif method == "standard":
            mean = statistics.mean(col)
            std = statistics.stdev(col) if len(col) > 1 else 1
            for i, val in enumerate(col):
                scaled[i][j] = (val - mean) / std
            stats.append({"mean": mean, "std": std})
    return {"scaled_data": scaled, "method": method, "stats": stats}

@mcp.tool()
def encode_categorical(values: List[str]) -> Dict[str, Any]:
    """One-hot style encoding for categorical values (returns mapping and encoded)."""
    unique = sorted(set(values))
    mapping = {v: i for i, v in enumerate(unique)}
    encoded = [mapping[v] for v in values]
    return {"mapping": mapping, "encoded": encoded, "n_classes": len(unique)}

@mcp.tool()
def text_features(texts: List[str]) -> List[Dict[str, Any]]:
    """Extract simple text features: length, word count, unique words, digit ratio."""
    features = []
    for text in texts:
        words = text.split()
        features.append({
            "char_length": len(text),
            "word_count": len(words),
            "unique_words": len(set(words)),
            "digit_ratio": sum(c.isdigit() for c in text) / len(text) if text else 0
        })
    return features

if __name__ == "__main__":
    mcp.run()
