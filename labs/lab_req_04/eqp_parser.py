#!/usr/bin/env python3
"""
Semantic EXPLAIN QUERY PLAN (EQP) Parser for LAB-REQ-04.
Extracts semantic access paths (SCAN, SEARCH, INDEX, COVERING INDEX)
without binding to exact ASCII tree formatting or exact strings.
"""

import re


def normalize_eqp_line(line):
    """
    Remove leading tree characters, pipe prefixes, or id|parent|notused columns.
    Examples:
      '0|0|0|SCAN orders' -> 'SCAN orders'
      '|--SCAN orders' -> 'SCAN orders'
      '`--SEARCH orders USING INDEX idx_user' -> 'SEARCH orders USING INDEX idx_user'
    """
    # Remove leading SQLite tabular prefix (e.g. 0|0|0|)
    line = re.sub(r"^\d+\|\d+\|\d+\|", "", line)
    # Remove leading ASCII tree symbols
    line = re.sub(r"^[\|\`\-\s]+", "", line)
    return line.strip()


def parse_semantic_access_path(line):
    """
    Classify a single EQP output line semantically.
    Returns dict:
      - raw: original line
      - normalized: cleaned text
      - category: SCAN | SEARCH_INDEX | COVERING_INDEX | SEARCH_OTHER | OTHER
      - table: target table name (if recognized)
      - index_name: name of index used (if recognized)
    """
    norm = normalize_eqp_line(line)
    upper = norm.upper()

    category = "OTHER"
    table = None
    index_name = None

    is_covering = "COVERING INDEX" in upper
    has_index = "INDEX" in upper
    is_search = upper.startswith("SEARCH") or " SEARCH " in upper
    is_scan = upper.startswith("SCAN") or " SCAN " in upper

    if is_covering:
        category = "COVERING_INDEX"
    elif is_search and has_index:
        category = "SEARCH_INDEX"
    elif is_search:
        category = "SEARCH_OTHER"
    elif is_scan:
        category = "SCAN"

    # Extract table name if pattern matches 'SCAN <table>' or 'SEARCH <table>'
    tbl_match = re.search(r"(?:SCAN|SEARCH)\s+([A-Za-z0-9_]+)", norm, re.IGNORECASE)
    if tbl_match:
        table = tbl_match.group(1)

    # Extract index name if pattern matches 'USING [COVERING ]?INDEX ([A-Za-z0-9_]+)'
    idx_match = re.search(r"INDEX\s+([A-Za-z0-9_]+)", norm, re.IGNORECASE)
    if idx_match:
        index_name = idx_match.group(1)

    return {
        "raw": line,
        "normalized": norm,
        "category": category,
        "table": table,
        "index_name": index_name,
        "is_covering": is_covering,
    }


def parse_eqp_output(raw_output):
    """
    Parse full multi-line EQP output and return list of semantic classifications.
    """
    if isinstance(raw_output, str):
        lines = raw_output.strip().splitlines()
    elif isinstance(raw_output, (list, tuple)):
        # If passed list of tuples from Python cursor, take the detail column (last element)
        lines = [item[-1] if isinstance(item, (list, tuple)) else str(item) for item in raw_output]
    else:
        lines = [str(raw_output)]

    results = []
    for line in lines:
        if not line.strip():
            continue
        parsed = parse_semantic_access_path(line)
        results.append(parsed)
    return results


def summarize_eqp_paths(parsed_records):
    """
    Summarize distinct access path categories present in the query plan.
    """
    categories = [r["category"] for r in parsed_records]
    return {
        "has_scan": "SCAN" in categories,
        "has_search_index": any(c in ("SEARCH_INDEX", "COVERING_INDEX") for c in categories),
        "has_covering_index": "COVERING_INDEX" in categories,
        "categories": categories,
    }
