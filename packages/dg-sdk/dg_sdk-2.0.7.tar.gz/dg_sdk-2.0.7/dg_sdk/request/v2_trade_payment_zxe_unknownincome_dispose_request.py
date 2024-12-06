from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_TRADE_PAYMENT_ZXE_UNKNOWNINCOME_DISPOSE



class V2TradePaymentZxeUnknownincomeDisposeRequest(object):
    """
    不明来账处理
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 商户号
    huifu_id = ""
    # 银行侧交易流水号
    bank_serial_no = ""
    # 操作类型
    operate_type = ""

    def post(self, extend_infos):
        """
        不明来账处理

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "bank_serial_no":self.bank_serial_no,
            "operate_type":self.operate_type
        }
        required_params.update(extend_infos)
        return request_post(V2_TRADE_PAYMENT_ZXE_UNKNOWNINCOME_DISPOSE, required_params)
