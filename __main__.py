from tabulate import tabulate

from transaction import TransactionGen

def generateTransactionsOnly(batch_size):
  generator = TransactionGen()
  transaction_list = generator.generateTransactions(batch_size)

  print("Transaction Information:")
  table = [["Date", "Previous", "Amount", "Type", "Debit", "Credit"]]

  for transaction in transaction_list:
    debit = ""
    credit = ""

    for account in transaction.cash_flows['debit']:
      debit += f"{account}\n"
    debit = debit[:-1]

    for account in transaction.cash_flows['credit']:
      credit += f"{account}\n"
    credit = credit[:-1]

    row = []
    row.append(transaction.date)
    row.append(transaction.orig_date)
    row.append(f"{transaction.amount:,}")
    row.append(transaction.type_)
    row.append(debit)
    row.append(credit)
    table.append(row)

  print(tabulate(table, headers="firstrow", 
                        tablefmt="pipe", 
                        colalign=('left', 'left', 'right', 'left', 'left')))

  print("\nEntries:")
  table = [["Date", "Entry"]]

  for transaction in transaction_list:
    row = []
    row.append(transaction.date)
    row.append(transaction.entry)
    table.append(row)

  print(tabulate(table, headers="firstrow", tablefmt="pipe"))

# END generateTransactionsOnly

while True:
  try:
    choice = int(input(
"""
Enter the number of the action you want to perform.
[0] - Exit (Or you could just close the prompt I guess)
[1] - Generate transactions only
[WIP] - Generate a financial position statement
>>> """))
  except ValueError:
    print("\nPlease enter a valid number!\n")
    continue

  if choice == 0:
    break

  elif choice == 1:
    while True:
      try:
        batch_size = int(input("How many transactions would you like to generate? (Cancel: 0)\n>>> "))
        break
      except ValueError:
        print("Please enter a valid number!\n")
        continue

    print("\n")
    generateTransactionsOnly(batch_size)

  else:
    print("\nPlease enter a valid number!\n")