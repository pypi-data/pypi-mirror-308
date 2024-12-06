import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.BaiJiaDBModelFactory import BaiJiaDBModelFactory
from sele.loginer.baijia.BaiJiaLoginerFactory import BaiJiaLoginerFactory   
from sele.publisher.StandardPublisher import StandardPublisher

class BaiJiaNAPS(NAPS):
  
  # override
  def publish(self):
    loginer = self.__get_loginer()
    models = self.__get_models()
    publisher= StandardPublisher(models,loginer)
    publisher.publish()

  # override
  def prepublish(self):
    loginer = self.__get_loginer()
    models = self.__get_models()
    publisher= StandardPublisher(models,loginer)
    publisher.prepublish()

  def __get_loginer(self):
    loginer_factory = BaiJiaLoginerFactory()
    return loginer_factory.create_account()

  def __get_models(self):
    query_condition = {
      'mode':'latest',
      'count':2,
    }
    factory = BaiJiaDBModelFactory()
    excepted_channel_ratio = {
      'events':1,
      'news':1,
    }
    return factory.create(excepted_channel_ratio,query_condition)
