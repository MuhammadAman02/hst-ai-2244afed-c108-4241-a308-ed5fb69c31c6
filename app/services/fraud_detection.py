from app.models.transaction import Transaction
from typing import List

def detect_fraud(transaction: Transaction, recent_transactions: List[Transaction]) -> bool:
    # Rule 1: Large transactions (over €10,000)
    if transaction.amount > 10000:
        return True

    # Rule 2: Multiple transactions in a short time
    recent_transactions_count = sum(1 for t in recent_transactions if (transaction.timestamp - t.timestamp).total_seconds() < 300)
    if recent_transactions_count > 5:
        return True

    # Rule 3: Unusual recipient (e.g., first-time transaction to this recipient)
    if transaction.recipient not in [t.recipient for t in recent_transactions]:
        return True

    return False