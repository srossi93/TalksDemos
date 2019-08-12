import hmc
import autograd.numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation

import argparse

if __name__ == '__main__':

    args = argparse.Namespace()
    args.animate = False
    args.save_tikz = True

    n_dim = 2
    mean = np.array([1., 2.])
    cov = (np.array([[1, .9], [.9, 1]]))
    rng = np.random.RandomState(seed=12345)

    print(mean)
    print(cov)

    def pot_energy(pos):
        pos_minus_mean = pos - mean
        return 0.5 * pos_minus_mean @ np.linalg.inv(cov) @ pos_minus_mean


    # Specify Hamiltonian system with isotropic Gaussian kinetic energy
    system = hmc.systems.EuclideanMetricSystem(pot_energy)

    # Hamiltonian is separable therefore use explicit leapfrog integrator
    integrator = hmc.integrators.LeapfrogIntegrator(system, step_size=0.125)

    # Use dynamic integration-time HMC implementation with multinomial
    # sampling from trajectories
    sampler = hmc.samplers.StaticMetropolisHMC(system, integrator, rng, n_step=5)

    # Sample an initial position from zero-mean isotropic Gaussian
    init_pos = np.array([-1., -1.])#rng.normal(size=n_dim)

    # Sample a Markov chain with 1000 transitions
    chains, chain_stats = sampler.sample_chain(250, init_pos)

    def loglikelihood(samples):
        pos_minus_mean = samples - mean
        return 0.5 * (np.diag(pos_minus_mean @ np.linalg.inv(cov) @ pos_minus_mean.T)
                      + np.log(np.linalg.det(cov)))

    samples = chains['pos']
    nlikl = []
    for i in range(1, len(samples)+1):
        nlikl.append(loglikelihood(samples[:i+1]).mean())


    N = 64
    X = np.linspace(-2, 4, N)
    Y = np.linspace(-1, 5, N)
    X, Y = np.meshgrid(X, Y)

    # Pack X and Y into a single 3-dimensional array
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y

    rv = multivariate_normal(mean, cov)
    Z = rv.pdf(pos)
    levelsf = MaxNLocator(nbins=20).tick_values(Z.min(), Z.max())
    fig, (ax0, ax1) = plt.subplots(1, 2)  # type: plt.Figure, (plt.Axes, plt.Axes)
    ax0.contour(X, Y, Z, levels=levelsf)
    ax1.set_xlim(0, 250)
    ax1.set_ylim(min(nlikl), max(nlikl))

    i = 1

    if args.animate:
        def animate(*args, **kwargs):
            global i
            ax0.plot(chains['pos'][:i-1, 0], chains['pos'][:i-1, 1], '.', c='black')
            ax0.plot(chains['pos'][i, 0], chains['pos'][i, 1], '.', c='r')
            ax1.plot(nlikl[:i], color='#377eb8')
            i += 1
            i = min(i, len(chains['pos'])-1)
            return ax0, ax1


        ani = animation.FuncAnimation(fig, animate, frames=250, interval=3, blit=False)
        plt.show()

    if args.save_tikz:
        ax0.plot(chains['pos'][..., 0], chains['pos'][..., 1], '.', c='black')
        ax1.plot(nlikl, color='#377eb8')
        plt.show()

