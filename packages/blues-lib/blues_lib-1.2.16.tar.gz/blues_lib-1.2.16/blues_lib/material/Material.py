from abc import ABC,abstractmethod

class Material(ABC):

  def __init__(self,condition=None):
    # {dict} the material dict
    self._rows = None
    # {dict} the data filter condition
    self._condition = condition if condition else self.get_default_condition()

    # fetch and keep the materials
    self.set()

  
  @abstractmethod
  def get_default_condition(self):
    '''
    Return the dfault condition
    '''
    pass

  @abstractmethod
  def set(self):
    '''
    Fetch and set rows
    '''
    pass
