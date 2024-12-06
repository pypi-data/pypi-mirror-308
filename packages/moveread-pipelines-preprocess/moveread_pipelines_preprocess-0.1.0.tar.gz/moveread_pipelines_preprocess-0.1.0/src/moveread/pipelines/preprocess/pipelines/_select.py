from typing_extensions import TypedDict, Literal
from dataclasses import dataclass
from haskellian import AsyncIter
import pure_cv as vc
from pipeteer import WriteQueue, ReadQueue, task, Transaction
import scoresheet_models as sm

class Input(TypedDict):
  img: str
  model: sm.Model

class Selected(TypedDict):
  contours: vc.Contours
  tag: Literal['selected']

class Recorrect(TypedDict):
  tag: Literal['recorrect']

Output = Selected | Recorrect

@dataclass
class Select:
  Input = Input
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]

  def items(self):
    return AsyncIter(self.Qin.items())
  
  async def select(self, key: str, grid_coords: vc.Rect):
    inp = await self.Qin.read(key)
    cnts = sm.contours(inp['model'], **grid_coords)
    async with Transaction(self.Qin, self.Qout, autocommit=True):
      await self.Qout.push(key, {'contours': cnts, 'tag': 'selected'})
      await self.Qin.pop(key)

  async def recorrect(self, key: str):
    async with Transaction(self.Qin, self.Qout, autocommit=True):
      await self.Qout.push(key, {'tag': 'recorrect'})
      await self.Qin.pop(key)

@task()
def select(Qin: ReadQueue[Input], Qout: WriteQueue[Output]):
  return Select(Qin, Qout)