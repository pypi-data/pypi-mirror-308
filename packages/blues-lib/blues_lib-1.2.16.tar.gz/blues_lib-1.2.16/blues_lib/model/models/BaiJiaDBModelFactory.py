import sys,os,re
from .ModelFactory import ModelFactory

sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from model.MaterialModel import MaterialModel
from schema.releaser.baijia.BaiJiaSchemaFactory import BaiJiaSchemaFactory
from material.DBMaterial import DBMaterial     

class BaiJiaDBModelFactory(ModelFactory):

  def __init__(self):
    self.schema_factory = BaiJiaSchemaFactory()

  def create_mix(self,conditions):
    '''
    Create multi diff channel schemas
    Parameters:
      conditions {dict<str,dict>} : the db material's query condition
    '''
    models = []
    for channel,condition in conditions.items():
      channel_models = None
      if channel == 'events':
        channel_models = self.create_events(condition)
      elif channel == 'news':
        channel_models = self.create_news(condition)

      if channel_models:
        models.extend(channel_models)
    return models

  def create_events(self,material_condition=None):
    '''
    Parameters:
      condition {dict} : the db material's query condition
    '''
    schema = self.schema_factory.create_events()
    db_material = DBMaterial(material_condition)
    materials = db_material.get()

    return MaterialModel(schema,materials).get()

  def create_news(self,material_condition=None):
    schema = self.schema_factory.create_news()
    db_material = DBMaterial(material_condition)
    materials = db_material.get()

    return MaterialModel(schema,materials).get()

