from src.utils import load_transactions_from_json
from src.external_api import convert_to_rubles
from src.logger_config import setup_logger

# астраиваем логгер для main
logger = setup_logger('main')

def main():
    logger.info("="*50)
    logger.info("С Ы")
    logger.info("="*50)
    
    logger.info("агрузка транзакций из data/operations.json")
    transactions = load_transactions_from_json('data/operations.json')
    
    if not transactions:
        logger.error("е удалось загрузить транзакции, программа завершена")
        print("е удалось загрузить транзакции")
        return
    
    logger.info(f"спешно загружено {len(transactions)} транзакций")
    print("\n" + "="*60)
    print("СЫ Т")
    print("="*60)
    
    total_rub = 0.0
    
    for i, transaction in enumerate(transactions, 1):
        try:
            logger.debug(f"бработка транзакции {i}: {transaction.get('description', 'Unknown')}")
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
            logger.error(f"шибка при обработке транзакции {i}: {e}")
            print(f"\n{i}. шибка: {e}")
    
    logger.info(f"тоговая сумма всех транзакций: {total_rub:.2f} RUB")
    print("\n" + "="*60)
    print(f"Т: {total_rub:.2f} RUB")
    print("="*60)
    
    logger.info("="*50)
    logger.info(" Ш")
    logger.info("="*50)

if __name__ == "__main__":
    main()
