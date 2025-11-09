import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { query } from '@anthropic-ai/claude-agent-sdk';

const server = new McpServer({
    name: 'notion-shell',
    version: '1.0.0'
});

server.registerTool(
    'notion_shell',
    {
        title: 'Notion Shell',
        description: 'For every notion-related query or task use this tool, raw prompts as input',
        inputSchema: {
            prompt: z.string(),
            working_dir: z.string().optional()
        },
        outputSchema: { output: z.string() }
    },
    async ({ prompt, working_dir }) => {
        if (!process.env.ANTHROPIC_API_KEY) {
            throw new Error('ANTHROPIC_API_KEY not configured');
        }

        const fullPrompt = `${prompt}\n\nUse notion-api skill and env var named NOTION_API_KEY is defined, use it in curl.`;

        const agentOptions = {
            cwd: working_dir || process.cwd(),
            settingSources: ['user'],
            permissionMode: 'bypassPermissions'
        };

        let output = '';
        let finalResult = null;

        for await (const message of query({ prompt: fullPrompt, options: agentOptions })) {
            if (message.type === 'assistant' && message.message?.content) {
                for (const block of message.message.content) {
                    if (block.type === 'text' && block.text) {
                        output += block.text;
                    }
                }
            }
            if (message.type === 'result' && message.result) {
                finalResult = message.result;
            }
        }

        const result = { output: (finalResult || output).trim() || 'No output' };
        return {
            content: [{ type: 'text', text: JSON.stringify(result) }],
            structuredContent: result
        };
    }
);

const transport = new StdioServerTransport();
await server.connect(transport);
