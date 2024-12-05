import time
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from tabulate import tabulate
import multiprocess as mp
import dill

class PostProcessor:
    def __init__(self, data_filename):
        print("Started Loading Data for PostProcessor", end="... ", flush=True)
        start = time.time()
        with open(data_filename, 'rb') as handle:
            data = dill.load(handle)
        end = time.time()
        print(f"Finished in {end - start} seconds")

        # Process loaded data
        self.samples = data.get("samples")
        self.title = data.get("title")
        self.U = data.get("U")
        self.dU = data.get("dU")
        self.d = data.get("d")
        self.M = data.get("M")
        self.N = data.get("N")
        self.K = data.get("K")
        self.h = data.get("h")
        self.As = data.get("As")
        self.sim_annealing = data.get("sim_annealing")


    def plot_empirical_probabilities(self, dpi, layout="23", tols=[1,2,3,4,5,6], running=False):
        # Ensure layout is valid
        if layout not in ["13", "23"]:
            raise ValueError("layout must be one of '13' or '23'")

        # Create subplots
        tiles = (1, 3) if layout == "13" else (2, 3)
        fig, axs = plt.subplots(*tiles, figsize=(12, 4) if layout == "13" else (12, 8), sharex=True, sharey=True)

        # Set title to subplots
        fig.suptitle(rf"Empirical $P(U(X_k)-U^*\leq \varepsilon)$ for {self.title} function with $d={self.d}$")

        def plot_tol_curve(p_idx):
            # Retrieve tolerance and axis
            tol = tols[p_idx]
            ax = axs[p_idx // 3][p_idx % 3] if layout == "23" else axs[p_idx]

            # Plot a curve per value of a
            for i, a in enumerate(self.As):
                # Compute each empirical probability
                probs = np.zeros(self.K // dpi)
                for k in range(0, self.K, dpi):
                    bests_U = [min([self.U(x[k]) for x in samples[i]]) for samples in self.samples]
                    probs[k // dpi] = len(list(filter(lambda u: u <= tol, bests_U))) / self.M

                    # Take the running best if running is specified
                    if running and k // dpi > 0:
                        probs[k // dpi] = max(probs[k // dpi], probs[k // dpi - 1])

                # Plot the computed curve
                ax.plot(range(0, self.K, dpi), probs, label=rf"$a={a}$" if not self.sim_annealing else r"$\overline{a}=$" + rf"${a}$")

                # Define axis limits
                ax.set_ylim(-0.02, 1.02)
                ax.set_xlim(0, self.K-1)

                # Add a badge 
                ax.text(0.95, 0.95, rf"$\varepsilon={tol}$", transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                
                # Set axis labels depending on positive
                if (p_idx // 3 == 0 and layout == "13") or (p_idx // 3 == 1 and layout == "23"):
                    ax.set_xlabel(r"Iteration count ($k$)")
                if p_idx % 3 == 0:
                    ax.set_ylabel(rf"$P(U(X_k)-U^*\leq \varepsilon)$")

        # Plot each tolerance plot
        for i in tqdm(range(len(tols)), desc="Plotting Empirical Probabilities"):
            plot_tol_curve(i)

        # Create figure legend
        ax = axs[0][0] if layout == "23" else axs[0]
        handles, labels = ax.get_legend_handles_labels()
        plt.tight_layout()
        fig.legend(handles, labels, loc='lower center', ncol=len(self.As), bbox_to_anchor=(0.5, 0))
        plt.subplots_adjust(bottom=0.2 if layout == "13" else 0.1)

        # Save and show plot
        if not os.path.exists("output"):
            os.makedirs("output")
        if not os.path.exists("output/plots"):
            os.makedirs("output/plots")
        plotname = f"output/plots/{self.title}_{time.time()}.png"
        plt.savefig(plotname)
        print(f"[SUCCESS] Saving plot to {plotname}")
        plt.show()

    def compute_tables(self, measured, dpi, mode="mean", running=True):
        # Check validity of mode
        if mode not in ["mean", "std", "best"]:
            raise ValueError("mode must be one of 'mean', 'std' or 'best'")

        # Function to compute the wanted quantity
        def compute_task(task_nb):
            a = self.As[task_nb]
            bests_sub = ["" for i in range(len(measured) + 1)]
            bests_sub[0] = f"a={a}"
            for i, k in enumerate(measured):
                if running:
                    bsts = [min([min([self.U(x[kk-1]) for kk in range(dpi, k + dpi, dpi)]) for x in samples[i]]) for samples in self.samples]
                else:
                    bsts = [min([U(x[k-1]) for x in samples[task_nb]]) for samples in self.samples]
                if mode == "mean":
                    bests_sub[i+1] = f"& {np.mean(bsts):.4f}"
                elif mode == "std":
                    bests_sub[i+1] = f"& {np.std(bsts):.4f}"
                elif mode == "best":
                    bests_sub[i+1] = f"& {np.min(bsts):.4f}"

            return bests_sub

        # Compute for each value of a in parallel
        with mp.Pool() as pool:
            bests = pool.map(compute_task, range(len(self.As)))
        
        # Add header row with number of iterations
        bests = [[""] + [f"K={K}" for K in measured], *bests]

        # Function to get transpose of matrix
        transpose = lambda X: [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]

        # Print the results
        bests[0][0] = mode
        print()
        print(tabulate(bests, headers="firstrow"))
        bests[0][0] = f"{mode}.T"
        print()
        print(tabulate(transpose(bests), headers="firstrow"))