from pydantic import BaseModel, constr

class OTPVerify(BaseModel):
    user_id: int
    code: constr(min_length=5, max_length=5)  # Memastikan kode 5 digit 