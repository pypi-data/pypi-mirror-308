from swastikai.memory import personal_memory

def test_get_request():
    client = personal_memory(api_key="SWK_API_KEY")
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

test_get_request()