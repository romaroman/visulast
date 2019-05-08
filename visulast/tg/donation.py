import liqpay
from visulast.config import Configuration


liqpay = liqpay.LiqPay(Configuration().tokens.liqpay_public_test, Configuration().tokens.liqpay_private_test)

# TODO: implement extended payment proceeding requests