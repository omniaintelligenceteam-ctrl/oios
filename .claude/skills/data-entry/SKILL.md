# Data Entry

Structure messy or raw data into clean, organized formats ready for sheets, databases, or docs.

## Trigger
User says things like: "organize this data", "format this for a spreadsheet", "clean up this list", "structure this info", pastes a block of unstructured data

## Process

### Step 1: Receive the raw input
Take whatever Wes gives — a list, a paste, a brain dump, a screenshot description — and identify what type of data it is.

### Step 2: Clarify (only if truly necessary)
Only ask questions if the data is too ambiguous to structure. Examples:
- "Is this a contact list or a task list?"
- "Do you want this sorted by date or by name?"

Don't ask if you can make a reasonable assumption — just state it.

### Step 3: Output the structured data

**Default: CSV-ready table format**
```
Column1, Column2, Column3
Value1, Value2, Value3
...
```

**If it's a task/to-do list:**
```
- [ ] [Task] | [Owner] | [Due Date] | [Priority]
```

**If it's a contact list:**
```
| Name | Company | Title | Email | Phone | Notes |
```

**If it's a CRM update or lead list:**
```
| Name | Company | Source | Status | Last Contact | Next Step |
```

**If it's a meeting list / schedule:**
```
| Date | Time | Meeting | Attendees | Purpose |
```

### Step 4: Present + confirm
- Show the structured output
- State what format you used and why
- Ask: "Want me to adjust the columns, sort order, or format?"

### Step 5: Offer next steps
- "Want me to add this to an existing doc or sheet?"
- "Want me to draft a follow-up action for any of these items?"

## Notes
- When in doubt, more columns is better than fewer — easier to delete than to add later.
- Flag obvious data quality issues (duplicates, missing fields, inconsistencies).
- Never make up data to fill gaps — leave blanks and note them.
