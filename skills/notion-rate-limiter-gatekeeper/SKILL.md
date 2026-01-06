---
name: notion-rate-limiter-gatekeeper
description: "Rate limiting gatekeeper for Notion API calls. MUST be executed BEFORE every curl, bash, or tool execution that calls the Notion API (api.notion.com). Enforces Notion's rate limit of 3 requests/second average to prevent HTTP 429 errors. Triggers when making any request to api.notion.com, using Notion MCP server, or any operation involving Notion pages, databases, blocks, or comments via API."
---

# Notion Rate Limiter Gatekeeper

## Purpose

Prevent Notion API rate limiting (HTTP 429) by enforcing the documented rate limit of **3 requests per second average** with burst allowance.

## CRITICAL: Pre-Execution Requirement

**Before EVERY Notion API call**, run the gatekeeper:

```bash
python3 /path/to/scripts/notion_rate_limiter.py gate
```

This command:
1. Checks if a request is allowed
2. Waits automatically if rate limit would be exceeded
3. Records the request timestamp

## Quick Reference

| Command | Purpose |
|---------|---------|
| `gate` | **Primary command** - Check, wait if needed, record (use before API calls) |
| `check` | Check if request allowed (exit 0=yes, 1=no) |
| `wait` | Block until request is allowed |
| `record` | Record a request was made |
| `status` | Show current rate limiter state |
| `reset` | Clear all recorded timestamps |

## Integration Patterns

### Pattern 1: Inline Before curl

```bash
python3 scripts/notion_rate_limiter.py gate && \
curl -X POST 'https://api.notion.com/v1/pages' \
  -H 'Authorization: Bearer $NOTION_TOKEN' \
  -H 'Notion-Version: 2022-06-28' \
  -d '{"parent":{"database_id":"..."}}'
```

### Pattern 2: In a Loop

```bash
for page_id in $PAGE_IDS; do
  python3 scripts/notion_rate_limiter.py gate
  curl -X GET "https://api.notion.com/v1/pages/$page_id" ...
done
```

### Pattern 3: Conditional Check

```bash
if python3 scripts/notion_rate_limiter.py check; then
  # Safe to proceed immediately
  curl ...
else
  # Need to wait - let gate handle it
  python3 scripts/notion_rate_limiter.py gate
  curl ...
fi
```

## Notion API Rate Limits (Reference)

From Notion API Documentation:

- **Rate limit**: Average of 3 requests per second per integration
- **Bursts**: Some bursts beyond average are allowed
- **Rate limited response**: HTTP 429 with `Retry-After` header
- **Size limits**:
    - Max 100 block elements per array
    - Max 500KB payload size
    - Max 2000 characters for text/URLs
    - Max 100 elements for multi-select, relations, people

## State Management

The rate limiter stores timestamps in `/tmp/notion_rate_limiter_state.json`. This persists across commands but resets on system restart.

To manually reset:
```bash
python3 scripts/notion_rate_limiter.py reset
```

## Workflow Integration

When working with Notion API:

1. **Always** run `gate` before any API call
2. **Check** `status` if debugging rate issues
3. **Reset** if starting a fresh batch operation
