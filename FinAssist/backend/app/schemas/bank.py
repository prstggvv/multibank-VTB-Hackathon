from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class BankName(str, Enum):
    VBANK = "vbank"
    ABANK = "abank"
    SBANK = "sbank"

class BankAuthRequest(BaseModel):
    bank_name: BankName = Field(..., description="Название банка для подключения")

class BankAuthResponse(BaseModel):
    message: str = Field(..., description="Сообщение о результате")
    success: bool = Field(..., description="Успешно ли подключение")
    connection_id: Optional[str] = Field(None, description="ID созданного подключения")
    bank_name: str = Field(..., description="Название банка")

class BankConnectionResponse(BaseModel):
    id: int
    bank_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BankApiResponse(BaseModel):
    data: Optional[Dict[str, Any]] = Field(None, description="Данные от API банка")
    success: bool = Field(..., description="Успешен ли запрос")
    bank_name: str = Field(..., description="Название банка")
    
    class Config:
        from_attributes = True
class BankAccountsRequest(BaseModel):
    bank_name: BankName = Field(..., description="Банк из которого запрашиваем счета")

class BankTransactionsRequest(BaseModel):
    bank_name: BankName = Field(..., description="Банк из которого запрашиваем транзакции")
    account_id: Optional[str] = Field(None, description="Конкретный счет (если не указан - все счета)")

class BankBalancesRequest(BaseModel):
    bank_name: BankName = Field(..., description="Банк из которого запрашиваем транзакции")
    account_id: Optional[str] = Field(None, description="Конкретный счет (если не указан - все счета)")



class Account(BaseModel):
    account_id: str = Field(..., description="ID счета")
    currency: str = Field(..., description="Валюта счета")
    account_type: str = Field(..., description="Тип счета")
    nickname: Optional[str] = Field(None, description="Название счета")
    status: str = Field(..., description="Статус счета")
    balance: Optional[float] = Field(None, description="Баланс счета")

class AccountsResponse(BaseModel):
    bank_name: str = Field(..., description="Название банка")
    accounts: List[Account] = Field(..., description="Список счетов")
    total_accounts: int = Field(..., description="Общее количество счетов")

class BalancesResponse(BaseModel):
    data: Dict
