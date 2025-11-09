from typing import Dict, List
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class BankConfig:

    BANKS: Dict[str, Dict[str, str]] = {
        "vbank": {
            "name": "VBank",
            "base_url": "https://vbank.open.bankingapi.ru",
            "auth_url": "https://vbank.open.bankingapi.ru/auth/bank-token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions",
            "balances_url": "/accounts/{account_id}/balances",
            "consents_request_url": "/account-consents/request"
        },
        "abank": {
            "name": "ABank", 
            "base_url": "https://abank.open.bankingapi.ru",
            "auth_url": "https://abank.open.bankingapi.ru/auth/bank-token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions",
            "balances_url": "/accounts/{account_id}/balances",
            "consents_request_url": "/account-consents/request"
        },
        "sbank": {
            "name": "SBank",
            "base_url": "https://sbank.open.bankingapi.ru", 
            "auth_url": "https://sbank.open.bankingapi.ru/auth/bank-token",
            "jwks_url": "https://sbank.open.bankingapi.ru/.well-known/jwks.json",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions",
            "balances_url": "/accounts/{account_id}/balances",
            "consents_request_url": "/account-consents/request"
        }
    }

    CLIENT_IDS: Dict[str, str] = {
        "vbank": "team039",
        "abank": "team039", 
        "sbank": "team039"
    }
    
    CLIENT_SECRETS: Dict[str, str] = {
        "vbank": CLIENT_SECRET,
        "abank": CLIENT_SECRET,
        "sbank": CLIENT_SECRET
    }

    DEFAULT_PERMISSIONS: List[str] = [
        "ReadAccountsDetail",    
        "ReadBalances",          
        "ReadTransactions"      
    ]

    REQUESTING_BANK: str = "team039"
    REQUESTING_BANK_NAME: str = "Team 039 App"
    CONSENT_REASON: str = "Агрегация счетов"

    @classmethod
    def generate_user_client_id(cls, user_id: int) -> str:
        return f"team039-{user_id}"
    
    @classmethod
    def get_consent_request_data(cls, user_id: int, bank_name: str) -> Dict:
        bank_config = cls.get_bank_config(bank_name)
        return {
            "client_id": cls.generate_user_client_id(user_id),
            "permissions": [
                "ReadAccountsDetail",    
                "ReadBalances",          
                "ReadTransactions"      
            ],
            "reason": cls.CONSENT_REASON,
            "requesting_bank": bank_name,
            "requesting_bank_name": bank_config["name"]
        }
        
    
    # @classmethod
    # def get_bank_headers_accounts(cls, access_token: str, consent_id: str = None, user_id: int = None) -> Dict[str, str]:
    #     headers = {
    #         "Authorization": f"Bearer {access_token}",
    #         "X-Requesting-Bank": cls.REQUESTING_BANK,
    #         "X-Consent-Id": consent_id
    #     }

    #     if consent_id:
    #         headers["X-Consent-Id"] = consent_id

    #     if user_id:
    #         headers["X-Client-Id"] = cls.generate_user_client_id(user_id)

    #     return headers
    
    # @classmethod
    # def get_bank_headers_consent(cls) -> Dict[str, str]:
    #     headers = {
    #         "X-Requesting-Bank": cls.REQUESTING_BANK,
    #     }
    #     return headers
    
    @classmethod
    def get_bank_config(cls, bank_name: str) -> Dict[str, str]:
        bank_name = bank_name.lower()
        if bank_name not in cls.BANKS:
            raise ValueError(f"Банк {bank_name} не поддерживается. Доступные: {list(cls.BANKS.keys())}")
        return cls.BANKS[bank_name]
    
    @classmethod
    def get_client_id(cls, bank_name: str) -> str:
        return cls.CLIENT_IDS.get(bank_name, "")
    
    @classmethod
    def get_client_secret(cls, bank_name: str) -> str:
        return cls.CLIENT_SECRETS.get(bank_name, "")
    
    @classmethod
    def get_supported_banks(cls) -> list:

        return list(cls.BANKS.keys())
    
    @classmethod
    def get_consent_request_url(cls, bank_name: str) -> str:
        config = cls.get_bank_config(bank_name)
        return config.get("consents_request_url", "/account-consents/request")
    
   
