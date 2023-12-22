import re
import unittest

from Backends.Common.PathHelper import PathHelper
from Backends.DataHandler import DumpDataLoader

class TemplateDealer:
    def __init__(self, start_index: int, deal_way: str="row",end_index:int=0):
        self._start_index = self.__validate_index(start_index)
        self._deal_way = self.__validate_deal(deal_way)
        self._end_index = self.__validate_index(end_index)
        return self

    def __validate_index(self, index:int)->int:
        if index.isinstance(int) and index >= 0:
            return index
        else:
            raise ValueError("Error: start_index should greater than 0: {0}".format(index))

    def __validate_deal(self, way:str)->str:
        way = way.lower()
        if  way.isinstance(str):
            if way == "row" or way == "r":
                return "row"  
            elif way == "col" or way == "column":
                return = "col" 
        else:
            raise ValueError("Error: No such deal_way: {0}".format(way))
    
    @property
    def deal_way(self) -> str:
        return self._deal_way
    
    @property
    def start_index(self) -> int:
        return self._start_index
    
    @property
    def end_index(self) -> int:
        return self._end_index
    
    @staticmethod
    def start_end_with(line:str,identifier:str)->bool:
        if line.startswith(identifier) and line.endswith(identifier):
            return True
        return False 
    
    @staticmethod
    def retrieve_dealers(template_text_lines):
        dealers:list[TemplateDealer] = []
        for index,line in enumerate(template_text_lines):
            if TemplateDealer.start_end_with(line,"=-="):
                dealers.append(TemplateDealer(index,"row"))
            elif TemplateDealer.start_end_with(line,"=|="):
                dealers.append(TemplateDealer(index,"col"))
            elif TemplateDealer.start_end_with(line,"<->"):
                dealers.append(TemplateDealer(index+1,"row"))
            elif TemplateDealer.start_end_with(line,"<|>"):
                dealers.append(TemplateDealer(index+1,"col"))
            dealers[index-1]._end_index = index # maybe null reference error. !TODO
        return dealers


class MyTestCase(unittest.TestCase):
    _find_start_index=False
    dealers:list[TemplateDealer]=[]
    
    key_pattern = re.compile(r"@(?P<Keys>.+?)@")
    value_ex_pattern = re.compile(r"{{(?P<Values>(?:(?!\.\.\.Data\.\.\.).)+?)}}") # exclude {{...Data...}}
    data_pattern = re.compile(r"{{(?P<Data>...Data...)}}")
    
    def setUp(self):
        # 在每个测试用例运行之前执行的设置代码
        self.standard_DUMP=PathHelper.get_absolute_path("../Data/Dyn/standard/3phase.dmp")
        self.template_DUMP=PathHelper.get_absolute_path("../Data/AnnotationTemplate.txt")
        pass

    def tearDown(self):
        # 在每个测试用例运行之后执行的清理代码
        pass

    def test_addition(self):
        with open(self.template_DUMP,"r",encoding="utf-8") as f:
            template_text_lines = f.readlines()
            self.dealers = TemplateDealer.retrieve_dealers(template_text_lines)
            
            # according the template dealer start and end index to replace the identifiers in each line by
            # the deal_way defined in the template dealer.
            for dealer in self.dealers:
                start = dealer.start_index
                end = dealer.end_index
                for line in template_text_lines[start:end]:
                    self.replace_match(self.key_pattern,line)
                    self.replace_match(self.value_ex_pattern,line)
                    self.replace_match(self.data_pattern,line)
            self.assertEqual(3, 3, "1 + 2 should be equal to 3")


    def replace_match(self,pattern:re.Pattern[str], line:str):
        for match in re.finditer(pattern,line):
            groupdict = match.groupdict()
            groups = match.groups()


    def test_subtraction(self):
        result = 5 - 2
        self.assertEqual(result, 3, "5 - 2 should be equal to 3")

if __name__ == '__main__':
    unittest.main()
