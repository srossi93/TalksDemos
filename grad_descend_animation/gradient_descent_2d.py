import autograd.numpy as np
import autograd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation
import tikzplotlib as tpl

import argparse


def f(x, y):
    return -1 * np.sin(0.5*x**2-0.25*y**2+3) * np.cos(2*x+1-np.exp(y))


def fdx(x, y):
    return autograd.grad(f, 0)(x, y)


def fdy(x, y):
    return autograd.grad(f, 1)(x, y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--animate', action='store_true',
                        help='Animation with matplotlib')
    parser.add_argument('--nsteps', type=int, default=50,
                        help='Number of GD iterations')
    parser.add_argument('--good_init', action='store_true',
                        help='Whether to start from a good or bad initial point')
    parser.add_argument('--lr', type=float, default=0.25,
                        help='Learning rate')
    parser.add_argument('--save_gif', action='store_true',
                        help='Whether to save or not an animated GIF')
    parser.add_argument('--save_tikz', action='store_true',
                        help='Whether to save or not a tikz plot for LaTeX')
    args = parser.parse_args()

    # args = argparse.Namespace()
    #
    # args.animate = True
    # args.nsteps = 120
    # args.good_init = True
    # args.lr = 0.25
    # args.save_gif = True
    # args.save_tikz = True

    xx = np.linspace(-1, 1, 64)
    yy = np.linspace(-3, 1.5, 64)

    x, y = np.meshgrid(xx, yy)
    z = f(x, y)

    if args.good_init:
        x_init = 0.2
        y_init = -0.1
    else:
        x_init = -0.3
        y_init = 0.4

    levelsf = MaxNLocator(nbins=20).tick_values(z.min(), z.max())
    levels = MaxNLocator(nbins=20).tick_values(z.min(), z.max())

    fig, ax = plt.subplots()

    x_list = []
    y_list = []
    colorbar_exist = False

    ax.clear()
    if args.animate:
        x_est = x_init
        y_est = y_init
        def animate(i):

            global colorbar_exist
            global x_est
            global y_est
            global z_est
        #
            ax.clear()
            cf = ax.contourf(x, y, z, levels=levelsf)
            cs = ax.contour(x, y, z, levels=levels, colors="white")
            if not colorbar_exist:
                fig.colorbar(cf)
                colorbar_exist = True
            ax.clabel(cs, fontsize=9, inline=1)
            z_est = f(x_est, y_est)
            x_list.append(x_est)
            y_list.append(y_est)
            ax.scatter(x_est, y_est, c="r")
            ax.plot(x_list, y_list, c="r")
            # ax.text(-0.75, 0.6, "Value : %.4f" % z_est, color='r')
            x_grad = fdx(x_est, y_est)
            y_grad = fdx(x_est, y_est)

            if np.abs(x_grad) < 1e-4 and np.abs(y_grad < 1e-4):
                print('Only marginal improvement on gradients')
                return ax
            x_est, y_est = x_est - fdx(x_est, y_est) * args.lr, y_est - fdy(x_est, y_est) * args.lr

            return ax

        ani = animation.FuncAnimation(fig, animate, frames=50, interval=5, blit=False)
        if args.save_gif:
            ani.save('gif/convergence_2d_%s.gif' %
                     '_'.join(['{0}={1}'.format(k, v) for k,v in vars(args).items()]))
        plt.show()

    if args.save_tikz:
        x_est = x_init
        y_est = y_init
        fig, ax = plt.subplots()

        x_list = []
        y_list = []

        for i in range(args.nsteps):
            z_est = f(x_est, y_est)
            x_list.append(x_est)
            y_list.append(y_est)
            x_grad = fdx(x_est, y_est)
            y_grad = fdx(x_est, y_est)

            if np.abs(x_grad) < 1e-4 and np.abs(y_grad < 1e-4):
                print('Only marginal improvement on gradients - Stopping simulator at t = %d' % i)
                break
            x_est, y_est = x_est - fdx(x_est, y_est) * args.lr, y_est - fdy(x_est, y_est) * args.lr

        cf = ax.contourf(x, y, z, levels=levelsf)
        cs = ax.contour(x, y, z, levels=levels, colors="white")
        ax.clabel(cs, fontsize=9, inline=1)
        ax.plot(x_list, y_list, c="r")
        tpl.save('tikz/convergence_2d_%s.tex' % '_'.join(['{0}={1}'.format(k, v) for k, v in vars(args).items()]),
                 figurewidth='\\figurewidth', figureheight='\\figureheight',
                 strict=True, externalize_tables=False, show_info=True)

        plt.show()
