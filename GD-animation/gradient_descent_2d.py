import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation

from matplotlib.animation import FileMovieWriter
import tikzplotlib as tpl 


class TikzWriter(FileMovieWriter):
    supported_formats = ['tex']

    def __init__(self, *args, extra_args=None, **kwargs):
        # extra_args aren't used but we need to stop None from being passed
        super().__init__(*args, extra_args=(), **kwargs)

    def setup(self, fig, dpi, frame_prefix):
        super().setup(fig, dpi, frame_prefix, clear_temp=False)
        self.fname_format_str = '%s%-%02d.%s'
        self.temp_prefix, self.frame_format = self.outfile.split('.')

    def grab_frame(self, **savefig_kwargs):
        '''
        Grab the image information from the figure and save as a movie frame.
        All keyword arguments in savefig_kwargs are passed on to the 'savefig'
        command that saves the figure.
        '''
        fname = self._base_temp_name() % self._frame_counter

        # Save the filename so we can delete it later if necessary
        self._temp_names.append(fname)
        self._frame_counter += 1  # Ensures each created name is 'unique'
        tpl.save(fname, figurewidth='\\figurewidth', figureheight='\\figureheight', externalize_tables=False, table_row_sep=r"\\", show_info=True)
        # print('hello')
        # Tell the figure to save its data to the sink, using the

    def finish(self):
        self._frame_sink().close()

def f(x, y):
    return -1 * np.sin(0.5*x**2-0.25*y**2+3) * np.cos(2*x+1-np.exp(y))

def fdx(x, y):
    return 2 * np.sin(2 * x - np.exp(y) + 1) * np.sin(0.5 * x**2 - 0.25 * y**2 + 3) - x * np.cos(2 * x - np.exp(y) + 1) * np.cos(0.5 * x**2 - 0.25 * y**2 + 3)

def fdy(x, y):
    return -1 * np.exp(y) * np.sin(2 * x - np.exp(y) + 1) * np.sin(0.5 * x**2 - 0.25 * y**2 + 3) + 0.5 * y * np.cos(2 * x - np.exp(y) + 1) * np.cos(0.5 * x**2 - 0.25 * y**2 + 3)

# lin_param = (-1, 1, 64)
xx = np.linspace(-1, 1, 64)
yy = np.linspace(-3, 1.5, 64)

x, y = np.meshgrid(xx, yy)
z = f(x, y)
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
levelsf = MaxNLocator(nbins=20).tick_values(z.min(), z.max())
levels = MaxNLocator(nbins=20).tick_values(z.min(), z.max())

fig, ax = plt.subplots()

# x_est = -0.3 #0.
# y_est = 0.4 #-0.1
x_est = 0.2
y_est = -0.1
r = 0.5  # Learning rate

x_list = []
y_list = []
colorbar_exist = False

ax.clear()
cf = ax.contourf(x, y, z, levels=levelsf)
cs = ax.contour(x, y, z, levels=levels, colors="white")
ax.clabel(cs, fontsize=9, inline=1)

for i in range(45):
# def animate(i):

    # global colorbar_exist
    # global x_est
    # global y_est
    # global z_est

    # if not colorbar_exist:
    #     fig.colorbar(cf)
    #     colorbar_exist = True
    
    z_est = f(x_est, y_est)
    # ax.scatter(x_est, y_est, c="r")
    x_list.append(x_est)
    y_list.append(y_est)
    # ax.text(-0.75, 0.6, "Value : %.4f" % z_est, color='r')

    x_est, y_est = x_est - fdx(x_est, y_est) * r, y_est - fdy(x_est, y_est) * r
    # return ax

ax.plot(x_list, y_list, c="r")
# ani = animation.FuncAnimation(fig, animate, frames=10, interval=20, blit=False)

# print(next(ani.frame_seq))
# ani.save('test.tex', writer=TikzWriter())
tpl.save('figs/gd_good_init.tex', figurewidth='\\figurewidth', strict=True,
         figureheight='\\figureheight', externalize_tables=False, show_info=True)
# plt.show()
