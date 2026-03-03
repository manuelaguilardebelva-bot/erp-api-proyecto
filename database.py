import os
import re
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Para usar asyncpg, necesitamos que la URL empiece con postgresql+asyncpg://
# Además, asyncpg no reconoce 'sslmode', por lo que lo limpiamos de la URL
if DATABASE_URL:
    # Cambiar protocolo
    url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    # Eliminar sslmode si existe para evitar conflictos
    ASYNC_DATABASE_URL = re.sub(r'\?sslmode=[^&]+', '', url)
    ASYNC_DATABASE_URL = re.sub(r'&sslmode=[^&]+', '', ASYNC_DATABASE_URL)
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Crear el motor asíncrono
engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

# Fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass

# Dependencia para FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
