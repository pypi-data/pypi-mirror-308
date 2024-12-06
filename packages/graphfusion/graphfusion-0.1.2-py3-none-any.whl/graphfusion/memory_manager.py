from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MemoryManager:
    def __init__(self):
        # Initialize storage for embeddings and associated data
        self.memory = []
        
    def store_in_memory(self, embedding, data, label=None):
        """Stores a new data entry with its embedding and optional label."""
        self.memory.append({
            "embedding": embedding,
            "data": data,
            "label": label
        })

    def get_related_nodes(self, query_embedding, top_k=5):
        """Retrieve top_k similar nodes based on the query embedding."""
        similar_entries = self.retrieve_similar(query_embedding, top_k=top_k)
        return [{"data": entry["data"], "similarity": entry["similarity"]} for entry in similar_entries]
        
    def retrieve_similar(self, query_embedding, top_k=5):
        """Retrieves top_k most similar entries based on cosine similarity."""
        if not self.memory:
            return []
        
        similarities = [
            cosine_similarity(query_embedding.reshape(1, -1), entry["embedding"].reshape(1, -1)).item()
            for entry in self.memory
        ]
        
        # Sort memory items by similarity score in descending order
        sorted_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.memory[i] for i in sorted_indices]
    
    def update_entry(self, memory_id, new_data):
        """Updates an existing memory entry with new data."""
        if 0 <= memory_id < len(self.memory):
            self.memory[memory_id]["data"] = new_data
    
    def forget_old_entries(self, reference_embedding, threshold=0.8):
        """
        Forget entries that are below the similarity threshold with respect to the reference_embedding.
        """
        self.memory = [
            entry for entry in self.memory 
            if self.compute_similarity(reference_embedding, entry['embedding']) >= threshold
        ]
    
    def update_on_feedback(self, feedback):
        """Adjusts memory relevance based on feedback (e.g., boosts or reduces similarity scores)."""
        for entry in self.memory:
            if feedback["relevance"] < 0.5:  # Example condition based on feedback
                entry["embedding"] *= 0.9  # Decrease relevance of similar entries

    def compute_similarity(self, embedding1, embedding2):
        """
        Compute the cosine similarity between two embeddings.
        """
        return cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1)).item()
