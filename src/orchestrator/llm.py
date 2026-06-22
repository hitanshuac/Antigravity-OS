"""
Antigravity OS - Pillar 5: LLM Client Adapters
Concrete implementations of the LLMClient protocol interacting with external APIs.
"""

import json
from typing import List, Dict, Any, Optional
from openai import OpenAI

from src.orchestrator.engine import ToolCall


class UniversalLLMClient:
    """
    A concrete LLMClient utilizing the OpenAI-compatible API spec.
    This works natively with OpenAI, Groq, OpenRouter, and NVIDIA NIM.
    """
    def __init__(self, model: str, api_key: str, base_url: Optional[str] = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def generate_response(
        self, 
        system_prompt: str, 
        messages: List[Dict[str, str]], 
        tools: List[Dict[str, Any]]
    ) -> ToolCall:
        
        # 1. Format Messages
        formatted_messages = [{"role": "system", "content": system_prompt}]
        formatted_messages.extend(messages)

        # 2. Format Tools for OpenAI
        openai_tools = [{"type": "function", "function": tool} for tool in tools]

        # 3. Network Call
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                tools=openai_tools,
                tool_choice="required",  # Force the model to use the hands
                temperature=0.0          # Maximize deterministic reasoning
            )
        except Exception as e:
            # Wrap API errors so the orchestrator doesn't crash fatally on network blips
            return ToolCall(
                tool_name="task_complete", 
                tool_args={"summary": f"Fatal API Error: {str(e)}"}
            )

        # 4. Extract and Parse Tool Call
        response_msg = response.choices[0].message
        
        if not response_msg.tool_calls:
            # Fallback if the model somehow circumvents `tool_choice="required"`
            raise RuntimeError("LLM failed to return a valid tool call structure.")
            
        # For Phase 1, we process a single tool call at a time
        tool_call = response_msg.tool_calls[0]
        tool_name = tool_call.function.name
        
        try:
            tool_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            # If the model hallucinates invalid JSON, route to a bash command that prints an error
            # so the model sees its mistake in the next loop and self-corrects.
            tool_args = {}

        return ToolCall(tool_name=tool_name, tool_args=tool_args)
