import sys,os,re
from .DBMaterial import DBMaterial
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.MaterialLogIO import MaterialLogIO
from util.BluesConsole import BluesConsole

class ChannelDBMaterial(DBMaterial):

  CHANNEL_DAILY_LIMIT = {
    'events':10,
    'news':5,
  }
  QUERY_CONDITION = {
    'mode':'latest',
    'count':None,
  }

  def __init__(self,platform,expected_channel_ratio=None,query_condition=None,channel_daily_limit=None):
    '''
    Parameters:
      platform {str} : the pub platform
      query_condition {dict} : the data query condition {'mode':'latest','count':None}
        - the count wll be calculated dynamic
      expected_channel_ratio {dict}: want to fetch channel count {'events':1,'news':0}
      channel_daily_limit {dict}: the daily count limit {'events':10,'news':5}
    '''
    self.__platform = platform
    self.__expected_channel_ratio = expected_channel_ratio if expected_channel_ratio else self.__get_default_ratio()
    self.__query_condition = query_condition if query_condition else self.QUERY_CONDITION
    self.__channel_daily_limit = channel_daily_limit if channel_daily_limit else self.CHANNEL_DAILY_LIMIT

    # internal state
    # {dict} the reamin count of channel in current day
    self.__remain_channel_ratio = None
    # {int} the remain total count of today
    self.__remain_total_count = 0
    # {dict} pubed channel count
    self.__pubed_channel_ratio = {}
    # {dict} the avail channel count
    self.__avail_channel_ratio = None
    # {int}
    self.__avail_total_count = 0
    # {list<dict>}
    self.__channel_materials = None

  def get(self):
    '''
    Get the material by input channel ratio
      - If the maximum number for the day has been reached, 0 is returned
      - If has no available material, 0 is returned
    '''
    self.__cal_remain()
    if not self.__remain_total_count:
      return None
    
    self.__set_channel_materials()
    self.__console()
    return self.__channel_materials if self.__avail_total_count else None

  def __console(self):
    BluesConsole.info('daily_limit: %s' % self.__channel_daily_limit,self.__platform)
    BluesConsole.info('expected_ratio: %s' % self.__expected_channel_ratio,self.__platform)
    BluesConsole.info('pubed_ratio: %s' % self.__pubed_channel_ratio,self.__platform)
    BluesConsole.info('remain_total: %s' % self.__remain_total_count,self.__platform)
    BluesConsole.info('remain_ratio: %s' % self.__remain_channel_ratio,self.__platform)
    BluesConsole.info('avail_total: %s' % self.__avail_total_count,self.__platform)
    BluesConsole.info('avail_ratio: %s' % self.__avail_channel_ratio,self.__platform)

  def __get_default_ratio(self):
    channel = list(self.CHANNEL_DAILY_LIMIT.keys())[0]
    return {channel:1}

  def __set_channel_materials(self):
    self.__query_condition['count'] = self.__remain_total_count
    # invoke the parent's get 
    materials = super().get(self.__query_condition)
    if not materials:
      return None

    channel_materials = {}
    self.__avail_total_count = len(materials)
    avail_channel_ratio = {}
    allocated_count = 0
    
    # the db's remain avail count may less than the expected count
    for channel,count in self.__remain_channel_ratio.items():

      if allocated_count>=self.__avail_total_count:
        break

      channel_materials[channel] = materials[allocated_count:allocated_count+count]
      avail_channel_ratio[channel] = len(channel_materials[channel])
      allocated_count+=count
    
    self.__avail_channel_ratio = avail_channel_ratio
    self.__channel_materials = channel_materials

  def __cal_remain(self):
    remain_channel_ratio = {}
    remain_total_count = 0

    for channel,count in self.__expected_channel_ratio.items():
      limit_count = self.__channel_daily_limit.get(channel,0)
      pubed_count = MaterialLogIO.get_today_pubed_count(self.__platform,channel)['count']
      self.__pubed_channel_ratio[channel] = pubed_count
      remain_count = limit_count - pubed_count
      # can't bigger than excpeted count
      remain_count = remain_count if remain_count<=count else count 

      if remain_count<=0:
        continue

      remain_total_count+=remain_count
      remain_channel_ratio[channel] = remain_count
    
    self.__remain_channel_ratio = remain_channel_ratio
    self.__remain_total_count = remain_total_count

