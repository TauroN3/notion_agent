---
name: notion-api
description: Comprehensive guide for using the Notion REST API to interact with pages, databases, blocks, and content. Use this skill when Claude needs to (1) Discover how to perform specific Notion API operations (e.g., "how do I query a database?", "how to format text with headers?"), (2) Understand Notion API structure and conventions, (3) Find the right API endpoint and request format for a task, (4) Work with page properties, database schemas, or block content, (5) Build integrations with Notion, or (6) Answer questions about authentication, pagination, filters, or any other Notion API features.
---

# Notion API Skill

This skill provides comprehensive guidance for working with the Notion REST API, helping you discover how to accomplish specific tasks and build integrations.

## How to Use This Skill

This skill is organized as a reference library. When you need to accomplish something with the Notion API:

1. **Start with common_tasks.md** for quick recipes and code examples
2. **Read specific references** for in-depth documentation on a topic
3. **Use grep patterns** to quickly find specific information in large files

## Quick Start

**First time using Notion API?** Start by reading:
1. `references/api_overview.md` - Authentication, conventions, basic concepts
2. `references/common_tasks.md` - Quick recipes for common operations

**Looking for a specific task?** Check `references/common_tasks.md` first.

**Need detailed documentation?** Read the relevant reference file based on what you're working with.

## Reference Files

### Quick Reference

**`references/common_tasks.md`** - START HERE for most queries  
Quick recipes for common operations with copy-paste code examples:
- Authentication setup and finding IDs
- Database operations (create, query, filter, sort)
- Page operations (create, read, update, delete)
- Content operations (add/update blocks, formatting)
- Complex structures (tables, nested lists, columns)
- Error handling patterns

Use this when users ask "how do I..." questions.

### Core Concepts

**`references/api_overview.md`**  
Foundational information about the Notion API:
- Base URL and request conventions
- Authentication (internal vs. public integrations, OAuth)
- Required headers and request format
- Pagination patterns
- Rate limits and error codes
- Size limits and best practices

Read this for:
- Authentication questions
- Understanding API structure
- Error troubleshooting
- Rate limiting questions

Grep patterns:
- `grep -i "authentication" references/api_overview.md` - Auth details
- `grep -i "pagination" references/api_overview.md` - Pagination info
- `grep -i "rate limit" references/api_overview.md` - Rate limiting
- `grep -A 10 "error code" references/api_overview.md` - Error codes

### Working with Pages

**`references/pages.md`**  
Everything about Notion pages:
- Page object structure and properties
- Creating pages (standalone and in databases)
- Reading and updating pages
- Page parent types
- Icons and covers
- Finding page IDs
- Common patterns and best practices

Read this when:
- Creating or updating pages
- Working with page properties
- Understanding page structure
- Questions about page operations

Grep patterns:
- `grep -A 20 "Create a Page" references/pages.md` - Page creation
- `grep -A 15 "Update Page" references/pages.md` - Page updates
- `grep "POST /v1/pages" references/pages.md` - Create endpoint
- `grep "PATCH /v1/pages" references/pages.md` - Update endpoint

### Working with Databases

**`references/databases.md`**  
Complete guide to databases:
- Database object structure and schema
- Creating and updating databases
- Querying databases with filters and sorts
- All filter conditions by property type
- Sort options and patterns
- Database property types
- Finding database IDs
- Pagination for large databases
- Best practices

Read this when:
- Working with databases
- Filtering or sorting data
- Creating database schemas
- Querying database entries
- Understanding database structure

Grep patterns:
- `grep -A 30 "Query a Database" references/databases.md` - Query syntax
- `grep -A 50 "Filter Conditions" references/databases.md` - All filter types
- `grep -A 20 "Compound Filters" references/databases.md` - AND/OR filters
- `grep -A 30 "Database Sorts" references/databases.md` - Sorting
- `grep "POST /v1/databases/.*/query" references/databases.md` - Query endpoint

### Working with Blocks

**`references/blocks.md`**  
Comprehensive guide to blocks (page content):
- Block object structure
- All block types with examples (30+ types)
- Creating and updating blocks
- Nested blocks and recursive reading
- Block-specific properties
- Layout blocks (columns, tables)
- Media blocks (images, videos, files)
- Rich text formatting in blocks

Read this when:
- Adding content to pages
- Creating formatted text
- Working with lists, headings, code blocks
- Adding images, tables, or other media
- Understanding block structure
- Reading page content

Grep patterns:
- `grep -A 15 "^### [A-Z]" references/blocks.md` - List all block types
- `grep -A 20 "Paragraph" references/blocks.md` - Paragraph blocks
- `grep -A 20 "Heading" references/blocks.md` - Heading blocks  
- `grep -A 20 "List" references/blocks.md` - List blocks
- `grep -A 20 "Table" references/blocks.md` - Table blocks
- `grep "Retrieve Block Children" references/blocks.md` - Reading blocks

### Property Types

**`references/properties.md`**  
Complete reference for all 25+ property types:
- Property objects (database schema)
- Property value objects (page data)
- All property types with schema and value examples
- Creating and updating properties
- Property-specific configurations
- Read-only vs. writable properties
- Paginated properties

Read this when:
- Working with database properties
- Creating database schemas
- Setting page property values
- Understanding property formats
- Questions about specific property types

Grep patterns:
- `grep -A 30 "### [A-Z]" references/properties.md` - List all property types
- `grep -A 30 "Title" references/properties.md` - Title property
- `grep -A 30 "Select" references/properties.md` - Select property
- `grep -A 30 "Date" references/properties.md` - Date property
- `grep -A 30 "Relation" references/properties.md` - Relation property
- `grep -A 30 "Formula" references/properties.md` - Formula property

## Discovery Patterns

### User Asks "How do I..."

**Format:** "How do I [action] in Notion API?"

**Response pattern:**
1. Check `references/common_tasks.md` for a matching recipe
2. If found, provide the code example directly
3. If not found, search relevant reference file for the operation
4. Provide complete, working code example
5. Mention any prerequisites (e.g., sharing page with integration)

**Examples:**
- "How do I create a database?" → common_tasks.md → "Create a New Database"
- "How do I filter a database by status?" → common_tasks.md → "Query Database with Filters"
- "How do I add a table to a page?" → common_tasks.md → "Add Table"

### User Asks "What are my available..."

**Format:** "What are my available [resources]?"

**Response pattern:**
1. Identify the resource type (databases, pages, users, etc.)
2. Point to the Search or List endpoint in common_tasks.md
3. Provide the exact API call to list the resource
4. Include pagination handling if needed

**Examples:**
- "What are my current available DBs?" → common_tasks.md → "List All Databases I Have Access To"
- "What pages do I have?" → common_tasks.md → "Search Only Pages"
- "Who are the users in my workspace?" → common_tasks.md → "List All Users"

### User Asks "How do I format..."

**Format:** "How do I format [text/content] with [style]?"

**Response pattern:**
1. Check if it's text formatting (bold, links, etc.) → common_tasks.md "Text Formatting"
2. Check if it's block formatting (headers, lists, etc.) → common_tasks.md "Complex Structures"
3. Provide rich text format example with proper annotations
4. Show complete block structure if needed

**Examples:**
- "How do I format text with bold and italic?" → common_tasks.md → "Bold, Italic, Underline Text"
- "How do I create headers?" → common_tasks.md → "Create Page with Content" (heading blocks)
- "How do I add bullet points?" → common_tasks.md → "Create Page with Content" (bulleted_list_item)

### User References Specific Property/Block Types

**Format:** User mentions a specific type like "select property" or "table block"

**Response pattern:**
1. Identify the type category (property or block)
2. Read the specific section from properties.md or blocks.md
3. Provide schema and value examples
4. Include any type-specific configuration options

**Examples:**
- "Tell me about select properties" → properties.md → search "### Select"
- "How do relation properties work?" → properties.md → search "### Relation"
- "Show me how to create a code block" → blocks.md → search "### Code"

## Important Reminders

### Before Making API Calls

1. **Authentication Required:** User needs an integration token (internal) or OAuth access token (public)
2. **Pages Must Be Shared:** Integration must be explicitly shared with pages/databases via Notion UI
3. **Headers Required:** Every request needs Authorization, Notion-Version, and Content-Type headers

### Common Pitfalls to Avoid

1. **404 Errors:** Usually means page isn't shared with integration, not that it doesn't exist
2. **Plain Strings:** Never use plain strings - always use rich text format for text content
3. **Property Matching:** Page properties must match database schema when creating database pages
4. **Recursive Reading:** Pages with nested content require recursive calls to get all blocks
5. **Pagination:** Always handle pagination for databases and pages with many items
6. **Rate Limits:** Implement exponential backoff for rate limit errors (429)

### Best Practices to Mention

1. Store page/database IDs when creating resources
2. Use property IDs instead of names for stability
3. Batch operations when possible to reduce API calls
4. Handle errors gracefully (especially 404 and 429)
5. Use async operations for large/recursive reads
6. Validate data before sending to API
7. Keep integration tokens secret (environment variables)

## Examples of Skill Usage

### Example 1: User wants to know available databases

**User:** "What are my current available databases in Notion?"

**Response:**
```javascript
// List all databases you have access to
const response = await notion.search({
  filter: {
    property: 'object',
    value: 'database'
  }
});

console.log(response.results); // Array of database objects
```

Note: Make sure your integration is shared with the databases you want to see.

### Example 2: User wants to format text with specific styling

**User:** "Write the following text and format it with headers and bullets"

**Response:**
```javascript
await notion.blocks.children.append({
  block_id: 'page-id',
  children: [
    {
      object: 'block',
      type: 'heading_1',
      heading_1: {
        rich_text: [{
          type: 'text',
          text: { content: 'Main Header' }
        }]
      }
    },
    {
      object: 'block',
      type: 'heading_2',
      heading_2: {
        rich_text: [{
          type: 'text',
          text: { content: 'Subheader' }
        }]
      }
    },
    {
      object: 'block',
      type: 'bulleted_list_item',
      bulleted_list_item: {
        rich_text: [{
          type: 'text',
          text: { content: 'First bullet point' }
        }]
      }
    },
    {
      object: 'block',
      type: 'bulleted_list_item',
      bulleted_list_item: {
        rich_text: [{
          type: 'text',
          text: { content: 'Second bullet point' }
        }]
      }
    }
  ]
});
```

### Example 3: User needs to query database with filters

**User:** "How do I get all tasks that are in progress and due this week?"

**Response:**
```javascript
const response = await notion.databases.query({
  database_id: 'your-database-id',
  filter: {
    and: [
      {
        property: 'Status',
        select: {
          equals: 'In Progress'
        }
      },
      {
        property: 'Due Date',
        date: {
          this_week: {}
        }
      }
    ]
  },
  sorts: [
    {
      property: 'Due Date',
      direction: 'ascending'
    }
  ]
});

console.log(response.results); // Array of matching pages
```

## Response Strategy

When responding to Notion API queries:

1. **Be Direct:** Provide working code immediately, not just explanations
2. **Be Complete:** Include all required fields and proper formatting
3. **Be Practical:** Use real-world examples that can be copy-pasted
4. **Be Accurate:** Double-check property formats and required fields
5. **Be Helpful:** Mention common pitfalls and prerequisites
6. **Be Concise:** Focus on the specific question, don't overwhelm with unrelated info

## Final Note

This skill contains the complete Notion API documentation extracted from https://developers.notion.com/. All information is current and comprehensive. Always provide accurate, working code examples based on the reference files.
