import re
import unittest

from Backends.Common.PathHelper import PathHelper

class MyTestCase(unittest.TestCase):
    key_pattern = re.compile(r"@(?P<Keys>.+?)@")
    value_ex_pattern = re.compile(r"{{(?P<Values>(?:(?!\.\.\.Data\.\.\.).)+?)}}") # exclude {{...Data...}}
    data_pattern = re.compile(r"{{(?P<Data>...Data...)}}")
    def setUp(self):
        # 在每个测试用例运行之前执行的设置代码
        self.standard_DUMP=PathHelper.get_absolute_path("../Data/Dyn/standard/3phase.dmp")
        self.template_DUMP=PathHelper.get_absolute_path("../Data/Dyn/standard/3phase.dmp")
        pass

    def tearDown(self):
        # 在每个测试用例运行之后执行的清理代码
        pass

    def test_addition(self):
        with open(self.template_DUMP,"r",encoding="utf-8") as f:
            self.template_text = f.read()
            template_text_lines = self.template_text.splitlines();
            for line in template_text_lines:
                for match in re.finditer(self.key_pattern,line):
                    keys=match.groupdict()
            self.assertEqual(3, 3, "1 + 2 should be equal to 3")

    def test_subtraction(self):
        result = 5 - 2
        self.assertEqual(result, 3, "5 - 2 should be equal to 3")

if __name__ == '__main__':
    unittest.main()
