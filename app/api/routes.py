from fastapi import APIRouter, Depends, HTTPException
from app.models.transaction import Transaction
from app.services.fraud_detection import detect_fraud
from app.db.database import get_db, Database
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/transactions/", response_model=Transaction)
async def create_transaction(transaction: Transaction, db: Database = Depends(get_db)):
    # Get recent transactions for the sender
    recent_transactions = db.get_recent_transactions(transaction.sender, timedelta(hours=24))
    
    # Perform fraud detection
    is_fraudulent = detect_fraud(transaction, recent_transactions)
    
    # Save the transaction with the fraud detection result
    transaction.is_fraudulent = is_fraudulent
    saved_transaction = db.save_transaction(transaction)
    
    if is_fraudulent:
        # In a real-world scenario, you might want to trigger alerts or additional checks here
        print(f"Potential fraud detected: {saved_transaction}")
    
    return saved_transaction

@router.get("/transactions/", response_model=List[Transaction])
async def get_transactions(db: Database = Depends(get_db)):
    return db.get_all_transactions()

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, db: Database = Depends(get_db)):
    transaction = db.get_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction