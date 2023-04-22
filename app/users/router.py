from .schemas import UsersInCreate, UsersInLogIn, UsersInUpdate, ValidateRekening
from .utils import register, login, get_detail_user, edit_user, validate_rekening, delete_user
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from .service import verify_token
from db.connection import get_async_session
from fastapi import Response
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/auth/register", summary="Registrasi User Baru" )
async def add_user(user: UsersInCreate, response: Response, db: AsyncSession = Depends(get_async_session)):
    result  = await register(user, db)
    response.status_code = result[1]
    logger.info(result, {'username': user.username})
    return result[0]

@router.post("/auth/login",summary="Login User" )
async def login_user(user: UsersInLogIn, response: Response, db: AsyncSession = Depends(get_async_session)):
    result = await login(user, db)
    response.status_code = result[1]
    logger.info(result, {'username': user.username})
    return result[0]

@router.get("/account", summary="Get Detail By User ID")
async def get_detail_by(response: Response, db: AsyncSession = Depends(get_async_session), _token : dict = Depends(verify_token)):
    result = await get_detail_user(db, _token)
    response.status_code = result[1]
    logger.info(result, {'user_id': _token['user_id']})
    return result[0]

@router.put("/account/{user_id}", summary= "update data profile")
async def update_user(response: Response, user_id : int, user: UsersInUpdate, db: AsyncSession = Depends(get_async_session), _token : dict = Depends(verify_token)):
    result = await edit_user(user_id, user, db)
    response.status_code = result[1]
    logger.info(result, {'user_id': user_id})
    return result[0]

@router.put("/validasi_akun", summary= "validasi akun berdasarkan no rekening")
async def update_user(response: Response, user: ValidateRekening, db: AsyncSession = Depends(get_async_session), _token : dict = Depends(verify_token)):
    result = await validate_rekening(user, db, _token)
    response.status_code = result[1]
    logger.info(result, {'user_id': _token['user_id']})
    return result[0]

@router.delete("/account/{user_id}", summary="Delete User By Id")
async def delete(response: Response, user_id: int, db: AsyncSession = Depends(get_async_session), _token : dict = Depends(verify_token)):
    result = await delete_user(user_id, db)
    response.status_code = result[1]
    logger.info(result, {'user_id': user_id})
    return result[0]