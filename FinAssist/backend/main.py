from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers import auth, bank

from app.database.database import engine, Base
from app.models import user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinAssist",
    description="""
    FinAssist - Универсальное приложение, которое объединяет данные со всех банковских счетов пользователя в одном месте. 
    Просто подключаете свои банки через API и мгновенно видите общий баланс, последние транзакции и состояние счетов из разных 
    банков на единой панели управления. Контроль финансов без необходимости переключаться между приложениями.

    Возможности:
    
    Аутентификация - регистрация и вход пользователей
    Работа с банками - подключение к банкам, получение счетов и транзакций
    Управление данными - хранение и анализ финансовой информации
    """,
    version="1.0.0",
    contact={
        "name": "СODE SHARKS🦈",
        "email": "team@example.com",
    },
    docs_url="/docs",  
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Аутентификация"]
)

app.include_router(
    bank.router,
    prefix="/banks",  
    tags=["Банки"],   
)







if __name__ == "__main__":
   
    uvicorn.run(
        "main:app",  
        host="0.0.0.0",  
        port=8000,  
        reload=True 
    )
