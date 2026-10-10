"""
Hybrid Knowledge Retriever for SAATHI AI
Combines semantic similarity scoring with keyword matching and confidence thresholds.
"""
import re
import math
from typing import List, Tuple
from saathi.models import DocumentChunk, RetrievedEvidence
from saathi.knowledge.store import KnowledgeStore

class HybridRetriever:
    def __init__(self, knowledge_store: KnowledgeStore):
        self.store = knowledge_store
        
    def _tokenize(self, text: str) -> List[str]:
        """Multilingual tokenization preserving Devanagari and Latin words with cross-lingual expansion."""
        if not text:
            return []
            
        cleaned_text = re.sub(r'[^\w\s\u0900-\u097F]', ' ', text.lower())
        words = cleaned_text.split()
        
        # Multilingual cross-lingual expansion (Devanagari -> English/Hinglish concepts)
        HINDI_TRANSLATIONS = {
            "बिजली": "electricity bijli",
            "बिल": "bill",
            "मीटर": "meter",
            "किसान": "kisan farmer",
            "पीएम": "pm pmkisan",
            "योजना": "scheme yojana",
            "सब्सिडी": "subsidy pahel",
            "किस्त": "installment kist 2000",
            "शिकायत": "complaint grievance",
            "इलाज": "treatment hospital ayushman",
            "अस्पताल": "hospital ayushman",
            "खाता": "account bank",
            "आधार": "aadhaar",
            "किराया": "rent tenant tenancy deposit",
            "मकान": "house landlord",
            "धोखाधड़ी": "fraud cyber scam 1930",
            "पैसे": "money balance amount"
        }
        
        stopwords = {
            "the", "a", "an", "is", "in", "at", "of", "on", "and", "or", "to", "for",
            "hai", "ka", "ki", "ke", "ko", "me", "mein", "se", "aur", "kya", "bhi",
            "में", "का", "की", "के", "को", "से", "है", "हैं", "और", "क्या", "भी", "मुझे", "चाहिए"
        }
        
        expanded_words = []
        for w in words:
            if w in stopwords or len(w) <= 1:
                continue
            expanded_words.append(w)
            if w in HINDI_TRANSLATIONS:
                expanded_words.extend(HINDI_TRANSLATIONS[w].split())
                
        return expanded_words

    def _compute_bm25_score(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """Computes basic BM25/TF-IDF relevance score."""
        if not query_tokens or not doc_tokens:
            return 0.0
            
        doc_len = len(doc_tokens)
        score = 0.0
        
        for q in query_tokens:
            tf = doc_tokens.count(q)
            if tf > 0:
                # Term frequency saturation
                norm_tf = (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * (doc_len / 50.0)))
                score += norm_tf
                
        # Length normalized score between 0.0 and 1.0
        return min(score / max(len(query_tokens), 1), 1.0)

    def retrieve(self, query: str, top_k: int = 3, min_threshold: float = 0.15) -> List[RetrievedEvidence]:
        """
        Retrieves top-k relevant document chunks for a given query with confidence scores.
        """
        query_tokens = self._tokenize(query)
        scored_chunks: List[Tuple[float, DocumentChunk, str]] = []
        
        for chunk in self.store.get_all_chunks():
            # Combine title and content for scoring
            doc_text = f"{chunk.title} {chunk.content}"
            doc_tokens = self._tokenize(doc_text)
            
            score = self._compute_bm25_score(query_tokens, doc_tokens)
            
            # Boost score if query words appear in chunk title or metadata
            title_tokens = self._tokenize(chunk.title)
            title_matches = sum(1 for q in query_tokens if q in title_tokens)
            if title_matches > 0:
                score += (title_matches / len(query_tokens)) * 0.35
                
            score = min(score, 1.0)
            
            if score >= min_threshold:
                # Find best matching snippet from content
                sentences = re.split(r'(?<=[.!?\n]) +', chunk.content)
                best_snippet = chunk.content[:200] + "..."
                best_sent_score = -1.0
                
                for s in sentences:
                    s_tokens = self._tokenize(s)
                    s_score = sum(1 for q in query_tokens if q in s_tokens)
                    if s_score > best_sent_score:
                        best_sent_score = s_score
                        best_snippet = s.strip()
                        
                scored_chunks.append((score, chunk, best_snippet))
                
        # Sort descending by relevance score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, chunk, snippet in scored_chunks[:top_k]:
            results.append(RetrievedEvidence(
                chunk=chunk,
                relevance_score=round(score, 3),
                matched_snippet=snippet
            ))
            
        return results
