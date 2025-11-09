from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models.user import User
from app.models.bank import BankConnection
from app.schemas.bank import (
    BankAuthRequest,
    BankAuthResponse,
    BankConnectionResponse,
    BankAccountsRequest,
    AccountsResponse,
    BalancesResponse,
    BankBalancesRequest,
)
from app.auth.utils import verify_token
from app.services.bank_api import bank_api_service


router = APIRouter()


async def get_current_user(
        authorisation: str = Header(...),
        db: Session = Depends(get_db)
) -> User:
    
    if not authorisation.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    
    token = authorisation.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    
    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post(
    "/auth",
    response_model=BankAuthResponse,
    summary="Подключение к банку",
    description="Создает подключение к банку и получает согласие на доступ к данным"
)
async def connect_to_bank(
    auth_request: BankAuthRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        
        consent_response = await bank_api_service.ensure_consent(
            auth_request.bank_name,
            current_user.id
        )
        if not consent_response:
            raise HTTPException(
                status_code=400, 
                detail=f"Не удалось получить согласие от {auth_request.bank_name}"
            )
        
        bank_connection = BankConnection(
             user_id=current_user.id,
             bank_name=auth_request.bank_name,
             consent_id=consent_response,
             external_client_id=f"team039-{current_user.id}"
        ) 

        return BankAuthResponse(
            message=f"Успешно подключено к {auth_request.bank_name}",
            success=True,
            connection_id=bank_connection.consent_id,
            bank_name=auth_request.bank_name
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при подключении к банку: {str(e)}"
        )
    



@router.get(
    "/connections",
    response_model=List[BankConnectionResponse],
    summary="Мои подключения к банкам",
    description="Возвращает список всех подключений пользователя к банкам"
)
def get_my_connections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    connections = db.query(BankConnection).filter(
        BankConnection.user_id == current_user.id
    ).all()
    return connections




@router.post(
    "/accounts",
    response_model=AccountsResponse,
    summary="Получить счета из банка",
    description="Возвращает список счетов пользователя из указанного банка"
)
async def get_bank_accounts(
    accounts_request: BankAccountsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:
        accounts_data = await bank_api_service.get_accounts(
            accounts_request.bank_name,
            current_user.id
        )

        if not accounts_data:
            raise HTTPException(
                status_code=400,
                detail=f"Не удалось получить счета из {accounts_request.bank_name}"
            )
        
        account_list = accounts_data.get("data", {}).get("account", [])
        accounts = []
        for acc in account_list:
            account = {
                "account_id": acc.get("accountId"),
                "currency": acc.get("currency", "RUB"),
                "account_type": acc.get("accountType", "Personal"),
                "nickname": acc.get("nickname"),
                "status": acc.get("status", "Unknown"),
                "balance": None  
            }
            accounts.append(account)
        
        return AccountsResponse(
            bank_name=accounts_request.bank_name,
            accounts=accounts,
            total_accounts=len(accounts)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении счетов: {str(e)}"
        )



# @router.post(
#     "/transactions",
#     response_model=TransactionsResponse,
#     summary="Получить транзакции из банка",
#     description="Возвращает транзакции по счетам пользователя из указанного банка"
# )
# async def get_bank_transactions(
#     transactions_request: BankTransactionsRequest,
#     current_user: User = Depends(get_current_user)
# ):
#     try:
#         transaсtions_data = await bank_api_service.get_transactions(
#             bank_name=transactions_request.bank_name,
#             user_id=current_user.id, 
#             account_id=transactions_request.account_id
#         )
#         if not transaсtions_data:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Не удалось получить транзакции из {transactions_request.bank_name}"
#             )
#         return BankApiResponse(
#             data=transaсtions_data,
#             success=True,
#             bank_name=transactions_request.bank_name
#         )
    
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Ошибка при получении транзакций: {str(e)}"
#         )

@router.post(
    "/balances",
    response_model=BalancesResponse,
    summary="Получить баланс счета",
    description="Возвращает баланс по счетам пользователя из указанного банка"
)
async def get_bank_balances(
    balances_request: BankBalancesRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        balances_data = await bank_api_service.get_balances(
            bank_name=balances_request.bank_name,
            user_id=current_user.id, 
            account_id=balances_request.account_id
        )

        if not balances_data:
            raise HTTPException(
                status_code=400,
                detail=f"Не удалось получить транзакции из {balances_data.bank_name}"
            )
        return BalancesResponse(
            data=balances_data
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении транзакций: {str(e)}"
        )



