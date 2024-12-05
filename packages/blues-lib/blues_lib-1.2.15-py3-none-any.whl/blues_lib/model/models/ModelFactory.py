from abc import ABC,abstractmethod

class ModelFactory(ABC):

  def create_mix(self,conditions):
    pass

  def create_events(self,condition):
    pass

  def create_news(self,condition):
    pass
    
  def create_gallery(self,condition):
    pass

  def create_video(self,condition):
    pass
