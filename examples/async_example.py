"""TikTok scraper API: asyncio + httpx example.

Runs DataGuru's TikTok APIs and prints the JSON they return:
  - TikTok Post: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Profile: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Search: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Shop: $0.0009 per successful request ($0.90 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/async_example.py
    python examples/async_example.py tiktok-post
"""
import asyncio
import json
import os
import re
import sys

import httpx

API_KEY = os.environ.get("DATAGURU_API_KEY") or sys.exit("Set DATAGURU_API_KEY (https://dashboard.dataguru.cc)")
CONCURRENCY = 4  # requests in flight at once; stay within your plan's rate limit

# Entries marked needs_input hold a placeholder value: replace it, then run that API by name.
CALLS = {
    "tiktok-post": {
        "name": "TikTok Post",
        "method": "POST",
        "url": "https://api.dataguru.cc/api/v1/tiktok/post",
        "query": {},
        "body": {
            "post_url": "https://www.tiktok.com/@khaby.lame/video/7681719358225239326"
        }
    },
    "tiktok-profile": {
        "name": "TikTok Profile",
        "method": "POST",
        "url": "https://api.dataguru.cc/api/v1/tiktok/profile",
        "query": {},
        "body": {
            "profile_url": "https://www.tiktok.com/@tiktok"
        }
    },
    "tiktok-search": {
        "name": "TikTok Search",
        "method": "POST",
        "url": "https://api.dataguru.cc/api/v1/tiktok/search",
        "query": {},
        "body": {
            "query": "cooking"
        }
    },
    "tiktok-shop": {
        "name": "TikTok Shop",
        "method": "POST",
        "url": "https://api.dataguru.cc/api/v1/tiktok/shop",
        "query": {},
        "body": {
            "product_url": "https://shop.tiktok.com/view/product/<product-id>"
        },
        "needs_input": True
    }
}


class Runner:
    """Runs APIs concurrently. A detail API waits for the search it depends on; each call runs once."""

    def __init__(self, client):
        self.client = client
        self.limit = asyncio.Semaphore(CONCURRENCY)
        self.tasks = {}

    def run(self, name):
        if name not in self.tasks:
            self.tasks[name] = asyncio.ensure_future(self._run(name))
        return self.tasks[name]

    async def _run(self, name):
        call = CALLS[name]
        query, body = dict(call["query"]), dict(call["body"])
        if "from" in call:
            src = call["from"]
            match = re.search(src["match"], json.dumps(await self.run(src["api"])))
            if not match:
                raise RuntimeError(f"No URL found in the {src['api']} results")
            (query if src["param"] in query else body)[src["param"]] = match.group(0)
        async with self.limit:
            response = await self.client.request(
                call["method"], call["url"], params=query or None,
                json=body if call["method"] != "GET" else None,
            )
        data = response.json()
        if response.status_code >= 400 or data.get("success") is False:
            error = data.get("error") or {}
            raise RuntimeError(f"{name}: HTTP {response.status_code} {error.get('code')}: {error.get('message')}")
        return data


async def main(names):
    headers = {"Authorization": f"Api-Key {API_KEY}"}
    async with httpx.AsyncClient(headers=headers, timeout=300) as client:
        runner = Runner(client)
        results = await asyncio.gather(*(runner.run(n) for n in names), return_exceptions=True)
    for name, data in zip(names, results):
        print(f"== {CALLS[name]['name']} ({name})")
        print(data if isinstance(data, Exception) else json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or [n for n, c in CALLS.items() if not c.get("needs_input")]
    unknown = [n for n in names if n not in CALLS]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(CALLS)}")
    asyncio.run(main(names))
