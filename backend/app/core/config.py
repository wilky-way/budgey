import os
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Budgey"
    
    # CORS
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:3000", "http://localhost:8000"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://budgey:budgey@postgres:5432/budgey")
    
    # YNAB
    YNAB_PERSONAL_ACCESS_TOKEN: Optional[str] = os.getenv("YNAB_PERSONAL_ACCESS_TOKEN")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()