"""
Movie recommendation system based on user ratings and clustering. Created by Nikifor Koseda and Mateusz Aftanas

To use it install the required dependencies and provide a JSON file named "ratings.json" with the following structure:

{
    "user1": {
        "movie1": rating,
        "movie2": rating,
        ...
    },
    "user2": {
        "movie1": rating,
        "movie3": rating,
        ...
    },

    ...
}

After that choose method of clustering. Hierarchical clustering is more accurate but K-means is faster. Then enter a username to get movie recommendations based on the ratings of similar users.
"""
import json
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

from scipy.cluster.hierarchy import linkage, dendrogram


# ==========================================
# 1. LOAD DATA
# ==========================================

with open("ratings.json", "r", encoding="utf-8") as file:
    ratings = json.load(file)

df = pd.DataFrame.from_dict(ratings, orient="index")

print("Original dataset:")
print(df)


# ==========================================
# 2. PREPARE DATA
# ==========================================

# Remove movies nobody rated
df = df.dropna(axis=1, how="all")

# Fill missing ratings with movie averages
imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(df)

# User names
users = df.index.tolist()

print("\nNumber of users:", len(users))
print("Number of movies:", len(df.columns))


# ==========================================
# 3. CHOOSE ALGORITHM
# ==========================================

print("\nChoose algorithm:")
print("1 - K-means")
print("2 - Hierarchical clustering")

choice = input("Your choice: ")

number_of_clusters = 3

if number_of_clusters >= len(users):
    raise ValueError("Number of clusters must be smaller than users.")

if choice == "1":

    model = KMeans(
        n_clusters=number_of_clusters,
        random_state=42,
        n_init=10
    )

elif choice == "2":

    model = AgglomerativeClustering(
        n_clusters=number_of_clusters,
        linkage="ward"
    )

else:
    print("Invalid choice!")
    exit()


# ==========================================
# 4. PERFORM CLUSTERING
# ==========================================

clusters = model.fit_predict(X)

print("\nClustering results:")

for user, cluster in zip(users, clusters):
    print(user, "-> Cluster", cluster)


# ==========================================
# 5. EVALUATE CLUSTERS
# ==========================================

if 1 < len(set(clusters)) < len(users):

    score = silhouette_score(X, clusters)

    print("\nSilhouette Score:", round(score, 3))


# ==========================================
# 6. REDUCE DATA TO 2 DIMENSIONS
# ==========================================

# PCA makes it possible to visualize many movie
# rating columns in a 2D scatter plot.

pca = PCA(n_components=2)

X_2d = pca.fit_transform(X)

print("\nInformation preserved by PCA:",
      round(sum(pca.explained_variance_ratio_) * 100, 2), "%")


# ==========================================
# 7. VISUALIZATION
# ==========================================

if choice == "1":

    # K-MEANS VISUALIZATION

    plt.figure(figsize=(10, 7))

    for cluster in range(number_of_clusters):

        # Select users belonging to this cluster
        points = X_2d[clusters == cluster]

        plt.scatter(
            points[:, 0],
            points[:, 1],
            label=f"Cluster {cluster}",
            s=100
        )

    # Convert K-means centers into 2D
    centers_2d = pca.transform(model.cluster_centers_)

    plt.scatter(
        centers_2d[:, 0],
        centers_2d[:, 1],
        marker="*",
        s=300,
        label="Cluster centers"
    )

    # Add user names next to dots
    for i, user in enumerate(users):
        plt.annotate(
            user,
            (X_2d[i, 0], X_2d[i, 1])
        )

    plt.title("K-means clustering of movie users")
    plt.xlabel("PCA component 1")
    plt.ylabel("PCA component 2")
    plt.legend()
    plt.grid()
    plt.show()


elif choice == "2":

    # HIERARCHICAL CLUSTERING VISUALIZATION

    # Build the hierarchical tree
    tree = linkage(X, method="ward")

    # Choose a tree height that produces the
    # requested number of clusters
    threshold = (
        tree[-number_of_clusters, 2] +
        tree[-(number_of_clusters - 1), 2]
    ) / 2

    plt.figure(figsize=(12, 7))

    dendrogram(
        tree,
        labels=users,
        color_threshold=threshold,
        leaf_rotation=45
    )

    plt.title("Hierarchical clustering dendrogram")
    plt.xlabel("Users")
    plt.ylabel("Distance between clusters")
    plt.tight_layout()
    plt.show()

    # Also show the final groups in 2D
    plt.figure(figsize=(10, 7))

    for cluster in range(number_of_clusters):

        points = X_2d[clusters == cluster]

        plt.scatter(
            points[:, 0],
            points[:, 1],
            label=f"Cluster {cluster}",
            s=100
        )

    for i, user in enumerate(users):
        plt.annotate(
            user,
            (X_2d[i, 0], X_2d[i, 1])
        )

    plt.title("Hierarchical clustering of movie users")
    plt.xlabel("PCA component 1")
    plt.ylabel("PCA component 2")
    plt.legend()
    plt.grid()
    plt.show()

# ==========================================
# 8. RECOMMENDATION
# ==========================================

user = input("Enter username: ")

if user not in ratings:
    print("User not found!")
else:
    user_index = users.index(user)
    user_cluster = clusters[user_index]

    # Find other users in the same cluster
    similar_users = [
        other_user
        for other_user in ratings
        if other_user != user
        and clusters[users.index(other_user)] == user_cluster
    ]

    # Function that collects ratings for movies the user hasn't rated
    def collect_ratings(other_users):
        movie_ratings = {}

        for other_user in other_users:
            for movie, rating in ratings[other_user].items():

                # Ignore movies already rated by our user
                if movie not in ratings[user]:
                    movie_ratings.setdefault(movie, []).append(rating)

        return movie_ratings

    # Function that returns the score of a movie for sorting
    def get_movie_score(movie_and_score):
        _movie, score = movie_and_score
        return score
    
    # First, try users from the same cluster
    recommendations = collect_ratings(similar_users)

    # If the cluster has no useful recommendations, use everyone
    if not recommendations:
        print("Not enough ratings in this cluster. Using all users.")
        recommendations = collect_ratings(ratings.keys())

    if not recommendations:
        print("No recommendations or anti-recommendations available.")

    else:
        # Calculate average rating for every movie
        movie_scores = {
            movie: sum(movie_ratings) / len(movie_ratings)
            for movie, movie_ratings in recommendations.items()
        }

        # Sort from highest to lowest
        sorted_movies = sorted(
            movie_scores.items(),
            key=get_movie_score,
            reverse=True
        )

        # Top 5 recommendations
        print("\n--- TOP 5 RECOMMENDATIONS ---")

        for movie, score in sorted_movies[:5]:
            print(f"{movie}: {score:.2f}/5")

        # Bottom 5 anti-recommendations
        print("\n--- TOP 5 ANTI-RECOMMENDATIONS ---")

        for movie, score in sorted_movies[-5:][::-1]:
            print(f"{movie}: {score:.2f}/5")
