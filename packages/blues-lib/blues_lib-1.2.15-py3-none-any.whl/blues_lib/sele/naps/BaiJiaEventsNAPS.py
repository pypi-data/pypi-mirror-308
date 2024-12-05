import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.BaiJiaDBModelFactory import BaiJiaDBModelFactory
from sele.loginer.baijia.BaiJiaLoginerFactory import BaiJiaLoginerFactory   
from sele.publisher.StandardPublisher import StandardPublisher
from util.BluesConsole import BluesConsole

class BaiJiaEventsNAPS(NAPS):

  def publish(self):
    loginer_factory = BaiJiaLoginerFactory()
    loginer = loginer_factory.create_account()

    factory = BaiJiaDBModelFactory()
    condition = {
      'mode':'latest',
      'count':1,
    }
    models = factory.create_events(condition)
    publisher= StandardPublisher(models,loginer)
    publisher.publish()

