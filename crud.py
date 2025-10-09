from sqlalchemy.orm import Session

import models
import schemas
import auth

def get_user_by_email(db: Session, email: str):
    """Busca usuário pelo email"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Cria um novo usuário"""
    hashed_pwd = auth.get_password_hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_pwd=hashed_pwd
    )
    # Adiciona o usuário na sessão
    db.add(db_user) 
    # Salva as mudanças no banco
    db.commit()
    db.refresh(db_user)

    return db_user