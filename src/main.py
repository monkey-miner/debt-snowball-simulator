import argparse

import pandas as pd

from loan_loader import process_loan_csv
from analysis import generate_snowball_comparison
from extra_payment import optimize_extra_payment

def get_args():
    """Get command line inputs."""
    parser = argparse.ArgumentParser(
        prog="DebtSnowballSimulator",
        description=(
            "Takes in loan data and provides "
            "comparable snowball payment timelines"
        )
    )

    parser.add_argument(
        "--csv",
        help=(
            "Provide the csv filename that contains loan data."
            "Default: loan_input.csv"
        ), 
        required=True
    )

    parser.add_argument(
        "--silent",
        help=("Runs without prompting for input preferences."),
        default=False, required=False
    )

    parser.add_argument(
        "--extra_payment", type=float,
        help=(
            "Optional: Provide extra payment for additional simulation."
            "Default: 0.0"
        ), required=False, default=0.0
    )

    return parser


if __name__ == "__main__":

    local_args = get_args().parse_args()

    loans = process_loan_csv(local_args.csv)

    generate_snowball_comparison(
        loans=loans, prompt_view=not(local_args.silent)
    )

    if local_args.extra_payment:
        optimize_extra_payment(
            loans=loans, 
            extra_payment=local_args.extra_payment
        )