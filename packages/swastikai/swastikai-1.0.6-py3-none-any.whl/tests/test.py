from swastikai.memory import personal_memory

api_key_value = "cgy_tt91Qj05Qi1cHiEkAbPUFFpFt84NaLCQj4tfP7oB2RwA4RZX70pu0Co4JtF8A7mu"

def test_get_request():
    client = personal_memory(api_key=api_key_value)
    paylod = {
        "agent_details": {
        "company_id": "Deloitte",
        "department_id": "Analytics",
        "team_id": "Dev Team",
        "agent_id": "RAG_123",
        "user_id": "Chirotpal",
        "agent_type": "iA",
        "agent_description": "This is a very helpful personal assisstant.",
        "system_prompt": ""
        },
        "memories": "",
        "last_user_prompt": "I love mangoes",
        "last_ai_response": "",
        "chat_history": [],
        "memory_category": "personal_memory"
        }

    response = client.retrieve_memory(paylod)
    print(response["memories"])

def get_balance():
    client = personal_memory(api_key=api_key_value)
    response = client.get_account_balance()
    print(response["credit_balance"])

#test_get_request()
get_balance()


