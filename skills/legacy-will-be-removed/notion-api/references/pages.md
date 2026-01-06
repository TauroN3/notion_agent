# Working with Pages

## Page Overview

Pages are the fundamental content units in Notion where users write notes, documents, and landing pages. Each page has:
- **Properties:** Structured metadata (title, dates, relations, etc.)
- **Content:** Free-form blocks (paragraphs, headers, lists, images, etc.)

**Key concept:** Page properties are best for structured data (dates, categories, relationships). Page content is best for free-form writing and storytelling.

## Page Object Structure

```json
{
  "object": "page",
  "id": "59833787-2cf9-4fdf-8782-e53db20768a5",
  "created_time": "2022-03-01T19:05:00.000Z",
  "last_edited_time": "2022-03-01T19:05:00.000Z",
  "created_by": { "object": "user", "id": "..." },
  "last_edited_by": { "object": "user", "id": "..." },
  "cover": { 
    "type": "external",
    "external": { "url": "https://example.com/cover.jpg" }
  },
  "icon": {
    "type": "emoji",
    "emoji": "📄"
  },
  "parent": {
    "type": "database_id",
    "database_id": "xxx"
  },
  "archived": false,
  "in_trash": false,
  "properties": {
    "Name": {
      "id": "title",
      "type": "title",
      "title": [{ "type": "text", "text": { "content": "My Page" } }]
    }
  },
  "url": "https://www.notion.so/My-Page-xxx"
}
```

### Parent Types

A page can be a child of:
1. **Database:** `{"type": "database_id", "database_id": "{uuid}"}`
2. **Page:** `{"type": "page_id", "page_id": "{uuid}"}`
3. **Workspace:** `{"type": "workspace", "workspace": true}`

## Finding Page IDs

### From Notion URL
1. Open page in Notion
2. Use Share menu → Copy link
3. Extract ID from URL format: `https://www.notion.so/Page-Title-{PAGE_ID}?v=...`
4. Format: 32-character string, can add hyphens in pattern 8-4-4-4-12

### Via API
- Use Search endpoint to find pages by title
- Use Query Database endpoint if page is in a database
- Store IDs when creating pages programmatically

## API Endpoints

### Create a Page

**POST** `/v1/pages`

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "parent": { "page_id": "xxx" },
    "properties": {
      "title": {
        "title": [{ "type": "text", "text": { "content": "My New Page" } }]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{ 
            "type": "text", 
            "text": { "content": "Page content goes here" } 
          }]
        }
      }
    ]
  }'
```

**Parameters:**
- `parent` (required) - Page, database, or workspace parent
- `properties` (required) - Page properties matching parent's schema
- `children` (optional) - Array of block objects for initial content
- `icon` (optional) - Emoji or external file icon
- `cover` (optional) - External or uploaded cover image

**Response:** Returns the created page object with ID

### Retrieve a Page

**GET** `/v1/pages/{page_id}`

```bash
curl https://api.notion.com/v1/pages/xxx \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
```

Returns the page object with properties. To get the page content (blocks), use the "Retrieve block children" endpoint with the page ID.

### Update Page Properties

**PATCH** `/v1/pages/{page_id}`

```bash
curl -X PATCH https://api.notion.com/v1/pages/xxx \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "properties": {
      "Name": {
        "title": [{ "type": "text", "text": { "content": "Updated Title" } }]
      }
    },
    "archived": false
  }'
```

**Updatable fields:**
- `properties` - Update specific properties (see property values reference)
- `icon` - Change emoji or icon
- `cover` - Change cover image
- `archived` - Archive (true) or unarchive (false) the page

**Note:** To update page content (blocks), use block endpoints.

### Archive a Page

```json
{
  "archived": true
}
```

Use PATCH endpoint to set `archived: true`. Archived pages can be restored by setting `archived: false`.

## Page Properties

When creating/updating pages, properties must match the parent's schema:

### Standalone Pages (page parent)
Only `title` property is allowed:
```json
{
  "properties": {
    "title": {
      "title": [{ "type": "text", "text": { "content": "Page Title" } }]
    }
  }
}
```

### Database Pages
Properties must conform to database schema. See the properties reference for all property types.

## Page Content (Blocks)

Page content is represented as child blocks. See blocks reference for details.

**To read page content:**
```bash
GET /v1/blocks/{page_id}/children
```

**To add content:**
```bash
PATCH /v1/blocks/{page_id}/children
```

Pages are themselves blocks, so you can use the page ID as a block ID in block endpoints.

## Icons and Covers

### Icons
Two types supported:
1. **Emoji:** `{"type": "emoji", "emoji": "📄"}`
2. **External file:** `{"type": "external", "external": {"url": "https://..."}}`
3. **Uploaded file:** `{"type": "file", "file": {"url": "...", "expiry_time": "..."}}`

### Covers
Same format as icons. Cover images are displayed at the top of the page.

## Common Use Cases

### Create a Simple Page with Content

```javascript
const response = await notion.pages.create({
  parent: { page_id: 'parent-page-id' },
  properties: {
    title: {
      title: [{ type: 'text', text: { content: 'Meeting Notes' } }]
    }
  },
  children: [
    {
      object: 'block',
      type: 'heading_1',
      heading_1: {
        rich_text: [{ type: 'text', text: { content: 'Agenda' } }]
      }
    },
    {
      object: 'block',
      type: 'bulleted_list_item',
      bulleted_list_item: {
        rich_text: [{ type: 'text', text: { content: 'Review Q4 goals' } }]
      }
    }
  ]
});
```

### Add Page to Database

```javascript
const response = await notion.pages.create({
  parent: { database_id: 'database-id' },
  properties: {
    'Name': {  // Match database property names
      title: [{ type: 'text', text: { content: 'Task Name' } }]
    },
    'Status': {
      select: { name: 'In Progress' }
    },
    'Due Date': {
      date: { start: '2024-12-31' }
    }
  }
});
```

### Update Multiple Properties

```javascript
await notion.pages.update({
  page_id: 'page-id',
  properties: {
    'Status': { select: { name: 'Done' } },
    'Completed Date': { date: { start: '2024-11-05' } }
  }
});
```

### Get Page with All Content

```javascript
// 1. Get page properties
const page = await notion.pages.retrieve({ page_id: 'xxx' });

// 2. Get page content (blocks)
const blocks = await notion.blocks.children.list({ block_id: 'xxx' });

// 3. Recursively get nested blocks if needed
for (const block of blocks.results) {
  if (block.has_children) {
    const children = await notion.blocks.children.list({ 
      block_id: block.id 
    });
    // Process children...
  }
}
```

## Best Practices

1. **Permissions:** Always share pages with your integration before API access (use "Add connections" in Notion UI)
2. **Store IDs:** Save page IDs when creating pages for future updates
3. **Batch Operations:** Create pages with initial content in one request when possible
4. **Handle 404s:** Could mean page doesn't exist OR integration lacks access
5. **Rich Text:** Use proper rich text format for all text content (see rich text reference)
6. **Recursive Content:** Page content may be deeply nested - use recursive functions to traverse all blocks

## Page Property Item Retrieval

For paginated properties (like rollup results), use:

**GET** `/v1/pages/{page_id}/properties/{property_id}`

This is necessary when property values are too large to fit in the page object response. The response is paginated if the property has many items.
