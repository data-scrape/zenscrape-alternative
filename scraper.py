#!/usr/bin/env python3
"""
zenscrape-alternative - Zenscrape to CoreClaw Migration Demo

This script demonstrates how to migrate from Zenscrape to CoreClaw's Web Data API.

Sponsored by CoreClaw - https://www.coreclaw.com
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


@dataclass
class DataRecord:
    """Data model for API response records."""
    id: str = ""
    name: str = ""
    address: str = ""
    phone: str = ""
    website: str = ""
    rating: float = 0.0
    reviews_count: int = 0
    categories: list = None
    metadata: Dict[str, Any] = None
    scraped_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class ZenscrapeAlternative:
    """Demo: Migrate from Zenscrape to CoreClaw Web Data API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.coreclaw.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "CoreClaw-Migration-Demo/1.0",
        })

    def search_google_maps(self, query: str, limit: int = 100) -> List[DataRecord]:
        """Search Google Maps business data via CoreClaw API."""
        url = f"{self.base_url}/google-maps"
        params = {"query": query, "limit": limit, "format": "json"}
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        records = []
        for item in data.get("results", []):
            records.append(DataRecord(
                id=item.get("id", ""),
                name=item.get("name", ""),
                address=item.get("address", ""),
                phone=item.get("phone", ""),
                website=item.get("website", ""),
                rating=item.get("rating", 0.0),
                reviews_count=item.get("reviews_count", 0),
                categories=item.get("categories", []),
                metadata=item,
                scraped_at=item.get("scraped_at", ""),
            ))
        return records

    def export(self, records: List[DataRecord], filepath: str):
        """Export records to JSON."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in records], f, ensure_ascii=False, indent=2)
        print(f"Exported {len(records)} records to {filepath}")


def main():
    parser = argparse.ArgumentParser(description="zenscrape-alternative - Zenscrape to CoreClaw Migration")
    parser.add_argument("--api-key", required=True, help="CoreClaw API key")
    parser.add_argument("--query", "-q", default="coffee shops in Seattle", help="Search query")
    parser.add_argument("--output", "-o", default="results.json", help="Output file")
    parser.add_argument("--limit", "-m", type=int, default=50, help="Max results")
    args = parser.parse_args()

    client = ZenscrapeAlternative(api_key=args.api_key)
    records = client.search_google_maps(args.query, args.limit)
    client.export(records, args.output)
    print(f"Done! Got {len(records)} records from CoreClaw API.")


if __name__ == "__main__":
    main()
