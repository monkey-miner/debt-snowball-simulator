"""Run comparison with extra payment applied."""

from copy import deepcopy

from analysis import generate_snowball_comparison

def optimize_extra_payment(loans: list, extra_payment: float):
    """Generate analysis based on extra payment."""
    str_extra_payment = f"{extra_payment: .2f}"
    loans_copy = deepcopy(loans)

    for i, loan in enumerate(loans_copy):

        loans_copy[i].add_extra_payment(extra_payment=extra_payment)
        
        extra_payment_filename = (
            "extra_payment_snowball_"
            f"{str_extra_payment.split('.')[0]}_{loan.name}.xlsx"
        )

        generate_snowball_comparison(
            loans=loans_copy, 
            output_file=extra_payment_filename, 
            prompt_view=False
        )
        
        loans_copy = deepcopy(loans)