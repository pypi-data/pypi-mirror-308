# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "该类作为接口基类"
"""
  * @File    :   Api.py
  * @Time    :   2023/04/29 19:16:03
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   该类作为接口基类
"""

import json
from xy_string.utils import is_empty_string
from xy_request_handler_base.Base import Base


class Api(Base):
    """api请求基类"""

    @property
    def json_arguments(self):
        content_type = self.request.headers.get("Content-Type")
        if not is_empty_string(content_type) and "json" in content_type.lower():
            return json.loads(bytes.decode(self.request.body))
        return None

    __code = 1
    __message = "请求失败"
    __data = {}
    __fail_code_cache = 1

    __response_dict = {"code": __code, "message": __message, "data": __data}

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        if isinstance(value, type(self.__code)):
            return
        self.__code = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if isinstance(value, type(self.__message)):
            return
        self.__message = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def success(self, message="请求成功"):
        self.__code = 0
        self.__message = message

    def fail(self, message="请求失败"):
        self.__code = self.__fail_code_cache + 1
        self.__message = message
        self.__fail_code_cache = self.__code

    def xy_response(self):
        self.__response_dict["code"] = self.__code
        self.__response_dict["message"] = self.__message
        self.__response_dict["data"] = self.__data
        self.write(json.dumps(self.__response_dict))
