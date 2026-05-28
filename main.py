from src.utils import load_transactions_from_json
from src.external_api import convert_to_rubles

def main():
    transactions = load_transactions_from_json('data/operations.json')
    
    if not transactions:
        print("е удалось загрузить транзакции")
        return
    
    print("\n" + "="*60)
    print("СЫ Т")
    print("="*60)
    
    total_rub = 0.0
    
    for i, transaction in enumerate(transactions, 1):
        try:
            amount_in_rub = convert_to_rubles(transaction)
            total_rub += amount_in_rub
            
            operation_amount = transaction.get('operationAmount', {})
            amount = operation_amount.get('amount', 'N/A')
            currency = operation_amount.get('currency', {}).get('code', 'N/A')
            description = transaction.get('description', 'ет описания')
            
            print(f"\n{i}. {description}")
            print(f"   Сумма: {amount} {currency}")
            print(f"    рублях: {amount_in_rub:.2f} RUB")
            
        except Exception as e:
            print(f"\n{i}. шибка: {e}")
    
    print("\n" + "="*60)
    print(f"Т: {total_rub:.2f} RUB")
    print("="*60)

if __name__ == "__main__":
    main()
