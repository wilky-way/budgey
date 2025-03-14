import logging
import ynab
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ynab.rest import ApiException

logger = logging.getLogger(__name__)

class YNABService:
    """
    Service for interacting with the YNAB API.
    Handles rate limiting and provides methods to fetch all required data.
    """
    
    def __init__(self, access_token):
        """
        Initialize the YNAB service with the provided access token.
        
        Args:
            access_token (str): YNAB API personal access token
        """
        self.configuration = ynab.Configuration(
            access_token=access_token
        )
        self.api_client = ynab.ApiClient(self.configuration)
        
        # Initialize API instances
        self.budgets_api = ynab.BudgetsApi(self.api_client)
        self.accounts_api = ynab.AccountsApi(self.api_client)
        self.categories_api = ynab.CategoriesApi(self.api_client)
        self.payees_api = ynab.PayeesApi(self.api_client)
        self.transactions_api = ynab.TransactionsApi(self.api_client)
        self.scheduled_transactions_api = ynab.ScheduledTransactionsApi(self.api_client)
        self.months_api = ynab.MonthsApi(self.api_client)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_budgets(self):
        """
        Get all budgets from YNAB.
        
        Returns:
            list: List of budget objects
        """
        try:
            logger.info("Fetching budgets from YNAB")
            response = self.budgets_api.get_budgets()
            return response.data.budgets
        except ApiException as e:
            logger.error(f"Error fetching budgets: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_accounts(self, budget_id, last_knowledge_of_server=None):
        """
        Get all accounts for a budget.
        
        Args:
            budget_id (str): The budget ID
            last_knowledge_of_server (int, optional): The starting server knowledge
            
        Returns:
            dict: Dictionary containing accounts and server_knowledge
        """
        try:
            logger.info(f"Fetching accounts for budget {budget_id}")
            params = {}
            if last_knowledge_of_server:
                params['last_knowledge_of_server'] = last_knowledge_of_server
                
            response = self.accounts_api.get_accounts(budget_id, **params)
            return {
                'accounts': response.data.accounts,
                'server_knowledge': response.data.server_knowledge
            }
        except ApiException as e:
            logger.error(f"Error fetching accounts: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_categories(self, budget_id, last_knowledge_of_server=None):
        """
        Get all categories for a budget.
        
        Args:
            budget_id (str): The budget ID
            last_knowledge_of_server (int, optional): The starting server knowledge
            
        Returns:
            dict: Dictionary containing category groups and server_knowledge
        """
        try:
            logger.info(f"Fetching categories for budget {budget_id}")
            params = {}
            if last_knowledge_of_server:
                params['last_knowledge_of_server'] = last_knowledge_of_server
                
            response = self.categories_api.get_categories(budget_id, **params)
            return {
                'category_groups': response.data.category_groups,
                'server_knowledge': response.data.server_knowledge
            }
        except ApiException as e:
            logger.error(f"Error fetching categories: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_payees(self, budget_id, last_knowledge_of_server=None):
        """
        Get all payees for a budget.
        
        Args:
            budget_id (str): The budget ID
            last_knowledge_of_server (int, optional): The starting server knowledge
            
        Returns:
            dict: Dictionary containing payees and server_knowledge
        """
        try:
            logger.info(f"Fetching payees for budget {budget_id}")
            params = {}
            if last_knowledge_of_server:
                params['last_knowledge_of_server'] = last_knowledge_of_server
                
            response = self.payees_api.get_payees(budget_id, **params)
            return {
                'payees': response.data.payees,
                'server_knowledge': response.data.server_knowledge
            }
        except ApiException as e:
            logger.error(f"Error fetching payees: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_transactions(self, budget_id, last_knowledge_of_server=None):
        """
        Get all transactions for a budget.
        
        Args:
            budget_id (str): The budget ID
            last_knowledge_of_server (int, optional): The starting server knowledge
            
        Returns:
            dict: Dictionary containing transactions and server_knowledge
        """
        try:
            logger.info(f"Fetching transactions for budget {budget_id}")
            params = {}
            if last_knowledge_of_server:
                params['last_knowledge_of_server'] = last_knowledge_of_server
                
            response = self.transactions_api.get_transactions(budget_id, **params)
            return {
                'transactions': response.data.transactions,
                'server_knowledge': response.data.server_knowledge
            }
        except ApiException as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_scheduled_transactions(self, budget_id, last_knowledge_of_server=None):
        """
        Get all scheduled transactions for a budget.
        
        Args:
            budget_id (str): The budget ID
            last_knowledge_of_server (int, optional): The starting server knowledge
            
        Returns:
            dict: Dictionary containing scheduled transactions and server_knowledge
        """
        try:
            logger.info(f"Fetching scheduled transactions for budget {budget_id}")
            params = {}
            if last_knowledge_of_server:
                params['last_knowledge_of_server'] = last_knowledge_of_server
                
            response = self.scheduled_transactions_api.get_scheduled_transactions(budget_id, **params)
            return {
                'scheduled_transactions': response.data.scheduled_transactions,
                'server_knowledge': response.data.server_knowledge
            }
        except ApiException as e:
            logger.error(f"Error fetching scheduled transactions: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ApiException)
    )
    def get_months(self, budget_id, last_knowledge_of_server=None):
        """
        Get all months for a budget.
        
        Args:
            budget_id (str): The budget ID
            last_knowledge_of_server (int, optional): The starting server knowledge
            
        Returns:
            dict: Dictionary containing months and server_knowledge
        """
        try:
            logger.info(f"Fetching months for budget {budget_id}")
            params = {}
            if last_knowledge_of_server:
                params['last_knowledge_of_server'] = last_knowledge_of_server
                
            response = self.months_api.get_budget_months(budget_id, **params)
            return {
                'months': response.data.months,
                'server_knowledge': response.data.server_knowledge
            }
        except ApiException as e:
            logger.error(f"Error fetching months: {str(e)}")
            raise