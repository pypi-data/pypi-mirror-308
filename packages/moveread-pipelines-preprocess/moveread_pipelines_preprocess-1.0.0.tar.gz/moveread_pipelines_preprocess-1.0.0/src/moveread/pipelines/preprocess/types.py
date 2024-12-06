from typing_extensions import TypedDict
from dataclasses import dataclass
import scoresheet_models as sm
from moveread.core import Image

class Input(TypedDict):
  img: str
  model: sm.Model

@dataclass
class Output:
  image: Image
  boxes: list[str]