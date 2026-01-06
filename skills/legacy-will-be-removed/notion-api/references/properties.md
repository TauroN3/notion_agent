# Property Types and Values

## Overview

Properties are the structured data in Notion pages, especially database pages. There are two related concepts:

1. **Property Objects** (Database Schema) - Define what types of data a database column can hold
2. **Property Value Objects** (Page Data) - The actual data values in a specific page

## Property Objects (Database Schema)

Appears in database objects to define the schema.

```json
{
  "Name": {
    "id": "title",
    "name": "Name",
    "type": "title",
    "title": {}
  },
  "Status": {
    "id": "abc123",
    "name": "Status",
    "type": "select",
    "select": {
      "options": [
        { "name": "Not Started", "color": "red", "id": "xyz" },
        { "name": "Done", "color": "green", "id": "def" }
      ]
    }
  }
}
```

Every property object has:
- `id` - Property identifier (stable even if name changes)
- `name` - Display name
- `type` - Property type
- `{type}` - Type-specific configuration

## Property Value Objects (Page Data)

Appears in page objects as actual data values.

```json
{
  "Name": {
    "id": "title",
    "type": "title",
    "title": [
      { "type": "text", "text": { "content": "My Page" } }
    ]
  },
  "Status": {
    "id": "abc123",
    "type": "select",
    "select": {
      "id": "xyz",
      "name": "Done",
      "color": "green"
    }
  }
}
```

## All Property Types

### Title (Required for all databases)

**Schema:**
```json
{
  "Name": {
    "id": "title",
    "type": "title",
    "title": {}
  }
}
```

**Value:**
```json
{
  "Name": {
    "type": "title",
    "title": [
      {
        "type": "text",
        "text": { "content": "Page Title" },
        "annotations": {...}
      }
    ]
  }
}
```

Every database has exactly ONE title property. It represents the page name.

### Rich Text

Multi-line text with formatting.

**Schema:**
```json
{
  "Description": {
    "id": "abc",
    "type": "rich_text",
    "rich_text": {}
  }
}
```

**Value:**
```json
{
  "Description": {
    "type": "rich_text",
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "Detailed description" },
        "annotations": {
          "bold": true,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        }
      }
    ]
  }
}
```

### Number

Numeric values with optional formatting.

**Schema:**
```json
{
  "Price": {
    "id": "abc",
    "type": "number",
    "number": {
      "format": "dollar"  // OR "number", "percent", etc.
    }
  }
}
```

Formats: `number`, `number_with_commas`, `percent`, `dollar`, `canadian_dollar`, `euro`, `pound`, `yen`, `ruble`, `rupee`, `won`, `yuan`, `real`, `lira`, `rupiah`, `franc`, `hong_kong_dollar`, `new_zealand_dollar`, `krona`, `norwegian_krone`, `mexican_peso`, `rand`, `new_taiwan_dollar`, `danish_krone`, `zloty`, `baht`, `forint`, `koruna`, `shekel`, `chilean_peso`, `philippine_peso`, `dirham`, `colombian_peso`, `riyal`, `ringgit`, `leu`, `argentine_peso`, `uruguayan_peso`, `singapore_dollar`

**Value:**
```json
{
  "Price": {
    "type": "number",
    "number": 99.99
  }
}
```

### Select

Single selection from predefined options.

**Schema:**
```json
{
  "Status": {
    "id": "abc",
    "type": "select",
    "select": {
      "options": [
        { "name": "Not Started", "color": "red", "id": "xxx" },
        { "name": "In Progress", "color": "yellow", "id": "yyy" },
        { "name": "Done", "color": "green", "id": "zzz" }
      ]
    }
  }
}
```

Colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`

**Value:**
```json
{
  "Status": {
    "type": "select",
    "select": {
      "id": "yyy",
      "name": "In Progress",
      "color": "yellow"
    }
  }
}
```

**Creating new options:** If you set a select value to a name that doesn't exist in the schema, it will be automatically created.

### Multi-Select

Multiple selections from predefined options.

**Schema:**
```json
{
  "Tags": {
    "id": "abc",
    "type": "multi_select",
    "multi_select": {
      "options": [
        { "name": "urgent", "color": "red", "id": "xxx" },
        { "name": "bug", "color": "red", "id": "yyy" },
        { "name": "feature", "color": "blue", "id": "zzz" }
      ]
    }
  }
}
```

**Value:**
```json
{
  "Tags": {
    "type": "multi_select",
    "multi_select": [
      { "id": "xxx", "name": "urgent", "color": "red" },
      { "id": "yyy", "name": "bug", "color": "red" }
    ]
  }
}
```

### Date

Date or date range, with optional time.

**Schema:**
```json
{
  "Due Date": {
    "id": "abc",
    "type": "date",
    "date": {}
  }
}
```

**Value (date only):**
```json
{
  "Due Date": {
    "type": "date",
    "date": {
      "start": "2024-12-31",
      "end": null,
      "time_zone": null
    }
  }
}
```

**Value (date with time):**
```json
{
  "Due Date": {
    "type": "date",
    "date": {
      "start": "2024-12-31T14:30:00.000Z",
      "end": null,
      "time_zone": "America/New_York"
    }
  }
}
```

**Value (date range):**
```json
{
  "Due Date": {
    "type": "date",
    "date": {
      "start": "2024-12-01",
      "end": "2024-12-31",
      "time_zone": null
    }
  }
}
```

### People

References to Notion users.

**Schema:**
```json
{
  "Assignee": {
    "id": "abc",
    "type": "people",
    "people": {}
  }
}
```

**Value:**
```json
{
  "Assignee": {
    "type": "people",
    "people": [
      {
        "object": "user",
        "id": "user-id-1"
      },
      {
        "object": "user",
        "id": "user-id-2"
      }
    ]
  }
}
```

### Files

File attachments.

**Schema:**
```json
{
  "Attachments": {
    "id": "abc",
    "type": "files",
    "files": {}
  }
}
```

**Value:**
```json
{
  "Attachments": {
    "type": "files",
    "files": [
      {
        "name": "document.pdf",
        "type": "external",
        "external": {
          "url": "https://example.com/document.pdf"
        }
      },
      {
        "name": "image.png",
        "type": "file",
        "file": {
          "url": "https://s3.aws...",
          "expiry_time": "2024-12-31T23:59:59.999Z"
        }
      }
    ]
  }
}
```

### Checkbox

Boolean value.

**Schema:**
```json
{
  "Completed": {
    "id": "abc",
    "type": "checkbox",
    "checkbox": {}
  }
}
```

**Value:**
```json
{
  "Completed": {
    "type": "checkbox",
    "checkbox": true
  }
}
```

### URL

Web link.

**Schema:**
```json
{
  "Website": {
    "id": "abc",
    "type": "url",
    "url": {}
  }
}
```

**Value:**
```json
{
  "Website": {
    "type": "url",
    "url": "https://example.com"
  }
}
```

### Email

Email address.

**Schema:**
```json
{
  "Contact Email": {
    "id": "abc",
    "type": "email",
    "email": {}
  }
}
```

**Value:**
```json
{
  "Contact Email": {
    "type": "email",
    "email": "user@example.com"
  }
}
```

### Phone Number

Phone number.

**Schema:**
```json
{
  "Phone": {
    "id": "abc",
    "type": "phone_number",
    "phone_number": {}
  }
}
```

**Value:**
```json
{
  "Phone": {
    "type": "phone_number",
    "phone_number": "+1-555-123-4567"
  }
}
```

### Formula

Computed property based on other properties.

**Schema:**
```json
{
  "Days Until Due": {
    "id": "abc",
    "type": "formula",
    "formula": {
      "expression": "dateBetween(prop(\"Due Date\"), now(), \"days\")"
    }
  }
}
```

**Value (Read-only - computed by Notion):**
```json
{
  "Days Until Due": {
    "type": "formula",
    "formula": {
      "type": "number",
      "number": 25
    }
  }
}
```

Formula results can be: `string`, `number`, `boolean`, `date`

### Relation

Link to pages in another database.

**Schema:**
```json
{
  "Related Tasks": {
    "id": "abc",
    "type": "relation",
    "relation": {
      "database_id": "other-database-id",
      "type": "dual_property",  // OR "single_property"
      "dual_property": {
        "synced_property_name": "Projects",
        "synced_property_id": "xyz"
      }
    }
  }
}
```

**Value:**
```json
{
  "Related Tasks": {
    "type": "relation",
    "relation": [
      { "id": "page-id-1" },
      { "id": "page-id-2" }
    ]
  }
}
```

**Important:** The related database must be shared with your integration!

### Rollup

Aggregate values from related pages.

**Schema:**
```json
{
  "Total Hours": {
    "id": "abc",
    "type": "rollup",
    "rollup": {
      "relation_property_name": "Related Tasks",
      "relation_property_id": "rel_id",
      "rollup_property_name": "Hours",
      "rollup_property_id": "hours_id",
      "function": "sum"
    }
  }
}
```

Functions: `count`, `count_values`, `empty`, `not_empty`, `unique`, `show_unique`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `median`, `min`, `max`, `range`, `show_original`, `count_per_group`, `percent_per_group`, `date_range`, `earliest_date`, `latest_date`

**Value (Read-only - computed by Notion):**
```json
{
  "Total Hours": {
    "type": "rollup",
    "rollup": {
      "type": "number",
      "number": 42,
      "function": "sum"
    }
  }
}
```

### Status

Custom status workflow (like select but with workflow features).

**Schema:**
```json
{
  "Status": {
    "id": "abc",
    "type": "status",
    "status": {
      "options": [
        { "name": "Not started", "color": "gray", "id": "xxx" },
        { "name": "In progress", "color": "blue", "id": "yyy" },
        { "name": "Complete", "color": "green", "id": "zzz" }
      ],
      "groups": [
        {
          "name": "To-do",
          "color": "gray",
          "id": "group1",
          "option_ids": ["xxx"]
        },
        {
          "name": "In progress",
          "color": "blue",
          "id": "group2",
          "option_ids": ["yyy"]
        },
        {
          "name": "Complete",
          "color": "green",
          "id": "group3",
          "option_ids": ["zzz"]
        }
      ]
    }
  }
}
```

**Value:**
```json
{
  "Status": {
    "type": "status",
    "status": {
      "id": "yyy",
      "name": "In progress",
      "color": "blue"
    }
  }
}
```

### Created Time

Automatic timestamp of page creation (read-only).

**Schema:**
```json
{
  "Created": {
    "id": "abc",
    "type": "created_time",
    "created_time": {}
  }
}
```

**Value:**
```json
{
  "Created": {
    "type": "created_time",
    "created_time": "2024-01-01T12:00:00.000Z"
  }
}
```

### Created By

Automatic user who created the page (read-only).

**Schema:**
```json
{
  "Created By": {
    "id": "abc",
    "type": "created_by",
    "created_by": {}
  }
}
```

**Value:**
```json
{
  "Created By": {
    "type": "created_by",
    "created_by": {
      "object": "user",
      "id": "user-id"
    }
  }
}
```

### Last Edited Time

Automatic timestamp of last edit (read-only).

**Schema:**
```json
{
  "Last Edited": {
    "id": "abc",
    "type": "last_edited_time",
    "last_edited_time": {}
  }
}
```

**Value:**
```json
{
  "Last Edited": {
    "type": "last_edited_time",
    "last_edited_time": "2024-01-01T15:30:00.000Z"
  }
}
```

### Last Edited By

Automatic user who last edited (read-only).

**Schema:**
```json
{
  "Last Edited By": {
    "id": "abc",
    "type": "last_edited_by",
    "last_edited_by": {}
  }
}
```

**Value:**
```json
{
  "Last Edited By": {
    "type": "last_edited_by",
    "last_edited_by": {
      "object": "user",
      "id": "user-id"
    }
  }
}
```

### Unique ID

Auto-incrementing unique identifier (read-only).

**Schema:**
```json
{
  "ID": {
    "id": "abc",
    "type": "unique_id",
    "unique_id": {
      "prefix": "TASK-"
    }
  }
}
```

**Value:**
```json
{
  "ID": {
    "type": "unique_id",
    "unique_id": {
      "number": 42,
      "prefix": "TASK-"
    }
  }
}
```

Displays as "TASK-42" in Notion.

### Verification

Wiki database verification status (Enterprise only).

**Schema:**
```json
{
  "Verification": {
    "id": "abc",
    "type": "verification",
    "verification": {}
  }
}
```

**Value:**
```json
{
  "Verification": {
    "type": "verification",
    "verification": {
      "state": "verified",
      "verified_by": {
        "object": "user",
        "id": "user-id"
      },
      "date": {
        "start": "2024-01-01T00:00:00.000Z",
        "end": null,
        "time_zone": null
      }
    }
  }
}
```

States: `verified`, `unverified`

## Setting Property Values

### Empty Values

To clear a property value, set it to an empty value:

```json
{
  "Property Name": {
    "type": "select",
    "select": null
  }
}
```

Or for arrays:
```json
{
  "Property Name": {
    "type": "multi_select",
    "multi_select": []
  }
}
```

### Using Property Names vs IDs

You can reference properties by name OR by ID:

**By name:**
```json
{
  "Status": {
    "select": { "name": "Done" }
  }
}
```

**By ID:**
```json
{
  "abc123": {
    "select": { "name": "Done" }
  }
}
```

Property IDs are stable even if names change, so they're safer for integrations.

## Paginated Properties

Some property values (rollup, relation with many items) may be too large for the page response. These return a paginated property item.

**Get paginated property:**
```bash
GET /v1/pages/{page_id}/properties/{property_id}
```

Returns paginated list of property values.

## Common Patterns

### Create Page with Various Property Types

```javascript
await notion.pages.create({
  parent: { database_id: 'xxx' },
  properties: {
    'Name': {
      title: [{ type: 'text', text: { content: 'Task Name' } }]
    },
    'Status': {
      select: { name: 'In Progress' }
    },
    'Tags': {
      multi_select: [
        { name: 'urgent' },
        { name: 'bug' }
      ]
    },
    'Due Date': {
      date: {
        start: '2024-12-31',
        end: null
      }
    },
    'Assignee': {
      people: [{ id: 'user-id' }]
    },
    'Priority': {
      number: 1
    },
    'Completed': {
      checkbox: false
    },
    'Notes': {
      rich_text: [
        {
          type: 'text',
          text: { content: 'Important notes' },
          annotations: { bold: true }
        }
      ]
    }
  }
});
```

### Update Multiple Properties

```javascript
await notion.pages.update({
  page_id: 'xxx',
  properties: {
    'Status': { select: { name: 'Done' } },
    'Completed': { checkbox: true },
    'Completed Date': { date: { start: '2024-11-05' } }
  }
});
```

### Clear a Property

```javascript
await notion.pages.update({
  page_id: 'xxx',
  properties: {
    'Due Date': { date: null },
    'Tags': { multi_select: [] }
  }
});
```

## Best Practices

1. **Match Schema:** Property values must match the database schema type
2. **Property IDs:** Use IDs instead of names for stability
3. **Validation:** Validate property types before sending to API
4. **Read-only Properties:** Don't attempt to set formula, rollup, created_time, etc.
5. **Relations:** Ensure related databases are shared with your integration
6. **Auto-create Options:** Select/multi-select options auto-create if they don't exist
7. **Empty Values:** Use `null` or `[]` to clear values
8. **Rich Text:** Always use rich text format, never plain strings
9. **Dates:** Use ISO 8601 format for dates/datetimes
10. **Pagination:** Handle paginated properties for relation/rollup with many values
