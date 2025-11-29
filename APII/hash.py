from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

contraseña = "123"
hash_generado = pwd_context.hash(contraseña)
print("Hash para la contraseña '123':")
print(hash_generado)