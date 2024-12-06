from typing_extensions import TypedDict
from dataclasses import dataclass
from haskellian import AsyncIter
from pipeteer import WriteQueue, ReadQueue, task, Transaction

class Input(TypedDict):
  contoured: str

@dataclass
class Validate:
  Input = Input
  Qin: ReadQueue[Input]
  Qout: WriteQueue[bool]

  def items(self):
    return AsyncIter(self.Qin.items())
  
  async def annotate(self, key: str, valid: bool):
    async with Transaction(self.Qin, self.Qout, autocommit=True):
      await self.Qout.push(key, valid)
      await self.Qin.pop(key)

@task()
def validate(Qin: ReadQueue[Input], Qout: WriteQueue[bool]):
  return Validate(Qin, Qout)