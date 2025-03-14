import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Boolean, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
Base = declarative_base()

class DatabaseService:
    """
    Service for interacting with the PostgreSQL database.
    Handles saving YNAB data and tracking server knowledge.
    """
    
    def __init__(self, db_url):
        """
        Initialize the database service with the provided connection URL.
        
        Args:
            db_url (str): PostgreSQL connection URL
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        
        # Initialize tables
        self._init_tables()
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        logger.info("Database service initialized")
    
    def _init_tables(self):
        """Initialize SQLAlchemy table definitions"""
        
        # Server Knowledge table to track delta syncs
        self.server_knowledge = Table(
            'server_knowledge',
            self.metadata,
            Column('budget_id', String, primary_key=True),
            Column('entity_type', String, primary_key=True),
            Column('knowledge', Integer, nullable=False),
            Column('updated_at', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
        )
        
        # Budget table
        self.budgets = Table(
            'budgets',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('name', String, nullable=False),
            Column('last_modified_on', DateTime),
            Column('first_month', String),
            Column('last_month', String),
            Column('currency_format_iso_code', String),
            Column('date_format', String),
            Column('currency_format_symbol', String)
        )
        
        # Account table
        self.accounts = Table(
            'accounts',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('budget_id', String, ForeignKey('budgets.id'), nullable=False),
            Column('name', String, nullable=False),
            Column('type', String, nullable=False),
            Column('on_budget', Boolean, nullable=False),
            Column('closed', Boolean, nullable=False),
            Column('note', String),
            Column('balance', Integer, nullable=False),
            Column('cleared_balance', Integer),
            Column('uncleared_balance', Integer),
            Column('transfer_payee_id', String),
            Column('deleted', Boolean, default=False)
        )
        
        # Category Group table
        self.category_groups = Table(
            'category_groups',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('budget_id', String, ForeignKey('budgets.id'), nullable=False),
            Column('name', String, nullable=False),
            Column('hidden', Boolean, default=False),
            Column('deleted', Boolean, default=False)
        )
        
        # Category table
        self.categories = Table(
            'categories',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('category_group_id', String, ForeignKey('category_groups.id'), nullable=False),
            Column('name', String, nullable=False),
            Column('hidden', Boolean, default=False),
            Column('budgeted', Integer),
            Column('activity', Integer),
            Column('balance', Integer),
            Column('goal_type', String),
            Column('goal_target', Integer),
            Column('goal_target_month', String),
            Column('goal_percentage_complete', Integer),
            Column('goal_months_to_budget', Integer),
            Column('goal_under_funded', Integer),
            Column('goal_overall_funded', Integer),
            Column('goal_overall_left', Integer),
            Column('deleted', Boolean, default=False)
        )
        
        # Payee table
        self.payees = Table(
            'payees',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('budget_id', String, ForeignKey('budgets.id'), nullable=False),
            Column('name', String, nullable=False),
            Column('transfer_account_id', String),
            Column('deleted', Boolean, default=False)
        )
        
        # Month table
        self.months = Table(
            'months',
            self.metadata,
            Column('budget_id', String, ForeignKey('budgets.id'), primary_key=True),
            Column('month', String, primary_key=True),
            Column('to_be_budgeted', Integer),
            Column('age_of_money', Integer),
            Column('income', Integer),
            Column('budgeted', Integer),
            Column('activity', Integer)
        )
        
        # Category Month table
        self.category_months = Table(
            'category_months',
            self.metadata,
            Column('budget_id', String, ForeignKey('budgets.id'), primary_key=True),
            Column('month', String, primary_key=True),
            Column('category_id', String, ForeignKey('categories.id'), primary_key=True),
            Column('budgeted', Integer),
            Column('activity', Integer),
            Column('balance', Integer)
        )
        
        # Transaction table
        self.transactions = Table(
            'transactions',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('budget_id', String, ForeignKey('budgets.id'), nullable=False),
            Column('account_id', String, ForeignKey('accounts.id'), nullable=False),
            Column('category_id', String, ForeignKey('categories.id')),
            Column('payee_id', String, ForeignKey('payees.id')),
            Column('date', String, nullable=False),
            Column('amount', Integer, nullable=False),
            Column('memo', String),
            Column('cleared', String, nullable=False),
            Column('approved', Boolean, nullable=False),
            Column('flag_color', String),
            Column('flag_name', String),
            Column('import_id', String),
            Column('deleted', Boolean, default=False)
        )
        
        # Subtransaction table
        self.subtransactions = Table(
            'subtransactions',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('transaction_id', String, ForeignKey('transactions.id'), nullable=False),
            Column('category_id', String, ForeignKey('categories.id')),
            Column('amount', Integer, nullable=False),
            Column('memo', String),
            Column('payee_id', String, ForeignKey('payees.id')),
            Column('deleted', Boolean, default=False)
        )
        
        # Scheduled Transaction table
        self.scheduled_transactions = Table(
            'scheduled_transactions',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('budget_id', String, ForeignKey('budgets.id'), nullable=False),
            Column('account_id', String, ForeignKey('accounts.id'), nullable=False),
            Column('category_id', String, ForeignKey('categories.id')),
            Column('payee_id', String, ForeignKey('payees.id')),
            Column('date', String),
            Column('amount', Integer, nullable=False),
            Column('memo', String),
            Column('frequency', String, nullable=False),
            Column('flag_color', String),
            Column('flag_name', String),
            Column('deleted', Boolean, default=False)
        )
        
        # Scheduled Subtransaction table
        self.scheduled_subtransactions = Table(
            'scheduled_subtransactions',
            self.metadata,
            Column('id', String, primary_key=True),
            Column('scheduled_transaction_id', String, ForeignKey('scheduled_transactions.id'), nullable=False),
            Column('category_id', String, ForeignKey('categories.id')),
            Column('amount', Integer, nullable=False),
            Column('memo', String),
            Column('payee_id', String, ForeignKey('payees.id')),
            Column('deleted', Boolean, default=False)
        )
    
    def get_server_knowledge(self, budget_id):
        """
        Get the server knowledge for all entity types for a budget.
        
        Args:
            budget_id (str): The budget ID
            
        Returns:
            dict: Dictionary of entity types and their server knowledge
        """
        session = self.Session()
        try:
            result = {}
            query = session.query(self.server_knowledge).filter_by(budget_id=budget_id)
            
            for row in query:
                result[row.entity_type] = row.knowledge
            
            return result
        finally:
            session.close()
    
    def _update_server_knowledge(self, budget_id, entity_type, knowledge):
        """
        Update the server knowledge for an entity type.
        
        Args:
            budget_id (str): The budget ID
            entity_type (str): The entity type (e.g., 'accounts', 'transactions')
            knowledge (int): The new server knowledge value
        """
        session = self.Session()
        try:
            # Check if record exists
            existing = session.query(self.server_knowledge).filter_by(
                budget_id=budget_id, 
                entity_type=entity_type
            ).first()
            
            if existing:
                # Update existing record
                session.execute(
                    self.server_knowledge.update().where(
                        (self.server_knowledge.c.budget_id == budget_id) & 
                        (self.server_knowledge.c.entity_type == entity_type)
                    ).values(
                        knowledge=knowledge,
                        updated_at=text('CURRENT_TIMESTAMP')
                    )
                )
            else:
                # Insert new record
                session.execute(
                    self.server_knowledge.insert().values(
                        budget_id=budget_id,
                        entity_type=entity_type,
                        knowledge=knowledge,
                        updated_at=text('CURRENT_TIMESTAMP')
                    )
                )
            
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating server knowledge: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_budgets(self, budgets):
        """
        Save budgets to the database.
        
        Args:
            budgets (list): List of budget objects from YNAB API
        """
        session = self.Session()
        try:
            for budget in budgets:
                # Check if budget exists
                existing = session.query(self.budgets).filter_by(id=budget.id).first()
                
                budget_data = {
                    'id': budget.id,
                    'name': budget.name,
                    'last_modified_on': budget.last_modified_on,
                    'first_month': budget.first_month,
                    'last_month': budget.last_month
                }
                
                # Add currency and date format if available
                if hasattr(budget, 'currency_format') and budget.currency_format:
                    budget_data['currency_format_iso_code'] = budget.currency_format.iso_code
                    budget_data['currency_format_symbol'] = budget.currency_format.symbol
                
                if hasattr(budget, 'date_format') and budget.date_format:
                    budget_data['date_format'] = budget.date_format.format
                
                if existing:
                    # Update existing budget
                    session.execute(
                        self.budgets.update().where(
                            self.budgets.c.id == budget.id
                        ).values(**budget_data)
                    )
                else:
                    # Insert new budget
                    session.execute(
                        self.budgets.insert().values(**budget_data)
                    )
            
            session.commit()
            logger.info(f"Saved {len(budgets)} budgets to database")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving budgets: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_accounts(self, budget_id, accounts_data):
        """
        Save accounts to the database.
        
        Args:
            budget_id (str): The budget ID
            accounts_data (dict): Dictionary containing accounts and server_knowledge
        """
        if 'server_knowledge' in accounts_data:
            self._update_server_knowledge(budget_id, 'accounts', accounts_data['server_knowledge'])
        
        if 'accounts' not in accounts_data:
            return
        
        accounts = accounts_data['accounts']
        session = self.Session()
        try:
            # Mark all accounts as deleted first (will be updated if still exist)
            session.execute(
                self.accounts.update().where(
                    self.accounts.c.budget_id == budget_id
                ).values(deleted=True)
            )
            
            for account in accounts:
                # Check if account exists
                existing = session.query(self.accounts).filter_by(id=account.id).first()
                
                account_data = {
                    'id': account.id,
                    'budget_id': budget_id,
                    'name': account.name,
                    'type': account.type,
                    'on_budget': account.on_budget,
                    'closed': account.closed,
                    'note': account.note,
                    'balance': account.balance,
                    'cleared_balance': account.cleared_balance,
                    'uncleared_balance': account.uncleared_balance,
                    'transfer_payee_id': account.transfer_payee_id,
                    'deleted': False
                }
                
                if existing:
                    # Update existing account
                    session.execute(
                        self.accounts.update().where(
                            self.accounts.c.id == account.id
                        ).values(**account_data)
                    )
                else:
                    # Insert new account
                    session.execute(
                        self.accounts.insert().values(**account_data)
                    )
            
            session.commit()
            logger.info(f"Saved {len(accounts)} accounts to database for budget {budget_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving accounts: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_categories(self, budget_id, categories_data):
        """
        Save categories and category groups to the database.
        
        Args:
            budget_id (str): The budget ID
            categories_data (dict): Dictionary containing category_groups and server_knowledge
        """
        if 'server_knowledge' in categories_data:
            self._update_server_knowledge(budget_id, 'categories', categories_data['server_knowledge'])
        
        if 'category_groups' not in categories_data:
            return
        
        category_groups = categories_data['category_groups']
        session = self.Session()
        try:
            # Mark all category groups and categories as deleted first
            session.execute(
                self.category_groups.update().where(
                    self.category_groups.c.budget_id == budget_id
                ).values(deleted=True)
            )
            
            session.execute(
                self.categories.update().where(
                    self.categories.c.category_group_id.in_(
                        session.query(self.category_groups.c.id).filter_by(budget_id=budget_id)
                    )
                ).values(deleted=True)
            )
            
            for group in category_groups:
                # Save category group
                group_data = {
                    'id': group.id,
                    'budget_id': budget_id,
                    'name': group.name,
                    'hidden': group.hidden,
                    'deleted': False
                }
                
                existing_group = session.query(self.category_groups).filter_by(id=group.id).first()
                
                if existing_group:
                    session.execute(
                        self.category_groups.update().where(
                            self.category_groups.c.id == group.id
                        ).values(**group_data)
                    )
                else:
                    session.execute(
                        self.category_groups.insert().values(**group_data)
                    )
                
                # Save categories in this group
                if hasattr(group, 'categories') and group.categories:
                    for category in group.categories:
                        category_data = {
                            'id': category.id,
                            'category_group_id': group.id,
                            'name': category.name,
                            'hidden': category.hidden,
                            'budgeted': getattr(category, 'budgeted', None),
                            'activity': getattr(category, 'activity', None),
                            'balance': getattr(category, 'balance', None),
                            'goal_type': getattr(category, 'goal_type', None),
                            'goal_target': getattr(category, 'goal_target', None),
                            'goal_target_month': getattr(category, 'goal_target_month', None),
                            'goal_percentage_complete': getattr(category, 'goal_percentage_complete', None),
                            'goal_months_to_budget': getattr(category, 'goal_months_to_budget', None),
                            'goal_under_funded': getattr(category, 'goal_under_funded', None),
                            'goal_overall_funded': getattr(category, 'goal_overall_funded', None),
                            'goal_overall_left': getattr(category, 'goal_overall_left', None),
                            'deleted': False
                        }
                        
                        existing_category = session.query(self.categories).filter_by(id=category.id).first()
                        
                        if existing_category:
                            session.execute(
                                self.categories.update().where(
                                    self.categories.c.id == category.id
                                ).values(**category_data)
                            )
                        else:
                            session.execute(
                                self.categories.insert().values(**category_data)
                            )
            
            session.commit()
            logger.info(f"Saved {len(category_groups)} category groups to database for budget {budget_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving categories: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_payees(self, budget_id, payees_data):
        """
        Save payees to the database.
        
        Args:
            budget_id (str): The budget ID
            payees_data (dict): Dictionary containing payees and server_knowledge
        """
        if 'server_knowledge' in payees_data:
            self._update_server_knowledge(budget_id, 'payees', payees_data['server_knowledge'])
        
        if 'payees' not in payees_data:
            return
        
        payees = payees_data['payees']
        session = self.Session()
        try:
            # Mark all payees as deleted first
            session.execute(
                self.payees.update().where(
                    self.payees.c.budget_id == budget_id
                ).values(deleted=True)
            )
            
            for payee in payees:
                payee_data = {
                    'id': payee.id,
                    'budget_id': budget_id,
                    'name': payee.name,
                    'transfer_account_id': getattr(payee, 'transfer_account_id', None),
                    'deleted': False
                }
                
                existing_payee = session.query(self.payees).filter_by(id=payee.id).first()
                
                if existing_payee:
                    session.execute(
                        self.payees.update().where(
                            self.payees.c.id == payee.id
                        ).values(**payee_data)
                    )
                else:
                    session.execute(
                        self.payees.insert().values(**payee_data)
                    )
            
            session.commit()
            logger.info(f"Saved {len(payees)} payees to database for budget {budget_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving payees: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_transactions(self, budget_id, transactions_data):
        """
        Save transactions to the database.
        
        Args:
            budget_id (str): The budget ID
            transactions_data (dict): Dictionary containing transactions and server_knowledge
        """
        if 'server_knowledge' in transactions_data:
            self._update_server_knowledge(budget_id, 'transactions', transactions_data['server_knowledge'])
        
        if 'transactions' not in transactions_data:
            return
        
        transactions = transactions_data['transactions']
        session = self.Session()
        try:
            # Mark all transactions as deleted first
            session.execute(
                self.transactions.update().where(
                    self.transactions.c.budget_id == budget_id
                ).values(deleted=True)
            )
            
            for transaction in transactions:
                transaction_data = {
                    'id': transaction.id,
                    'budget_id': budget_id,
                    'account_id': transaction.account_id,
                    'category_id': getattr(transaction, 'category_id', None),
                    'payee_id': getattr(transaction, 'payee_id', None),
                    'date': transaction.date,
                    'amount': transaction.amount,
                    'memo': getattr(transaction, 'memo', None),
                    'cleared': transaction.cleared,
                    'approved': transaction.approved,
                    'flag_color': getattr(transaction, 'flag_color', None),
                    'flag_name': getattr(transaction, 'flag_name', None),
                    'import_id': getattr(transaction, 'import_id', None),
                    'deleted': False
                }
                
                existing_transaction = session.query(self.transactions).filter_by(id=transaction.id).first()
                
                if existing_transaction:
                    session.execute(
                        self.transactions.update().where(
                            self.transactions.c.id == transaction.id
                        ).values(**transaction_data)
                    )
                else:
                    session.execute(
                        self.transactions.insert().values(**transaction_data)
                    )
                
                # Save subtransactions if any
                if hasattr(transaction, 'subtransactions') and transaction.subtransactions:
                    # Delete existing subtransactions for this transaction
                    session.execute(
                        self.subtransactions.delete().where(
                            self.subtransactions.c.transaction_id == transaction.id
                        )
                    )
                    
                    for subtransaction in transaction.subtransactions:
                        subtransaction_data = {
                            'id': subtransaction.id,
                            'transaction_id': transaction.id,
                            'category_id': getattr(subtransaction, 'category_id', None),
                            'amount': subtransaction.amount,
                            'memo': getattr(subtransaction, 'memo', None),
                            'payee_id': getattr(subtransaction, 'payee_id', None),
                            'deleted': False
                        }
                        
                        session.execute(
                            self.subtransactions.insert().values(**subtransaction_data)
                        )
            
            session.commit()
            logger.info(f"Saved {len(transactions)} transactions to database for budget {budget_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving transactions: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_scheduled_transactions(self, budget_id, scheduled_transactions_data):
        """
        Save scheduled transactions to the database.
        
        Args:
            budget_id (str): The budget ID
            scheduled_transactions_data (dict): Dictionary containing scheduled_transactions and server_knowledge
        """
        if 'server_knowledge' in scheduled_transactions_data:
            self._update_server_knowledge(budget_id, 'scheduled_transactions', scheduled_transactions_data['server_knowledge'])
        
        if 'scheduled_transactions' not in scheduled_transactions_data:
            return
        
        scheduled_transactions = scheduled_transactions_data['scheduled_transactions']
        session = self.Session()
        try:
            # Mark all scheduled transactions as deleted first
            session.execute(
                self.scheduled_transactions.update().where(
                    self.scheduled_transactions.c.budget_id == budget_id
                ).values(deleted=True)
            )
            
            for transaction in scheduled_transactions:
                transaction_data = {
                    'id': transaction.id,
                    'budget_id': budget_id,
                    'account_id': transaction.account_id,
                    'category_id': getattr(transaction, 'category_id', None),
                    'payee_id': getattr(transaction, 'payee_id', None),
                    'date': getattr(transaction, 'date', None),
                    'amount': transaction.amount,
                    'memo': getattr(transaction, 'memo', None),
                    'frequency': transaction.frequency,
                    'flag_color': getattr(transaction, 'flag_color', None),
                    'flag_name': getattr(transaction, 'flag_name', None),
                    'deleted': False
                }
                
                existing_transaction = session.query(self.scheduled_transactions).filter_by(id=transaction.id).first()
                
                if existing_transaction:
                    session.execute(
                        self.scheduled_transactions.update().where(
                            self.scheduled_transactions.c.id == transaction.id
                        ).values(**transaction_data)
                    )
                else:
                    session.execute(
                        self.scheduled_transactions.insert().values(**transaction_data)
                    )
                
                # Save subtransactions if any
                if hasattr(transaction, 'subtransactions') and transaction.subtransactions:
                    # Delete existing subtransactions for this transaction
                    session.execute(
                        self.scheduled_subtransactions.delete().where(
                            self.scheduled_subtransactions.c.scheduled_transaction_id == transaction.id
                        )
                    )
                    
                    for subtransaction in transaction.subtransactions:
                        subtransaction_data = {
                            'id': subtransaction.id,
                            'scheduled_transaction_id': transaction.id,
                            'category_id': getattr(subtransaction, 'category_id', None),
                            'amount': subtransaction.amount,
                            'memo': getattr(subtransaction, 'memo', None),
                            'payee_id': getattr(subtransaction, 'payee_id', None),
                            'deleted': False
                        }
                        
                        session.execute(
                            self.scheduled_subtransactions.insert().values(**subtransaction_data)
                        )
            
            session.commit()
            logger.info(f"Saved {len(scheduled_transactions)} scheduled transactions to database for budget {budget_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving scheduled transactions: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_months(self, budget_id, months_data):
        """
        Save months and category months to the database.
        
        Args:
            budget_id (str): The budget ID
            months_data (dict): Dictionary containing months and server_knowledge
        """
        if 'server_knowledge' in months_data:
            self._update_server_knowledge(budget_id, 'months', months_data['server_knowledge'])
        
        if 'months' not in months_data:
            return
        
        months = months_data['months']
        session = self.Session()
        try:
            # Delete existing months for this budget
            session.execute(
                self.months.delete().where(
                    self.months.c.budget_id == budget_id
                )
            )
            
            for month in months:
                month_data = {
                    'budget_id': budget_id,
                    'month': month.month,
                    'to_be_budgeted': getattr(month, 'to_be_budgeted', None),
                    'age_of_money': getattr(month, 'age_of_money', None),
                    'income': getattr(month, 'income', None),
                    'budgeted': getattr(month, 'budgeted', None),
                    'activity': getattr(month, 'activity', None)
                }
                
                session.execute(
                    self.months.insert().values(**month_data)
                )
                
                # Save category months if any
                if hasattr(month, 'categories') and month.categories:
                    # Delete existing category months for this month
                    session.execute(
                        self.category_months.delete().where(
                            (self.category_months.c.budget_id == budget_id) &
                            (self.category_months.c.month == month.month)
                        )
                    )
                    
                    for category in month.categories:
                        category_month_data = {
                            'budget_id': budget_id,
                            'month': month.month,
                            'category_id': category.id,
                            'budgeted': getattr(category, 'budgeted', None),
                            'activity': getattr(category, 'activity', None),
                            'balance': getattr(category, 'balance', None)
                        }
                        
                        session.execute(
                            self.category_months.insert().values(**category_month_data)
                        )
            
            session.commit()
            logger.info(f"Saved {len(months)} months to database for budget {budget_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving months: {str(e)}")
            raise
        finally:
            session.close()