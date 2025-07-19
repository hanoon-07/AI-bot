from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from mem0 import Memory
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o-mini", temperature=0.7)

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": os.getenv('MODEL_CHOICE', 'gpt-4o-mini')
        }
    },
    "vector_store": {
        "provider": "supabase",
        "config": {
            "connection_string": os.environ['DATABASE_URL'],
            "collection_name": "memories"
        }
    }    
}
memory = Memory.from_config(config)

def chat_with_memory(user_message, user_id="user1"):
    memories = memory.search(query=user_message, user_id=user_id, limit=3)
    memory_context = "\n".join([m['memory'] for m in memories.get('results', [])])

    messages = [
        SystemMessage(content=f"""You are a helpful assistant. Use these memories to personalize your responses:
        
Previous memories:
{memory_context}

Be conversational and remember what the user has told you."""),

        HumanMessage(content=user_message)
    ]

    response = llm.invoke(messages)
    ai_response = response.content

    memory.add([
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ai_response}
    ], user_id=user_id)

    return ai_response

# Interface
print("🤖 Chatbot with Memory Started!")
print("Type 'quit' to exit")
print("-" * 40)


while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("👋 Goodbye!")
        break

    if user_input:
        try:
            response = chat_with_memory(user_input)
            print(f"🤖 Bot: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
