from typing_extensions import Literal, Sequence, TypedDict
from dataclasses import dataclass, field
from pydantic import BaseModel
import sequence_edits as se
from chess_notation import Language, PawnCapture, PieceCapture, MotionStyles

@dataclass
class ManualPred:
  san: str
  tag: Literal['manual'] = 'manual'

@dataclass
class AutoPred:
  san: str
  prob: float
  tag: Literal['predicted'] = 'predicted'
  
Pred = ManualPred | AutoPred

class Preds(BaseModel):
  reqId: str
  tag: Literal['preds'] = 'preds'
  preds: Sequence[Pred]

class Done(BaseModel):
  reqId: str
  tag: Literal['done'] = 'done'

Message = Preds | Done

NA = Literal['N/A']
def no_na(value):
  if value != 'N/A':
    return value

@dataclass
class Annotations:
  lang: Language | NA | None = None
  pawn_capture: PawnCapture | NA | None = None
  piece_capture: PieceCapture | NA | None = None
  end_correct: int | None = None
  manual_ucis: dict[int, str] = field(default_factory=dict)
  edits: Sequence[se.Edit] = field(default_factory=list)

  def motions(self) -> MotionStyles:
    styles = MotionStyles()
    if (pawn_cap := no_na(self.pawn_capture)) is not None:
      styles.pawn_captures = [pawn_cap]
    if (piece_cap := no_na(self.piece_capture)) is not None:
      styles.piece_captures = [piece_cap]
    return styles
  
  def langs(self) -> list[Language]:
    if (l := no_na(self.lang)) is not None:
      return [l]
    else:
      return ['EN', 'CA']

@dataclass
class Meta:
  title: str
  id: str
  @classmethod
  def of(cls, entry: tuple[str, 'Input']):
    k, v = entry
    return cls(id=k, title=v['title'])

class Input(TypedDict):
  title: str
  boxes: Sequence[str]
  ocrpreds: Sequence[Sequence[tuple[str, float]]]
  """MOVE x TOP_PREDS x (word, logprob)"""

@dataclass
class Item:
  title: str
  boxes: Sequence[str]
  anns: Annotations

@dataclass
class CorrectResult:
  annotations: Annotations
  pgn: Sequence[str]
  early: bool
  tag: Literal['correct'] = field(default='correct', kw_only=True)

@dataclass
class BadlyPreprocessed:
  tag: Literal['badly-preprocessed'] = 'badly-preprocessed'

Output = CorrectResult | BadlyPreprocessed
