from typing_extensions import TypedDict, NotRequired
import asyncio
from pipeteer import activity
import pure_cv as vc
from moveread.core import Image
from moveread.pipelines.preprocess import Output, PreprocessContext
from ._correct import Corrected

class Input(TypedDict):
  img: str
  contours: vc.Contours
  corrected: NotRequired[Corrected|None]
  blobs: list[str]

def extract_boxes(img: bytes, cnts: vc.Contours) -> list[bytes]:
  mat = vc.decode(img)
  h, w = mat.shape[:2]
  boxes = vc.extract_contours(mat, cnts * [w, h])
  return [vc.encode(box, '.png') for box in boxes if box.size > 0] # just in case

async def store_boxes(inp: Input, ctx: PreprocessContext) -> Output:
  url, cnts = inp['img'], inp['contours']
  if (corr := inp.get('corrected')):
    cnts = vc.corners.unwarp_relative_contours(cnts, corr.corners)

  img = await ctx.blobs.read(url)

  image = Image(url=url, meta=Image.Meta(
    boxes=Image.BoxContours(contours=cnts, relative=True),
    perspective_corners=corr and corr.corners,
  ))

  boxes = extract_boxes(img, cnts)
  name, _ = url.rsplit('.', 1)
  urls = [f'{name}/boxes/{i}.png' for i in range(len(boxes))]
  await asyncio.gather(*[ctx.blobs.insert(url, box) for url, box in zip(urls, boxes)])

  ctx.log(f'Inserted {len(boxes)} boxes: {", ".join(urls[:2])}, ...', level='DEBUG')

  return Output(image=image, boxes=urls)

@activity()
async def preoutput(inp: Input, ctx: PreprocessContext) -> Output:
  out = await store_boxes(inp, ctx)
  corr = inp.get('corrected')
  def delete(blob: str):
    return blob != inp['img'] and (corr is None or blob != corr.img)
  del_blobs = [blob for blob in inp['blobs'] if delete(blob)]
  await asyncio.gather(*[ctx.blobs.delete(blob) for blob in del_blobs])
  ctx.log(f'Deleted {len(del_blobs)} images: {del_blobs}', level='DEBUG')
  return out
  