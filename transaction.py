from datetime import date

import json
import random

class Transaction(object):
  """
  A transaction. It contains information about the following:
  * The kind of transaction it is. (TODO: I used the word account for some reason.)
  * The entry itself in plain text.
  * The date of transaction.
  * If the transaction is related to a previous transaction, the date of the
    transaction in question.

  TODO:
  * The amount of money exchanged in the transaction.
  * The flow of accounts, i.e. accounts debited and credited.
  """
  def __init__(self, account, entry, date, orig_date=None):
    """
    Initialize the attributes.

    Arguments:
      `account`: The transaction in question. (TODO: Again, transaction, not
        account.)
      `entry`: The entry in plain text.
      `date`: The date of transaction.
      `orig_date`: If the transaction is related to a previous transaction,
        the date of the transaction in question.
    """

    self.account = account
    self.entry = entry
    self.date = date
    self.orig_date = orig_date

  def __str__(self):
    return self.entry

class TransactionGen:
  """
  This class handles generating transactions for general journal entries. It
  picks a random name from a predetermined list of names for suppliers and
  customers, a random date within a single month, and a random amount for the
  user (and the program) to work with.
  """

  def __init__(self):
    """
    Read the JSON database that will be used throughout the lifetime of the
    program, then divide the data into separate attributes for convenience and
    readability.
    """

    self.data = self.loadJSON()
    self.cash_flows = self.data["cash_flows"]
    self.entries = self.data["entries"]
    self.accounts = list(self.cash_flows.keys())
    self.names = self.data["names"]

    self.generated_accounts = []
    self.generated_transactions = []
    self.generated_dates = []

  def _convertToTransaction(self, account, entry, date, orig_date=None, min_amount=100000, max_amount=10000000):
    """
    Entries in the database contains placeholder text like `name` and `amount`.
    Replace the placeholder text with a random value the placeholder asks for,
    then convert it into a transaction object.

    '`amount`' is replaced by a random value between a range specified by the
    user, or by default, between 100k and 10m. (TODO: Maybe make it more
    dynamic make it more accurate to the account it's for.)

    '`name`' is replaced by a random name in the database's predetermined list
    of names. This method also detects whether the name is of a supplier's or
    a customer's.

    Arguments:
      `account`: The transaction type. (TODO: Transaction, not account.)
      `entry`: The entry to handle.
      `date`: The date of an original transaction.
      `min_amount`: The minimum amount for randomization.
      `max_amount`: The maximum amount for randomization.

    Returns:
      The transaction in object form.
    """

    if "`amount`" in entry:
      random_amount = random.randint(min_amount, max_amount)
      entry = entry.replace("`amount`", f"PHP {format(random_amount, ',')}")

    if "`name`" in entry:
      if account in ["purchases", "purchase_return", "account_payment"]:
        random_name = random.choice(self.names["suppliers"])
      elif account in ["sales", "sales_return", "account_collection"]:
        random_name = random.choice(self.names["customers"])
      else:
        random_name = "`NAME ERROR`"
      entry = entry.replace("`name`", random_name)

    return Transaction(account, entry, date, orig_date)

  def loadJSON(self):
    """
    Load the database the class will work with.

    Returns:
      A dictionary containing the data from the JSON database.
    """

    with open("transaction_db.json") as file:
      return json.load(file)

  def generateDate(self, year=0, month=0, min_day=1):
    """
    Generate a random date for an entry. The user may specify a year and/or
    month to use instead of a random one. Transactions related to a previous
    transaction will use a minimum day to place the new date after that
    transaction date.

    Arguments:
      `year`: The year to be used. If none specified, a random year between
        2020 and 2030 will be used.
      `month`: The month to be used. If none specified, a random month will be
        used.
      `min_day`: The minimum day. If specified, the random date will be a date
        after input day.

    Returns:
      A `datetime.date` object containing the final randomized date.
    """

    if year == 0:
      year = random.randint(2020, 2030)
    if month == 0:
      month = random.randint(1, 12)

    # Subtract current month from the month after to get number of days in month
    days_in_month = (date(year, month + 1, 1) - date(year, month, 1)).days

    while True:
      day = random.randint(min_day+1, days_in_month)
      if (min_day < days_in_month) or (min_day > 1):
        break

    random_date = date(year, month, day)
    return random_date

  def generateName(self, category):
    """
    Pick a random name under either the 'customers' or 'suppliers' category
    from the database's list of names.

    Arguments:
      `category`: Either 'customers' and 'suppliers'.
    
    Returns:
      The final randomized name string.
    """
    return random.choice(self.data["names"][category])

  def generateTransactions(self, batch_size=5):
    """
    Generate a batch of randomized entries. The batch size, may be specified
    by the user. The main attraction of the class.

    This method will not add transactions that require a previous date to the
    batch list. It will automatically sort the transactions by date.

    Arguments:
      `batch_size`: The number of entries to generate. By default, 5 entries
      will be generated.

    Return:
      The list of randomly generated entries.
    """

    for _ in range(batch_size):
      try:
        date = self.generateDate(year=2022, month=1)
      except Exception as e:
        print(f"{type(self)}\n\n\n")
        raise e
      orig_date = None

      while True:
        account = random.choice(self.accounts)

        if account in ["purchase_return", "sales_return", "account_payment", "account_collection", "accrued_salaries_payment"]:
          if (account in ["account_payment", "purchase_return"]) and ("purchases" in self.generated_accounts):
            orig_account = "purchases"
          elif (account in ["account_collection", "sales_return"]) and ("sales" in self.generated_accounts):
            orig_account = "sales"
          elif (account == "accrued_salaries_payment") and (self.generated_accounts.count("salaries_expense") > self.generated_accounts.count("accrued_salaries_payment")):
            orig_account = "salaries_expense"
          elif (account in ["bad_debt_allowance", "bad_debt_writeoff"]) and (account in self.generated_accounts):
            continue
          else:
            continue

          orig_date = self.generated_dates[self.generated_accounts.index(orig_account)]
          date = self.generateDate(year=orig_date.year, month=orig_date.month, min_day=orig_date.day)
        
        self.generated_accounts.append(account)
        break

      entry = self.entries[account] # TODO: Instead of entries, choose from accounts, then fetch entry.
      transaction = self._convertToTransaction(account, entry, date, orig_date=orig_date)

      self.generated_dates.append(date)
      self.generated_transactions.append(transaction)

    return self.generated_transactions
