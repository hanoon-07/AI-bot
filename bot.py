from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from mem0 import Memory
import os
from dotenv import load_dotenv
from io_utils import get_user_info, fetch_service_info
from formatters import deleteMemory

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

def chat_with_memory(user_message, user_id="default"):
    memories = memory.search(query=user_message, user_id=user_id, limit=3)
    memory_context = "\n".join([m['memory'] for m in memories.get('results', [])])

    userInfo = get_user_info(user_id)
    faq = fetch_service_info()

    messages = [
        SystemMessage(content=f"""
                    You are a helpful assistant for a company called Cafu:
                    here are some faqs
                    {faq}
                    this is info about the user
                    {userInfo}
                    Previous memories:
                    {memory_context}

                    Act just like a app assistant ."""),

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
id=input("enter your id to get started please")

print("🤖 Chatbot with Memory Started!")
print("Type 'quit' to exit")
print("-" * 40)


while True:

    user_input = input("\nYou: ").strip()
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("👋 Goodbye!")
        break

    if user_input.lower()=="delete":
        print("deleting your memory")
        deleteMemory(id)
        continue

    if user_input:
        try:
            response = chat_with_memory(user_input,id)
            print(f"🤖 Bot: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
