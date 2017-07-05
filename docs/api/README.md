# WEB API Reference

Use `httpie` to test all Web APIs

https://github.com/jakubroztocil/httpie

### Crawler

```bash
make run_crawler
```

#### GET A news article

```bash
http http://0.0.0.0:9527 url==[news page]
```

### NewsFeed

```bash
make run_newsfeed
```

#### GET News articles from a RSS/Atom feed

```bash
http http://0.0.0.0:9528 url==[feed xml] fulltext==true include==[keyword]
```

### FbFeed

```bash
make run_fbfeed
```

#### GET Facebook posts by fbid

```bash
http http://0.0.0.0:9529 fbid==[facebook id or name] search==true include==[keyword] num==20
```

### Archiver

```bash
make run_news_archiver
```

#### GET News archives with keywords

```bash
http http://0.0.0.0:9530/api/v1/archive/news/list include==[keyword]
```

#### GET A news archive by hashid

```bash
http http://0.0.0.0:9530/api/v1/archive/news/<hashid> 
```

#### GET Facebook archives with keywords

```bash
http http://0.0.0.0:9530/api/v1/archive/facebook/list include==[keyword]
```

#### GET A facebook archive by hashid

```bash
http http://0.0.0.0:9530/api/v1/archive/facebook/<hashid> 
```