from typing import Generic, TypeVar
from dataclasses import dataclass, field
from haskellian import ManagedAsync

T = TypeVar('T')

@dataclass
class Streams(Generic[T]):
  channels: dict[str, ManagedAsync[T]] = field(default_factory=dict)

  def listen(self, id: str) -> ManagedAsync[T]:
    if not id in self.channels:
      self.channels[id] = ManagedAsync()
    return self.channels[id]
  
  def push(self, id: str, value: T):
    self.listen(id).push(value)

  def delete(self, id: str):
    if id in self.channels:
      del self.channels[id]

  def clear(self):
    self.channels.clear()