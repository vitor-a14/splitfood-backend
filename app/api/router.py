from fastapi import APIRouter

from .user.views import router as user_router
from .group.views import router as group_router
from .item.views import router as item_router

router = APIRouter()


router.include_router(user_router, prefix='/user', tags=['user'])
router.include_router(group_router, prefix='/group', tags=['group'])
router.include_router(item_router, prefix='/item', tags=['item'])
