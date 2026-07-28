#!/usr/bin/env python3
"""
Generate learning curve figures for UPI-TRM experiments on 4x4 Sudoku.
Output:
  - figures/upi_trm_success_curve.png (success rate only)
  - figures/upi_trm_value_loss_curve.png (value loss only)

Data source: Seed 42 (representative). See Table 1 in paper for multi-seed summary.
Multi-seed peaks: 42%, 42%, 44% -> mean 42.7% ± 1.2%
Multi-seed @ step 1000: 26%, 40%, 28% -> mean 31.3% ± 7.6%
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # headless backend for CI/servers
import matplotlib.pyplot as plt
import numpy as np

# Robust output directory relative to script location
ROOT = Path(__file__).resolve().parents[1]  # .../UPI_TRM_ICLR
FIG_DIR = ROOT / "figures"


def main():
    """Generate and save all figures."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Data from experiments: Seed 42 (representative run)
    steps = np.arange(100, 1100, 100)  # Steps 100, 200, ..., 1000

    # UPI-TRM persistent latent success rates (%) - Seed 42
    upi_trm_success = np.array([30, 32, 34, 32, 32, 28, 42, 36, 32, 26])

    # Value loss at each checkpoint
    upi_trm_value_loss = np.array([92.3, 115.7, 143.3, 188.5, 31.8, 280.7, 31.5, 63.4, 34.3, 63.8])

    # PPO-TRM stays at 0%
    ppo_trm_success = np.zeros(10)

    # Set style
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'legend.fontsize': 9,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'figure.dpi': 150,
    })

    # ============================================================
    # Figure 1: Success Rate ONLY
    # ============================================================
    fig1, ax1 = plt.subplots(figsize=(5, 3.5))

    ax1.plot(steps, upi_trm_success, 'o-', color='#2E86AB', linewidth=2,
             markersize=6, label='UPI-TRM')
    ax1.plot(steps, ppo_trm_success, 'x--', color='#E94F37', linewidth=1.5,
             markersize=5, label='PPO-TRM')

    ax1.set_xlabel('Training Steps')
    ax1.set_ylabel('Success Rate (%)')
    ax1.set_title('4×4 Sudoku Success Rate (Seed 42)')
    ax1.set_xlim(0, 1100)
    ax1.set_ylim(0, 50)
    ax1.axhline(y=42, color='#2E86AB', linestyle='--', alpha=0.4, linewidth=1)
    ax1.annotate('Peak: 42%', xy=(700, 42), xytext=(550, 46),
                 fontsize=9, color='#2E86AB', alpha=0.8)
    ax1.legend(loc='lower right', framealpha=0.9)
    ax1.text(0.98, 0.25, '(3-seed avg in table)', transform=ax1.transAxes,
             fontsize=7, ha='right', va='bottom', alpha=0.6)
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "upi_trm_success_curve.png", dpi=150, bbox_inches='tight')
    print(f"Saved: {FIG_DIR / 'upi_trm_success_curve.png'}")
    plt.close(fig1)

    # ============================================================
    # Figure 2: Value Loss ONLY
    # ============================================================
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))

    ax2.plot(steps, upi_trm_value_loss, 's-', color='#E94F37', linewidth=2, markersize=6)

    ax2.set_xlabel('Training Steps')
    ax2.set_ylabel('Value Loss')
    ax2.set_title('UPI-TRM Value Loss (4×4 Sudoku, Seed 42)')
    ax2.set_xlim(0, 1100)
    ax2.set_ylim(0, 300)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "upi_trm_value_loss_curve.png", dpi=150, bbox_inches='tight')
    print(f"Saved: {FIG_DIR / 'upi_trm_value_loss_curve.png'}")
    plt.close(fig2)

    print("\nDone generating figures.")


if __name__ == "__main__":
    main()
