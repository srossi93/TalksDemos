import hmc
import autograd.numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation
import tikzplotlib as tpl
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--animate', action='store_true',
                        help='Animation with matplotlib')
    parser.add_argument('--save_gif', action='store_true',
                        help='Whether to save or not an animated GIF')
    parser.add_argument('--save_tikz', action='store_true',
                        help='Whether to save or not a tikz plot for LaTeX')
    args = parser.parse_args()

    n_dim = 2
    mean = np.array([1., 2.])
    cov = (np.array([[1, .9], [.9, 1]]))
    rng = np.random.RandomState(seed=12345)

    def pot_energy(pos):
        pos_minus_mean = pos - mean
        return 0.5 * pos_minus_mean @ np.linalg.inv(cov) @ pos_minus_mean


    # Specify Hamiltonian system with isotropic Gaussian kinetic energy
    system = hmc.systems.EuclideanMetricSystem(pot_energy)

    # Hamiltonian is separable therefore use explicit leapfrog integrator
    integrator = hmc.integrators.LeapfrogIntegrator(system, step_size=0.125)

    # Use Hybrid HMC implementation of trajectory sampling
    sampler = hmc.samplers.StaticMetropolisHMC(system, integrator, rng, n_step=5)

    # Sample an initial position
    init_pos = np.array([-3., -3.])

    # Sample a Markov chain
    chains, chain_stats = sampler.sample_chain(250, init_pos)

    def loglikelihood(samples):
        pos_minus_mean = samples - mean
        return 0.5 * (np.diag(pos_minus_mean @ np.linalg.inv(cov) @ pos_minus_mean.T)
                      + np.log(np.linalg.det(cov)))

    samples = chains['pos']
    nlikl = [loglikelihood(samples[:i+1]).mean() for i in range(1, len(samples)+1)]


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
    levelsf = MaxNLocator(nbins=10).tick_values(Z.min(), Z.max())
    fig, (ax0, ax1) = plt.subplots(1, 2)  # type: plt.Figure, (plt.Axes, plt.Axes)
    ax0.contour(X, Y, Z, levels=levelsf)
    ax1.set_xlim(0, 250)
    ax1.set_ylim(min(nlikl), max(nlikl))

    i = 1
    step = 2
    if args.animate or args.save_gif:
        def animate(*args, **kwargs):
            global i
            ax0.plot(chains['pos'][:i, 0], chains['pos'][:i, 1], '.', c='black')
            ax0.plot(chains['pos'][i:i+step, 0], chains['pos'][i:i+step, 1], '.', c='r')
            ax1.plot(nlikl[:i+step], color='#377eb8')
            i += step
            i = min(i, len(chains['pos'])-1)
            return ax0, ax1


        ani = animation.FuncAnimation(fig, animate, frames=int(250/step), interval=10, blit=False)
        if args.animate:
            plt.show()
        if args.save_gif:
            ani.save('gif/mcmc_animation.gif', writer=animation.PillowWriter())

    if args.save_tikz:
        ax0.plot(chains['pos'][..., 0], chains['pos'][..., 1], '.', c='black')
        ax1.plot(nlikl, color='#377eb8')
        tpl.save('tikz/mcmc_animation.tex',
                 figurewidth='\\figurewidth', figureheight='\\figureheight',
                 strict=True, externalize_tables=False, show_info=True)
        plt.show()

