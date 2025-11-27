[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Meisam%20Tavakoli-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meisam-tavakoli)
[![GitHub](https://img.shields.io/badge/GitHub-Meisam--Tavakoli--97-181717?style=flat&logo=github&logoColor=white)](https://github.com/Meisam-Tavakoli-97)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-4285F4?style=flat&logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=aAzQLBoAAAAJ&hl=en)




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
