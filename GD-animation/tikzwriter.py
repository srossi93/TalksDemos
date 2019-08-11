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