import sys
sys.path.append("../src")
import numpy as np
import GlobalOptimizationDNLA as DNLA

# Define Rastrigin function, its gradient and an initial distribution
d = 10
title = "Rastrigin"
U = lambda x: d + np.linalg.norm(x) ** 2 - np.sum(np.cos(2*np.pi*x))
dU = lambda x: 2 * x + 2 * np.pi * np.sin(2*np.pi*x)
initial = lambda: np.random.multivariate_normal(np.zeros(d) + 3, 10 * np.eye(d))

# Compute iterates according to algorithm
algorithm = DNLA.Algorithm(d=d, M=100, N=10, K=14000, h=0.01, title=title, U=U, dU=dU, initial=initial)
samples_filename = algorithm.generate_samples(As=[1,2,3,4], sim_annealing=False)

# Plot empirical probabilities
postprocessor = DNLA.PostProcessor(samples_filename)
postprocessor.plot_empirical_probabilities(dpi=10, layout="32", tols=[1,2,3,4,5,6], running=False)
