from fastapi import APIRouter

# from .auth import router as auth_router
from .auth_with_cookie import router as auth_with_cookie_router
from .users import router as users_router
from .accounts import router as accounts_router

router = APIRouter(prefix="/v1")
# router.include_router(auth_router)
router.include_router(auth_with_cookie_router)
router.include_router(users_router)
router.include_router(accounts_router)
