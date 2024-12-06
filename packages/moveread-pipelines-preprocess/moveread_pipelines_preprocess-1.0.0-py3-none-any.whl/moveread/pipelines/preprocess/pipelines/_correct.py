from typing_extensions import TypedDict, Literal
from dataclasses import dataclass, field
from uuid import uuid4
from haskellian import AsyncIter
import pure_cv as vc
from kv import KV
from dslog import Logger
from pipeteer import task, ReadQueue, WriteQueue, Transaction
from moveread.pipelines.preprocess import PreprocessContext

class Input(TypedDict):
  img: str
  descaled_img: str

@dataclass
class Corrected:
  img: str
  corners: vc.Corners
  tag: Literal['corrected'] = 'corrected'

@dataclass
class Rotated:
  rotation: vc.Rotation
  img: str
  tag: Literal['rotated'] = 'rotated'

Output = Corrected | Rotated

@dataclass
class Correct:
  Input = Input
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  blobs: KV[bytes]
  log: Logger

  def items(self):
    return AsyncIter(self.Qin.items())

  async def correct(self, key: str, corners: vc.Corners):
    inp = await self.Qin.read(key)
    mat = vc.decode(await self.blobs.read(inp['img']))
    h, w = mat.shape[:2]
    corners = vc.corners.pad(corners, padx=0.04, pady=0.04)
    corr_img = vc.encode(vc.corners.correct(mat, corners * [w, h]), '.png')
    
    corr_key = f'{key}/corrected-{uuid4()}.png'
    await self.blobs.insert(corr_key, corr_img)

    async with Transaction(self.Qin, self.Qout, autocommit=True):
      await self.Qout.push(key, Corrected(img=corr_key, corners=corners, tag='corrected'))
      await self.Qin.pop(key)
    
    self.log(f'Corrected "{key}" to "{corr_key}"', level='DEBUG')

  
  async def rotate(self, key: str, rotation: vc.Rotation):
    inp = await self.Qin.read(key)
    mat = vc.decode(await self.blobs.read(inp['img']))
    rot_img = vc.encode(vc.rotate(mat, rotation), '.png')
    
    rot_key = f'{key}/rotated-{uuid4()}.png'
    await self.blobs.insert(rot_key, rot_img)

    async with Transaction(self.Qin, self.Qout, autocommit=True):
      await self.Qout.push(key, Rotated(rotation=rotation, img=rot_key, tag='rotated'))
      await self.Qin.pop(key)
    
    self.log(f'Rotated "{key}" to "{rot_key}"', level='DEBUG')

@task()
def correct(Qin: ReadQueue[Input], Qout: WriteQueue[Output], ctx: PreprocessContext):
  return Correct(Qin, Qout, blobs=ctx.blobs, log=ctx.log)
