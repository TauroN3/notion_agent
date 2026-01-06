FROM node:25-bookworm

RUN apt update && \
    apt upgrade -y && \
    apt install -y curl git bash && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash appuser

RUN npm install -g @anthropic-ai/claude-code

WORKDIR /app

RUN mkdir -p /home/appuser/.claude/skills /home/appuser/.claude/agents && \
    chown -R appuser:appuser /home/appuser/.claude

COPY skills/ /home/appuser/.claude/skills/
COPY agents/ /home/appuser/.claude/agents/
COPY settings.json /home/appuser/.claude/settings.json

RUN chown -R appuser:appuser /app

USER appuser

ENV HOME=/home/appuser

ENV ANTHROPIC_API_KEY=""
ENV NOTION_API_KEY=""

ENTRYPOINT ["claude", "--dangerously-skip-permissions", "-p"]