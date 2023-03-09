from fastapi import APIRouter
from . import render

router = APIRouter(prefix='/v1')
router.include_router(render.router)