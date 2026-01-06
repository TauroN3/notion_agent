# Quick Reference: Common Tasks

This guide provides quick recipes for common Notion API operations.

## Authentication & Setup

### Get Your Integration Token
1. Go to https://www.notion.so/my-integrations
2. Create or select your integration
3. Copy the "Internal Integration Token" from Configuration tab
4. Store securely in environment variable: `NOTION_API_KEY`

### Share Pages with Integration
**Before API access works, you MUST share pages/databases:**
1. Open page in Notion
2. Click ••• menu (top right)
3. Scroll to "Add connections"
4. Search and select your integration

## Finding IDs

### Get Page ID from URL
```
URL: https://www.notion.so/My-Page-abc123def456...
ID: abc123def456... (32 characters)
```

### Get Database ID from URL
```
URL: https://www.notion.so/workspace/abc123?v=def456
Database ID: abc123 (between workspace name and ?v=)
```

### Search for Page/Database by Title
```bash
curl -X POST https://api.notion.com/v1/search \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "query": "My Page Title",
    "filter": { "property": "object", "value": "page" }
  }'
```

## Database Operations

### List All Databases I Have Access To
```bash
curl -X POST https://api.notion.com/v1/search \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "filter": { "property": "object", "value": "database" }
  }'
```

### Get Database Schema
```bash
curl https://api.notion.com/v1/databases/{database_id} \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
```

Response includes `properties` object with full schema.

### Create a New Database
```javascript
const database = await notion.databases.create({
  parent: { page_id: 'parent-page-id' },
  title: [{ type: 'text', text: { content: 'My Database' } }],
  properties: {
    'Name': { title: {} },  // Required: one title property
    'Status': {
      select: {
        options: [
          { name: 'Not Started', color: 'red' },
          { name: 'Done', color: 'green' }
        ]
      }
    },
    'Due Date': { date: {} },
    'Tags': {
      multi_select: {
        options: [
          { name: 'urgent', color: 'red' },
          { name: 'bug', color: 'orange' }
        ]
      }
    }
  }
});
```

### Get All Items from Database
```javascript
const response = await notion.databases.query({
  database_id: 'database-id'
  // No filter = get all items
});

// With pagination for large databases:
let allPages = [];
let hasMore = true;
let startCursor = undefined;

while (hasMore) {
  const response = await notion.databases.query({
    database_id: 'database-id',
    start_cursor: startCursor,
    page_size: 100
  });
  allPages.push(...response.results);
  hasMore = response.has_more;
  startCursor = response.next_cursor;
}
```

### Query Database with Filters
```javascript
// Find all "In Progress" tasks
const response = await notion.databases.query({
  database_id: 'database-id',
  filter: {
    property: 'Status',
    select: { equals: 'In Progress' }
  }
});

// Find high-priority incomplete tasks
const response = await notion.databases.query({
  database_id: 'database-id',
  filter: {
    and: [
      { property: 'Status', select: { does_not_equal: 'Done' } },
      { property: 'Priority', multi_select: { contains: 'High' } }
    ]
  }
});

// Find tasks due this week
const response = await notion.databases.query({
  database_id: 'database-id',
  filter: {
    property: 'Due Date',
    date: { this_week: {} }
  }
});
```

### Query Database with Sorting
```javascript
const response = await notion.databases.query({
  database_id: 'database-id',
  sorts: [
    { property: 'Priority', direction: 'ascending' },
    { property: 'Due Date', direction: 'ascending' }
  ]
});
```

### Add Property to Existing Database
```javascript
await notion.databases.update({
  database_id: 'database-id',
  properties: {
    'New Column': { rich_text: {} }
  }
});
```

### Remove Property from Database
```javascript
await notion.databases.update({
  database_id: 'database-id',
  properties: {
    'Column to Remove': null
  }
});
```

## Page Operations

### Create a Simple Page
```javascript
const page = await notion.pages.create({
  parent: { page_id: 'parent-page-id' },
  properties: {
    title: {
      title: [{ type: 'text', text: { content: 'My Page Title' } }]
    }
  }
});
```

### Create Page with Content
```javascript
const page = await notion.pages.create({
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
    },
    {
      object: 'block',
      type: 'to_do',
      to_do: {
        rich_text: [{ type: 'text', text: { content: 'Prepare presentation' } }],
        checked: false
      }
    }
  ]
});
```

### Add Page to Database
```javascript
const page = await notion.pages.create({
  parent: { database_id: 'database-id' },
  properties: {
    'Name': {  // Must match database properties
      title: [{ type: 'text', text: { content: 'Task Name' } }]
    },
    'Status': {
      select: { name: 'In Progress' }
    },
    'Due Date': {
      date: { start: '2024-12-31' }
    },
    'Tags': {
      multi_select: [
        { name: 'urgent' },
        { name: 'bug' }
      ]
    }
  }
});
```

### Get Page Properties
```javascript
const page = await notion.pages.retrieve({
  page_id: 'page-id'
});

// Properties are in page.properties
console.log(page.properties);
```

### Update Page Properties
```javascript
await notion.pages.update({
  page_id: 'page-id',
  properties: {
    'Status': { select: { name: 'Done' } },
    'Completed': { checkbox: true },
    'Notes': {
      rich_text: [
        { type: 'text', text: { content: 'Completed ahead of schedule' } }
      ]
    }
  }
});
```

### Archive a Page
```javascript
await notion.pages.update({
  page_id: 'page-id',
  archived: true
});
```

### Restore Archived Page
```javascript
await notion.pages.update({
  page_id: 'page-id',
  archived: false
});
```

## Content Operations

### Get Page Content (All Blocks)
```javascript
// Get immediate children
const blocks = await notion.blocks.children.list({
  block_id: 'page-id',
  page_size: 100
});

// Recursively get all content including nested blocks
async function getAllBlocks(blockId) {
  let allBlocks = [];
  let hasMore = true;
  let startCursor = undefined;
  
  while (hasMore) {
    const response = await notion.blocks.children.list({
      block_id: blockId,
      start_cursor: startCursor,
      page_size: 100
    });
    
    for (const block of response.results) {
      allBlocks.push(block);
      
      if (block.has_children) {
        const children = await getAllBlocks(block.id);
        allBlocks.push(...children);
      }
    }
    
    hasMore = response.has_more;
    startCursor = response.next_cursor;
  }
  
  return allBlocks;
}

const allContent = await getAllBlocks('page-id');
```

### Add Content to Page
```javascript
await notion.blocks.children.append({
  block_id: 'page-id',
  children: [
    {
      object: 'block',
      type: 'paragraph',
      paragraph: {
        rich_text: [
          {
            type: 'text',
            text: { content: 'This is a new paragraph' }
          }
        ]
      }
    },
    {
      object: 'block',
      type: 'heading_2',
      heading_2: {
        rich_text: [
          {
            type: 'text',
            text: { content: 'New Section' }
          }
        ]
      }
    }
  ]
});
```

### Update Block Content
```javascript
// Only works for certain block types (paragraph, heading, list items, etc.)
await notion.blocks.update({
  block_id: 'block-id',
  paragraph: {
    rich_text: [
      {
        type: 'text',
        text: { content: 'Updated paragraph text' }
      }
    ]
  }
});
```

### Delete Block
```javascript
await notion.blocks.delete({
  block_id: 'block-id'
});
```

## Text Formatting

### Bold, Italic, Underline Text
```javascript
{
  type: 'text',
  text: { content: 'Formatted text' },
  annotations: {
    bold: true,
    italic: true,
    underline: true,
    strikethrough: false,
    code: false,
    color: 'default'
  }
}
```

### Colored Text
```javascript
{
  type: 'text',
  text: { content: 'Red text' },
  annotations: {
    bold: false,
    italic: false,
    underline: false,
    strikethrough: false,
    code: false,
    color: 'red'
  }
}
```

Colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`

### Text with Link
```javascript
{
  type: 'text',
  text: {
    content: 'Click here',
    link: { url: 'https://example.com' }
  },
  annotations: { /* ... */ }
}
```

### Code Inline
```javascript
{
  type: 'text',
  text: { content: 'console.log()' },
  annotations: {
    bold: false,
    italic: false,
    underline: false,
    strikethrough: false,
    code: true,  // Makes it inline code
    color: 'default'
  }
}
```

### Mention User
```javascript
{
  type: 'mention',
  mention: {
    type: 'user',
    user: { id: 'user-id' }
  }
}
```

### Mention Page
```javascript
{
  type: 'mention',
  mention: {
    type: 'page',
    page: { id: 'page-id' }
  }
}
```

## Complex Structures

### Create Nested List
```javascript
await notion.blocks.children.append({
  block_id: 'page-id',
  children: [
    {
      object: 'block',
      type: 'bulleted_list_item',
      bulleted_list_item: {
        rich_text: [{ type: 'text', text: { content: 'Parent item' } }],
        children: [
          {
            object: 'block',
            type: 'bulleted_list_item',
            bulleted_list_item: {
              rich_text: [{ type: 'text', text: { content: 'Child item 1' } }]
            }
          },
          {
            object: 'block',
            type: 'bulleted_list_item',
            bulleted_list_item: {
              rich_text: [{ type: 'text', text: { content: 'Child item 2' } }]
            }
          }
        ]
      }
    }
  ]
});
```

### Create To-Do List
```javascript
await notion.blocks.children.append({
  block_id: 'page-id',
  children: [
    {
      object: 'block',
      type: 'to_do',
      to_do: {
        rich_text: [{ type: 'text', text: { content: 'Task 1' } }],
        checked: false
      }
    },
    {
      object: 'block',
      type: 'to_do',
      to_do: {
        rich_text: [{ type: 'text', text: { content: 'Task 2' } }],
        checked: true
      }
    }
  ]
});
```

### Add Table
```javascript
// 1. Create table block
const table = await notion.blocks.children.append({
  block_id: 'page-id',
  children: [{
    object: 'block',
    type: 'table',
    table: {
      table_width: 3,
      has_column_header: true,
      has_row_header: false
    }
  }]
});

const tableId = table.results[0].id;

// 2. Add table rows
await notion.blocks.children.append({
  block_id: tableId,
  children: [
    {
      object: 'block',
      type: 'table_row',
      table_row: {
        cells: [
          [{ type: 'text', text: { content: 'Header 1' } }],
          [{ type: 'text', text: { content: 'Header 2' } }],
          [{ type: 'text', text: { content: 'Header 3' } }]
        ]
      }
    },
    {
      object: 'block',
      type: 'table_row',
      table_row: {
        cells: [
          [{ type: 'text', text: { content: 'Row 1 Col 1' } }],
          [{ type: 'text', text: { content: 'Row 1 Col 2' } }],
          [{ type: 'text', text: { content: 'Row 1 Col 3' } }]
        ]
      }
    }
  ]
});
```

### Add Image
```javascript
// External URL
{
  object: 'block',
  type: 'image',
  image: {
    type: 'external',
    external: {
      url: 'https://example.com/image.png'
    },
    caption: [
      { type: 'text', text: { content: 'Image caption' } }
    ]
  }
}
```

### Add Code Block
```javascript
{
  object: 'block',
  type: 'code',
  code: {
    rich_text: [{
      type: 'text',
      text: {
        content: 'function hello() {\n  console.log("Hello!");\n}'
      }
    }],
    language: 'javascript',
    caption: []
  }
}
```

### Add Callout
```javascript
{
  object: 'block',
  type: 'callout',
  callout: {
    rich_text: [{
      type: 'text',
      text: { content: 'Important information here' }
    }],
    icon: {
      type: 'emoji',
      emoji: '💡'
    },
    color: 'blue_background'
  }
}
```

### Add Toggle List
```javascript
{
  object: 'block',
  type: 'toggle',
  toggle: {
    rich_text: [{
      type: 'text',
      text: { content: 'Click to expand' }
    }],
    children: [
      {
        object: 'block',
        type: 'paragraph',
        paragraph: {
          rich_text: [{ type: 'text', text: { content: 'Hidden content' } }]
        }
      }
    ]
  }
}
```

## User & Comments

### List All Users
```javascript
const users = await notion.users.list({});
```

### Get Current Bot User Info
```javascript
const bot = await notion.users.me({});
```

### Get User by ID
```javascript
const user = await notion.users.retrieve({
  user_id: 'user-id'
});
```

### Add Comment to Page
```javascript
await notion.comments.create({
  parent: { page_id: 'page-id' },
  rich_text: [{
    type: 'text',
    text: { content: 'This is a comment' }
  }]
});
```

### Get Comments on Page
```javascript
const comments = await notion.comments.list({
  block_id: 'page-id'
});
```

## Search

### Search Everything
```javascript
const results = await notion.search({
  query: 'search term'
});
```

### Search Only Pages
```javascript
const pages = await notion.search({
  query: 'search term',
  filter: {
    property: 'object',
    value: 'page'
  }
});
```

### Search Only Databases
```javascript
const databases = await notion.search({
  query: 'search term',
  filter: {
    property: 'object',
    value: 'database'
  }
});
```

### Search with Sorting
```javascript
const results = await notion.search({
  query: 'search term',
  sort: {
    direction: 'descending',
    timestamp: 'last_edited_time'
  }
});
```

## Error Handling

### Check if Page/Database is Shared
```javascript
try {
  const page = await notion.pages.retrieve({ page_id: 'xxx' });
  console.log('Access granted!');
} catch (error) {
  if (error.code === 'object_not_found') {
    console.log('Not shared with integration OR doesn\'t exist');
  }
}
```

### Handle Rate Limits
```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.code === 'rate_limited') {
        const retryAfter = error.headers?.['retry-after'] || 1;
        console.log(`Rate limited, waiting ${retryAfter}s...`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}

// Use it:
const result = await withRetry(() => 
  notion.pages.create({ /* ... */ })
);
```

## Tips & Best Practices

1. **Always share pages** with integration before API access
2. **Store IDs** when creating resources for later use
3. **Handle pagination** for large databases and pages
4. **Use property IDs** instead of names for stability
5. **Batch operations** when possible to reduce API calls
6. **Handle rate limits** with exponential backoff
7. **Use rich text** format for all text, never plain strings
8. **Recursive reading** needed for nested block structures
9. **Validate before sending** to avoid API errors
10. **Keep tokens secret** - never commit to source control
