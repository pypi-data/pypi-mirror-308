from pipeteer import workflow, WorkflowContext
import pure_cv as vc
from moveread.pipelines.tatr import extract
from moveread.pipelines.preprocess import Input, Output
from moveread.pipelines.preprocess.pipelines import (
  select, validate, correct, preoutput, descale, Corrected
)

@workflow()
async def preprocess(inp: Input, ctx: WorkflowContext) -> Output:
  model = inp['model']
  blobs = [inp['img']]

  async def _extract(img: str, corrected: Corrected | None = None) -> Output:
    """Autoextract and validate.
    - If OK, then output
    - Else if corrected, then select
    - Else correct
    """
    if (r := await ctx.call(extract, { 'img': corrected.img if corrected else img, 'model': model })):
      blobs.append(r.contoured)

    if r and await ctx.call(validate, { 'contoured': r.contoured }):
      return await _preoutput(img, r.contours, corrected)
    elif corrected is not None:
      return await _select(img, corrected)
    else:
      return await _correct(img)


  async def _correct(img: str) -> Output:
    """Correct or rotate.
    - If correct, then extract (the corrected image)
    - Else rotate and extract (as if starting anew, but with the rotated image)
    """
    descaled = await ctx.call(descale, { 'img': img, 'height': 768 })
    corr = await ctx.call(correct, { 'img': img, 'descaled_img': descaled })
    blobs.extend([descaled, corr.img])

    if corr.tag == 'rotated':
      return await _extract(corr.img)
    else:
      return await _extract(img, corr)
    
  async def _select(orig: str, corrected: Corrected) -> Output:
    """Select or recorrect.
    - If select, then output
    - Else go back to correction
    """
    descaled = await ctx.call(descale, { 'img': corrected.img, 'height': 768 })
    blobs.append(descaled)

    r = await ctx.call(select, { 'img': descaled, 'model': model })
    if r['tag'] == 'recorrect':
      return await _correct(orig)
    else:
      return await _preoutput(orig, r['contours'], corrected)


  async def _preoutput(img: str, cnts: vc.Contours, corrected: Corrected | None = None) -> Output:
    return await ctx.call(preoutput, { 'img': img, 'corrected': corrected, 'contours': cnts, 'blobs': blobs})
  
  return await _extract(inp['img'])


