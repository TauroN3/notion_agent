## notion_agent
Claude Agent that provides a full coverage of the Notion API.

## Agent architecture:
Agents:
- main claude context
  - notion read only: has access to the read api skills, for fast queries and without modifying any data 
  - notion read write: has full access to the read/write skills, for editing and inserting data
  - note formatter: has full read/write access, consumes a scheme that it will check that all notes follows it. keeps order around.

Skills:
- read-data-notion-api
- write-data-notion-api
- notion-api (legacy, will be removed after confirming that splitting the skill is stable)
- notion-formatter (TBD)
- notion-rate-limit-gatekeeper (TBD)

Tools:
- none

## Codebase structure
- main agent image can be built with the Dockerfile
  ```
  docker build -t notion_agent .
  ```
- communication with the agent can be performed directly to the docker image (TBD)
- if any other form of communication is desired, a 'wrappers' folder is present (MCP, HTTP Server, etc?)

## Secret hanadling
TBD

## Security notice
It is reccomended to use Docker with MicroVM support for security as I did not fine-tuned claude-code's permissions at all at this stage
