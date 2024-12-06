from typing_extensions import Literal, TypedDict
import asyncio
from pydantic import BaseModel
from haskellian import iter as I
from fastapi import FastAPI
import numpy as np
import pure_cv as vc
from pipeteer import multitask
from moveread.pipelines.preprocess import PreprocessContext
from moveread.pipelines.preprocess.pipelines import (
  validate, correct, select, Validate, Correct, Select
)

class ValidationItem(Validate.Input):
  id: str
  tag: Literal['validate']

class CorrectItem(TypedDict):
  id: str
  img: str
  tag: Literal['correct']

class SelectItem(Select.Input):
  id: str
  img: str
  tag: Literal['select']

  
Item = ValidationItem | CorrectItem | SelectItem

@multitask(validate, correct, select)
def api(val: Validate, corr: Correct, sel: Select, ctx: PreprocessContext):
  app = FastAPI(generate_unique_id_function=lambda route: route.name)

  def val_item(item: tuple[str, Validate.Input]) -> ValidationItem:
    k, v = item; url = ctx.blobs.url(v['contoured'])
    return { 'id': k, 'contoured': url, 'tag': 'validate' }
  
  def sel_item(item: tuple[str, Select.Input]) -> SelectItem:
    k, v = item; url = ctx.blobs.url(v['img'])
    return { 'id': k, 'img': url, 'model': v['model'], 'tag': 'select' }
  
  def corr_item(item: tuple[str, Correct.Input]) -> CorrectItem:
    k, v = item; url = ctx.blobs.url(v['descaled_img'])
    return { 'id': k, 'img': url, 'tag': 'correct' }

  @app.get('/items')
  async def get_items() -> list[Item]:
    tasks = (
      val.items().map(val_item).sync(),
      corr.items().map(corr_item).sync(),
      sel.items().map(sel_item).sync(),
    )
    items = I.flatten(await asyncio.gather(*tasks)).sync()
    return items
  
  class Corners(BaseModel):
    tl: tuple[float, float]
    tr: tuple[float, float]
    br: tuple[float, float]
    bl: tuple[float, float]

  class CorrectParams(BaseModel):
    corners: Corners

  @app.post('/correct')
  async def correct(id: str, params: CorrectParams):
    cs = params.corners
    await corr.correct(id, np.array([cs.tl, cs.tr, cs.br, cs.bl]))
    return True
  
  class RotateParams(BaseModel):
    rotation: vc.Rotation
  
  @app.post('/rotate')
  async def rotate(id: str, params: RotateParams):
    await corr.rotate(id, params.rotation)
    return True

  class SelectParams(BaseModel):
    gridCoords: vc.Rect
  
  @app.post('/select')
  async def select(id: str, params: SelectParams):
    await sel.select(id, params.gridCoords)
    return True
  
  @app.post('/recorrect')
  async def recorrect(id: str):
    await sel.recorrect(id)
    return True
  
  @app.post('/annotate')
  async def annotate(id: str, annotation: Literal['correct', 'incorrect']):
    await val.annotate(id, annotation == 'correct')
    return True
  
  return app