"""
Example usage of the SimpleAIAgent with Groq API
"""

from agent import SimpleAIAgent

def main():
    # Create an agent with default system prompt (Groq-powered)
    agent = SimpleAIAgent()
    
    # Example 1: Single task execution
    print("=" * 50)
    print("Example 1: Single Task Execution (Using Groq)")
    print("=" * 50)
    task1 = "What are the steps to make a simple Python API?"
    print(f"Task: {task1}\n")
    response1 = agent.execute_task(task1)
    print(f"Response:\n{response1}\n")
    
    # Example 2: Another task (conversation continues)
    print("=" * 50)
    print("Example 2: Follow-up Question (Maintains Context)")
    print("=" * 50)
    task2 = "Can you provide a code example for the first step?"
    print(f"Task: {task2}\n")
    response2 = agent.execute_task(task2)
    print(f"Response:\n{response2}\n")
    
    # Example 3: Custom system prompt
    print("=" * 50)
    print("Example 3: Custom System Prompt")
    print("=" * 50)
    
    custom_prompt = """You are a Python expert assistant. 
When answering questions, always provide:
1. A clear explanation
2. Code examples when relevant
3. Best practices and tips

Focus on practical, production-ready solutions."""
    
    agent2 = SimpleAIAgent(system_prompt=custom_prompt)
    task3 = "How do I handle errors in Python?"
    print(f"Task: {task3}\n")
    response3 = agent2.execute_task(task3)
    print(f"Response:\n{response3}\n")
    
    # Example 4: Interactive conversation
    print("=" * 50)
    print("Example 4: Start Interactive Conversation")
    print("=" * 50)
    print("Starting interactive mode...\n")
    agent.multi_turn_conversation()

if __name__ == "__main__":
    main()
