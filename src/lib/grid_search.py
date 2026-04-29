import numpy as np
import os
import json
from lib.convergence_analysis import compute_rho_for_acc_admm
 


def choose_adaptive_intervals(
    kappa: float,
    n_points: int = 100,
    center=None,
    span=None,
    iteration: int = 0,
    shrink_factor: float = 0.5,
):
    """
    Adaptive grid search intervals.

    Iteration 0:
        v1 in [0, 5]
        v2 in [0, 2]

    Later iterations:
        use the best point from the previous iteration and the previous
        interval upper bounds to shrink the search region toward 0.
    """

    if center is None or span is None or iteration == 0:
        v1_min, v1_max = 0, 5
        v2_min, v2_max = 0, 2
    else:
        best_v1, best_v2 = center
        prev_v1_max, prev_v2_max = span

        
        r1 = best_v1 / prev_v1_max if prev_v1_max > 0 else 0.0
        r2 = best_v2 / prev_v2_max if prev_v2_max > 0 else 0.0

        
        frac1 = max(0.3, min(0.8, r1 ** shrink_factor))
        frac2 = max(0.3, min(0.8, r2 ** shrink_factor))

        v1_min = 0.0
        v2_min = 0.0
        v1_max = prev_v1_max * frac1
        v2_max = prev_v2_max * frac2

    v1_grid = np.linspace(v1_min, v1_max, n_points)
    v2_grid = np.linspace(v2_min, v2_max, n_points)
    

    return v1_grid, v2_grid


def run_grid_search(kappa, *, threshold, n_ZF, algo, alpha, n_points, json_filename, key):
    """
    If kappa is a float → evaluate one κ.
    If kappa is a list/array → evaluate all κ values in a loop.
    Save all results into `json_filename`.
    """

    
    if not isinstance(kappa, (int, float)):   # list, array, iterable
        all_results = {}

        for k in kappa:
            r = run_grid_search(float(k), threshold=threshold, n_ZF=n_ZF, algo=algo, alpha=alpha,
                n_points=n_points, json_filename=json_filename, key=key)
            all_results[str(k)] = r
        return all_results

    
    kappa = float(kappa)

    def _resolve(th, k):
        if callable(th):
            return float(th(k))
        if isinstance(th, dict):
            return float(th.get(k, np.inf))
        return float(th)

    L = kappa
    best_v1 = None
    best_v2 = None
    best_rate = float("inf")

    max_iter = 6       # number of zoom steps
    tol = 1e-7         

    span = None        

    for it in range(max_iter):

        # generate adaptive grid using the best point from the previous iteration
        v1_values, v2_values = choose_adaptive_intervals(
            kappa,
            n_points=n_points,
            center=(best_v1, best_v2) if best_v1 is not None and best_v2 is not None else None,
            span=span,
            iteration=it,
        )

        cutoff = _resolve(threshold, kappa)
        prev_best = best_rate

        current_best_rate = best_rate
        current_best_v1 = best_v1
        current_best_v2 = best_v2

        for v1 in v1_values:
            for v2 in v2_values:
                try:
                    rate = compute_rho_for_acc_admm(
                        1, L, n_ZF,
                        algo=algo,
                        v1=v1,
                        v2=v2,
                        rho_max=1.3,
                        eps=1e-6,
                        alpha=alpha
                    )
                except Exception:
                    continue

                if rate <= cutoff:
                    print(f"[Iter {it}] κ={kappa:.3g} | v1={v1:.5f} v2={v2:.5f} | rate={rate:.5f}")

                    if rate < current_best_rate:
                        current_best_rate = rate
                        current_best_v1 = float(v1)
                        current_best_v2 = float(v2)

        # update global best after finishing this iteration
        best_rate = current_best_rate
        best_v1 = current_best_v1
        best_v2 = current_best_v2

        print(f"--> Iter {it} BEST: rate={best_rate:.6f}, v1={best_v1}, v2={best_v2}")

        # save current interval upper bounds for the next iteration
        span = (float(v1_values[-1]), float(v2_values[-1]))

        # stopping condition
        if abs(prev_best - best_rate) < tol:
            print(f"Converged at iteration {it}")
            break


    def _unique(lst):
        out, seen = [], set()
        for x in lst:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    
    result = {
    "kappa": kappa,
    "best_rate": best_rate,
    "v1": float(best_v1) if best_v1 is not None else None,
    "v2": float(best_v2) if best_v2 is not None else None,
    }

    ### save jason ###
    # load existing content if present
    data = {}
    if os.path.exists(json_filename):
        try:
            with open(json_filename, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    data[key] = {}
    data[key][str(float(kappa))] = result
    with open(json_filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Stored κ={kappa} results in '{json_filename}'")

    return result


def load_results(key, json_filename="results.json"):
    if not os.path.exists(json_filename):
        raise FileNotFoundError(f"File '{json_filename}' does not exist.")

    with open(json_filename, "r") as f:
        data = json.load(f)

    if key not in data:
        raise KeyError(f"Key '{key}' not found in '{json_filename}'.")

    dataset = data[key]

    kappa_values = []
    rate_values = []
    v1_values = []
    v2_values = []

    for _, result in dataset.items():
        kappa_values.append(result["kappa"])
        rate_values.append(result["best_rate"])
        v1_values.append(result["v1"])
        v2_values.append(result["v2"])

    return kappa_values, rate_values, v1_values, v2_values