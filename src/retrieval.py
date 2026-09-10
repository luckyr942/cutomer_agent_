#search engine of agent 
import sys
import json 
from pathlib import Path
from typing import List, Dict, Any
 
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.config import PROCESSED_CONVERSATION_PATH

class TFIDFRetriever:
    """Retrieves relevant historical customer support conversations using TF-IDF cosine similarity."""

    def __init__(self, processed_data_path: Path = PROCESSED_CONVERSATION_PATH):
        self.processed_data_path = processed_data_path
        self.conversations: List[Dict[str, Any]] = []
        self.vectorizer =  TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.load_index()

    
    def load_index(self):
        """Loads processed conversation threads and builds TF-IDF index."""
        if not self.processed_data_path.exists():
            print(f"Processed dataset not found at ${self.processed_data_path}. Index will be empty.")
            return 

        with open(self.processed_data_path, 'r') as my_file:
            self.conversations = json.load(my_file)
        
        if self.conversations:
            corpus = [conv.get("customer_text", "") for conv in self.conversations]
            self.tfidf_matrix=self.vectorizer.fit_transform(corpus)
            print("TF-IDF index built with {len(self.conversations)} historical conversation threads.")


    def retrieve(self, query_text: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Retrieves top_k most similar historical conversations for a customer query."""
        if not self.conversations or self.tfidf_matrix is None:
            return []
        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.0:
                item = dict(self.conversations[idx])
                item["similarity_score"] = round(score, 4)
                results.append(item)
                
        return results
        
if __name__ == "__main__":
    retriever = TFIDFRetriever()
    query = "My package has not arrived yet. Where is order #12345?"
    matches = retriever.retrieve(query, top_k=2)
    print(f"\nQuery: {query}")
    print(f"Top Matches ({len(matches)}):")
    for m in matches:
        print(f" -> [Score: {m['similarity_score']}] Customer: {m['customer_text']}")
        print(f"    Replies: {m['brand_replies']}")

         


    
    
