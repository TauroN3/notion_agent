import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { spawn } from 'child_process';

const DOCKER_IMAGE = process.env.NOTION_AGENT_IMAGE || 'notion_agent';
const DOCKER_PATH = process.env.DOCKER_PATH;

const server = new McpServer({
    name: 'notion-agent-wrapper',
    version: '1.0.0'
});

server.registerTool(
    'notion_agent',
    {
        title: 'Notion Agent',
        description: 'Manages Notion notes - reads, writes, and modifies content based on user queries',
        inputSchema: {
            prompt: z.string().describe('The query or task to perform on Notion')
        },
        outputSchema: { output: z.string() }
    },
    async ({ prompt }) => {
        const anthropicKey = process.env.ANTHROPIC_API_KEY;
        const notionKey = process.env.NOTION_API_KEY;

        if (!anthropicKey) {
            throw new Error('ANTHROPIC_API_KEY not configured');
        }
        if (!notionKey) {
            throw new Error('NOTION_API_KEY not configured');
        }

        const fullPrompt = `${prompt}

IMPORTANT: Execute the request, don't just explain how to do it.
Use the read-data-notion-api skill for reading and write-data-notion-api skill for writing.
Before each API call, use the notion-rate-limiter-gatekeeper skill.
The NOTION_API_KEY env var is defined - use it in curl requests with: -H "Authorization: Bearer $NOTION_API_KEY"`;

        const output = await runDockerAgent(fullPrompt, anthropicKey, notionKey);

        return {
            content: [{ type: 'text', text: output }],
            structuredContent: { output }
        };
    }
);

function runDockerAgent(prompt, anthropicKey, notionKey) {
    return new Promise((resolve, reject) => {
        const args = [
            'run',
            '--rm',
            '-e', `ANTHROPIC_API_KEY=${anthropicKey}`,
            '-e', `NOTION_API_KEY=${notionKey}`,
            DOCKER_IMAGE,
            prompt
        ];

        const proc = spawn(DOCKER_PATH, args, {
            stdio: ['ignore', 'pipe', 'pipe']
        });

        let stdout = '';
        let stderr = '';

        proc.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        proc.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        proc.on('close', (code) => {
            if (code === 0) {
                resolve(stdout.trim() || 'No output');
            } else {
                reject(new Error(stderr || `Docker process exited with code ${code}`));
            }
        });

        proc.on('error', (err) => {
            reject(new Error(`Failed to spawn docker: ${err.message}`));
        });
    });
}

const transport = new StdioServerTransport();
await server.connect(transport);