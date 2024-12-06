from dataclasses import dataclass
from pipeteer import task, ReadQueue, WriteQueue, Context as BaseContext
from kv import KV, LocatableKV
from moveread.pipelines.correct import api, SDK, Input, Output, Annotations

@dataclass
class Context(BaseContext):
  cache: KV[Annotations]
  blobs: LocatableKV[bytes]

@task()
def correct(Qin: ReadQueue[Input], Qout: WriteQueue[Output], ctx: Context):
  sdk = SDK(Qin, Qout, ctx.cache)
  return api(sdk, ctx.blobs, logger=ctx.log)
