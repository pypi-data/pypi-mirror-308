from typing import Sequence
from dataclasses import dataclass
from kv import KV
from pipeteer.queues import ReadQueue, WriteQueue, Transaction, InexistentItem
import sequence_edits as se
import game_prediction as gp
from moveread.pipelines.correct import Annotations, Meta, Input, Output, CorrectResult, BadlyPreprocessed, Item

@dataclass
class SDK:
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  cache: KV[Annotations]

  async def items(self):
    async for e in self.Qin.items():
      yield Meta.of(e)

  async def item(self, id: str):
    inp = await self.Qin.safe_read(id)
    if inp:
      anns = await self.cache.safe_read(id)or Annotations()
      return Item(title=inp['title'], boxes=inp['boxes'], anns=anns)
  
  async def confirm(self, id: str, pgn: Sequence[str], early: bool):
    try:
      anns = await self.cache.safe_read(id) or Annotations()
      result = CorrectResult(pgn=pgn, early=early, annotations=anns)
      async with Transaction(self.Qin, self.Qout, autocommit=True):
        await self.Qout.push(id, result)
        await self.Qin.pop(id)
      return True
    except InexistentItem:
      return False

  async def repreprocess(self, id: str):
    try:
      async with Transaction(self.Qin, self.Qout, autocommit=True):
        await self.Qin.pop(id)
        await self.Qout.push(id, BadlyPreprocessed())
      return True
    except InexistentItem:
      return False

  async def annotate(self, id: str, anns: Annotations):
    return await self.cache.insert(id, anns)
  
  async def predict(self, id: str, *, fen: str, beam_width: int = 4):
    task = await self.Qin.read(id)
    anns = await self.cache.safe_read(id) or Annotations()
    preds = task['ocrpreds'][:(anns and anns.end_correct)]
    preds = se.apply(anns.edits or [], list(preds), fill=[('', 0)])

    return gp.guided_predict(
      preds, manual_ucis=anns.manual_ucis, fen=fen, beam_width=beam_width,
      motions=anns.motions(), languages=anns.langs()
    )