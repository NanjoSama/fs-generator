from tabulate import tabulate

from transaction import TransactionGen

generator = TransactionGen()

table = [["Date", "Previous", "Entry"]]
transaction_list = generator.generateTransactions(10)

for transaction in transaction_list:
  row = []
  row.append(transaction.date)
  row.append(transaction.orig_date)
  row.append(transaction.entry)
  table.append(row)

print(tabulate(table, headers="firstrow", tablefmt="pipe"))