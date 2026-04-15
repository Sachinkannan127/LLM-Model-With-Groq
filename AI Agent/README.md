# Simple AI Agent with Groq

A lightweight Python AI agent powered by Groq's API. This agent can execute tasks autonomously, maintain conversation context, and be customized with different system prompts.

## Features

- **Task Execution**: Execute single tasks or queries with Groq
- **Conversation History**: Maintains context across multiple turns
- **Custom System Prompts**: Configure the agent's behavior and expertise
- **Interactive Mode**: Start interactive conversations with the agent
- **Streamlit Web App**: Run the agent in a browser-based chat interface
- **Easy to Extend**: Simple architecture for adding custom features

## Prerequisites

- Python 3.8+
- A Groq API key (get one at https://console.groq.com)

## Setup

1. **Clone the repository** (or copy the files to your project)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key**:
   ```bash
   # On Windows (PowerShell)
   $env:GROQ_API_KEY="your-api-key-here"
   
   # On Windows (Command Prompt)
   set GROQ_API_KEY=your-api-key-here
   
   # On macOS/Linux
   export GROQ_API_KEY="your-api-key-here"
   ```

## Usage

### Basic Usage

```python
from agent import SimpleAIAgent

# Create an agent
agent = SimpleAIAgent()

# Execute a task
response = agent.execute_task("What is machine learning?")
print(response)
```

### Custom System Prompt

```python
custom_prompt = """You are a Python expert. 
Provide clear explanations and code examples."""

agent = SimpleAIAgent(system_prompt=custom_prompt)
response = agent.execute_task("How do I use decorators in Python?")
print(response)
```

### Interactive Conversation

```python
agent = SimpleAIAgent()
agent.multi_turn_conversation()  # Start interactive mode
```

### Run Command Line Examples

```bash
python main.py
```

### Run the Streamlit Web App

```bash
streamlit run app.py
```

The app provides:
1. A chat-style interface
2. Sidebar controls for model, temperature, max tokens, and history window
3. Custom system prompt editing
4. Conversation clearing without restarting the app

This will run four examples:
1. Single task execution
2. Follow-up question with context
3. Custom system prompt
4. Interactive conversation mode

## Project Structure

```
.
├── app.py            # Streamlit web app
├── agent.py           # Main agent class
├── main.py            # CLI example usage
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## API Reference

### SimpleAIAgent

#### `__init__(system_prompt=None)`
Initialize the agent with an optional custom system prompt.

#### `execute_task(task, temperature=0.7)`
Execute a single task and return the response. Context is maintained in conversation history.

**Parameters:**
- `task` (str): The task or question
- `temperature` (float): Controls randomness (0.0-1.0)

#### `multi_turn_conversation()`
Start an interactive conversation mode where you can chat with the agent.

#### `clear_history()`
Clear the conversation history.

#### `get_conversation_summary()`
Get the number of messages in the conversation history.

## Tips

- **Temperature**: Lower values (0.0-0.3) for focused, deterministic responses; higher values (0.7-1.0) for creative outputs
- **Context**: The agent maintains conversation history for multi-turn interactions
- **Custom Prompts**: Different system prompts can make the agent specialized (e.g., Python expert, writer, analyst)

## Costs

Groq API calls are billed based on tokens. Check [Groq's pricing](https://groq.com/pricing/) for current rates.

## Support

For issues with the Groq API, visit: https://console.groq.com/docs

## License

This project is provided as-is for learning and development purposes.
