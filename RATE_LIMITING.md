# Rate Limiting Documentation

## Overview

Lucida Flow implements robust rate limiting to ensure we **never exceed Lucida.to's request limits** and maintain good citizenship with their service.

## Rate Limiting Features

### 1. **Multi-Level Limits**

```python
- Per-Minute Limit: 30 requests
- Per-Hour Limit: 500 requests
- Minimum Delay: 2.0 seconds between requests
```

### 2. **Sliding Window Algorithm**

Instead of simple fixed-window limiting, we use a **sliding window** that tracks the exact timestamp of each request. This means:

- ✅ More accurate limit enforcement
- ✅ No sudden bursts at window boundaries
- ✅ Smooth, predictable request patterns

### 3. **Exponential Backoff**

When errors occur (500 errors, timeouts, etc.):

```
Error #1: Wait 2 seconds
Error #2: Wait 4 seconds
Error #3: Wait 8 seconds
Error #4: Wait 16 seconds
...up to 300 seconds (5 minutes)
```

### 4. **429 Response Handling**

If Lucida.to returns a `429 Too Many Requests`:

- Automatically honors `Retry-After` header
- Falls back to 60-second wait if header missing
- Increments error counter for backoff

## CLI Commands

### View Rate Limit Stats

```bash
python cli.py stats
```

Shows:

- Requests in last minute
- Requests in last hour
- Total tracked requests
- Consecutive errors
- Configured limits

### Example Output

```
Rate Limiter Statistics:

          Request Stats
┌────────────────────────┬───────┐
│ Metric                 │ Value │
├────────────────────────┼───────┤
│ Requests (last minute) │ 5     │
│ Requests (last hour)   │ 23    │
│ Total tracked requests │ 23    │
│ Consecutive errors     │ 0     │
└────────────────────────┴───────┘

          Rate Limits
┌─────────────────────┬───────┐
│ Limit Type          │ Value │
├─────────────────────┼───────┤
│ Per minute          │ 30    │
│ Per hour            │ 500   │
│ Min delay (seconds) │ 2.0   │
└─────────────────────┴───────┘
```

## Custom Configuration

### Via Python API

```python
from lucida_client import LucidaClient

# More conservative limits
client = LucidaClient(
    requests_per_minute=20,  # Lower limit
    requests_per_hour=300,   # Lower limit
)

# More aggressive (not recommended)
client = LucidaClient(
    requests_per_minute=60,
    requests_per_hour=1000,
)
```

### Via Environment Variables

Create a `.env` file:

```env
LUCIDA_REQUESTS_PER_MINUTE=30
LUCIDA_REQUESTS_PER_HOUR=500
LUCIDA_MIN_DELAY=2.0
```

## How It Works

### Request Flow

```
1. User calls search/download/info
   ↓
2. _rate_limit() is called
   ↓
3. RateLimiter checks:
   - Time since last request
   - Requests in last minute
   - Requests in last hour
   - Consecutive error count
   ↓
4. If needed, waits appropriate time
   ↓
5. Request proceeds
   ↓
6. Response handled:
   - Success: Reset error counter
   - 429: Honor Retry-After
   - 500+: Increment error counter
```

### Sliding Window Implementation

```python
# Track all request timestamps
request_times = deque(maxlen=500)  # Last 500 requests

# Check last minute
one_minute_ago = current_time - 60
recent = sum(1 for t in request_times if t > one_minute_ago)

# If at limit, wait for oldest to expire
if recent >= 30:
    oldest = min(t for t in request_times if t > one_minute_ago)
    wait_time = 60 - (current_time - oldest) + 1
    time.sleep(wait_time)
```

## Best Practices

### ✅ DO

- Use the CLI for normal usage (rate limiting automatic)
- Check stats with `python cli.py stats` if concerned
- Trust the rate limiter - it will wait when needed
- Use search filters to reduce unnecessary requests

### ❌ DON'T

- Try to bypass rate limiting
- Make parallel requests from multiple processes
- Set very aggressive limits (respect the service)
- Retry failed requests manually (exponential backoff handles it)

## Troubleshooting

### "Rate limit: waiting Xs" messages

**Normal!** This means the rate limiter is working correctly. The system will automatically wait and retry.

### Consecutive errors increasing

Check:

1. Network connection
2. Lucida.to service status
3. Whether you're being rate limited

Use `python cli.py stats` to monitor.

### Requests seem slow

This is intentional! The 2-second minimum delay ensures:

- We never overwhelm Lucida.to
- More reliable long-term access
- Good citizenship with shared resources

## Technical Details

### Memory Usage

The rate limiter tracks up to 500 request timestamps (about 4KB of memory). Old timestamps are automatically discarded.

### Thread Safety

**Not thread-safe by default.** If using multiple threads, create one `LucidaClient` instance per thread or add your own locking.

### Precision

Uses `time.time()` with microsecond precision for accurate rate limiting.

## Examples

### Check if safe to make request

```python
client = LucidaClient()
stats = client.get_rate_limit_stats()

if stats['requests_last_minute'] < 25:
    # Safe to make request
    client.search("query", "amazon_music")
else:
    print("Close to minute limit, waiting...")
```

### Monitor during batch operations

```python
client = LucidaClient()

for query in large_query_list:
    result = client.search(query, "amazon_music")

    # Check stats periodically
    if query_index % 10 == 0:
        stats = client.get_rate_limit_stats()
        print(f"Progress: {stats['requests_last_hour']}/500 hourly")
```

## Summary

The rate limiting system ensures **100% compliance** with Lucida.to's limits through:

1. ✅ Multi-level rate limiting (minute, hour)
2. ✅ Sliding window algorithm (accurate tracking)
3. ✅ Minimum 2-second delays (prevents bursts)
4. ✅ Exponential backoff (handles errors gracefully)
5. ✅ 429 response handling (respects server limits)
6. ✅ Request tracking (full visibility)

**You cannot exceed the limits** - the system will automatically wait as needed.
