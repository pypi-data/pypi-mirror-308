import requests

from datamart_yhdr.settings import const


class DMInterface:
    def __init__(self, username: str, password: str, env="PROD", url="default"):
        """
        初始化银河德睿数据平台接口对象
        :param username: 用户名
        :param password: 密码
        """
        self.username = username
        self.password = password

        if env == "PROD":
            if url == "default":
                halo_url = const.HALO_URL
            elif url == "trader":
                halo_url = const.HALO_URL_TRADER
            elif url == "backup":
                halo_url = const.HALO_URL_BACKUP
            else:
                raise ValueError("Token请求失败，请检查url入参。")
            self.token_url = halo_url + const.TOKEN_CREATE
            self.query_url = halo_url + const.QUERY
            self.command_url = halo_url + const.COMMAND
            self.batch_url = halo_url + const.BATCH
            self.workspace = const.WORKSPACE

        elif env == "UAT":
            halo_url = const.HALO_URL_UAT
            self.token_url = halo_url + const.TOKEN_CREATE
            self.query_url = halo_url + const.QUERY
            self.command_url = halo_url + const.COMMAND
            self.batch_url = halo_url + const.BATCH
            self.workspace = const.WORKSPACE
        elif env == "DEV":
            halo_url = const.HALO_URL_DEV
            self.token_url = halo_url + const.TOKEN_CREATE
            self.query_url = halo_url + const.QUERY
            self.command_url = halo_url + const.COMMAND
            self.batch_url = halo_url + const.BATCH
            self.workspace = const.WORKSPACE

        self.token = self.get_token()

    def get_token(self):
        """
        用于获取数据平台接口授权
        :return: 接口授权
        """
        token_params = {
            "username": self.username,
            "password": self.password,
            "workspace": self.workspace
        }
        token = requests.post(self.token_url, json=token_params, timeout=5)
        if "success" in token.json():
            if not token.json()["success"]:
                raise ConnectionError("请求失败，请检查用户名与密码。")
            else:
                access_token = token.json()["value"]["accessToken"]
        else:
            raise ConnectionError("请求失败，请检查网络环境。如果您的ip地址是10.255开头，请加入参数url=\"trader\"。"
                                  "其他情况请尝试加入参数url=\"backup\"")
        return access_token

    def get_query(self, query: str, **kwargs):
        """
        用于获取数据
        :param query: 查询接口名称
        :param kwargs: 用于自定义其他传参
            args: dict ->接口内部传参，存在部分参输必填的情况
            limit: int ->设置获取条数，sql接口默认返回10条，传参为limit=-1时返回全部
            offset: int ->跳过条数，默认不跳过
        :return: List[dict]
        """
        data = []
        query_params = {"code": query}
        query_params.update(kwargs)
        get_query = requests.post(self.query_url, headers={'Authorization': self.token}, json=query_params).json()
        if "success" in get_query:
            if not get_query["success"]:
                raise ConnectionRefusedError("请求失败，请检查入参，入参设置方式详见数据接口支持列表说明。")
        if "data" in get_query:
            data.extend(get_query["data"])
            return data
        if "value" in get_query:
            data.extend(get_query["value"])
        return data

    def submit_command(self, command: str, data: list, silent_mode=False):
        """

        :param silent_mode: 无通报模式
        :param data: 发送数据
        :param command: 触发指令
        :return:
        """
        command_params = {"code": command}
        for item in data:
            command_params.update({"args": item})
            sub = requests.post(self.command_url, headers={'Authorization': self.token}, json=command_params).json()

            if "success" in sub:
                if not sub["success"]:
                    raise ConnectionAbortedError(f"请求失败，请检查操作入参。\n失败条目：{item}\n备注：{sub.get('remarks')}")
                else:
                    if not silent_mode:
                        print(f"请求成功。\n入参：{item}\n请求结果：{sub.get('remarks')}")
            else:
                raise ConnectionError("请求失败，未知原因。")
        return True

    def batch_command(self, command: str, data: list, silent_mode=False):
        """

        :param silent_mode: 无通报模式
        :param data: 发送数据
        :param command: 触发指令
        :return:
        """
        command_params = {"code": command}
        command_params.update({"args": data})
        sub = requests.post(self.batch_url, headers={'Authorization': self.token}, json=command_params).json()

        if "success" in sub:
            if not sub["success"]:
                raise ConnectionAbortedError(f"请求失败，请检查操作入参。\n备注：{sub.get('remarks')} \n问题数据：{sub.get('failItems')}")
            else:
                if not silent_mode:
                    print("请求成功。")
        else:
            raise ConnectionError("请求失败，未知原因。")
        return True


if __name__ == '__main__':
    print("Hello world.")
