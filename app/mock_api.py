class MockAPI:
    @staticmethod
    def confirm_transaction(transaction_id):
        print(f"Confirming transaction with ID {transaction_id} via mock API.")
