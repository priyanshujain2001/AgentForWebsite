from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from scrape_website import WebScraper  # Assuming scrape_url.py has the WebScraper class
from vector_db import VectorCli
from completion import generate_answer_with_citations  # Placeholder for your answer generation function
import traceback
import json 
from flask_httpauth import HTTPBasicAuth 
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
auth = HTTPBasicAuth()
db = VectorCli()  # Initialize your FAISS vector database


@app.route('/api/v1/index', methods=['POST'])
def index_url():
    auth = request.authorization
    if not auth or not (auth.username == 'your_username' and auth.password == 'your_password'):
        return jsonify({"message": "Unauthorized"}), 401
    data = request.json
    urls = data.get('url', [])
    scraper = WebScraper(urls)  # Initialize web scraper with the provided URLs

    indexed_urls = []
    failed_urls = []

    # Scrape and index content from each URL
    for url in urls:
        try:
            result = scraper.scrape_and_chunk()  # Scrape and chunk the content
            texts = [chunk['text'] for chunk in result]  # Extract text chunks
            tags = {"base_url": url}  # Use the URL as a tag
            db.update_index(texts, tags)  # Update index with scraped texts and tags
            indexed_urls.append(url)
        except Exception as e:
            print("traceback", traceback.format_exc())
            failed_urls.append(url)  # Handle any exceptions

    return jsonify({
        "status": "success",
        "indexed_urls": indexed_urls,
        "failed_urls": failed_urls if failed_urls else None
    })


@app.route('/api/v1/chat', methods=['POST'])
def chat_answer():
    auth = request.authorization
    if not auth or not (auth.username == 'your_username' and auth.password == 'your_password'):
        return jsonify({"message": "Unauthorized"}), 401
    try:
        data = request.json
        messages = data.get("messages", [])
        
        user_questions = [msg['content'] for msg in messages if msg['role'] == 'user']
        final_query = ", ".join(user_questions)  # Create a single comma-separated string of user questions
        
        # Retrieve relevant context from the vector database
        context = db.retriever(final_query)  # Use the query method to get context    
        
        # Generate an answer with citations
        response, citations = generate_answer_with_citations(json.dumps(messages), context)
        
        return jsonify({
            "response": [{
                "answer": {
                    "content": response,
                    "role": "assistant"
                }
            }],
            "citation": citations
        })
    except Exception as e:
        return {}, 500


if __name__ == "__main__":
    app.run(debug=True, port=8081)  # Flask CORS should be handled separately using Flask-CORS package