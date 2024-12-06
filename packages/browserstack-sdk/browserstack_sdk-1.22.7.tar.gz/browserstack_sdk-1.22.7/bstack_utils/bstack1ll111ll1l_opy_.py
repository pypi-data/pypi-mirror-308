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
from collections import deque
from bstack_utils.constants import *
class bstack1llllll1ll_opy_:
    def __init__(self):
        self._1lll11111ll_opy_ = deque()
        self._1lll111ll11_opy_ = {}
        self._1lll1111l11_opy_ = False
    def bstack1lll111llll_opy_(self, test_name, bstack1lll111l1ll_opy_):
        bstack1lll111l111_opy_ = self._1lll111ll11_opy_.get(test_name, {})
        return bstack1lll111l111_opy_.get(bstack1lll111l1ll_opy_, 0)
    def bstack1lll1111l1l_opy_(self, test_name, bstack1lll111l1ll_opy_):
        bstack1lll111lll1_opy_ = self.bstack1lll111llll_opy_(test_name, bstack1lll111l1ll_opy_)
        self.bstack1lll11l1111_opy_(test_name, bstack1lll111l1ll_opy_)
        return bstack1lll111lll1_opy_
    def bstack1lll11l1111_opy_(self, test_name, bstack1lll111l1ll_opy_):
        if test_name not in self._1lll111ll11_opy_:
            self._1lll111ll11_opy_[test_name] = {}
        bstack1lll111l111_opy_ = self._1lll111ll11_opy_[test_name]
        bstack1lll111lll1_opy_ = bstack1lll111l111_opy_.get(bstack1lll111l1ll_opy_, 0)
        bstack1lll111l111_opy_[bstack1lll111l1ll_opy_] = bstack1lll111lll1_opy_ + 1
    def bstack1l1l1l11_opy_(self, bstack1lll111l1l1_opy_, bstack1lll111l11l_opy_):
        bstack1lll111ll1l_opy_ = self.bstack1lll1111l1l_opy_(bstack1lll111l1l1_opy_, bstack1lll111l11l_opy_)
        event_name = bstack111l11l11l_opy_[bstack1lll111l11l_opy_]
        bstack1lll1111ll1_opy_ = bstack1ll1ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᗲ").format(bstack1lll111l1l1_opy_, event_name, bstack1lll111ll1l_opy_)
        self._1lll11111ll_opy_.append(bstack1lll1111ll1_opy_)
    def bstack1l11ll11l1_opy_(self):
        return len(self._1lll11111ll_opy_) == 0
    def bstack1l1l11111_opy_(self):
        bstack1lll1111lll_opy_ = self._1lll11111ll_opy_.popleft()
        return bstack1lll1111lll_opy_
    def capturing(self):
        return self._1lll1111l11_opy_
    def bstack1l1lll1l1_opy_(self):
        self._1lll1111l11_opy_ = True
    def bstack111l111l1_opy_(self):
        self._1lll1111l11_opy_ = False