"""Simple AI Agent using Groq API
Autonomous agent that can execute tasks and interact with Groq
"""

import os
import re
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SimpleAIAgent:
    """A simple autonomous AI agent powered by Claude."""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initialize the AI agent.
        
        Args:
            system_prompt: Custom system prompt for the agent. 
                         If None, uses a default autonomous agent prompt.
        """
        self.client = Groq()
        self.conversation_history = []
        self.default_model = "llama-3.1-8b-instant"
        
        if system_prompt is None:
            system_prompt = """You are a helpful AI agent designed to assist with various tasks.
You can help with:
- Answering questions
- Generating ideas and solutions
- Writing and editing content
- Analyzing information
- Solving problems step by step

Be clear, concise, and helpful in your responses.
When mentioning topic or subtopic, format both label and value in bold markdown.
Example:
**Topic:** **Python**
**Subtopic:** **Error Handling**"""
        
        self.system_prompt = system_prompt
    
    def execute_task(
        self,
        task: str,
        temperature: float = 0.7,
        model: Optional[str] = None,
        max_tokens: int = 512,
        history_window: int = 8,
    ) -> str:
        """
        Execute a single task or query.
        
        Args:
            task: The task or question for the agent
            temperature: Controls randomness (0.0-1.0). Higher = more creative
            
        Returns:
            The agent's response
        """
        self.conversation_history.append({
            "role": "user",
            "content": task
        })

        # Keep only recent turns for lower latency while preserving short-term context.
        max_messages = max(2, history_window * 2)
        recent_history = self.conversation_history[-max_messages:]
        messages = [{"role": "system", "content": self.system_prompt}] + recent_history
        
        response = self.client.chat.completions.create(
            model=model or self.default_model,
            max_tokens=max_tokens,
            messages=messages,
            temperature=temperature
        )
        
        assistant_message = response.choices[0].message.content
        assistant_message = self._bold_topic_subtopic_lines(assistant_message)
        
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message

    def _bold_topic_subtopic_lines(self, text: str) -> str:
        """Normalize Topic/Subtopic lines so labels and values are bold."""
        pattern = re.compile(
            r"^(\s*(?:[-*]\s+)?)\*\*?(topic|subtopic)\*\*?(\s*[:\-]\s*)(.+)$",
            re.IGNORECASE,
        )
        formatted_lines = []

        for line in text.splitlines():
            match = pattern.match(line)
            if match:
                prefix, label, _, value = match.groups()
                formatted_lines.append(f"{prefix}**{label.title()}:** **{value.strip()}**")
            else:
                formatted_lines.append(line)

        return "\n".join(formatted_lines)
    
    def multi_turn_conversation(self):
        """Start an interactive multi-turn conversation with the agent."""
        print("AI Agent started. Type 'exit' to quit.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'exit':
                print("Exiting agent. Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = self.execute_task(user_input)
            print(f"\nAgent: {response}\n")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> int:
        """Get the number of messages in conversation history."""
        return len(self.conversation_history)
