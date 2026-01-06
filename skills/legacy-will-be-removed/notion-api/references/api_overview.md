# Notion API Overview

## Base URL and Conventions

**Base URL:** `https://api.notion.com`

All API requests must use HTTPS. The API follows RESTful conventions with GET, POST, PATCH, and DELETE operations.

### JSON Conventions

- All resources have an `"object"` property indicating the resource type (e.g., "database", "page", "user")
- Resources are addressable by UUIDv4 `"id"` (dashes in IDs are optional when making requests)
- Property names use `snake_case` (not camelCase or kebab-case)
- Temporal values use ISO 8601 format:
  - Datetimes include time: `2020-08-12T02:12:33.231Z`
  - Dates are date-only: `2020-08-12`
- The API does not support empty strings - use `null` instead

### Required Headers

All API requests must include:
- `Authorization: Bearer {TOKEN}` - Your integration token or OAuth access token
- `Notion-Version: 2022-06-28` - API version (use latest version from docs)
- `Content-Type: application/json` - For POST/PATCH requests

Example curl request:
```bash
curl 'https://api.notion.com/v1/users' \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
```

## Authentication

### Internal Integrations

Internal integrations are workspace-specific and use a single integration token:
1. Create integration at https://www.notion.so/profile/integrations
2. Copy the integration token from the Configuration tab
3. **Important:** Share specific pages/databases with the integration via the "Add connections" menu (••• menu → Add connections)
4. Include the token in all API requests

**Keep tokens secret!** Never commit tokens to source control - use environment variables.

### Public Integrations (OAuth 2.0)

Public integrations work across any workspace using OAuth 2.0:

**Setup:**
1. Create public integration in dashboard (select "Public" type)
2. Set redirect URI(s) in integration settings
3. Note your `client_id` and `client_secret`

**Authorization Flow:**
1. Direct user to authorization URL (format: `https://api.notion.com/v1/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&owner=user`)
2. User authorizes and selects pages to share
3. Notion redirects to your `redirect_uri` with a `code` parameter
4. Exchange code for access_token via POST to `https://api.notion.com/v1/oauth/token`:
   - Use HTTP Basic Auth: base64-encode `{client_id}:{client_secret}`
   - Body: `{"grant_type": "authorization_code", "code": "{CODE}", "redirect_uri": "{REDIRECT_URI}"}`
5. Store the returned `access_token` and `refresh_token`

**Refreshing tokens:**
```bash
POST /v1/oauth/token
Authorization: Basic {base64(client_id:client_secret)}
Content-Type: application/json

{"grant_type": "refresh_token", "refresh_token": "{REFRESH_TOKEN}"}
```

### Integration Capabilities

Integrations can have granular capabilities that control what they can do:
- **Read content** - View pages and databases
- **Update content** - Modify pages and databases  
- **Insert content** - Create new pages and databases
- **Read user information** - Access user data
- **Read comments** - View comments
- **Insert comments** - Add comments

Configure capabilities in integration settings. Public integrations show capabilities during OAuth authorization.

## Pagination

Endpoints returning lists support cursor-based pagination (default: 10 items, max: 100 per page).

### Paginated Response Structure
```json
{
  "object": "list",
  "results": [...],  // Array of objects
  "has_more": true,  // Whether more results exist
  "next_cursor": "abc123",  // Use this for next page
  "type": "block"  // Result type
}
```

### Paginated Endpoints
- GET `/v1/blocks/{block_id}/children`
- GET `/v1/comments`
- GET `/v1/databases/{database_id}/query` (POST)
- POST `/v1/search`
- GET `/v1/pages/{page_id}/properties/{property_id}`

### Request Parameters
- **GET requests:** Add `?page_size=100&start_cursor={cursor}` to query string
- **POST requests:** Include `{"page_size": 100, "start_cursor": "{cursor}"}` in body

### Pagination Example
```javascript
let hasMore = true;
let startCursor = undefined;
const allResults = [];

while (hasMore) {
  const response = await notion.databases.query({
    database_id: databaseId,
    start_cursor: startCursor,
    page_size: 100
  });
  
  allResults.push(...response.results);
  hasMore = response.has_more;
  startCursor = response.next_cursor;
}
```

## Rate Limits

The Notion API implements rate limiting. When rate limits are exceeded:
- Status code: `429 Too Many Requests`
- Response includes `retry-after` header (seconds until retry)

Best practices:
- Implement exponential backoff
- Use asynchronous operations (job queues) for large operations
- Cache responses when appropriate
- Batch operations when possible

## Common Error Codes

- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Integration lacks required capabilities or page access
- `404 Not Found` - Resource doesn't exist or integration lacks access
- `429 Too Many Requests` - Rate limit exceeded
- `500/502/503/504` - Notion server errors (retry with exponential backoff)

**Note:** A 404 can mean either the resource doesn't exist OR your integration doesn't have access to it. Always verify pages/databases are shared with your integration.

## Size Limits

- **Blocks:** Maximum ~2000 characters per block
- **API Request:** Maximum ~100 blocks per request
- **Database Schema:** Recommended maximum 50KB
- **File Uploads:** 
  - Free workspaces: Limited per file size
  - Paid workspaces: 5 GiB per file
  - Files >20 MiB must use multi-part upload
- **Filename length:** Maximum 900 bytes (including extension)

## Notion SDK

Official JavaScript SDK available: `@notionhq/client`

```javascript
const { Client } = require('@notionhq/client');
const notion = new Client({ auth: process.env.NOTION_API_KEY });

// SDK handles headers and token automatically
const response = await notion.pages.create({
  parent: { page_id: 'xxx' },
  properties: { title: { title: [{ text: { content: 'My Page' } }] } }
});
```

The SDK is recommended as it handles authentication, versioning, and provides TypeScript types.
