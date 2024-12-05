import sys,os,re,json
from .Material import Material

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO

class DBMaterial(Material):
  '''
  The material from db
  '''
  
  # override
  def set(self):
    mode = self._condition.get('mode')
    count = self._condition.get('count')
    rows = None

    if mode == 'latest':
      rows = self.__latest(count)

    if rows:
      self.__format(rows)
      self._rows = rows

  # override
  def get_default_condition(self):
    return {
      'mode':'latest',
      'count':1,
    }

  # getter : all
  def get(self):
    return self._rows

  # getter : first one
  def first(self):
    if not self._rows:
      return None

    return self._rows[0]
    
  def __latest(self,count=1):
    response = BluesMaterialIO.latest(count)
    return response.get('data')

  def __format(self,rows):
    '''
    Set the foramt entity dict, extract the json fields to object
    Returns 
      {list<dict>}
    '''
    for material in rows:
      texts = json.loads(material.get('material_body_text'))
      images = json.loads(material.get('material_body_image'))
      body = json.loads(material.get('material_body'))
      
      # convert the json to object
      material['material_body_text']=texts
      material['material_body_image']=images
      material['material_body']=body

