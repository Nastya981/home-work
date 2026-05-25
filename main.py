from utils import load_transactions_from_json
from external_api import convert_to_rubles

def main():
    transactions = load_transactions_from_json('data/operations.json')
    
    if not transactions:
        print("е удалось загрузить транзакции")
        return
    
    print("\n" + "="*50)
    print("СЫ Т")
    print("="*50)
    
    total = 0
    for t in transactions:
        rub = convert_to_rubles(t)
        total += rub
        print(f"{t.get('description', 'ет описания')}: {t['amount']} {t['currency']} = {rub:.2f} RUB")
    
    print("="*50)
    print(f"Т: {total:.2f} RUB")
    print("="*50)

if __name__ == "__main__":
    main()
