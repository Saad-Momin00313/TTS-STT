import sqlite3
from typing import Dict, Any, List
import uuid
from datetime import datetime

class Database:
    def __init__(self, db_path: str):
        """Initialize database connection"""
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create assets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                quantity REAL NOT NULL,
                purchase_price REAL NOT NULL,
                purchase_date TEXT NOT NULL,
                sector TEXT,
                metadata TEXT
            )
        ''')
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                asset_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                date TEXT NOT NULL,
                fees REAL,
                FOREIGN KEY (asset_id) REFERENCES assets (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _generate_id(self, prefix: str = None) -> str:
        """Generate a unique ID for assets or transactions"""
        if prefix:
            return f"{prefix}_{uuid.uuid4()}"
        return str(uuid.uuid4())
    
    def add_asset(self, asset_data: Dict[str, Any]) -> str:
        """Add a new asset to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Generate ID if not provided
            if 'id' not in asset_data:
                asset_data['id'] = self._generate_id(asset_data['symbol'])
            
            cursor.execute('''
                INSERT INTO assets (id, symbol, name, type, quantity, purchase_price, purchase_date, sector, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                asset_data['id'],
                asset_data['symbol'],
                asset_data['name'],
                asset_data['type'],
                asset_data['quantity'],
                asset_data['purchase_price'],
                asset_data.get('purchase_date', datetime.now().strftime('%Y-%m-%d')),
                asset_data.get('sector'),
                str(asset_data.get('metadata', {}))
            ))
            
            conn.commit()
            return asset_data['id']
            
        except sqlite3.IntegrityError as e:
            print(f"Error adding asset: {str(e)}")
            return None
        finally:
            conn.close()
    
    def get_all_assets(self) -> Dict[str, Any]:
        """Get all assets from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM assets')
        assets = {}
        
        for row in cursor.fetchall():
            assets[row[0]] = {
                'id': row[0],
                'symbol': row[1],
                'name': row[2],
                'type': row[3],
                'quantity': row[4],
                'purchase_price': row[5],
                'purchase_date': row[6],
                'sector': row[7],
                'metadata': eval(row[8]) if row[8] else {}
            }
        
        conn.close()
        return assets
    
    def filter_assets(self, **filters) -> Dict[str, Any]:
        """Filter assets based on provided criteria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build WHERE clause dynamically
        where_clauses = []
        params = []
        
        for key, value in filters.items():
            if value is not None:
                where_clauses.append(f"{key} = ?")
                params.append(value)
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1"
        query = f"SELECT * FROM assets WHERE {where_clause}"
        
        cursor.execute(query, params)
        assets = {}
        
        for row in cursor.fetchall():
            assets[row[0]] = {
                'id': row[0],
                'symbol': row[1],
                'name': row[2],
                'type': row[3],
                'quantity': row[4],
                'purchase_price': row[5],
                'purchase_date': row[6],
                'sector': row[7],
                'metadata': eval(row[8]) if row[8] else {}
            }
        
        conn.close()
        return assets
    
    def update_asset(self, asset_id: str, asset_data: Dict[str, Any]) -> bool:
        """Update an existing asset"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE assets
                SET quantity = ?, purchase_price = ?, sector = ?, metadata = ?
                WHERE id = ?
            ''', (
                asset_data['quantity'],
                asset_data['purchase_price'],
                asset_data.get('sector'),
                str(asset_data.get('metadata', {})),
                asset_id
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error updating asset: {str(e)}")
            return False
        finally:
            conn.close()
    
    def remove_asset(self, asset_id: str) -> bool:
        """Remove an asset from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Remove associated transactions first
            cursor.execute('DELETE FROM transactions WHERE asset_id = ?', (asset_id,))
            
            # Remove the asset
            cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error removing asset: {str(e)}")
            return False
        finally:
            conn.close()
    
    def add_transaction(self, transaction_data: Dict[str, Any]) -> str:
        """Add a new transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            transaction_id = self._generate_id()
            
            cursor.execute('''
                INSERT INTO transactions (id, asset_id, transaction_type, quantity, price, date, fees)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction_id,
                transaction_data['asset_id'],
                transaction_data['transaction_type'],
                transaction_data['quantity'],
                transaction_data['price'],
                transaction_data.get('date', datetime.now().strftime('%Y-%m-%d')),
                transaction_data.get('fees', 0.0)
            ))
            
            conn.commit()
            return transaction_id
            
        except Exception as e:
            print(f"Error adding transaction: {str(e)}")
            return None
        finally:
            conn.close()
    
    def get_transactions(self, asset_id: str) -> List[Dict[str, Any]]:
        """Get all transactions for an asset"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM transactions WHERE asset_id = ?', (asset_id,))
        transactions = []
        
        for row in cursor.fetchall():
            transactions.append({
                'id': row[0],
                'asset_id': row[1],
                'transaction_type': row[2],
                'quantity': row[3],
                'price': row[4],
                'date': row[5],
                'fees': row[6]
            })
        
        conn.close()
        return transactions
    
    def clear_all_data(self):
        """Clear all data from the database (use with caution!)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM transactions')
            cursor.execute('DELETE FROM assets')
            conn.commit()
            print("All data cleared from database")
        except Exception as e:
            print(f"Error clearing database: {str(e)}")
        finally:
            conn.close() 