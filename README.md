# Notebooks for Sortledton paper

This repository contains the Jupyter notebooks used to analyse and to generate the plots featured in the Sortledton paper.

After downloading repository, fetch the database with the results from [Zenodo](https://zenodo.org/record/5155577) and place it into data/data21.sqlite3. It is a 600 MB database and it was a bit too much to store it in this repository.

The content of this repository: 
* automerge.pl: A script to load the results of new experiment executions into the database data/data21.sqlite3
* pip_freeze.txt: Dependendencies for the Python environment and Jupyter.
* generate-experiments.ipynb
* block-size-analysis.ipynb: Notebook for analyis of the effect of different block sizes - Figures 4b and 7 in the paper.
* graphalytics-microbenchmarks-access-patterns.ipynb: Notebooks for analysis of effect of different access patterns on Graphalyics kernel runtimes - Figures 4a, 4c and 8 in the paper. 
* insertions-throughput.ipynb: Notebook for analysis of edge insertion throughput of different data structures - Figure 9 in the paper.
* insertions-scalability.ipynb: Notebook for analysis of edge insertion scalability of different data structures - Figure 10 in the paper.
* mixed-throughput-and-memory.ipynb: Notebook for analysis of throughput and memory consumption over time of different data structures - Figure 11 in the paper.
* graphalytics-microbenchmarks-csr.ipynb: Notebook for analysis of Graphalytics kernel runtimes on different structures compared to CSR - Figure 12 in the paper.

