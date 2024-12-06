from dataclasses import dataclass
from pipeteer import Context
from kv import LocatableKV

@dataclass
class PreprocessContext(Context):
  blobs: LocatableKV[bytes]