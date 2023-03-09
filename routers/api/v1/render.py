from fastapi import APIRouter, status, HTTPException, Body
from schemas.render import RenderSchema
from fastapi.responses import FileResponse
from tasks import render_task
from utils.py_object_id import PyObjectId
from db import db
from enum import Enum

router = APIRouter(prefix='/render', tags=['Render'])

@router.post('/', response_description='Request for render new model', response_model=RenderSchema, status_code=status.HTTP_201_CREATED)
async def create(render_request: RenderSchema = Body(example={
  'token_id': '1',
  'eyes': 'Coffee',
  'accessory_face': 'Logo',
  'hair': 'Long White',
  'boobs': 'S',
  'nipples': 'Ordinary',
  'accessory_boobs': 'Choker',
  'butts': 'Peach',
  'surprise': 'Gucci',
  'legs': 'Grid',
  'accessory_butts': 'Butterfly',
  'accessory_legs': 'Chains',
  'background': 'Purple Bitch',
  'skin': 'Acid',
  'hand': 'Base',
})):
  frame_id = await db.renders.count_documents({})
  render_request.frame_id = frame_id + 1
  new_render = await db.renders.insert_one(render_request.dict(by_alias=True))
  render_task.delay(str(new_render.inserted_id))
  render = await db.renders.find_one({'_id': PyObjectId(new_render.inserted_id)})
  return RenderSchema(**render)

class Derivative(str, Enum):
  close = 'close'
  mid = 'mid'
  range = 'range'
  model = 'model'

@router.get('/{id}', response_model=RenderSchema)
async def show(id: str):
  if (render := await db.renders.find_one({'_id': PyObjectId(id)})) is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Render {id} not found")
  return RenderSchema(**render)

@router.get('/{id}/{derivative}', response_description='Show specific render')
async def derivative(id: str, derivative: Derivative):
  if (render := await db.renders.find_one({'_id': PyObjectId(id)})) is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Render {id} not found")

  render = RenderSchema(**render)

  if render.files is not None:
    if derivative is Derivative.model:
      filename = f"{render.frame_id}_{derivative}.gltf"
      content_disposition_type = 'attachment'
    else:
      filename = f"{render.frame_id}_{derivative}.png"
      content_disposition_type = 'inline'
    
    return FileResponse(render.files.dict()[derivative], content_disposition_type=content_disposition_type, filename=filename)

  return 