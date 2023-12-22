import re
import unittest

from Backends.Common.PathHelper import PathHelper
from Backends.DataHandler import DumpDataLoader

class TemplateDealer:
    def __init__(self, start_index: int, deal_way: str="row"):
        self.__init_index(start_index)
        self.__init_deal(deal_way)
        return self

    def __init_index(self, start_index):
        if start_index.isinstance(int) and start_index >= 0:
            self._start_index= start_index
        else:
            raise ValueError("Error: start_index should greater than 0: {0}".format(start_index))

    def __init_deal(self, deal_way):
        deal_way = deal_way.lower()
        if  deal_way.isinstance(str):
            if deal_way == "row" or deal_way == "r":
                self._deal_way = "row"  
            elif deal_way == "col" or deal_way == "column":
                self._deal_way = "col" 
        else:
            raise ValueError("Error: No such deal_way: {0}".format(deal_way))
    
    @property
    def deal_way(self) -> str:
        return self._deal_way
    
    @property
    def start_index(self) -> int:
        return self._start_index
    
    @staticmethod
    def start_end_with(line:str,identifier:str)->bool:
        if line.startswith(identifier) and line.endswith(identifier):
            return True
        return False 
    
    @staticmethod
    def retrieve_dealers(template_text_lines):
        dealers = []
        for index,line in enumerate(template_text_lines):
            if TemplateDealer.start_end_with(line,"=-="):
                dealers.append(TemplateDealer(index,"row"))
            elif TemplateDealer.start_end_with(line,"=|="):
                dealers.append(TemplateDealer(index,"col"))
            elif TemplateDealer.start_end_with(line,"<->"):
                dealers.append(TemplateDealer(index+1,"row"))
            elif TemplateDealer.start_end_with(line,"<|>"):
                dealers.append(TemplateDealer(index+1,"col"))
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
            for dealer in self.dealers:
                line = ""
                for match in re.finditer(self.key_pattern,line):
                    keys=match.groupdict()
                    keys =match.groups()
                for match in re.finditer(self.value_ex_pattern,line):
                    values=match.groupdict()
                    values=match.groups()
                for match in re.finditer(self.data_pattern,line):
                    data=match.groupdict()
                    data=match.groups()
                    
            self.assertEqual(3, 3, "1 + 2 should be equal to 3")


    def test_subtraction(self):
        result = 5 - 2
        self.assertEqual(result, 3, "5 - 2 should be equal to 3")

if __name__ == '__main__':
    unittest.main()
