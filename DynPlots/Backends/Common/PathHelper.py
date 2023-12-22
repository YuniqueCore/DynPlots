import inspect
import os
from typing import Union


class PathHelper:
    # 检查给定路径是否存在,并且是否是指定类型
    @staticmethod
    def is_valid_path(path: Union[str, os.PathLike[str]], expected_type: str = "path", throw: bool = False) -> bool:
        """
        检查给定路径是否存在。
        :param path: 要检查的路径
        :param expected_type: Checking Type, path | file | dir
        :param throw: 是否在路径非法或者不存在时抛出异常
        :return: bool: 如果路径存在, 则返回 True, 否则返回 False 或者抛出异常。
        """

        if not os.path.exists(path):
            if expected_type.lower() == "path":
                if throw:
                    raise FileNotFoundError(f"The path {path} does not exist.")
                else:
                    return False
            elif expected_type.lower() == "file":
                if os.path.isfile(path):
                    return True, ""
                elif throw:
                    raise FileNotFoundError(f"The File {path} does not exist.")
                else:
                    return False
            elif expected_type.lower() == "dir":
                if os.path.isdir(path):
                    return True, ""
                elif throw:
                    raise FileNotFoundError(f"The Directory {path} does not exist.")
                else:
                    return False
        return True

    @staticmethod
    def get_absolute_path(relative_path, base_file=None):
        """
        获取绝对路径
        :param relative_path: 相对路径
        :param base_file: 基础文件
        :return: 绝对路径
        """
        # Determine the base file
        if base_file is None:
            # If base_file is not provided, use the calling file
            frame = inspect.stack()[1]
            base_file = frame[0].f_globals.get('__file__', None)
            if base_file:
                base_file = os.path.abspath(base_file)
    
        if not base_file:
            raise ValueError("Unable to determine the base file.")
    
        # Calculate the absolute path
        abs_relpath = os.path.join(os.path.dirname(base_file), relative_path)
        absolute_path = os.path.abspath(abs_relpath)
    
        return absolute_path

    