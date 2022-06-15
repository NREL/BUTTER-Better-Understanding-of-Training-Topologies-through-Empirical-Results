<img src="examples/star-collage.png?raw=true" alt="Collage image demonstrating several axis of the BUTTER dataset" width=300px />

# NREL Butter Deep Learning Dataset

This repository contains code, notebooks, and instructions that can be used to reproduce the figures and analysis in our upcoming paper and provide examples to access the NREL Butter Empirical Deep Learning Dataset via AWS S3.

The dataset was generated using our BUTTER Empirical Deep Learning Experimental Framework - [DOE Code record](https://www.osti.gov/doecode/biblio/74457), [Github Repository](https://github.com/NREL/BUTTER-Empirical-Deep-Learning-Experimental-Framework)

## Quick Links:

- OEDI Data Lake Dataset Page: [Link](https://data.openei.org/submissions/5708)
- OEDI Data Lake Files Viewer: [Link](https://data.openei.org/s3_viewer?bucket=oedi-data-lake&prefix=butter%2F)
- Dataset Readme: [Link](https://github.com/openEDI/documentation/blob/main/BUTTER.md)

## How to cite the dataset:

**If you benefit from this code or concept, please cite these resources:**

+ Our upcoming **dataset publication**, which is currently under review for the [NeurIPS 2022 Datasets and Benchmarks Track](https://neurips.cc/Conferences/2022/CallForDatasetsBenchmarks).

+ The **[BUTTER Dataset](https://data.openei.org/submissions/5708)** itself:
> Tripp, Charles, Perr-Sauer, Jordan, Hayne, Lucas, & Lunacek, Monte. BUTTER - Empirical Deep Learning Dataset. United States. https://dx.doi.org/10.25984/1872441

# Data Access

## Access Method 1: Using the OEDI Data Lake S3 UI

Use a web browser and naigate to: https://data.openei.org/s3_viewer?bucket=oedi-data-lake&prefix=butter%2F

## Access Method 2: Using AWS Command Line

To list all top-level prefixes in the dataset:

`aws s3 ls --no-sign-request s3://oedi-data-lake/butter/`

To download files of interest:

`!aws s3 cp --no-sign-request s3://oedi-data-lake/butter/300_epoch_sweep_summary/dataset=201_pol/learning_rate=0.0001/batch_size=256/kernel_regularizer.type=__HIVE_DEFAULT_PARTITION__/label_noise=0/epochs=300/shape=exponential/ test-data/ --recursive`

## Access Method 3: Python with PyArrow and S3FS

See [BUTTER-Access-Example-Python.ipynb](examples/BUTTER-Access-Example-Python.ipynb)


# Quickstart

To run this code locally, you just have to install the requirements and then start up Jupyter to browse the notebooks:

```
git clone
pip install -r requirements.txt
jupyter notebook
```

The repository contains two directories with notebooks:

### **/examples**:
Code and Jupyter notebooks demonstrating access to the BUTTER dataset in the OEDI data lake.

- **BUTTER-Access-Example-Python.ipynb**: Code that loads BUTTER data from the OEDI data lake using Python.
- **BUTTER-star-collage.ipynb**: Code to load and plot the images in the BUTTER "star" image at the top of this README, demonstrating the use of multiple sweeps.

### **/code_for_paper**:
Code and Jupyter notebooks needed to reproduce figures in the paper.

- **paper_viz_figure_1.ipynb**: Code to generate figure 1 in the paper.
- **paper_analysis_figures.ipynb**: Code to generate all figures in the analysis section of the paper.
- **paper_appendix_figures.ipynb**: Code to generate all figures in the appendix of the paper.

## (Optional) Using a local copy of the dataset

The code in this repository will automatically load data from the OEDI Data Lake on Amazon S3. If you have a fast internet connection, there is no need to download the data in a separate step. However, in some cases, it may be convenient to download the data to disk and load it from there. To do this, you just need to set the following environment variable:
```
export DMP_BUTTER_DATA_DIR=/path/to/data
```

`/path/to/data` should be a directory which contains the sweep directories, eg. `/path/to/data/primary_sweep_summary`

# Contributors
Charles Tripp, Jordan Perr-Sauer, Lucas Hayne, Monte Lunacek
