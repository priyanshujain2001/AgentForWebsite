# README.md

# Project Title: AI-Powered URL Indexer and Chatbot

## Description
This project is an AI-based application that allows users to scrape content from specified URLs, index it for faster retrieval, and interact with an AI chatbot that can answer questions based on the scraped content.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirment.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following entries:
   ```
   pinecone_api_key=<your_pinecone_api_key>
   jina_api_key=<your_jina_api_key>
   GEMINI_API_KEY=<your_gemini_api_key>
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

## API Usage Examples

### 1. Index URLs
**Endpoint**: `/api/v1/index`  
**Method**: `POST`  
**Request**:
```json
{
    "url": ["http://example1.com", "http://example2.com"]
}
```
**Response**:
```json
{
    "status": "success",
    "indexed_urls": ["http://example1.com", "http://example2.com"],
    "failed_urls": null
}
```

### 2. Chat with the Assistant
**Endpoint**: `/api/v1/chat`  
**Method**: `POST`  
**Request**:
```json
{
    "messages": [
        {"content": "What is the main topic of the first URL?", "role": "user"},
        {"content": "Tell me more about the second URL.", "role": "user"}
    ]
}
```
**Response**:
```json
{
    "response": [
        {
            "answer": {
                "content": "The main topic of the first URL is about...",
                "role": "assistant"
            }
        }
    ],
    "citation": ["http://example1.com", "http://example2.com"]
}
```

## Brief Report

### Approach
The project combines web scraping, natural language processing, and an AI model to create a responsive chatbot. The setup involves using Flask for building APIs, BeautifulSoup for web scraping, and Pinecone for vector storage and retrieval.

### Challenges Faced
- **API Integration**: Configuring third-party APIs (such as Pinecone and Jina) required careful attention to their documentation.
- **Error Handling**: Constructing robust error handling for various stages of the process to ensure graceful degradation in case of failures.

### Potential Improvements
- **Enhanced Scraping Logic**: Implementing more advanced content extraction techniques to gather richer data from web pages.
- **User Authentication**: Adding a more secure user authentication system to safeguard API access.
- Saving all results in databas for further debugging.
- applying check on indexing so that no indexes text should be same.
- caching of embeddings queries.
- making this proactive 
- adjust tone and length as per user 
- **Front-end Enhancements**: Improving the frontend interface for better user experience and interactivity.


