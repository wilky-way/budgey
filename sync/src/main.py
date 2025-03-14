import os
import time
import logging
import schedule
from dotenv import load_dotenv

from src.services.ynab_service import YNABService
from src.services.db_service import DatabaseService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def sync_ynab_data():
    """
    Main function to sync YNAB data to the database.
    Uses delta sync when possible to minimize API calls.
    """
    try:
        logger.info("Starting YNAB data sync")
        
        # Initialize services
        ynab_service = YNABService(
            access_token=os.getenv("YNAB_PERSONAL_ACCESS_TOKEN")
        )
        db_service = DatabaseService(
            db_url=os.getenv("DATABASE_URL")
        )
        
        # Get budgets
        budgets = ynab_service.get_budgets()
        db_service.save_budgets(budgets)
        
        # For each budget, sync all data
        for budget in budgets:
            budget_id = budget.id
            logger.info(f"Syncing data for budget: {budget.name} ({budget_id})")
            
            # Get server knowledge from database
            server_knowledge = db_service.get_server_knowledge(budget_id)
            
            # Sync accounts
            accounts = ynab_service.get_accounts(budget_id, server_knowledge.get('accounts'))
            db_service.save_accounts(budget_id, accounts)
            
            # Sync categories
            categories = ynab_service.get_categories(budget_id, server_knowledge.get('categories'))
            db_service.save_categories(budget_id, categories)
            
            # Sync payees
            payees = ynab_service.get_payees(budget_id, server_knowledge.get('payees'))
            db_service.save_payees(budget_id, payees)
            
            # Sync transactions (most frequently updated)
            transactions = ynab_service.get_transactions(budget_id, server_knowledge.get('transactions'))
            db_service.save_transactions(budget_id, transactions)
            
            # Sync scheduled transactions
            scheduled_transactions = ynab_service.get_scheduled_transactions(budget_id, server_knowledge.get('scheduled_transactions'))
            db_service.save_scheduled_transactions(budget_id, scheduled_transactions)
            
            # Sync months
            months = ynab_service.get_months(budget_id, server_knowledge.get('months'))
            db_service.save_months(budget_id, months)
            
            logger.info(f"Completed sync for budget: {budget.name}")
        
        logger.info("YNAB data sync completed successfully")
    
    except Exception as e:
        logger.error(f"Error during YNAB data sync: {str(e)}")
        raise

def main():
    """
    Main entry point for the sync service.
    Performs initial sync and then schedules hourly updates.
    """
    logger.info("Starting YNAB sync service")
    
    # Perform initial sync
    sync_ynab_data()
    
    # Schedule hourly sync
    schedule.every(1).hour.do(sync_ynab_data)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()