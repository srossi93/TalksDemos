#!env /home/srossi/anaconda3/bin/python3
import autograd
import autograd.numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation
import tikzplotlib as tpl
import argparse

# plt.rcParams['text.usetex'] = True

if __name__ == '__main__':
    true_mean = np.array([1., 2.])
    true_cov = np.array([[1, .9], [.9, 1]])
    rng = np.random.RandomState(seed=12345)

    vi_mean = np.array([2., 0.])
    vi_logvars = np.array([1., 1.])

    def true_kl(vi_mean, vi_logvars):
        d = 2
        vi_cov = np.diag(np.exp(vi_logvars))
        true_cov_inv = np.linalg.inv(true_cov)
        return 0.5 * (
               np.log(np.linalg.det(true_cov) / np.linalg.det(vi_cov))
               + np.trace(true_cov_inv @ vi_cov)
               + (vi_mean - true_mean) @ true_cov_inv @ (vi_mean - true_mean).T
               - d
        )

    def loglikelihood(samples):
        return -multivariate_normal(true_mean, true_cov).logpdf(samples)

    hist_kl = []
    hist_vi_mean = []
    hist_vi_logvars = []
    hist_nloglik = []
    previous_grad_vi_mean = 0.
    previous_grad_vi_logvars = 0.
    for _ in range(50):
        hist_kl.append(true_kl(vi_mean, vi_logvars))
        hist_vi_mean.append(np.copy(vi_mean))
        hist_vi_logvars.append(np.copy(vi_logvars))
        grad_vi_mean = autograd.grad(true_kl, 0)(vi_mean, vi_logvars)
        grad_vi_logvars = autograd.grad(true_kl, 1)(vi_mean, vi_logvars)

        vi_mean = vi_mean - .1 * (grad_vi_mean + 0.25 * previous_grad_vi_mean)
        vi_logvars = vi_logvars - .1 * (grad_vi_logvars + 0.25 * previous_grad_vi_logvars)

        samples = multivariate_normal(vi_mean, np.diag(np.exp(vi_logvars))).rvs(8192*16, rng)
        hist_nloglik.append(loglikelihood(samples).mean())
        previous_grad_vi_mean = grad_vi_mean
        previous_grad_vi_logvars = grad_vi_logvars



    fig, (ax0, ax1) = plt.subplots(1, 2)  # type: plt.Figure, (plt.Axes, plt.Axes)
    i = 0
    step = 1
    def animate(*args, **kwargs):
        global i
        ax0.clear()
        ax1.clear()

        ax0.set_xlim(-2, 4)
        ax0.set_ylim(-1, 5)
        ax1.set_xlim(0, len(hist_nloglik))
        ax1.set_ylim(min(hist_nloglik), max(hist_nloglik))

        N = 70
        X = np.linspace(-2, 4, N)
        Y = np.linspace(-1, 5, N)
        X, Y = np.meshgrid(X, Y)

        # Pack X and Y into a single 3-dimensional array
        pos = np.empty(X.shape + (2,))
        pos[:, :, 0] = X
        pos[:, :, 1] = Y
        rv = multivariate_normal(true_mean, true_cov)
        Z = rv.pdf(pos)
        levelsf = MaxNLocator(nbins=8).tick_values(Z.min(), Z.max())
        ax0.contour(X, Y, Z, levels=levelsf,)

        X = np.linspace(hist_vi_mean[i][0] - 5 * np.exp(hist_vi_logvars[i][0]), hist_vi_mean[i][0] + 5 * np.exp(hist_vi_logvars[i][0]), 32)
        Y = np.linspace(hist_vi_mean[i][1] - 5 * np.exp(hist_vi_logvars[i][1]), hist_vi_mean[i][1] + 5 * np.exp(hist_vi_logvars[i][1]), 32)
        # Y = np.linspace(-1, 5, N)
        X, Y = np.meshgrid(X, Y)

        # Pack X and Y into a single 3-dimensional array
        pos = np.empty(X.shape + (2,))
        pos[:, :, 0] = X
        pos[:, :, 1] = Y
        rv = multivariate_normal(hist_vi_mean[i], np.diag(np.exp(hist_vi_logvars[i])))
        Z = rv.pdf(pos)
        levelsf = MaxNLocator(nbins=8).tick_values(Z.min(), Z.max())
        ax0.contour(X, Y, Z, levels=levelsf, cmap='plasma')
        ax1.plot(hist_nloglik[:i])

        i += step
        i = min(i, len(hist_nloglik) - 1)
        return ax0, ax1

    ani = animation.FuncAnimation(fig, animate, frames=int(250/step), interval=1, blit=False)

    plt.show()