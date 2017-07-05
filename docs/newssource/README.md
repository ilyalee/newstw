# Add a News source by Example (Mirror Media)

https://www.mirrormedia.mg

### Tips and Step-by-step guide

1. edit `config/lang/zh_tw.cfg`, append the translaton: `mirrormedia: 鏡週刊` to the end of file.

2. edit `config/feeds.cfg`, append the RSS feed: `mirrormedia: https://www.mirrormedia.mg/rss/rss.xml` to the `[Electronic media]` section.

3. edit `crawler/web_shape_var.py`, append code below to the file:

```python3
source['mirrormedia'] = [
    "mirrormedia.mg"
]
context['mirrormedia'] = [
    {'save': "title", 'path': ".article_title > h1", 'ind': 0},
    {'save': "summary", 'path': "article", 'ind': 0},
    {'save': "_rawtime", 'path': ".date", 'ind': 0},
    {'tzinfo': "Asia/Taipei", 'format': "YYYY.MM.DD HH:mm"}
]
```

4. Run crawler service to fetch articles, make sure crawler is working fine.

5. Restart web and scheduler services.

6. Make sure everything is fine.

7. Done. Have a nice day.