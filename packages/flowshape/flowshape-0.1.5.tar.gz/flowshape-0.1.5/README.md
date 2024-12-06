# FlowShape
This package provides functionality for the analysis of cell shape using the spherical harmonics decomposition.
Please refer to our paper ["Cell shape characterization, alignment, and comparison using FlowShape"](https://doi.org/10.1093/bioinformatics/btad383) for more information.

A local branch of [lie_learn](https://github.com/AMLab-Amsterdam/lie_learn) that does not depend on cython is included (spheremesh/lie_learn). 

## Installation
Flow shape is available on pypi. Install via:

`pip install flowshape`

## Demo

For the [demos](./demo/), you will need [JupyterLab](https://jupyter.org/install), as well as [Meshplot](https://skoch9.github.io/meshplot/tutorial/) for plotting.

To install both, run:

`conda install -c conda-forge jupyterlab meshplot`

Then, to open JupyterLab, run:

`jupyter-lab`

Download the demo folder from this repository and open the `demo.ipynb` notebook. 

Further, `demo_alignment.ipynb` shows how to align meshes.
`demo_from_img.ipynb` shows how to use marching cubes to make meshes from image stacks.
There are some additional dependencies for this notebook.

## How to use
See the [demos](./demo/) for examples on how to use the package. 
The API consists only of functions operating on NumPy ndarrays and there are no classes. 
Most functions have docstrings in the source. 

## Citation

Bibtex:
```bibtex
@article{10.1093/bioinformatics/btad383,
    author = {van Bavel, Casper and Thiels, Wim and Jelier, Rob},
    title = "{Cell shape characterization, alignment, and comparison using FlowShape}",
    journal = {Bioinformatics},
    volume = {39},
    number = {6},
    pages = {btad383},
    year = {2023},
    month = {06},
    issn = {1367-4811},
    doi = {10.1093/bioinformatics/btad383},
    url = {https://doi.org/10.1093/bioinformatics/btad383},
    eprint = {https://academic.oup.com/bioinformatics/article-pdf/39/6/btad383/50738096/btad383.pdf},
}
```
