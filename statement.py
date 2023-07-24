import json
import random

from tabulate import tabulate

class Account(object):
  def __init__(self, acct_data, amount):
    self.id_ = acct_data[0]
    self.type_ = acct_data[1]
    self.flow = acct_data[2]
    self.amount = amount

class FinancialPosition(object):
  def __init__(self):
    self.account_list = self.loadJSON()
    self.data = []
    self.debit_total = 0
    self.credit_total = 0

  def loadJSON(self):
    with open("statement_db.json") as file:
      return json.load(file)

  def generateAccounts(self, min_amount=100000, max_amount=1000000):
    for data in list(self.account_list.values())[0]:
      amount = random.randint(min_amount, max_amount)

      if data[2] == "debit":
        self.debit_total += amount
      elif data[2] == "credit":
        self.credit_total += amount
      else:
        print([print(i) for i in data])
        print()
        message = f"Invalid flow direction: {data[2]}"
        raise ValueError(message)

      self.data.append(Account(data, amount))


  def tabulate(self):
    table = [["ID", "Account", "Debit", "Credit"]]

    for data in self.data:
      flow = ""
      row = []

      row.append(data.id_)
      row.append(data.type_)

      if data.flow == "debit":
        row.append(f"{data.amount:,}")
        row.append("")
      elif data.flow == "credit":
        row.append("")
        row.append(f"{data.amount:,}")
      else:
        message = f"Invalid flow direction.:{data.flow}"
        raise ValueError(message)

      table.append(row)

    table.append(["", "Total", f"{self.debit_total:,}", f"{self.credit_total:,}"])

    return tabulate(table, headers="firstrow", 
                           tablefmt="pipe",
                           colalign=('left', 'left', 'right', 'right'))

