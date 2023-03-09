from pydantic import BaseModel, Field
from bson import ObjectId
from utils.py_object_id import PyObjectId


class FilesSchema(BaseModel):
  close: str
  mid: str
  range: str
  model: str


class ErrorSchema(BaseModel):
  type: str
  stack_trace: str


class RenderSchema(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
  token_id: str
  frame_id: int = None
  eyes: str = None
  accessory_face: str = None
  hair: str = None
  boobs: str = None
  nipples: str = None
  accessory_boobs: str = None
  butts: str = None
  surprise: str = None
  legs: str = None
  accessory_butts: str = None
  accessory_legs: str = None
  background: str = None
  skin: str = None
  hand: str = None
  files: FilesSchema = None
  complete: bool = False
  error: ErrorSchema = None

  @property
  def traits(self):
    traits = {
      'eyes': self.eyes,
      'accessory_face': self.accessory_face,
      'hair': self.hair,
      'boobs': self.boobs,
      'nipples': self.nipples,
      'accessory_boobs': self.accessory_boobs,
      'butts': self.butts,
      'surprise': self.surprise,
      'legs': self.legs,
      'accessory_butts': self.accessory_butts,
      'accessory_legs': self.accessory_legs,
      'background': self.background,
      'skin': self.skin,
      'hand': self.hand,
    }

    filtered = {k: v for k, v in traits.items() if v is not None}
    return filtered


  class Config:
    json_encoders = { ObjectId: str }
    schema_extra = {
      'example': {
        '_id': '62d94327d8b868eb0fdc7fa1',
        'token_id': '1',
        'frame_id': 1,
        'eyes': 'Coffee',
        'accessory_face': 'Logo',
        'hair': 'Long White',
        'boobs': 'S',
        'nipples': 'Ordinary',
        'accessory_boobs': 'Choker',
        'butts': 'Peach',
        'surprise': 'Gucci',
        'legs': 'Grid',
        'accessory_butts': 'Butterfly',
        'accessory_legs': 'Chains',
        'background': 'Purple Bitch',
        'skin': 'Acid',
        'hand': 'Base',
        'files': None,
        'complete': False,
        'error': ''
      }
    }