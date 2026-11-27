"""TikTok scraper API: Scrapy spider example.

Runs DataGuru's TikTok APIs and prints the JSON they return:
  - TikTok Post: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Profile: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Search: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Shop: $0.0009 per successful request ($0.90 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    scrapy runspider examples/scrapy_spider.py -O tiktok.json
    scrapy runspider examples/scrapy_spider.py -a apis=tiktok-post -O tiktok.json
"""
import json
import os
import re
from urllib.parse import urlencode

import scrapy

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


class TiktokSpider(scrapy.Spider):
    """Each DataGuru call is one Scrapy request; detail APIs are requested from the search callback."""

    name = "tiktok"
    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_TIMEOUT": 300,      # some sites take a while to scrape
        "RETRY_ENABLED": False,       # a retried request could be billed twice
        "HTTPERROR_ALLOW_ALL": True,  # errors come back as JSON; parse() reports them
        "ROBOTSTXT_OBEY": False,      # requests go to api.dataguru.cc, not the website itself
    }

    def __init__(self, apis=None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.environ.get("DATAGURU_API_KEY")
        if not self.api_key:
            raise ValueError("Set DATAGURU_API_KEY (https://dashboard.dataguru.cc)")
        self.wanted = apis.split(",") if apis else [n for n, c in CALLS.items() if not c.get("needs_input")]
        unknown = [n for n in self.wanted if n not in CALLS]
        if unknown:
            raise ValueError(f"Unknown API {unknown}. Choose from: {', '.join(CALLS)}")

    def request_for(self, name, value=None):
        call = CALLS[name]
        query, body = dict(call["query"]), dict(call["body"])
        if value is not None:
            param = call["from"]["param"]
            (query if param in query else body)[param] = value
        url = call["url"] + ("?" + urlencode(query) if query else "")
        headers = {"Authorization": f"Api-Key {self.api_key}"}
        if call["method"] == "GET":
            return scrapy.Request(url, headers=headers, callback=self.parse, cb_kwargs={"name": name})
        return scrapy.http.JsonRequest(url, data=body, method=call["method"], headers=headers,
                                       callback=self.parse, cb_kwargs={"name": name})

    async def start(self):  # Scrapy 2.13+
        for request in self.start_requests():
            yield request

    def start_requests(self):  # older Scrapy
        # Detail APIs need a URL from their search first; request the search instead.
        needed = dict.fromkeys(CALLS[n]["from"]["api"] if "from" in CALLS[n] else n for n in self.wanted)
        for name in needed:
            yield self.request_for(name)

    def parse(self, response, name):
        data = json.loads(response.text)
        if response.status >= 400 or data.get("success") is False:
            self.logger.error("%s failed: %s", name, data.get("error"))
            return
        if name in self.wanted:
            yield {"api": name, "data": data}
        # Feed the first matching URL into each detail API that depends on this one.
        for detail, call in CALLS.items():
            if call.get("from", {}).get("api") == name and detail in self.wanted:
                match = re.search(call["from"]["match"], json.dumps(data))
                if match:
                    yield self.request_for(detail, match.group(0))
                else:
                    self.logger.warning("No URL for %s in the %s results", detail, name)
