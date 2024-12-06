from typing_extensions import TypedDict, TYPE_CHECKING
from dataclasses import dataclass
from uuid import uuid4
from pipeteer import activity, Context
import pure_cv as vc
import scoresheet_models as sm
if TYPE_CHECKING:
  from kv import KV
  from moveread.tatr import TableDetector

class Input(TypedDict):
  model: 'sm.Model'
  img: str

@dataclass
class Output:
  contours: 'vc.Contours'
  contoured: str

@dataclass(kw_only=True)
class TatrContext(Context):
  model: 'TableDetector'
  blobs: 'KV[bytes]'
  descaled_h: int = 768

def n_boxes(model: sm.Model) -> int:
  return model.rows * len(model.block_cols) * 2

@activity()
async def extract(input: Input, ctx: TatrContext) -> Output | None:
  name, _ = input['img'].rsplit('.', 1)
  mat = vc.decode(await ctx.blobs.read(input['img']))
  model = input['model']
  ctx.log(f'Detecting {input["img"]}...')
  cnts = ctx.model.detect(mat, max_cells=n_boxes(model), n_rows=model.rows)
  ctx.log(f'Detected {len(cnts)} contours')

  descaled = vc.descale_max(mat, target_max=ctx.descaled_h)
  h, w = descaled.shape[:2]
  contoured = vc.draw.gradient_contours(descaled, cnts * [w, h])
  contoured = vc.encode(contoured, format='.jpg')
  cont = f'{name}/contoured_{uuid4()}.jpg'
  await ctx.blobs.insert(cont, contoured)

  return Output(contours=cnts, contoured=cont)

