# Generate loan repayment simulation

steps to run from command line:

1. Clone the repo locally
3. Navigate to the local repo
4. Install requirements
5. Run the program with arguments


```
git clone https://github.com/monkey-miner/debt-snowball-simulator.git
cd debt-snowball-simulator
pip install -r requirements.txt
${python|python3} src/main.py --csv "${loan_input.csv}" --extra_payment ${float.amount} --silent ${True|False}
```
