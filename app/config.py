from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_user: str
    db_password: str
    db_port: str
    secret_key: str
    mail_password: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    
    class Config:
        env_file = ".env"



settings = Settings()