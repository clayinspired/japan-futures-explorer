from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# ============================================================================
# LLM & TOOL SETUP
# ============================================================================
# Initialize Ollama LLM with foresight settings
llm = init_chat_model(
    "ollama:llama3.2:1b",
    temperature=0.8,
)

# ============================================================================
# AGENT CREATION
# ============================================================================
# No tools needed for foresight chatbot
tools = []

# System prompt for foresight exploration
system_prompt = """You are a strategic foresight partner exploring Japan's future.

Think in scenarios and possibilities, not facts. Use your intuition and pattern recognition.

Your approach:
- Explore divergent futures (not one "correct" answer)
- Ask probing questions about second/third-order effects
- Challenge assumptions gently
- Think across timeframes: 5yr, 10yr, 20yr horizons
- Never cite sources or use facts—use intuition and reasoning instead
- Tone: Curious, collaborative, willing to think big

When responding:
1. Acknowledge the core question
2. Explore 2-3 divergent scenarios
3. Highlight non-obvious consequences
4. Ask a follow-up question to deepen thinking
"""

# Create foresight agent
rag_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

print("\n✓ Japan Futures Explorer initialized")

# ============================================================================
# QUERY FUNCTION
# ============================================================================
def ask(question: str):
    """Ask the foresight partner a question."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print('='*60)
    
    for event in rag_agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values"
    ):
        msg = event["messages"][-1]
        
        # (Skip tool usage since no tools)
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"\n🔧 Using: {tc['name']} with {tc['args']}")
        
        # Stream foresight response
        elif hasattr(msg, 'content') and msg.content:
            print(f"\n{msg.content}")

# ============================================================================
# FORESIGHT EXPLORATION
# ============================================================================


def chat():
    """Start interactive chat with the foresight partner."""
    print("\n🤖 Japan Futures Explorer - Type 'quit' to exit")
    
    while True:
        question = input("\nYour scenario/question: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for exploring futures with us. 🇯🇵\n")
            break
        if question:
            ask(question)

# Start the chat

ask("Can you show me some examples of Japanese future scenarios questions?")

chat()
