"""Clustering - Group similar experiments"""
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import Dict, List

class ExperimentClustering:
    """Group experiments into clusters using KMeans"""
    
    def __init__(self, n_clusters: int = 3, random_state: int = 42):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10
        )
        self.is_trained = False
        self.cluster_labels = None
    
    def fit_predict(self, X: np.ndarray) -> Dict:
        """
        Fit and predict clusters
        
        Returns:
            Cluster assignments and centers
        """
        if len(X) < self.n_clusters:
            raise ValueError(f"Need at least {self.n_clusters} samples")
        
        # Scale
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit
        self.cluster_labels = self.model.fit_predict(X_scaled)
        self.is_trained = True
        
        # Calculate cluster statistics
        cluster_stats = {}
        for cluster_id in range(self.n_clusters):
            mask = self.cluster_labels == cluster_id
            cluster_size = np.sum(mask)
            cluster_stats[f"cluster_{cluster_id}"] = {
                "size": int(cluster_size),
                "percentage": float(100 * cluster_size / len(X)),
                "center": self.model.cluster_centers_[cluster_id].tolist()
            }
        
        return {
            "cluster_assignments": self.cluster_labels.tolist(),
            "cluster_stats": cluster_stats,
            "inertia": float(self.model.inertia_),
            "n_clusters": self.n_clusters
        }
    
    def predict_cluster(self, x: List[float]) -> Dict:
        """Predict cluster for new sample"""
        if not self.is_trained:
            raise ValueError("Model not trained. Call fit_predict() first.")
        
        x_scaled = self.scaler.transform([x])[0]
        
        # Calculate distance to each center
        distances = np.linalg.norm(
            self.model.cluster_centers_ - x_scaled,
            axis=1
        )
        
        cluster_id = int(np.argmin(distances))
        
        return {
            "cluster_id": cluster_id,
            "distance_to_center": float(np.min(distances)),
            "all_distances": distances.tolist()
        }
    
    def get_cluster_members(self, cluster_id: int) -> List[int]:
        """Get indices of experiments in a cluster"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        return np.where(self.cluster_labels == cluster_id)[0].tolist()
    
    def find_optimal_clusters(self, X: np.ndarray, 
                             max_clusters: int = 10) -> Dict:
        """Find optimal number of clusters using elbow method"""
        if len(X) < max_clusters:
            max_clusters = len(X) - 1
        
        X_scaled = self.scaler.fit_transform(X)
        
        inertias = []
        silhouette_scores = []
        
        from sklearn.metrics import silhouette_score
        
        for k in range(2, max_clusters + 1):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(km.inertia_)
            
            score = silhouette_score(X_scaled, km.labels_)
            silhouette_scores.append(score)
        
        # Find elbow (knee)
        differences = np.diff(inertias)
        elbow = 2 + np.argmin(differences)
        
        return {
            "inertias": inertias,
            "silhouette_scores": silhouette_scores,
            "suggested_clusters": int(elbow),
            "k_values": list(range(2, max_clusters + 1))
        }
