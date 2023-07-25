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
      return list(json.load(file).values())[0]

  def generateAccounts(self, min_amount=100_000, max_amount=1_000_000):
    # Length check. (TODO: There must be a better way of doing this.)
    debit_length = 0
    credit_length = 0
    for data in self.account_list:
      if data[2] == "debit":
        debit_length += 1
      if data[2] == "credit":
        credit_length += 1

    len1 = min(debit_length, credit_length)
    len2 = max(debit_length, credit_length)

    # Generate the first list.
    list1 = [random.randint(min_amount, max_amount) for _ in range(len1)]

    # Calculate the sum of the first list, the average, and its modulo
    # remainder
    target = sum(list1)
    avg = target // len2
    rem = target % len2

    # Generate the second list using the average. Populate it with `len2 - 1`
    # instances of the average, then append the average again plus its
    # remainder.
    list2 = [avg] * (len2 - 1) + [avg + rem]

    # Calculate the max variation to be used for modification.
    max_var = min((avg - min_amount), (max_amount - avg))

    # Variate the integers in the list. AKA add a variation from one integer
    # and subtract it from another.
    for i in range(1, len2, 2):
      integer = random.randint(1, max_var)
      list2[i-1] += integer
      list2[i] -= integer

    # Shuffle for good measure.
    random.shuffle(list2)

    # Assign the lists to debit and credit
    if debit_length <= credit_length:
      debit_list = list1
      credit_list = list2
    elif credit_length < debit_length:
      credit_list = list1
      debit_list = list2

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

