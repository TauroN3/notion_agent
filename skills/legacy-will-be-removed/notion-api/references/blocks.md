# Working with Blocks and Page Content

## Block Overview

Blocks are the building units of page content in Notion. Everything users see on a page - paragraphs, headings, lists, images, etc. - is represented as a block.

**Key concepts:**
- Pages ARE blocks (special type that can have children)
- Blocks can have child blocks (nesting)
- Each block has a `type` and type-specific properties
- Rich text formatting is used extensively in blocks

## Block Object Structure

```json
{
  "object": "block",
  "id": "abc123",
  "parent": {
    "type": "page_id",
    "page_id": "xxx"
  },
  "created_time": "2024-01-01T12:00:00.000Z",
  "last_edited_time": "2024-01-01T12:00:00.000Z",
  "created_by": { "object": "user", "id": "xxx" },
  "last_edited_by": { "object": "user", "id": "xxx" },
  "has_children": false,
  "archived": false,
  "in_trash": false,
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "This is a paragraph" },
        "annotations": {
          "bold": false,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        }
      }
    ],
    "color": "default"
  }
}
```

Common properties for all blocks:
- `object`: Always "block"
- `id`: Block UUID
- `type`: Block type (paragraph, heading_1, etc.)
- `created_time`, `last_edited_time`: ISO 8601 timestamps
- `has_children`: Boolean indicating if block has child blocks
- `archived`: Boolean for archived status
- `{type}`: Type-specific properties (e.g., `paragraph`, `heading_1`)

## API Endpoints

### Retrieve Block Children

**GET** `/v1/blocks/{block_id}/children`

Returns child blocks of a block (or page). Only returns first level - recursive calls needed for nested blocks.

```bash
curl https://api.notion.com/v1/blocks/xxx/children?page_size=100 \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
```

**Parameters:**
- `page_size` (optional) - Max 100, default 100
- `start_cursor` (optional) - Pagination cursor

**Response:** Paginated list of block objects

### Append Block Children

**PATCH** `/v1/blocks/{block_id}/children`

Add blocks to a parent block (or page). Blocks are appended to the end by default.

```bash
curl -X PATCH https://api.notion.com/v1/blocks/xxx/children \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{
            "type": "text",
            "text": { "content": "New paragraph" }
          }]
        }
      }
    ]
  }'
```

**Parameters:**
- `children` (required) - Array of block objects to append
- `after` (optional) - Block ID to append after (instead of at end)

**Note:** Maximum ~100 blocks per request, ~2000 characters per block

### Retrieve a Block

**GET** `/v1/blocks/{block_id}`

```bash
curl https://api.notion.com/v1/blocks/xxx \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
```

Returns the block object. Use "Retrieve block children" to get its child blocks.

### Update a Block

**PATCH** `/v1/blocks/{block_id}`

Update block content. Only certain block types support updates.

```bash
curl -X PATCH https://api.notion.com/v1/blocks/xxx \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "paragraph": {
      "rich_text": [{
        "type": "text",
        "text": { "content": "Updated content" }
      }]
    }
  }'
```

**Updatable block types:**
- paragraph, heading_1, heading_2, heading_3
- bulleted_list_item, numbered_list_item, toggle
- to_do, quote, callout, code

**Non-updatable:** Most media blocks, column_list, table, etc.

### Delete a Block

**DELETE** `/v1/blocks/{block_id}`

```bash
curl -X DELETE https://api.notion.com/v1/blocks/xxx \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
```

Sets `archived: true` on the block. Block still exists but is archived.

## Block Types

### Text Blocks

**Paragraph**
```json
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Paragraph text" }
    }],
    "color": "default"
  }
}
```

**Headings (heading_1, heading_2, heading_3)**
```json
{
  "type": "heading_1",
  "heading_1": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Heading text" }
    }],
    "color": "default",
    "is_toggleable": false
  }
}
```

**Callout**
```json
{
  "type": "callout",
  "callout": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Important note" }
    }],
    "icon": {
      "type": "emoji",
      "emoji": "💡"
    },
    "color": "gray_background"
  }
}
```

**Quote**
```json
{
  "type": "quote",
  "quote": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Quote text" }
    }],
    "color": "default"
  }
}
```

**Code**
```json
{
  "type": "code",
  "code": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "console.log('Hello');" }
    }],
    "caption": [],
    "language": "javascript"
  }
}
```

Supported languages: abap, arduino, bash, basic, c, clojure, coffeescript, c++, c#, css, dart, diff, docker, elixir, elm, erlang, flow, fortran, f#, gherkin, glsl, go, graphql, groovy, haskell, html, java, javascript, json, julia, kotlin, latex, less, lisp, livescript, lua, makefile, markdown, markup, matlab, mermaid, nix, objective-c, ocaml, pascal, perl, php, plain text, powershell, prolog, protobuf, python, r, reason, ruby, rust, sass, scala, scheme, scss, shell, sql, swift, typescript, vb.net, verilog, vhdl, visual basic, webassembly, xml, yaml, java/c/c++/c#

### List Blocks

**Bulleted List Item**
```json
{
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "List item" }
    }],
    "color": "default",
    "children": []  // Nested items
  }
}
```

**Numbered List Item**
```json
{
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Numbered item" }
    }],
    "color": "default",
    "children": []
  }
}
```

**To-Do**
```json
{
  "type": "to_do",
  "to_do": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Task to do" }
    }],
    "checked": false,
    "color": "default",
    "children": []
  }
}
```

**Toggle**
```json
{
  "type": "toggle",
  "toggle": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Toggle title" }
    }],
    "color": "default",
    "children": []
  }
}
```

### Media Blocks

**Image**
```json
{
  "type": "image",
  "image": {
    "type": "external",  // OR "file" OR "file_upload"
    "external": {
      "url": "https://example.com/image.png"
    },
    "caption": []
  }
}
```

**Video**
```json
{
  "type": "video",
  "video": {
    "type": "external",
    "external": {
      "url": "https://youtube.com/watch?v=xxx"
    },
    "caption": []
  }
}
```

**File**
```json
{
  "type": "file",
  "file": {
    "type": "external",
    "external": {
      "url": "https://example.com/document.pdf"
    },
    "caption": []
  }
}
```

**PDF**
```json
{
  "type": "pdf",
  "pdf": {
    "type": "external",
    "external": {
      "url": "https://example.com/document.pdf"
    },
    "caption": []
  }
}
```

**Audio**
```json
{
  "type": "audio",
  "audio": {
    "type": "external",
    "external": {
      "url": "https://example.com/audio.mp3"
    },
    "caption": []
  }
}
```

### Embed Blocks

**Bookmark**
```json
{
  "type": "bookmark",
  "bookmark": {
    "url": "https://example.com",
    "caption": []
  }
}
```

**Embed**
```json
{
  "type": "embed",
  "embed": {
    "url": "https://example.com/embed"
  }
}
```

**Link Preview** (Read-only)
```json
{
  "type": "link_preview",
  "link_preview": {
    "url": "https://example.com"
  }
}
```

### Database Blocks

**Child Database** (Read-only)
```json
{
  "type": "child_database",
  "child_database": {
    "title": "Database Name"
  }
}
```

**Child Page** (Read-only reference)
```json
{
  "type": "child_page",
  "child_page": {
    "title": "Page Name"
  }
}
```

### Layout Blocks

**Divider**
```json
{
  "type": "divider",
  "divider": {}
}
```

**Table of Contents**
```json
{
  "type": "table_of_contents",
  "table_of_contents": {
    "color": "default"
  }
}
```

**Breadcrumb**
```json
{
  "type": "breadcrumb",
  "breadcrumb": {}
}
```

**Column List & Column**

Column list contains column blocks:
```json
{
  "type": "column_list",
  "column_list": {}
}
```

Each column is a child block:
```json
{
  "type": "column",
  "column": {}
}
```

**Note:** Create column_list first, then append column blocks as children, then append content blocks to each column.

**Table**

```json
{
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "has_row_header": false
  }
}
```

Table rows are child blocks:
```json
{
  "type": "table_row",
  "table_row": {
    "cells": [
      [{"type": "text", "text": {"content": "Cell 1"}}],
      [{"type": "text", "text": {"content": "Cell 2"}}],
      [{"type": "text", "text": {"content": "Cell 3"}}]
    ]
  }
}
```

### Special Blocks

**Synced Block**

Original synced block:
```json
{
  "type": "synced_block",
  "synced_block": {
    "synced_from": null,
    "children": []
  }
}
```

Reference to synced block:
```json
{
  "type": "synced_block",
  "synced_block": {
    "synced_from": {
      "type": "block_id",
      "block_id": "original-block-id"
    }
  }
}
```

**Template**
```json
{
  "type": "template",
  "template": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Template button text" }
    }],
    "children": []
  }
}
```

**Link to Page**
```json
{
  "type": "link_to_page",
  "link_to_page": {
    "type": "page_id",
    "page_id": "xxx"
  }
}
```

**Equation**
```json
{
  "type": "equation",
  "equation": {
    "expression": "E = mc^2"
  }
}
```

### Unsupported Block Types

Some blocks cannot be created/updated via API (read-only):
- `unsupported` - Any block type not yet supported
- `link_preview` - Can be returned but not created
- `child_page` - Reference only (create pages with POST /v1/pages)
- `child_database` - Reference only (create databases with POST /v1/databases)

## Working with Rich Text

All text content in blocks uses rich text format. See the separate rich_text reference for complete details.

Basic rich text example:
```json
{
  "type": "text",
  "text": {
    "content": "Hello world",
    "link": null
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "Hello world",
  "href": null
}
```

## Colors

Supported colors for blocks:
- `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`
- Background versions: `gray_background`, `brown_background`, etc.

## Common Patterns

### Create Page with Multiple Block Types

```javascript
const page = await notion.pages.create({
  parent: { page_id: 'xxx' },
  properties: {
    title: { title: [{ type: 'text', text: { content: 'My Page' } }] }
  },
  children: [
    {
      object: 'block',
      type: 'heading_1',
      heading_1: {
        rich_text: [{ type: 'text', text: { content: 'Introduction' } }]
      }
    },
    {
      object: 'block',
      type: 'paragraph',
      paragraph: {
        rich_text: [{ type: 'text', text: { content: 'This is a paragraph.' } }]
      }
    },
    {
      object: 'block',
      type: 'bulleted_list_item',
      bulleted_list_item: {
        rich_text: [{ type: 'text', text: { content: 'First bullet' } }]
      }
    }
  ]
});
```

### Recursively Read All Page Content

```javascript
async function getAllBlocks(blockId, allBlocks = []) {
  const response = await notion.blocks.children.list({
    block_id: blockId,
    page_size: 100
  });
  
  for (const block of response.results) {
    allBlocks.push(block);
    
    if (block.has_children) {
      await getAllBlocks(block.id, allBlocks);
    }
  }
  
  if (response.has_more) {
    const moreBlocks = await getAllBlocks(blockId, allBlocks);
    allBlocks.push(...moreBlocks);
  }
  
  return allBlocks;
}

const allContent = await getAllBlocks('page-id');
```

### Create Nested Lists

```javascript
await notion.blocks.children.append({
  block_id: 'xxx',
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
              rich_text: [{ type: 'text', text: { content: 'Child item' } }]
            }
          }
        ]
      }
    }
  ]
});
```

### Create Multi-Column Layout

```javascript
// 1. Create column_list
const columnList = await notion.blocks.children.append({
  block_id: 'page-id',
  children: [{
    object: 'block',
    type: 'column_list',
    column_list: {}
  }]
});

const columnListId = columnList.results[0].id;

// 2. Add columns
const columns = await notion.blocks.children.append({
  block_id: columnListId,
  children: [
    { object: 'block', type: 'column', column: {} },
    { object: 'block', type: 'column', column: {} }
  ]
});

// 3. Add content to each column
await notion.blocks.children.append({
  block_id: columns.results[0].id,
  children: [{
    object: 'block',
    type: 'paragraph',
    paragraph: {
      rich_text: [{ type: 'text', text: { content: 'Left column' } }]
    }
  }]
});

await notion.blocks.children.append({
  block_id: columns.results[1].id,
  children: [{
    object: 'block',
    type: 'paragraph',
    paragraph: {
      rich_text: [{ type: 'text', text: { content: 'Right column' } }]
    }
  }]
});
```

## Best Practices

1. **Batch Appends:** Include multiple blocks in one append request (max ~100 blocks)
2. **Recursive Reading:** Always recursively read blocks with `has_children: true`
3. **Block Limits:** Respect ~2000 character limit per block
4. **Pagination:** Handle pagination for pages with many blocks
5. **Error Handling:** Handle unsupported blocks gracefully (type: "unsupported")
6. **Async Operations:** Use async/await for recursive operations to avoid overwhelming API
7. **Rate Limits:** Be mindful of rate limits when recursively reading large pages
8. **Rich Text:** Always use proper rich text format, not plain strings
9. **Child Blocks:** Some blocks support children (paragraph, list items, toggle), others don't
10. **Updates:** Not all block types can be updated - check documentation per type
