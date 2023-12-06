"""Provide summary analysis and output timelines to file."""

import pandas as pd

from payment_timeline import base_payment_timelines, snowball_payment_timeline


def generate_snowball_comparison(
    loans: list, 
    output_file: str="debt_snowball_analysis.xlsx", 
    prompt_view: bool=False
):
    """Create snowball comparison for all sort options."""

    sort_cols = [
        col for col in pd.DataFrame([loan.to_dict for loan in loans]).columns 
        if not col=='name'
    ]

    ascending_map = {
        "ascending": True,
        "descending": False
    }

    dfs = {
        "original_payment_timeline": base_payment_timelines(loans)
    }

    for sort_col in sort_cols:
        for order_key, order_value in ascending_map.items():
            print(f"Running: {sort_col} {order_key}: {order_value}")
            dfs[f"{sort_col}_{order_key}"] = snowball_payment_timeline(
                loans, sort_col=sort_col, ascending=order_value
            )

    output_snowball(
        snowball_dfs=dfs, output_file=output_file, prompt_view=prompt_view
    )

    priority_options = {str(i+1): col for i, col in enumerate(sort_cols)}
    
    order_options = {
        str(i+1): order for i, order in enumerate(["ascending", "descending"])
    }

    selected_view = "2"
    selected_order = "1"

    if prompt_view:
        selected_view = input(
            f"Which view would you like to see more detail on?:\n{priority_options}\n"
        )
        selected_order = input(
            f"Would you like the loans {selected_view} sorted"
            f"ascending or descending?:\n{order_options}\n"
        )

    preview_plan(
        loans=loans, snowball_dfs=dfs, 
        sort_col=priority_options[selected_view], ascending=order_options[selected_order]
    )

    print(
        "You can view your results in more detail in the "
        f"{output_file} file in this directory"
    )
    
    return dfs


def output_snowball(
    snowball_dfs: dict, output_file: str, prompt_view: bool
) -> str:
    """Provide output file and summary of comparison."""
    output_snowball_comparison(
        snowball_dfs=snowball_dfs, output_file=output_file
    )
    
    summary_overview = summarize_snowball_comparison(snowball_dfs=snowball_dfs)
    print_overview_to_screen(summary_overview, prompt_view=prompt_view)

    return None


def output_snowball_comparison(
        snowball_dfs: dict, output_file: str
    ) -> dict:
    """Output comparison payment timelines."""
    with pd.ExcelWriter(
        output_file,
        date_format="%m-%d-%Y",
        datetime_format="%m-%d-%Y"
    ) as writer:
        for sheet_name, df in snowball_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name)
    
    return None


def summarize_snowball_comparison(snowball_dfs: dict) -> dict:
    """Summarize snowball comparisons."""

    return {
        k: {
            "months": len(v), 
            "last_payment_date": (
                v.tail(1).reset_index()["index"].dt.date[0].strftime("%m-01-%Y")
            ),
            "total_payments": v.filter(like="min_payment").sum().sum().round(2)
        }
        for k, v in snowball_dfs.items()
    }


def print_overview_to_screen(overview: dict, prompt_view: bool):
    """Output overview summary to screen."""

    overview_options = {
        str(i+1): v for i, v in enumerate(["months", "total_payments"])
    }

    selected_priority = "1"

    if prompt_view:
        selected_priority = input(
            "How would you like to prioritize the results overview?:"
            f"\n{overview_options}\n"
        )
    
    sorted_overview = sorted(
        overview.items(), 
        key=lambda x: x[1].get(
            overview_options[selected_priority]
        )
    )

    for key, value in sorted_overview:
        print(
            f"{key}:\n\tMonths: {value['months']}"
            f" (Roughly {value['months']/12: .2f} Years)"
            f"\n\tLast Payment: {value['last_payment_date']}",
            f"\n\tTotal Payments: {value['total_payments']}"
        )

    return None


def preview_plan(
    loans: list, snowball_dfs: dict, 
    sort_col: str, ascending: str
) -> pd.DataFrame:
    """Preview the selected snowball payment plan."""
    
    sort_direction = ascending == "ascending"
    
    loans_df = (
        pd.DataFrame(
            [loan.to_dict for loan in loans]    
        ).sort_values(by=sort_col, ascending=sort_direction)
    )

    total_balance = loans_df["balance"].sum()
    monthly_payment = loans_df["min_payment"].sum()

    print(
        f"Original total debt: {total_balance: .2f}"
        f"Total monthly payments: {monthly_payment}"
    )
    print(f"{sort_col} view will prioritize loans in the following order:")
    print(loans_df["name"].reset_index(drop=True))
    print(snowball_dfs[f"{sort_col}_{ascending}"])
    
    return None
