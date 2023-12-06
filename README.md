# Generate loan repayment simulation

steps to run:

git clone https://github.com/monkey-miner/debt-snowball-simulator.git
cd debt-snowball-simulator
pip install -r requirements.txt
${python|python3} src/main.py --csv "${loan_input.csv}" --extra_payment ${float.amount} --silent ${True|False}