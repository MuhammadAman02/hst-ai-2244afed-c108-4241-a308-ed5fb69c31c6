from nicegui import ui
from app.models.transaction import Transaction
from app.services.fraud_detection import detect_fraud
from app.db.database import get_db
from datetime import datetime, timedelta
import httpx

async def submit_transaction(sender: str, recipient: str, amount: float):
    transaction = Transaction(
        amount=amount,
        sender=sender,
        recipient=recipient,
        timestamp=datetime.now()
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/transactions/", json=transaction.dict())
    
    if response.status_code == 200:
        result = response.json()
        if result['is_fraudulent']:
            ui.notify('Potential fraud detected!', color='negative')
        else:
            ui.notify('Transaction processed successfully', color='positive')
    else:
        ui.notify('Error processing transaction', color='negative')

async def get_transactions():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/transactions/")
    
    if response.status_code == 200:
        return response.json()
    else:
        ui.notify('Error fetching transactions', color='negative')
        return []

@ui.page('/')
async def main():
    ui.label('Irish Fraud Detection System').classes('text-h3 text-weight-bold')

    with ui.card():
        ui.label('Submit New Transaction').classes('text-h5')
        sender = ui.input('Sender')
        recipient = ui.input('Recipient')
        amount = ui.number('Amount', format='%.2f')
        ui.button('Submit', on_click=lambda: submit_transaction(sender.value, recipient.value, amount.value))

    with ui.card():
        ui.label('Recent Transactions').classes('text-h5')
        table = ui.table(columns=[
            {'name': 'id', 'label': 'ID', 'field': 'id', 'required': True, 'align': 'left'},
            {'name': 'amount', 'label': 'Amount', 'field': 'amount', 'sortable': True},
            {'name': 'sender', 'label': 'Sender', 'field': 'sender', 'sortable': True},
            {'name': 'recipient', 'label': 'Recipient', 'field': 'recipient', 'sortable': True},
            {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'sortable': True},
            {'name': 'is_fraudulent', 'label': 'Fraudulent?', 'field': 'is_fraudulent', 'sortable': True},
        ], rows=[])

        async def refresh_transactions():
            transactions = await get_transactions()
            table.rows = transactions
            ui.notify('Transactions refreshed', color='info')

        ui.button('Refresh', on_click=refresh_transactions)

    await refresh_transactions()

ui.run(port=8080)