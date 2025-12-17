import requests
import time
import sys

BASE_URL = "http://localhost:8000/api"

def test_ingest():
    print("Testing Ingestion...")
    try:
        response = requests.post(f"{BASE_URL}/ingest")
        if response.status_code == 200:
            print(f"Success: {response.json()}")
            return True
        else:
            print(f"Failed: {response.text}")
            return False
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def test_query(question):
    print(f"Testing Query: {question}")
    try:
        response = requests.post(f"{BASE_URL}/query", json={"query": question})
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data['answer']}")
            print("Sources:")
            for src in data['sources']:
                print(f" - {src['source']} (Page {src['page']})")
            return True
        else:
            print(f"Failed: {response.text}")
            return False
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def main():
    # Wait for server to be up
    print("Waiting for server...")
    for _ in range(10):
        try:
            r = requests.get("http://localhost:8000/")
            if r.status_code == 200:
                print("Server is up!")
                break
        except:
            time.sleep(2)
    else:
        print("Server failed to start.")
        return

    if test_ingest():
        test_query("What involves a retriever and generator?")
        test_query("Who created Python?")

if __name__ == "__main__":
    main()
