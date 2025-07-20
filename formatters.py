from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="supabase")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)



def deleteMemory(user_id):
    result = supabase.rpc('delete_user_memories', {'user_id_param': user_id}).execute()
    return result.data



