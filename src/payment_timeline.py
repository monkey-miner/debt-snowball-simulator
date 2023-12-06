"""Calculate base and custom payment timelines."""

import pandas as pd

def base_payment_timelines(loans):
    """Generate a base payment timeline for all loans."""
    payment_dfs = {}
    for loan in loans:
        tmp_df = loan.base_payment_timeline
        tmp_df["extra_payment"] = 0
        payment_dfs[loan.name] = tmp_df
    return combine_loan_dfs(payment_dfs)


def combine_loan_dfs(loan_df_map: dict) -> pd.DataFrame:
    """Combine and process dataframes."""
    combined_df = pd.concat(
        list(loan_df_map.values()), axis=1, keys=list(loan_df_map.keys())
    )
    
    date_cols = [
        col for col in combined_df.columns if col[1]=="date"
    ]
    
    date_index = pd.DatetimeIndex(
        combined_df[date_cols].ffill().max(axis=1)
    )
    combined_df = (
        combined_df.set_index(date_index).drop(columns=date_cols).fillna(0)
    )
    
    return combined_df


def snowball_payment_timeline(
    loans: list, sort_col: str, ascending: bool
):
    """Create a custom snowball payment timeline."""
    loan_dicts = [loan.to_dict for loan in loans]
    loan_order = (
        pd.DataFrame(loan_dicts).sort_values(by=sort_col, ascending=ascending)
    )

    organized_loans = loan_order.name.to_list()
    custom_payment_timeline = base_payment_timelines(loans)
    total_rows = len(custom_payment_timeline)
    
    first_payment = (
        custom_payment_timeline.iloc[0:1]
        .filter(like="min_payment").sum(axis=1)[0]
    )

    for priority_loan in organized_loans:
        extra_payment_idx = 1

        while extra_payment_idx < total_rows:
            tmp_balance = (
                custom_payment_timeline[priority_loan]["balance"][extra_payment_idx-1]
            )

            last_record = custom_payment_timeline.iloc[[extra_payment_idx]].copy()
            
            extra_payment = (
                first_payment - last_record.filter(like="min_payment").sum(axis=1)[0]
            )

            total_payment = (
                    last_record[(priority_loan), "payment"] + extra_payment
            )[0]

            min_payment = last_record[(priority_loan, "min_payment")] + extra_payment

            if not (tmp_balance > 0):
                total_payment, extra_payment,  tmp_balance, min_payment = 0, 0, 0, 0

            tmp_balance -= total_payment
            last_record[(priority_loan, "payment")] = total_payment
            last_record[(priority_loan, "extra_payment")] = extra_payment
            last_record[(priority_loan, "balance")] = (tmp_balance if tmp_balance > 0 else 0)
            last_record[(priority_loan, "min_payment")] = min_payment
            custom_payment_timeline.iloc[extra_payment_idx] = last_record
            extra_payment_idx += 1
    
    custom_payment_timeline = custom_payment_timeline[custom_payment_timeline.sum(1).ne(0)]

    return custom_payment_timeline