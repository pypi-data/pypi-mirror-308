import sys,os,re
from .SchemaEntityText import SchemaEntityText  
from .SchemaEntityImage import SchemaEntityImage  
from .SchemaValueReplacer import SchemaValueReplacer  
from .SchemaSelectorReplacer import SchemaSelectorReplacer  

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.SchemaTransformerDeco import SchemaTransformerDeco
from sele.transformer.Transformer import Transformer

class SchemaTransformerChain(Transformer):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'

  @SchemaTransformerDeco()
  def resolve(self,request):
    '''
    Deal the atom by the event chain
    '''
    handler = self.__get_chain()
    return handler.handle(request)

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    entity_text = SchemaEntityText()
    entity_image = SchemaEntityImage()
    value_replacer = SchemaValueReplacer()
    selector_replacer = SchemaSelectorReplacer()

    entity_text.set_next(entity_image) \
      .set_next(value_replacer) \
      .set_next(selector_replacer)

    return entity_text
