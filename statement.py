import json
import random

from tabulate import tabulate

class Account:
  def __init__(self, acct_data, amount):
    self.acct_id = acct_data[0]
    self.acct_type = acct_data[1]
    self.acct_flow = acct_data[2]
    self.amount = amount

class FinancialPosition:
  def __init__(self):
    self.account_list = self.loadJSON("statement_db.json")
    self.data = []
    self.debit_total = 0
    self.credit_total = 0

  def loadJSON(self, filename):
    with open(filename) as file:
      return list(json.load(file).values())[0]

  def generateAccounts(self, min_amount=100_000, max_amount=1_000_000):
    # Split account list between direction of cash flow.
    debit_accounts = [data for data in self.account_list if data[2] == "debit"]
    credit_accounts = [data for data in self.account_list if data[2] == "credit"]
    len1 = min(len(debit_accounts), len(credit_accounts))
    len2 = max(len(debit_accounts), len(credit_accounts))

    # Generate the first list, calculate the sum of the first list, the
    # average, and its modulo remainder
    list1 = [random.randint(min_amount, max_amount) for _ in range(len1)]
    target = sum(list1)
    avg = target // len2
    rem = target % len2

    # Generate the second list using the average. Populate it with `len2 - 1`
    # instances of the average, then append the average again plus its
    # remainder.
    list2 = [avg] * (len2 - 1) + [avg + rem]

    # Calculate the max variation to be used for modification.
    max_var = min((avg - min_amount), (max_amount - avg))

    # Variate the integers in the list.
    for i in range(1, len2, 2):
      integer = random.randint(1, max_var)
      list2[i-1] += integer
      list2[i] -= integer

    # Shuffle for good measure.
    random.shuffle(list2)

    # Assign the lists to debit and credit
    debit_list = list1 if len(debit_accounts) <= len(credit_accounts) else list2
    credit_list = list1 if len(credit_accounts) < len(debit_accounts) else list2

    # Pop the lists and assign the amounts to the accounts. Totals are also
    # calculated.
    for data in self.account_list:
      amount = 0
      if data[2] == "debit":
        amount = debit_list.pop()
        self.debit_total += amount
      elif data[2] == "credit":
        amount = credit_list.pop()
        self.credit_total += amount
      else:
        message = f"Invalid flow direction: {data[2]}"
        raise ValueError(message)

      self.data.append(Account(data, amount))

  def tabulate(self):
    table = [["ID", "Account", "Debit", "Credit"]] + [
      [data.acct_id, data.acct_type, f"{data.amount:,}", ""]
        if data.acct_flow == "debit"
        else [data.acct_id, data.acct_type, "", f"{data.amount:,}"]
        for data in self.data
    ]

    table.append(["", "Total", f"{self.debit_total:,}", f"{self.credit_total:,}"])

    return tabulate(table, headers="firstrow", 
                           tablefmt="pipe",
                           colalign=('left', 'left', 'right', 'right'))

