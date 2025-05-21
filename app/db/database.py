from app.models.transaction import Transaction
from typing import List, Optional
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.transactions = []
        self.transaction_id_counter = 1

    def save_transaction(self, transaction: Transaction) -> Transaction:
        transaction.id = self.transaction_id_counter
        self.transaction_id_counter += 1
        self.transactions.append(transaction)
        return transaction

    def get_all_transactions(self) -> List[Transaction]:
        return self.transactions

    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def get_recent_transactions(self, sender: str, time_period: timedelta) -> List[Transaction]:
        current_time = datetime.now()
        return [
            t for t in self.transactions
            if t.sender == sender and (current_time - t.timestamp) <= time_period
        ]

db = Database()

def get_db():
    return db