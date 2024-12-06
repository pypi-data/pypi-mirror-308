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
from browserstack_sdk.bstack111l11l11_opy_ import bstack11lllll1_opy_
from browserstack_sdk.bstack11l1ll1l1l_opy_ import RobotHandler
def bstack1l11lllll_opy_(framework):
    if framework.lower() == bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬጔ"):
        return bstack11lllll1_opy_.version()
    elif framework.lower() == bstack1ll1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬጕ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ጖"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1ll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩ጗")