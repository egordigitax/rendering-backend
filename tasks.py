import asyncio
from celery import Celery
from schemas.render import FilesSchema, RenderSchema, ErrorSchema
from settings import settings
from db import db
from utils.py_object_id import PyObjectId
from utils.blender_api import Api, ModelSetup
import traceback

worker = Celery(__name__, broker=settings.broker_url, backend=settings.result_backend)

async def render_proccess(render_id: str):
  render = await db.renders.find_one({'_id': PyObjectId(render_id)})

  if render is None:
    return

  render = RenderSchema(**render)

  try:
    model = ModelSetup.create_model(**render.traits)

    result = Api.render(model, render.frame_id)

    render.complete = True
    render.files = FilesSchema(
      close=result['images']['close'],
      mid=result['images']['mid'],
      range=result['images']['range'],
      model=result['model']
    )
  except Exception as error:
    render.error = ErrorSchema(
      type=type(error).__name__,
      stack_trace=''.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
    )
    raise error
  finally:
    await db.renders.update_one(
      { '_id': PyObjectId(render_id) },
      { '$set': render.dict(by_alias=True) }
    )


@worker.task(name='render_task')
def render_task(render_id: str):
  loop = asyncio.get_event_loop()
  coroutine = render_proccess(render_id)
  loop.run_until_complete(coroutine)
