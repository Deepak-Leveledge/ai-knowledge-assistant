from backend.database.mongo import save_chat, get_user_docs



def test_save_chat():
    test_user_id = "test_user"
    
    try:
        save_chat(user_id=test_user_id, question="What is machine learning?", answer="machinf is a subfeaild of AI.")
        print("chat is saved successfully.")
    except Exception as e:
        print(f"Error saving chat: {e}")


def test_get_user_docs():
    test_user_id = "test_user"
    try:
        docs= get_user_docs(user_id=test_user_id)
        print(f"Retrieved {len(docs)} documents for user {test_user_id}.")
        print(docs)
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        
        
if __name__ == "__main__":
    # test_save_chat()
    test_get_user_docs()


    