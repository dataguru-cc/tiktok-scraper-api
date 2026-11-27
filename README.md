# TikTok Scraper API

Scrape TikTok with a JSON API. This repo has working Python examples for DataGuru's TikTok scraper APIs: TikTok Post, TikTok Profile, TikTok Search and TikTok Shop.

[DataGuru](https://dataguru.cc) runs the scraping, proxies, retries and parsing, and returns clean JSON. You pay only for successful requests, from $0.0009 per request, out of a prepaid balance: no subscription. New accounts get $1.00 of free credit.

## TikTok APIs

| API | What it returns | Price | Page |
| --- | --- | --- | --- |
| [TikTok Post](#tiktok-post) | Get details of a public TikTok post/video: caption, creator, video download links, music, views, likes, shares and bookmarks. | $0.0009 | [https://dataguru.cc/apis/tiktok-post/](https://dataguru.cc/apis/tiktok-post/) |
| [TikTok Profile](#tiktok-profile) | Get a public TikTok profile: username, name, bio, follower and following counts, likes, verification, stats and profile photo. | $0.0009 | [https://dataguru.cc/apis/tiktok-profile/](https://dataguru.cc/apis/tiktok-profile/) |
| [TikTok Search](#tiktok-search) | Search TikTok for videos by keyword or hashtag with metrics, music details, and media URLs. | $0.0009 | [https://dataguru.cc/apis/tiktok-search/](https://dataguru.cc/apis/tiktok-search/) |
| [TikTok Shop](#tiktok-shop) | Scrape TikTok Shop product details, sale price, sales count, creator commission rate and seller profile. | $0.0009 | [https://dataguru.cc/apis/tiktok-shop/](https://dataguru.cc/apis/tiktok-shop/) |

## Quick start

1. Create a free account and an API key at [dashboard.dataguru.cc](https://dashboard.dataguru.cc).
2. Install and run:

```bash
git clone https://github.com/dataguru-cc/tiktok-scraper-api.git
cd tiktok-scraper-api
pip install -r requirements.txt
export DATAGURU_API_KEY="your key"
python examples/sdk_example.py tiktok-post
```

## Examples

Every example covers all 4 TikTok APIs. Pass an API name to run just one; with no name each script runs them all, and each call is billed at the price above.

| File | Style | Run |
| --- | --- | --- |
| [`examples/sdk_example.py`](examples/sdk_example.py) | [DataGuru Python SDK](https://github.com/dataguru-cc/dataguru-python) (`pip install dataguru-sdk`), one function per API, saves JSON to `output/` | `python examples/sdk_example.py` |
| [`examples/requests_example.py`](examples/requests_example.py) | Plain `requests`, synchronous | `python examples/requests_example.py` |
| [`examples/async_example.py`](examples/async_example.py) | `asyncio` + `httpx`, concurrent with a limit | `python examples/async_example.py` |
| [`examples/scrapy_spider.py`](examples/scrapy_spider.py) | Scrapy spider, items to JSON/CSV | `scrapy runspider examples/scrapy_spider.py -O tiktok.json` |

All requests use the header `Authorization: Api-Key YOUR_API_KEY`. Errors return `{"success": false, "error": {"code", "message", "request_id"}}`, with HTTP 402 when the balance runs out and 429 (with `Retry-After`) when rate limited. Failed requests are not charged.

## API reference

### TikTok Post

Get details of a public TikTok post/video: caption, creator, video download links, music, views, likes, shares and bookmarks.

- Endpoint: `POST https://api.dataguru.cc/api/v1/tiktok/post`
- Price: $0.0009 per successful request ($0.90 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/tiktok-post/
- Documentation: https://dataguru.cc/documentation/tiktok-post/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `post_url` | string | yes | Public TikTok post or video URL, e.g. https://www.tiktok.com/@tiktok/video/7299103344556677 |

**Response fields:** `id`, `canonical_url`, `description`, `created_at`, `created_at_unix`, `schedule_time`, `location_created`, `index_enabled`, `text_language`, `is_advertisement`, `is_ai_generated_content`, `ai_generated_content_description`, `secret`, `private_item`, `for_friend`, `original_item`, `official_item`, `take_down`, `digged`, `collected`, `duet_enabled`, `stitch_enabled`, `item_comment_status`, `backend_type`, `content_desc`, `is_content_classified`, `content_classification_reason`, `stats`, `author`, `videos_and_audio`, `video`, `music`, `repost`, `hashtags`, `mentions`, `stickers_on_item`, `effect_stickers`, `anchors`, `warn_info`, `app_context`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/tiktok/post" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"post_url": "https://www.tiktok.com/@khaby.lame/video/7681719358225239326"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "id": "1234567890",
  "canonical_url": "https://example.com/...",
  "description": "string",
  "created_at": "2026-01-01T12:00:00Z",
  "created_at_unix": 0,
  "schedule_time": 0,
  "location_created": "string",
  "index_enabled": false,
  "text_language": "string",
  "is_advertisement": false,
  "is_ai_generated_content": false,
  "ai_generated_content_description": "string",
  "secret": false,
  "private_item": false,
  "for_friend": false,
  "original_item": false,
  "official_item": false,
  "take_down": 0,
  "digged": false,
  "collected": false,
  "duet_enabled": false,
  "stitch_enabled": false,
  "item_comment_status": 0,
  "backend_type": "string",
  "content_desc": "string",
  "is_content_classified": false,
  "content_classification_reason": "string",
  "stats": {
    "likes": 0,
    "comments": 0,
    "shares": 0,
    "plays": 0,
    "bookmarks": 0,
    "reposts": 0
  },
  "author": {
    "id": "1234567890",
    "username": "string",
    "nickname": "string",
    "signature": "string",
    "avatar": "string",
    "verified": false,
    "secret": false,
    "private_account": false,
    "open_favorite": false,
    "comment_setting": 0,
    "duet_setting": 0,
    "stitch_setting": 0,
    "room_id": "1234567890",
    "unique_id_modify_time": 0,
    "nickname_modify_time": 0,
    "created_at": "2026-01-01T12:00:00Z",
    "created_at_unix": 0,
    "stats": {
      "followers": 0,
      "following": 0,
      "likes": 0,
      "videos": 0,
      "digg_count": 0,
      "friends": 0
    }
  },
  "videos_and_audio": {
    "video_id": "1234567890",
    "video_url": "https://example.com/...",
    "music_id": "1234567890",
    "music_title": "string",
    "music_author": "string",
    "music_url": "https://example.com/...",
    "duration": 0,
    "cover_image_url": "https://example.com/...",
    "dynamic_cover_url": "https://example.com/...",
    "download_url": "https://example.com/...",
    "play_url": "https://example.com/..."
  },
  "video": {
    "id": "1234567890",
    "height": 0,
    "width": 0,
    "duration": 0,
    "ratio": "string",
    "cover": "string",
    "origin_cover": "string",
    "dynamic_cover": "string",
    "play_url": "https://example.com/...",
    "download_url": "https://example.com/...",
    "format": "string",
    "bitrate": 0,
    "codec_type": "string",
    "definition": "string",
    "volume_info": {
      "loudness": 0.0,
      "peak": 0.0
    }
  },
  "music": {
    "id": "1234567890",
    "title": "string",
    "author": "string",
    "album": "string",
    "duration": 0,
    "cover": "string",
    "play_url": "https://example.com/...",
    "original": false,
    "precise_duration": {
      "precise_duration": 0.0,
      "precise_shoot_duration": 0.0,
      "precise_audition_duration": 0.0,
      "precise_video_duration": 0.0
    }
  },
  "repost": {
    "can_repost": false
  },
  "hashtags": [
    {
      "id": "1234567890",
      "title": "string",
      "url": "https://example.com/..."
    }
  ],
  "mentions": [
    {
      "id": "1234567890",
      "username": "string",
      "security_user_id": "1234567890"
    }
  ],
  "stickers_on_item": [
    {
      "stickerText": [
        "string"
      ],
      "stickerType": 0
    }
  ],
  "effect_stickers": [
    "string"
  ],
  "anchors": [
    "string"
  ],
  "warn_info": [
    "string"
  ],
  "app_context": {
    "language": "string",
    "region": "string",
    "request_id": "1234567890",
    "cluster_region": "string"
  },
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "TikTok Post",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### TikTok Profile

Get a public TikTok profile: username, name, bio, follower and following counts, likes, verification, stats and profile photo.

- Endpoint: `POST https://api.dataguru.cc/api/v1/tiktok/profile`
- Price: $0.0009 per successful request ($0.90 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/tiktok-profile/
- Documentation: https://dataguru.cc/documentation/tiktok-profile/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile_url` | string | yes | Public TikTok profile URL or username, e.g. https://www.tiktok.com/@tiktok |

**Response fields:** `id`, `short_id`, `username`, `nickname`, `profile_url`, `bio`, `security_user_id`, `avatar`, `verified`, `private_account`, `is_secret`, `is_commerce_account`, `commerce_category`, `is_seller`, `is_organization`, `is_ad_virtual`, `is_embed_banned`, `ftc`, `bio_link`, `region`, `language`, `created_at`, `created_at_iso`, `username_last_changed_at`, `nickname_last_changed_at`, `followers`, `following`, `likes`, `video_count`, `digg_count`, `friend_count`, `duet_setting`, `stitch_setting`, `comment_setting`, `download_setting`, `following_visibility`, `open_favorite`, `relation`, `profile_tabs`, `is_live`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/tiktok/profile" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"profile_url": "https://www.tiktok.com/@tiktok"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "id": "1234567890",
  "short_id": "1234567890",
  "username": "string",
  "nickname": "string",
  "profile_url": "https://example.com/...",
  "bio": "string",
  "security_user_id": "1234567890",
  "avatar": "string",
  "verified": false,
  "private_account": false,
  "is_secret": false,
  "is_commerce_account": false,
  "commerce_category": "string",
  "is_seller": false,
  "is_organization": false,
  "is_ad_virtual": false,
  "is_embed_banned": false,
  "ftc": false,
  "bio_link": "https://example.com/...",
  "region": "string",
  "language": "string",
  "created_at": 0,
  "created_at_iso": "string",
  "username_last_changed_at": 0,
  "nickname_last_changed_at": 0,
  "followers": 0,
  "following": 0,
  "likes": 0,
  "video_count": 0,
  "digg_count": 0,
  "friend_count": 0,
  "duet_setting": 0,
  "stitch_setting": 0,
  "comment_setting": 0,
  "download_setting": 0,
  "following_visibility": 0,
  "open_favorite": false,
  "relation": 0,
  "profile_tabs": {
    "music": false,
    "questions": false,
    "playlists": false,
    "can_expand_playlist": false
  },
  "is_live": false,
  "room_id": "1234567890",
  "recommend_reason": "string",
  "canonical_url": "https://example.com/...",
  "share_title": "string",
  "share_description": "string",
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "TikTok Profile",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### TikTok Search

Search TikTok for videos by keyword or hashtag with metrics, music details, and media URLs.

- Endpoint: `POST https://api.dataguru.cc/api/v1/tiktok/search`
- Price: $0.0009 per successful request ($0.90 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/tiktok-search/
- Documentation: https://dataguru.cc/documentation/tiktok-search/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | no | Number of video results to return. Default: `5`. |
| `query` | string | yes | Search keyword, hashtag or search URL (e.g. cooking or |

**Response fields:** `query`, `search_url`, `total_results`, `results`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/tiktok/search" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "cooking"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "tiktok_search": {
    "query": "string",
    "search_url": "https://example.com/...",
    "total_results": 0,
    "results": [
      {
        "video_id": "1234567890",
        "video_url": "https://example.com/...",
        "description": "string",
        "created_at": "2026-01-01T12:00:00Z",
        "music_id": "1234567890",
        "music_title": "string",
        "music_author": "string",
        "music_url": "https://example.com/...",
        "duration": 0,
        "cover_image_url": "https://example.com/...",
        "dynamic_cover_url": "https://example.com/...",
        "download_url": "https://example.com/...",
        "play_url": "https://example.com/...",
        "view_count": 0,
        "like_count": 0,
        "comment_count": 0,
        "share_count": 0,
        "collect_save_count": 0
      }
    ]
  },
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "TikTok Search",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### TikTok Shop

Scrape TikTok Shop product details, sale price, sales count, creator commission rate and seller profile.

- Endpoint: `POST https://api.dataguru.cc/api/v1/tiktok/shop`
- Price: $0.0009 per successful request ($0.90 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/tiktok-shop/
- Documentation: https://dataguru.cc/documentation/tiktok-shop/

This API needs a real input value: replace the placeholder in the examples, then run it by name.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `product_url` | string | yes | TikTok Shop product URL or ID (e.g. https://shop.tiktok.com/view/product/1728493011) |

**Response fields:** `product_id`, `product_title`, `flash_sale_price`, `currency`, `total_sold_units`, `commission_rate_for_creators_pct`, `shop_seller_profile`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/tiktok/shop" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://shop.tiktok.com/view/product/<product-id>"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "tiktok_shop": {
    "product_id": "1234567890",
    "product_title": "string",
    "flash_sale_price": 0.0,
    "currency": "USD",
    "total_sold_units": 0,
    "commission_rate_for_creators_pct": 0.0,
    "shop_seller_profile": {
      "seller_name": "string",
      "seller_id": "1234567890"
    }
  },
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "TikTok Shop",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

## More

- Python SDK and examples for all DataGuru APIs: [github.com/dataguru-cc/dataguru-python](https://github.com/dataguru-cc/dataguru-python) ([docs](https://dataguru-python.readthedocs.io/))
- Every API, with a live playground: [https://dataguru.cc/apis/](https://dataguru.cc/apis/)
- Use DataGuru from Claude, ChatGPT or Cursor through the MCP server: [https://dataguru.cc/mcp/](https://dataguru.cc/mcp/)
- Run thousands of inputs from a CSV at half price with batch jobs: [https://dataguru.cc/documentation/](https://dataguru.cc/documentation/)
- Other scraper APIs: [1688](https://github.com/dataguru-cc/1688-scraper-api), [Airbnb](https://github.com/dataguru-cc/airbnb-scraper-api), [Alibaba](https://github.com/dataguru-cc/alibaba-scraper-api), [AliExpress](https://github.com/dataguru-cc/aliexpress-scraper-api), [Amazon](https://github.com/dataguru-cc/amazon-scraper-api), [arXiv](https://github.com/dataguru-cc/arxiv-scraper-api), [ASOS](https://github.com/dataguru-cc/asos-scraper-api), [Best Buy](https://github.com/dataguru-cc/best-buy-scraper-api), [Booking.com](https://github.com/dataguru-cc/booking-scraper-api), [Brave Search](https://github.com/dataguru-cc/brave-search-scraper-api), [CA State Bar](https://github.com/dataguru-cc/california-state-bar-scraper-api), [Capterra](https://github.com/dataguru-cc/capterra-scraper-api), [CoinGecko](https://github.com/dataguru-cc/coingecko-scraper-api), [CoinMarketCap](https://github.com/dataguru-cc/coinmarketcap-scraper-api), [Companies House](https://github.com/dataguru-cc/companies-house-scraper-api), [Costco](https://github.com/dataguru-cc/costco-scraper-api), [CourtListener](https://github.com/dataguru-cc/courtlistener-scraper-api), [Crunchbase](https://github.com/dataguru-cc/crunchbase-scraper-api), [Discord](https://github.com/dataguru-cc/discord-scraper-api), [DoorDash](https://github.com/dataguru-cc/doordash-scraper-api), [eBay](https://github.com/dataguru-cc/ebay-scraper-api), [Etsy](https://github.com/dataguru-cc/etsy-scraper-api), [Expedia](https://github.com/dataguru-cc/expedia-scraper-api), [Fiverr](https://github.com/dataguru-cc/fiverr-scraper-api), [Flipkart](https://github.com/dataguru-cc/flipkart-scraper-api), [Glassdoor](https://github.com/dataguru-cc/glassdoor-scraper-api), [Google Flights](https://github.com/dataguru-cc/google-flights-scraper-api), [Google Patents](https://github.com/dataguru-cc/google-patents-scraper-api), [Google Scholar](https://github.com/dataguru-cc/google-scholar-scraper-api), [Google Search](https://github.com/dataguru-cc/google-search-scraper-api), [Grubhub](https://github.com/dataguru-cc/grubhub-scraper-api), [Home Depot](https://github.com/dataguru-cc/home-depot-scraper-api), [Instagram](https://github.com/dataguru-cc/instagram-scraper-api), [Investing.com](https://github.com/dataguru-cc/investing-com-scraper-api), [Justia](https://github.com/dataguru-cc/justia-scraper-api), [Kayak](https://github.com/dataguru-cc/kayak-scraper-api), [Kick](https://github.com/dataguru-cc/kick-scraper-api), [Lazada](https://github.com/dataguru-cc/lazada-scraper-api), [MarketWatch](https://github.com/dataguru-cc/marketwatch-scraper-api), [Mercado Libre](https://github.com/dataguru-cc/mercado-libre-scraper-api), [Monster](https://github.com/dataguru-cc/monster-scraper-api), [OpenCorporates](https://github.com/dataguru-cc/opencorporates-scraper-api), [OpenTable](https://github.com/dataguru-cc/opentable-scraper-api), [PACER](https://github.com/dataguru-cc/pacer-scraper-api), [PitchBook](https://github.com/dataguru-cc/pitchbook-scraper-api), [PubMed](https://github.com/dataguru-cc/pubmed-scraper-api), [Reddit](https://github.com/dataguru-cc/reddit-scraper-api), [Redfin](https://github.com/dataguru-cc/redfin-scraper-api), [Resy](https://github.com/dataguru-cc/resy-scraper-api), [Rightmove](https://github.com/dataguru-cc/rightmove-scraper-api), [SEC EDGAR](https://github.com/dataguru-cc/sec-edgar-scraper-api), [Seeking Alpha](https://github.com/dataguru-cc/seeking-alpha-scraper-api), [Shopee](https://github.com/dataguru-cc/shopee-scraper-api), [Skyscanner](https://github.com/dataguru-cc/skyscanner-scraper-api), [Target](https://github.com/dataguru-cc/target-scraper-api), [TradingView](https://github.com/dataguru-cc/tradingview-scraper-api), [TripAdvisor](https://github.com/dataguru-cc/tripadvisor-scraper-api), [Trulia](https://github.com/dataguru-cc/trulia-scraper-api), [TrustRadius](https://github.com/dataguru-cc/trustradius-scraper-api), [Twitch](https://github.com/dataguru-cc/twitch-scraper-api), [Uber Eats](https://github.com/dataguru-cc/uber-eats-scraper-api), [Upwork](https://github.com/dataguru-cc/upwork-scraper-api), [Vrbo](https://github.com/dataguru-cc/vrbo-scraper-api), [Walmart](https://github.com/dataguru-cc/walmart-scraper-api), [Wayfair](https://github.com/dataguru-cc/wayfair-scraper-api), [X (Twitter)](https://github.com/dataguru-cc/twitter-scraper-api), [Yahoo Finance](https://github.com/dataguru-cc/yahoo-finance-scraper-api), [YouTube](https://github.com/dataguru-cc/youtube-scraper-api), [Zillow](https://github.com/dataguru-cc/zillow-scraper-api), [ZoomInfo](https://github.com/dataguru-cc/zoominfo-scraper-api), [Zoopla](https://github.com/dataguru-cc/zoopla-scraper-api)

## License

The example code is MIT licensed. Use of the DataGuru API is subject to the [terms of service](https://dataguru.cc/terms/).
