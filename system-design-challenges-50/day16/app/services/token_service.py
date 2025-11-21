from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..db.models.token import Token
from ..db.models.user import User
from ..schemas.auth import Token as TokenSchema
from ..core.security import create_access_token
from ..core.config import settings
from ..core.exceptions import InvalidTokenException, TokenExpiredException

class TokenService:
    def __init__(self, db: Session):
        self.db = db

    def refresh_access_token(self, refresh_token: str) -> TokenSchema:
        """Refresh access token using refresh token."""
        # In a real implementation, we would validate the refresh token
        # For now, we'll just create a new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": "user"}, expires_delta=access_token_expires
        )
        
        return TokenSchema(
            access_token=new_access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    def revoke_token(self, token: str) -> None:
        """Revoke a token."""
        db_token = self.db.query(Token).filter(Token.token == token).first()
        if db_token:
            db_token.is_revoked = True
            self.db.commit()

    def is_token_valid(self, token: str) -> bool:
        """Check if a token is valid."""
        db_token = self.db.query(Token).filter(Token.token == token).first()
        if not db_token or db_token.is_revoked:
            return False
        
        # Check if token is expired
        if db_token.expires_at < datetime.utcnow():
            return False
            
        return True