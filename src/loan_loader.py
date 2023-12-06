"""Manage loan objects."""

import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

import numpy as np
import pandas as pd


def process_loan_csv(csv_input):
    """Load Loan class objects from csv input file."""
    
    loans_from_csv = pd.read_csv(
        csv_input, skip_blank_lines=True, comment="#"
    ).to_dict(orient="records")

    loaded_loans = [Loan(**loan) for loan in loans_from_csv]
    
    return loaded_loans


class Loan():
    def __init__(
        self, name: str, balance: float, 
        min_payment: float, interest_rate: float,
    ):
        """Initialize Loan object."""

        self.name = name
        self.balance = balance
        self.min_payment = min_payment
        self.interest_rate = interest_rate
        self.base_payment_timeline = self.get_payment_timeline()
        self.payment_months = len(self.base_payment_timeline)
        self.to_dict = {
            "name": self.name,
            "balance": self.balance,
            "min_payment": self.min_payment,
            "interest_rate": self.interest_rate,
            "payment_months": self.payment_months
        }

    def calculate_interest(
        self, current_balance: float
    ):
        """Calculate monthly interest rate for current balance."""
        current_interest = (current_balance * self.interest_rate) / 12
        return current_interest

    def calculate_deducted_payment(
        self, current_balance: float
    ):
        """Calculate the amount to deduct from the balance."""
        interest_portion = self.calculate_interest(current_balance)
        payment = self.min_payment - interest_portion

        return payment

    def get_payment_timeline(
        self
    ) -> pd.DataFrame:
        """Generate payment timeline."""
        current_balance = self.balance
        start_date = datetime.now().replace(day=1)
        payment_series = [{
            f"date": start_date.date(), 
            f"payment": 0, 
            f"balance": current_balance
        }]

        while current_balance > 0:
            start_date = start_date + relativedelta(months=1)

            payment = self.calculate_deducted_payment(
                    current_balance=current_balance
            )

            current_balance -= payment

            payment_series.append({
                f"date": start_date.date(),
                f"payment": payment, 
                f"balance": current_balance
            })
        df = pd.DataFrame(payment_series)
        df["min_payment"] = self.min_payment
        df.loc[df["balance"] < 0, "balance"] = 0
        df.index = pd.to_datetime(df.index)
        
        return df
    
    def add_extra_payment(self, extra_payment: float):
        self.min_payment += float(extra_payment)
        self.base_payment_timeline = self.get_payment_timeline()
        self.payment_months = len(self.base_payment_timeline)
        self.to_dict = {
            "name": self.name,
            "balance": self.balance,
            "min_payment": self.min_payment,
            "interest_rate": self.interest_rate,
            "payment_months": self.payment_months
        }
        return None

    def __repr__(self):
        return (json.dumps(self.to_dict))