# coding: UTF-8
import sys
bstack11111l1_opy_ = sys.version_info [0] == 2
bstack1llllll1_opy_ = 2048
bstack111l1_opy_ = 7
def bstack1ll1ll_opy_ (bstack1llll1_opy_):
    global bstack11lll11_opy_
    bstack1111l1l_opy_ = ord (bstack1llll1_opy_ [-1])
    bstack1ll1lll_opy_ = bstack1llll1_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1111l1l_opy_ % len (bstack1ll1lll_opy_)
    bstack1111l1_opy_ = bstack1ll1lll_opy_ [:bstack1l1llll_opy_] + bstack1ll1lll_opy_ [bstack1l1llll_opy_:]
    if bstack11111l1_opy_:
        bstack111l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llllll1_opy_ - (bstack11_opy_ + bstack1111l1l_opy_) % bstack111l1_opy_) for bstack11_opy_, char in enumerate (bstack1111l1_opy_)])
    else:
        bstack111l11l_opy_ = str () .join ([chr (ord (char) - bstack1llllll1_opy_ - (bstack11_opy_ + bstack1111l1l_opy_) % bstack111l1_opy_) for bstack11_opy_, char in enumerate (bstack1111l1_opy_)])
    return eval (bstack111l11l_opy_)
class bstack11llll11l1_opy_:
    def __init__(self, handler):
        self._1ll1ll11111_opy_ = None
        self.handler = handler
        self._1ll1l1llll1_opy_ = self.bstack1ll1ll1111l_opy_()
        self.patch()
    def patch(self):
        self._1ll1ll11111_opy_ = self._1ll1l1llll1_opy_.execute
        self._1ll1l1llll1_opy_.execute = self.bstack1ll1l1lllll_opy_()
    def bstack1ll1l1lllll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᙌ"), driver_command, None, this, args)
            response = self._1ll1ll11111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1ll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᙍ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1l1llll1_opy_.execute = self._1ll1ll11111_opy_
    @staticmethod
    def bstack1ll1ll1111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver