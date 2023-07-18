from tabulate import tabulate

from transaction import TransactionGen

generator = TransactionGen()

table = [["Date", "Previous", "Amount", "Type", "Entry"]]
transaction_list = generator.generateTransactions(10)

for transaction in transaction_list:
  row = []
  row.append(transaction.date)
  row.append(transaction.orig_date)
  row.append(f"{transaction.amount:,}")
  row.append(transaction.type_)
  row.append(transaction.entry)
  table.append(row)

print(tabulate(table, headers="firstrow", tablefmt="pipe", colalign=('left', 'left', 'right', 'left')))