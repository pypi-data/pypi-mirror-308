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

# Test several values of h
for h in [0.01, 0.02]:
    # Compute iterates according to algorithm
    algorithm = DNLA.Algorithm(d=d, M=50, N=250, K=500, h=h, title=title, U=U, dU=dU, initial=initial)
    samples_filename = algorithm.generate_samples(As=[1,2,3,4,5,6], sim_annealing=True)

    # Compute table of averages and standard deviations
    postprocessor = DNLA.PostProcessor(samples_filename)
    postprocessor.compute_tables([50, 500], 1, "mean")
    postprocessor.compute_tables([50, 500], 1, "std")