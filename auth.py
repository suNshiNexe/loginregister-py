from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    ## Verifica senha corresponde --> hash
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    ## Retorna hash --> texto
    return pwd_context.hash(password)