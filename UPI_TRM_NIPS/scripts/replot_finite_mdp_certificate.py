#!/usr/bin/env python3
"""Re-render the Finite-MDP certificate figures from cached .dat files.

Reads ``fig_value_decomposition.dat`` and ``fig_cpi_certificate.dat`` that were
written by ``experiments/finite_mdp_certificate.py`` and re-plots them with
matplotlib using thicker lines, larger fonts, and a larger legend. This
avoids depending on gnuplot and keeps the underlying data untouched.

Usage:
    python3 scripts/replot_finite_mdp_certificate.py \
        [--indir results/finite_mdp_certificate] \
        [--outdir results/finite_mdp_certificate] \
        [--suffix ""]

Outputs are written as ``fig_value_decomposition<suffix>.pdf`` and
``fig_cpi_certificate<suffix>.pdf`` (and matching .png files).
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Palette matches the original gnuplot figures.
LZ_COLORS = {
    0.20: "#1b9e77",
    0.50: "#d95f02",
    0.80: "#7570b3",
    0.95: "#e7298a",
}

CPI_COLORS = {
    "gap":             "#0f4c81",
    "penalty_decomp":  "#c0392b",
    "penalty_exact":   "#2d8659",
}


def read_tsv(path: Path) -> Tuple[List[str], List[List[float]]]:
    with path.open("r", encoding="ascii") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        rows = [[float(x) for x in row] for row in reader if row]
    return header, rows


def plot_value_decomposition(
    data_path: Path,
    pdf_path: Path,
    png_path: Path,
    line_width: float,
    font_size: float,
    legend_font_size: float,
) -> None:
    header, rows = read_tsv(data_path)
    n_col = [int(r[0]) for r in rows]

    lz_pairs: List[Tuple[float, int, int]] = []
    for idx, name in enumerate(header):
        if name.startswith("err_"):
            L_z = float(name.split("_", 1)[1])
            bound_idx = header.index(f"bound_{name.split('_', 1)[1]}")
            lz_pairs.append((L_z, idx, bound_idx))

    fig, ax = plt.subplots(figsize=(9.0, 7.5))
    for L_z, err_idx, bound_idx in lz_pairs:
        color = LZ_COLORS.get(round(L_z, 2), None)
        err = [r[err_idx] for r in rows]
        bnd = [r[bound_idx] for r in rows]
        ax.plot(n_col, err,
                color=color, linewidth=line_width, linestyle="-",
                label=f"$L_z={L_z:.2f}$ error")
        ax.plot(n_col, bnd,
                color=color, linewidth=line_width, linestyle="--",
                label=f"$L_z={L_z:.2f}$ bound")

    ax.set_yscale("log")
    ax.set_xlabel("Evaluator depth $n$", fontsize=font_size)
    ax.set_ylabel("Value error / certificate", fontsize=font_size)
    ax.set_title("Finite-MDP value-error decomposition", fontsize=font_size)
    ax.tick_params(axis="both", which="major", labelsize=font_size - 1)
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.7)

    fig.subplots_adjust(left=0.10, right=0.98, top=0.94, bottom=0.30)
    leg = fig.legend(loc="lower center", bbox_to_anchor=(0.5, 0.00),
                     ncol=2, frameon=True, fontsize=legend_font_size,
                     columnspacing=2.0, handlelength=2.4, handletextpad=0.5)
    leg.get_frame().set_linewidth(0.8)

    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=200)
    plt.close(fig)


def plot_cpi_certificate(
    data_path: Path,
    pdf_path: Path,
    png_path: Path,
    line_width: float,
    marker_size: float,
    font_size: float,
    legend_font_size: float,
) -> None:
    _header, rows = read_tsv(data_path)
    alpha = [r[0] for r in rows]
    gap   = [r[1] for r in rows]
    pd_   = [r[2] for r in rows]
    pe_   = [r[3] for r in rows]

    fig, ax = plt.subplots(figsize=(9.0, 7.5))
    ax.plot(alpha, gap,
            color=CPI_COLORS["gap"], linewidth=line_width, linestyle="-",
            marker="o", markersize=marker_size,
            label=r"$\hat L - \eta$")
    ax.plot(alpha, pd_,
            color=CPI_COLORS["penalty_decomp"], linewidth=line_width, linestyle="--",
            marker="s", markersize=marker_size,
            label="decomposition penalty")
    ax.plot(alpha, pe_,
            color=CPI_COLORS["penalty_exact"], linewidth=line_width, linestyle=":",
            marker="^", markersize=marker_size,
            label=r"exact $A$ penalty")

    ax.set_yscale("log")
    ax.set_xlim(0.05, 1.0)
    ax.set_xlabel(r"Mixture weight $\alpha$", fontsize=font_size)
    ax.set_ylabel("Positive surrogate gap / certificate", fontsize=font_size)
    ax.set_title("Finite-MDP CPI certificate (log scale)", fontsize=font_size)
    ax.tick_params(axis="both", which="major", labelsize=font_size - 1)
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.7)

    fig.subplots_adjust(left=0.12, right=0.98, top=0.94, bottom=0.30)
    leg = fig.legend(loc="lower center", bbox_to_anchor=(0.5, 0.08),
                     ncol=3, frameon=True, fontsize=legend_font_size,
                     columnspacing=1.8, handlelength=2.4, handletextpad=0.5)
    leg.get_frame().set_linewidth(0.8)

    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=200)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indir", type=Path,
                        default=Path("results/finite_mdp_certificate"),
                        help="Directory containing the cached .dat files.")
    parser.add_argument("--outdir", type=Path, default=None,
                        help="Directory to write figures to (defaults to --indir).")
    parser.add_argument("--suffix", default="",
                        help="Optional filename suffix (e.g. _large).")
    parser.add_argument("--line-width", type=float, default=3.0,
                        help="Line width for plotted curves.")
    parser.add_argument("--marker-size", type=float, default=9.0,
                        help="Marker size for CPI linespoints.")
    parser.add_argument("--font-size", type=float, default=18.0,
                        help="Axis-label and title font size (pt).")
    parser.add_argument("--legend-font-size", type=float, default=17.0,
                        help="Legend font size (pt).")
    args = parser.parse_args()

    indir = args.indir.resolve()
    outdir = (args.outdir or args.indir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    plot_value_decomposition(
        data_path=indir / "fig_value_decomposition.dat",
        pdf_path=outdir / f"fig_value_decomposition{args.suffix}.pdf",
        png_path=outdir / f"fig_value_decomposition{args.suffix}.png",
        line_width=args.line_width,
        font_size=args.font_size,
        legend_font_size=args.legend_font_size,
    )
    plot_cpi_certificate(
        data_path=indir / "fig_cpi_certificate.dat",
        pdf_path=outdir / f"fig_cpi_certificate{args.suffix}.pdf",
        png_path=outdir / f"fig_cpi_certificate{args.suffix}.png",
        line_width=args.line_width,
        marker_size=args.marker_size,
        font_size=args.font_size,
        legend_font_size=args.legend_font_size,
    )
    print(f"Wrote figures to {outdir}")


if __name__ == "__main__":
    main()
