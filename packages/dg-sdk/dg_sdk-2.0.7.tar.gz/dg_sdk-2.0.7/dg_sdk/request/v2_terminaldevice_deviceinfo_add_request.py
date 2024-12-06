from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TERMINALDEVICE_DEVICEINFO_ADD



class V2TerminaldeviceDeviceinfoAddRequest(object):
    """
    新增终端报备
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 商户号
    huifu_id = ""

    def post(self, extend_infos):
        """
        新增终端报备

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id
        }
        required_params.update(extend_infos)
        return request_post(V2_TERMINALDEVICE_DEVICEINFO_ADD, required_params)
