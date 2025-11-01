from backend.services.vectore_store import VectorStore
from langchain_core.documents import Document

# Create a Document object
doc = Document(page_content="This is the content of my document.",
               metadata={"source": "my_file.txt", "page": 1})

# You can then access its attributes
print(f"Page Content: {doc.page_content}")
print(f"Metadata: {doc.metadata}")
def test_vector_store():
    # Initialize vector store
    try:
        vs = VectorStore()
        print("✅ Vector store initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing vector store: {str(e)}")
        return

    # Test document addition
    try:
        # Create sample documents
        docs = [
    Document(
        page_content="Machine learning is a subset of artificial intelligence",
        metadata={"source": "test1.txt", "page": 1}
    ),
    Document(
        page_content="Python is a popular programming language",
        metadata={"source": "test2.txt", "page": 1}
    ),
    Document(
        page_content="Data science involves statistics, programming, and domain expertise",
        metadata={"source": "test3.txt", "page": 1}
    ),
    Document(
        page_content="Natural language processing enables computers to understand human language",
        metadata={"source": "test4.txt", "page": 1}
    ),
    Document(
        page_content="Deep learning uses neural networks with many layers",
        metadata={"source": "test5.txt", "page": 1}
    ),
    Document(
        page_content="Supervised learning requires labeled data for training",
        metadata={"source": "test6.txt", "page": 1}
    ),
    Document(
        page_content="Unsupervised learning finds hidden patterns in data",
        metadata={"source": "test7.txt", "page": 1}
    ),
    Document(
        page_content="Reinforcement learning trains agents through rewards and penalties",
        metadata={"source": "test8.txt", "page": 1}
    ),
    Document(
        page_content="Big data technologies help process large volumes of information",
        metadata={"source": "test9.txt", "page": 1}
    ),
    Document(
        page_content="Cloud computing provides scalable resources over the internet",
        metadata={"source": "test10.txt", "page": 1}
    ),
    Document(
        page_content="Cybersecurity protects systems and data from digital attacks",
        metadata={"source": "test11.txt", "page": 1}
    ),
    Document(
        page_content="Blockchain is a decentralized ledger technology",
        metadata={"source": "test12.txt", "page": 1}
    )
]
        
        # Add documents
        vs.add_documents(docs)
        print("✅ Documents added successfully")
    except Exception as e:
        print(f"❌ Error adding documents: {str(e)}")
        return

    # Test search functionality
    try:
        # Perform a search
        query = "What is machine learning?"
        results = vs.search(query, top_k=2)
        print("\n✅ Search successful")
        print(f"Query: '{query}'")
        print("Results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. Source: {result['source']}, Page: {result['page']}")
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")

if __name__ == "__main__":
    test_vector_store()