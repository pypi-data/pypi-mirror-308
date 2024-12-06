from typing_extensions import TypedDict
from uuid import uuid4
from pipeteer import activity
import pure_cv as vc
from moveread.pipelines.preprocess import PreprocessContext

class Input(TypedDict):
  img: str
  height: int

@activity()
async def descale(inp: Input, ctx: PreprocessContext) -> str:
  img, h = inp['img'], inp['height']
  mat = vc.decode(await ctx.blobs.read(img))
  descaled = vc.encode(vc.descale_h(mat, h), '.jpg')

  name, _ = img.rsplit('.', 1)
  out_key = f'{name}-descaled-{uuid4()}.jpg'
  await ctx.blobs.insert(out_key, descaled)

  return out_key
