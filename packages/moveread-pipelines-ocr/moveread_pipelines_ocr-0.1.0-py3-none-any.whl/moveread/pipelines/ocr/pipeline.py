from typing_extensions import Sequence, TypedDict, NotRequired
from dataclasses import dataclass
import asyncio
import base64
from kv import KV
from pipeteer import activity, Context

class Input(TypedDict):
  boxes: Sequence[str]
  endpoint: NotRequired[str|None]
  """Custom endpoint (for specific OCR model)"""

@dataclass
class Output:
  preds: Sequence[Sequence[tuple[str, float]]]
  """`preds[ply][top_k] = (label, logprob)`"""

@dataclass
class OcrContext(Context):
  blobs: KV[bytes]
  default_endpoint: str = '/v1/models/baseline:predict'
  tfs_host: str = 'http://localhost'
  tfs_port: int = 8051
  batch_size: int = 8

@activity()
async def ocr_predict(inp: Input, ctx: OcrContext) -> Output:
  import tf.serving as tfs
  import math
  from haskellian import iter as I
  
  preds: Sequence[Sequence[tuple[str, float]]] = []
  endpoint = inp.get('endpoint') or ctx.default_endpoint

  async def predict(b64imgs) -> Sequence[tfs.ImagePreds]:
    nonlocal endpoint
    out = await tfs.predict(b64imgs, endpoint=endpoint)
    if out.tag == 'left':
      if endpoint == ctx.default_endpoint:
        raise Exception(out.value)
      else:
        ctx.log(f'Failed to predict with {endpoint}: {out.value}. Defaulting to {ctx.default_endpoint}')
        endpoint = ctx.default_endpoint
        return await predict(b64imgs)
    else:
      return out.value

  bs = ctx.batch_size
  n_batches = math.ceil(len(inp['boxes'])/bs)
  for i, urls in I.batch(bs, inp['boxes']).enumerate():
    ctx.log(f'Predicting batch {i+1}/{n_batches} ([{bs*i}:{bs*i+len(urls)}])')
    imgs = await asyncio.gather(*[ctx.blobs.read(url) for url in urls])
    b64imgs = [base64.urlsafe_b64encode(img).decode() for img in imgs]
    for img_preds in await predict(b64imgs):
      preds.append(list(zip(img_preds.preds, img_preds.logprobs)))

  ctx.log('Done predicting')
  
  return Output(preds=preds)
    

