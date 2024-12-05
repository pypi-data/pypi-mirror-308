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

for (N, K) in [(1, 140000), (10, 14000), (100, 1400), (1000, 140), (10000, 14)]:
    # Compute iterates according to algorithm
    algorithm = DNLA.Algorithm(d=d, M=100, N=N, K=K, h=0.01, title=title, U=U, dU=dU, initial=initial)
    samples_filename = algorithm.generate_samples(As=[4,12,20,40], sim_annealing=True)

    # Compute table of averages
    postprocessor = DNLA.PostProcessor(samples_filename)
    postprocessor.compute_tables([K], (N * K) // 100000, "mean")