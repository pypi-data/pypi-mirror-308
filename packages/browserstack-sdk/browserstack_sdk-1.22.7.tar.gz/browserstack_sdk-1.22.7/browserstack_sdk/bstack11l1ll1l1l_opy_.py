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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l1111l11_opy_, bstack11l111111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1llll1l_opy_(bstack111lllllll_opy_):
        bstack111lllll1l_opy_ = []
        if bstack111lllllll_opy_:
            tokens = str(os.path.basename(bstack111lllllll_opy_)).split(bstack1ll1ll_opy_ (u"ࠦࡤࠨཛ"))
            camelcase_name = bstack1ll1ll_opy_ (u"ࠧࠦࠢཛྷ").join(t.title() for t in tokens)
            suite_name, bstack11l1111111_opy_ = os.path.splitext(camelcase_name)
            bstack111lllll1l_opy_.append(suite_name)
        return bstack111lllll1l_opy_
    @staticmethod
    def bstack111llllll1_opy_(typename):
        if bstack1ll1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤཝ") in typename:
            return bstack1ll1ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣཞ")
        return bstack1ll1ll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤཟ")