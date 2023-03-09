from pydantic import BaseSettings


class Settings(BaseSettings):
  mode: str
  database_url: str
  database_name: str
  broker_url: str
  result_backend: str
  blender_path: str

  @property
  def is_dev(self):
    return self.mode == 'development'

  @property
  def is_prod(self):
    return self.mode == 'production'

  class Config:
    env_file = ".env"

settings = Settings()