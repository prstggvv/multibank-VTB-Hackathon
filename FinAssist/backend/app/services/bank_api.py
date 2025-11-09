import httpx
import json
from typing import Dict, Optional, List, Any
from app.config.banks import BankConfig
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.bank import BankConnection

class BankAPIService:
    def __init__(self):
        self.token_cache = {}
        self.consent_cache = {}


    async def get_bank_token(self, bank_name: str) -> Optional[str]:

        if bank_name in self.token_cache:
            print(f"Используем токен из кеша для {bank_name}")
            return self.token_cache[bank_name]
        
        try: 
            bank_config = BankConfig.get_bank_config(bank_name)
            client_id = BankConfig.get_client_id(bank_name)
            client_secret = BankConfig.get_client_secret(bank_name)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    bank_config["auth_url"],
                    params={
                        "client_id": client_id,
                        "client_secret": client_secret
                    }
                )

                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data["access_token"]

                    self.token_cache[bank_name] = access_token
                    print(f"Токен для {bank_name} успешно получен")
                    return access_token
                else:
                    print(f"Ошибка получения токена от {bank_name}: {response.status_code} - {response.text}")
                    return None
                
        except Exception as e:
            print(f"Исключение при получении токена от {bank_name}: {e}")
            return None
        




    async def ensure_consent(self, bank_name: str, user_id: int, db: Session = None) -> Optional[str]:
        close_db = False
        if db is None:
            db = next(get_db())
            close_db = True
        
        try:
            consent_record = db.query(BankConnection).filter(
                BankConnection.external_client_id == f"team039-{user_id}",
                BankConnection.bank_name == bank_name,
                BankConnection.is_active == True
            ).first()
            
            if consent_record:
                return consent_record.consent_id 
            
            consent_response = await self.request_consent(bank_name, user_id)
            
            if not consent_response or "consent_id" not in consent_response:
                print(f"Не удалось получить согласие для {bank_name} пользователя {user_id}")
                return None
            
            new_consent = BankConnection(
                user_id=user_id,
                bank_name=bank_name,
                consent_id=consent_response["consent_id"],
                external_client_id=f"team039-{user_id}",
                is_active=True
            )
            
            db.add(new_consent)
            db.commit()
            db.refresh(new_consent)
            
            return new_consent.consent_id  
            
        except Exception as e:
            print(f"Ошибка в ensure_consent: {e}")
            if db:
                db.rollback()
            return None
        finally:
            if close_db and db:
                db.close()



    async def request_consent(self, bank_name: str, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            access_token = await self.get_bank_token(bank_name)
            if not access_token:
                return None
           
            bank_config = BankConfig.get_bank_config(bank_name)
            consent_data = BankConfig.get_consent_request_data(user_id, bank_name)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=f"{bank_config['base_url']}{bank_config['consents_request_url']}",
                    json=consent_data,
                    headers={"Authorization": f"Bearer {access_token}",
                             "X-Requesting-Bank": "team039"},
                )
                if response.status_code == 200:
                    return response.json()
                return None
                
                
        except Exception as e:
            print(f"Исключение при запросе согласия от {bank_name}: {e}")
            return None
    



    async def get_accounts(self, bank_name: str, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            
            access_token = await self.get_bank_token(bank_name)
            if not access_token:
                print(f"Не удалось получить токен для запроса счетов от {bank_name}")
                return None
            
            consent_id = await self.ensure_consent(bank_name, user_id)
            if not consent_id:
                print(f"Не удалось получить согласие для запроса счетов от {bank_name}")
                return None
            print(consent_id)
            bank_config = BankConfig.get_bank_config(bank_name)

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{bank_config['base_url']}{bank_config['accounts_url']}",
                    headers={"Authorization": f"Bearer {access_token}",
                             "X-Requesting-Bank": "team039",
                             "X-Consent-Id": consent_id,
                             },
                    params={"client_id": f"team039-{user_id}"}
                )

                if response.status_code == 200:
                    account_data = response.json()
                    return account_data
                else:
                    print(f"Ошибка получения счетов от {bank_name}: {response.status_code} - {response.text}")
                    return None
                
        except Exception as e:
            print(f"Исключение при получении счетов от {bank_name}: {e}")
            return None





    # async def get_transactions(self, bank_name: str, account_id: str, user_id:int) -> Optional[Dict[str, Any]]:
    #     try:
    #         access_token = await self.get_bank_token(bank_name)
    #         if not access_token:
    #             print(f"Не удалось получить токен для запроса транзакций от {bank_name}")
    #             return None
            
    #         consent_id = await self.ensure_consent(bank_name, user_id)
    #         print(consent_id)
    #         if not consent_id:
    #             print(f"Не удалось получить согласие для запроса счетов от {bank_name}")
    #             return None
        
            
    #         bank_config = BankConfig.get_bank_config(bank_name)
    #         transactions_url = bank_config["transactions_url"].format(account_id=account_id)
            
    #         print(consent_id)
    #         print( f"{bank_config['base_url']}{transactions_url}")
    #         async with httpx.AsyncClient() as client:
    #             response = await client.get(
    #                 f"{bank_config['base_url']}{transactions_url}",
    #                 headers={"Authorization": f"Bearer {access_token}",
    #                          "X-Requesting-Bank": "team039",
    #                          "X-Consent-Id": consent_id,
    #                          }
    #             )
    #             if response.status_code == 200:
    #                 transactions_data = response.json()
    #                 return transactions_data
    #             print(f"Ошибка получения транзакций от {bank_name}: {response.status_code} - {response.text}")
    #             return None
            
    #     except Exception as e:
    #         print(f"Исключение при получении транзакций от {bank_name}: {e}")
            
    #         return None
        


    async def get_balances(self, bank_name: str, account_id: str, user_id:int) -> Optional[Dict[str, Any]]:
        try:
            access_token = await self.get_bank_token(bank_name)
            if not access_token:
                print(f"Не удалось получить токен для запроса транзакций от {bank_name}")
                return None
            
            consent_id = await self.ensure_consent(bank_name, user_id)
            print(consent_id)
            if not consent_id:
                print(f"Не удалось получить согласие для запроса счетов от {bank_name}")
                return None
        
            
            bank_config = BankConfig.get_bank_config(bank_name)
            balances_url = bank_config["balances_url"].format(account_id=account_id)
            
            print( f"{bank_config['base_url']}{balances_url}")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{bank_config['base_url']}{balances_url}",
                    headers={"Authorization": f"Bearer {access_token}",
                             "X-Requesting-Bank": "team039",
                             "X-Consent-Id": consent_id,
                             }
                )
                if response.status_code == 200:
                    transactions_data = response.json()
                    return transactions_data
                print(f"Ошибка получения транзакций от {bank_name}: {response.status_code} - {response.text}")
                return None
            
        except Exception as e:
            print(f"Исключение при получении транзакций от {bank_name}: {e}")
            
            return None

bank_api_service = BankAPIService()