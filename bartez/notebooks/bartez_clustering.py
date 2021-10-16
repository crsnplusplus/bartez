import networkx as nx
import bartez.tests.test_utils as test_utils

from sklearn import cluster
from copy import copy
from bartez.graph.cluster import BartezCluster


def listToDict(list):
    listdict = {}

    for i in range(len(list)):
        listdict[i] = list[i]

    return listdict

def graphToEdgeMatrix(G):

    # Initialize Edge Matrix
    edgeMat = [[0 for x in range(len(G))] for y in range(len(G))]

    # For loop to set 0 or 1 ( diagonal elements are set to 1)
    for node in G:
        tempNeighList = G.neighbors(node)
        for neighbor in tempNeighList:
            edgeMat[node][neighbor] = 1
        edgeMat[node][node] = 1

    return edgeMat


# Initialize some variables to help us with the generalization of the program
kClusters = 8
n_init = 100
damping = 0.6
results = []
nmiResults = []
arsResults = []

# Prepare crossrod, entries and graph
crossword = test_utils.get_test_crossword()
entries = crossword.get_entries()
graph = test_utils.get_test_graph(crossword)

G = graph

# Transform our graph data into matrix form
edgeMat = graphToEdgeMatrix(G)
adjMatrix = nx.to_scipy_sparse_matrix(G)
# Positions the nodes using Fruchterman-Reingold force-directed algorithm
# Too technical to discuss right now, just go with it
pos = nx.spring_layout(G)
#drawCommunities(G, pos)

#cluster = BartezCluster(G)

###########################
# Spectral Clustering Model
spectral = cluster.SpectralClustering(n_clusters=kClusters, affinity="precomputed", n_init=n_init, degree=20)
spectral.fit(adjMatrix)

# Transform our data to list form and store them in results list
results.append(list(spectral.labels_))

################################
# Agglomerative Clustering Model
#agglomerative = cluster.AgglomerativeClustering(n_clusters=kClusters, linkage="ward")
#agglomerative.fit(adjMatrix.toarray())

# Transform our data to list form and store them in results list
#results.append(list(agglomerative.labels_))

##########################
# K-means Clustering Model
#kmeans = cluster.KMeans(n_clusters=kClusters, n_init=n_init)
#kmeans.fit(edgeMat)

# Transform our data to list form and store them in results list
#results.append(list(kmeans.labels_))

#######################################
# Affinity Propagation Clustering Model
#affinity = cluster.affinity_propagation(S=edgeMat, max_iter=n_init, damping=damping)

# Transform our data to list form and store them in results list
#results.append(list(affinity[1]))

#######################################
# MiniBatchKMeans Propagation Clustering Model
mini_batch_kmeans = cluster.MiniBatchKMeans(n_clusters=kClusters, n_init=n_init)
#mini_batch_kmeans.fit(edgeMat)

# Transform our data to list form and store them in results list
#results.append(list(mini_batch_kmeans.labels_))



###
for cluster_model_result in results:
    model_clusters = []
    model_entries = copy(entries)

    crossword.clear_all_non_blocks()

    for result_index, cluster_index in enumerate(cluster_model_result):

        if len(model_clusters) <= cluster_index:
            while len(model_clusters) <= cluster_index: model_clusters.append([])

        model_clusters[cluster_index].append(int(result_index))


    for model_cluster_index, model_cluster in enumerate(model_clusters):
        for model_result in model_cluster:
            value = model_entries[model_result].get_value()
            if model_cluster_index >= 10: model_cluster_index = model_cluster_index % 10
            model_entries[model_result].set_value(str(model_cluster_index)*len(value))
        crossword.set_board_values_from_entries(model_entries)

    crossword.print_crossword()
    crossword.clear_all_non_blocks()