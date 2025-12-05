# Simple Search Engine

A fully functional search engine built from scratch using Python, demonstrating core information retrieval concepts.

## 🎯 What This Project is About

This project implements the **fundamental concepts** that power all search engines:

1. **Inverted Index** - Maps words to documents (the core data structure)
2. **TF-IDF Ranking** - Calculates document relevance scores
3. **Tokenization** - Breaks text into searchable words
4. **Query Processing** - Handles search queries and finds matches
5. **RESTful API Design** - Exposes search functionality via HTTP

## 🏗️ Architecture

```
Frontend (HTML/JS) → FastAPI Backend → Search Engine Core → Inverted Index
```

### Components

- **`search_engine.py`** - Core search logic (indexing, TF-IDF, ranking)
- **`main.py`** - FastAPI REST API endpoints
- **`index.html`** - Web interface for searching
- **`sample_documents.py`** - Pre-loaded sample documents

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

### 3. Open in Browser

Navigate to: `http://localhost:8000`

The server will automatically load 10 sample documents about programming topics.

## 📚 API Endpoints

### Search Documents
```
GET /search?q=python&top_k=10
```

Returns ranked search results for the query.

### Add Document
```
POST /documents
Content-Type: application/json

{
  "title": "My Document",
  "content": "Document content here..."
}
```

Adds a new document to the search index.

### Get All Documents
```
GET /documents
```

Returns all indexed documents.

### Get Statistics
```
GET /stats
```

Returns search engine statistics (total documents, words, etc.).

### Interactive API Documentation
Visit `http://localhost:8000/docs` for automatic Swagger UI documentation.

## 🔍 How It Works

### 1. Indexing Process

When you add a document:

1. **Tokenization**: Text is broken into words (lowercase, punctuation removed)
2. **Inverted Index Building**: For each word, we record which documents contain it
3. **Statistics**: We track word frequencies for TF-IDF calculations

**Example:**
```
Document 1: "Python is great"
Document 2: "Python web apps"

Inverted Index:
"python" → [Doc1, Doc2]
"great" → [Doc1]
"web" → [Doc2]
"apps" → [Doc2]
```

### 2. Search Process

When you search for "python":

1. **Query Tokenization**: "python" → ["python"]
2. **Find Candidates**: Use inverted index to find documents containing "python"
3. **Calculate Scores**: For each candidate, calculate TF-IDF score
4. **Rank Results**: Sort by score (highest first)
5. **Return Top K**: Return the top results

### 3. TF-IDF Scoring

**TF (Term Frequency)**: How often a word appears in a document
```
TF = count(word in document) / total words in document
```

**IDF (Inverse Document Frequency)**: How rare/common a word is
```
IDF = log(total documents / documents containing word)
```

**TF-IDF Score**: 
```
Score = TF × IDF
```

**Why this works:**
- Common words (like "the", "is") have low IDF → low scores
- Rare, relevant words have high IDF → high scores
- Documents with more occurrences of query words get higher TF → higher scores

## 🎓 Key Concepts Explained

### Inverted Index

Instead of storing: `Document → Words`
We store: `Word → Documents`

**Why?** Searching becomes O(1) lookup instead of scanning all documents!

### Tokenization

Breaking text into searchable units:
- "Python is great!" → ["python", "is", "great"]
- Handles: lowercase conversion, punctuation removal, whitespace splitting

### Ranking

Not all matches are equal. TF-IDF scores documents by:
- **Relevance**: How well does it match the query?
- **Importance**: How important are the matching words?
- **Quality**: Documents with more relevant content rank higher

## 🔧 Customization

### Add More Documents

Use the web interface or API:
```python
POST /documents
{
  "title": "Your Title",
  "content": "Your content here..."
}
```

### Adjust Ranking

Modify the `_calculate_tfidf` method in `search_engine.py` to experiment with different scoring algorithms.

### Change Top K Results

Modify the `top_k` parameter in the search endpoint (default: 10).

## 🚀 Next Steps / Extensions

Want to extend this? Here are ideas:

1. **BM25 Ranking** - Improved ranking algorithm (better than TF-IDF)
2. **Vector Embeddings** - Semantic search using word embeddings
3. **Database Storage** - Persist index to database (SQLite, PostgreSQL)
4. **Autocomplete** - Suggest queries as user types
5. **Faceted Search** - Filter by categories/tags
6. **Multi-field Search** - Search in title, content, tags separately
7. **Fuzzy Matching** - Handle typos and misspellings
8. **Pagination** - Handle large result sets
9. **Caching** - Cache frequent queries
10. **Distributed Search** - Scale across multiple servers


## 🐛 Troubleshooting

**Port already in use?**
```bash
uvicorn main:app --port 8001
```

**CORS errors?**
The frontend is configured to work with `localhost:8000`. If using a different port, update `API_BASE` in `index.html`.

**No results?**
Make sure sample documents loaded. Check server logs on startup.

## 📝 License

Feel free to use and modify as needed!

---


