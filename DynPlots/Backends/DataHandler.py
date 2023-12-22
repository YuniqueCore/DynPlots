from os import PathLike
from Common.PathHelper import PathHelper


PLOTs_NAME_SOURCE = PathHelper.get_absolute_path("../../Data/Dyn/All.lst")
PLOTs_NAME= []


PathHelper.is_valid_path(PLOTs_NAME_SOURCE,"file",True)
with open(PLOTs_NAME_SOURCE,"r",encoding="utf-8") as f:
    PLOTs_NAME = [l.strip() for l in f.readlines()]





class DumpDataLoader(object):
    raw_data=""
    
    def __init__(self,data_path:PathLike[str]|str) -> None:
        self.data_path=data_path # The path of data
        
    def LoadData(data_path:PathLike[str]|str):
        PathHelper.is_valid_path(data_path,"file",True)
        
            
        
    def RetrieveDataTable():
        pass
    

import re

class DataProcessor:
    start_line_index=0
    
    
    def __init__(self, template_text:str):
        self.template_text = template_text
        self.horizontal_keys = []
        self.horizontal_values = []
        self.horizontal_datas = []
        self.vertical_keys = []
        self.vertical_values = []
        self.vertical_datas = []

        self.process_template()
        
    def _start_end_with(line:str,identifier:str)->bool:
            if line.startswith(identifier) and line.endswith(identifier):
                return True
            return False

    def process_template(self):
        # Define regular expression patterns
        horizontal_pattern = re.compile(r"@(.+?)@.*{{(.+?)}}")
        key_pattern = re.compile(r"@(?P<Keys>.+?)@")
        value_ex_pattern = re.compile(r"{{(?P<Values>(?:(?!\.\.\.Data\.\.\.).)+?)}}") # exclude {{...Data...}}
        data_pattern = re.compile(r"{{(?P<Data>...Data...)}}")
        
        template_text_lines = self.template_text.splitlines();
        for line in template_text_lines:
            for match in re.finditer(key_pattern,line):
                keys=match.groupdict()
                
            
        
        # Process horizontal lines
        for match in re.finditer(horizontal_pattern, self.template_text):
            key, value = match.groups()
            self.horizontal_keys.append(key)
            self.horizontal_values.append(value)
            if "Data" in value:
                self.horizontal_datas.append([])

        # Process vertical lines
        for match in re.finditer(key_pattern, self.template_text):
            key = match.group(1)
            self.vertical_keys.append(key)
            if "Data" in self.template_text:
                self.vertical_datas.append([])

    def process_actual_data(self, actual_data_text:str):
        actual_data_lines:list[str] = actual_data_text.split()
        data_start = False
        
        
            
        for line in actual_data_lines:
            if self._start_end_with(line,'=-=')  or self._start_end_with(line,'<|>'):
                continue
            elif line.strip() == "":
                data_start = True
                continue

            if data_start:
                data_values = line.split()
                for i, value in enumerate(data_values):
                    if "Data" in self.horizontal_values[i]:
                        self.horizontal_datas[i].append(value)
                    if "Data" in self.vertical_values:
                        self.vertical_datas[self.vertical_keys.index("Time")].append(data_values[0])
                        self.vertical_datas[self.vertical_keys.index(self.vertical_values)].append(value)

    def print_extracted_data(self):
        print("Horizontal Keys:", self.horizontal_keys)
        print("Horizontal Values:", self.horizontal_values)
        print("Horizontal Datas:", self.horizontal_datas)
        print("Vertical Keys:", self.vertical_keys)
        print("Vertical Values:", self.vertical_values)
        print("Vertical Datas:", self.vertical_datas)

# Read template file
with open("DataAnnotationTemplate.txt", "r") as template_file:
    template_data = template_file.read()
    # Read actual data file
    with open("ActualData.txt", "r") as actual_data_file:
        actual_data = actual_data_file.read()
    # Create DataProcessor instance with the template
    processor = DataProcessor(template_data)
    # Process actual data
    processor.process_actual_data(actual_data)
    # Print extracted data
    processor.print_extracted_data()

