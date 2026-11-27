"""TikTok scraper API: DataGuru Python SDK example.

Runs DataGuru's TikTok APIs and prints the JSON they return:
  - TikTok Post: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Profile: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Search: $0.0009 per successful request ($0.90 per 1,000)
  - TikTok Shop: $0.0009 per successful request ($0.90 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/sdk_example.py            # every API below
    python examples/sdk_example.py tiktok-post
"""
import json
import sys
from pathlib import Path

from dataguru import DataGuru, DataGuruError

def tiktok_post(dg):
    """TikTok Post: Get details of a public TikTok post/video: caption, creator, video download links, music, views, likes, shares and bookmarks."""
    return dg.call(
        "tiktok-post",
        post_url="https://www.tiktok.com/@khaby.lame/video/7681719358225239326",
    )


def tiktok_profile(dg):
    """TikTok Profile: Get a public TikTok profile: username, name, bio, follower and following counts, likes, verification, stats and profile photo."""
    return dg.call(
        "tiktok-profile",
        profile_url="https://www.tiktok.com/@tiktok",
    )


def tiktok_search(dg):
    """TikTok Search: Search TikTok for videos by keyword or hashtag with metrics, music details, and media URLs."""
    return dg.call(
        "tiktok-search",
        query="cooking",
    )


def tiktok_shop(dg):
    """TikTok Shop: Scrape TikTok Shop product details, sale price, sales count, creator commission rate and seller profile."""
    # Replace the placeholder with a real value before running.
    return dg.call(
        "tiktok-shop",
        product_url="https://shop.tiktok.com/view/product/<product-id>",
    )


EXAMPLES = {
    "tiktok-post": tiktok_post,
    "tiktok-profile": tiktok_profile,
    "tiktok-search": tiktok_search,
    "tiktok-shop": tiktok_shop,
}
DEFAULT = ['tiktok-post', 'tiktok-profile', 'tiktok-search']


def main(names):
    out = Path("output")
    out.mkdir(exist_ok=True)
    with DataGuru() as dg:  # reads DATAGURU_API_KEY
        for name in names:
            data = EXAMPLES[name](dg)
            (out / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{name}: saved output/{name}.json")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or DEFAULT
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(EXAMPLES)}")
    try:
        main(names)
    except DataGuruError as error:
        sys.exit(f"DataGuru error: {error}")
