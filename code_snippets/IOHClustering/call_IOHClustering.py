# /// script
# requires-python = "==3.10"
# dependencies = [
#   "ioh",
#   "iohclustering",
# ]
# ///

from iohclustering import get_problem

# Get benchmark problem by its ID (e.g., ID=5) with k=2 clusters
# Alternatively, by name (e.g., "iris_pca")
clustering_problem, retransform = get_problem(fid=5, k=2)

### evaluation point
dim = clustering_problem.meta_data.n_variables
eval_point = [0.0]*dim

### print function value for eval_point
print(clustering_problem(eval_point))