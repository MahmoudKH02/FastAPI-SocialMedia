from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, schemas
from ..database import get_db
from ..utils import hashing, oauth2

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credential: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = db.query(models.User) \
        .filter(models.User.email == user_credential.username) \
        .first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    
    if not hashing.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    
    token = oauth2.create_token(data={"user_id": user.id})
    
    return {"access_token": token, "token_type": "bearer"}
