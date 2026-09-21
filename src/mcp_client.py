from __future__ import annotations

import json
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.config import MCP_SERVER_PATH, ROOT_DIR


class TravelMCPClient:
    """Short-lived stdio MCP client used by the UI and CLI."""

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[str(MCP_SERVER_PATH)],
            cwd=str(ROOT_DIR),
        )
        try:
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    available = await session.list_tools()
                    names = {tool.name for tool in available.tools}
                    if name not in names:
                        return {"status": "error", "message": f"MCP tool '{name}' not found."}
                    result = await session.call_tool(name, arguments=arguments)
        except Exception as exc:
            return {
                "status": "error",
                "message": f"MCP server unavailable: {type(exc).__name__}",
            }

        for item in result.content:
            text = getattr(item, "text", None)
            if text:
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"status": "success", "text": text}
        return {"status": "error", "message": "MCP tool returned no text content."}
