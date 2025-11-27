# Accelerated ADMM: Automated Parameter Tuning and Improved Linear Convergence

This repository contains the code from our paper

> M. Tavakoli, F. Jakob, G. Carnevale, G. Notarstefano, and A. Iannelli. *"Accelerated ADMM: Automated Parameter Tuning and Improved Linear Convergence."*


## Installation

The code has been developed and tested with **Python 3.10.7**.  
All required packages can be installed via

```bash
pip install -r requirements.txt
```

All SDPs are solved with the commericial solver MOSEK.

```bash 
pip install Mosek
```

An academic license can be requested [here](https://www.mosek.com/products/academic-licenses/). Other open-source solvers might work as well (e.g. cvxopt), however, we observed best numerical stability with MOSEK.


## Running Experiments

The main numerical experiments presented in the paper can be reproduced using the following Jupyter notebooks:

- `convergence_rates.ipynb`: Reproduces Figure 1, Figure 3, and Figure 4.

- `parameter_grid_search.ipynb`: Reproduces Figure 2.

- `lasso_test.ipynb`: Reproduces Figure 5.




## Contact

🧑‍💻 Meisam Tavakoli

📧 meisam.tavakoli@studio.unibo.it

🧑‍💻 Fabian Jakob

📧 fabian.jakob@ist.uni-stuttgart.de
