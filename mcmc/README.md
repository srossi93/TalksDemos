# Hamiltonian Monte Carlo Animation (with LaTeX export)

This project provides an animation for MCMC sampling methods (in this case HMC).

```bash
> python3 mcmc.py --help
usage: mcmc.py [-h] [--animate] [--save_gif] [--save_tikz]

optional arguments:
  -h, --help   show this help message and exit
  --animate    Animation with matplotlib
  --save_gif   Whether to save or not an animated GIF
  --save_tikz  Whether to save or not a tikz plot for LaTeX
```

Examples: 

```bash
# Show matplotlib animation and save the tikz file
> python3 mcmc.py --animate --save_tikz
```

## LaTeX and Tikz disclaimer

If you want to use the resulting plot in a Beamer animation, you need to locate the last two `\addplot` 
in the `.tex` file (which corresponds to the samples and curve) and replace it with this header
```latex
\addplot [..., 
          select coords between index={0}{\idx}, unbounded coords=jump]
```
I know -- it sucks -- but it's the only way. 

An example of Beamer animation can be found in `presentation_example.tex`
but it's also reported here for convenience.
```latex
\begin{frame}[fragile]{}
  \centering
  \pgfplotsset{select coords between index/.style 2 args={
        x filter/.code={
            \ifnum\coordindex<#1\def\pgfmathresult{}\fi
            \ifnum\coordindex>#2\def\pgfmathresult{}\fi
          }
      }}

  \setlength\figureheight{.55\textwidth}
  \setlength\figurewidth{.55\textwidth}
  %  Looping, autoplaying at 4 frames per sec
  \begin{animateinline}[loop,autoplay]{8}    
    %  Animate first 15 frames with steps of 4
    \multiframe{63}{idx=1+4}{                
      \input{figs/gd_bad_init.tex}
    }
  \end{animateinline}

\end{frame}
```

In `./tikz/` you already have two prepared figures that can be directly imported in our LaTeX project (if you need it).

If you don't care about animating the trajectory, you can just use the resulting `.tex` as it is.
Refer to [tikzplotlib](https://github.com/nschloe/tikzplotlib) for additional details and options for exporting 
matplotlib figures for LaTeX.


### Acknowledgements
If you use or intent to use these scripts for you documents or keynotes, please consider to 
acknowledge the Author ([Simone Rossi](srossi93.gitlab.io)).

The implementation for Hamiltonian MonteCarlo is by Matt Graham [[github](https://github.com/matt-graham/hamiltonian-monte-carlo)].