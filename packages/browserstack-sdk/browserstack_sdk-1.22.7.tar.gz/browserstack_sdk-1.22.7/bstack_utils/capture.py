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
import builtins
import logging
class bstack11ll11l1l1_opy_:
    def __init__(self, handler):
        self._111l1l11ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1l11l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ဪ"), bstack1ll1ll_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨါ"), bstack1ll1ll_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫာ"), bstack1ll1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪိ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1l1l1l_opy_
        self._111l1l1ll1_opy_()
    def _111l1l1l1l_opy_(self, *args, **kwargs):
        self._111l1l11ll_opy_(*args, **kwargs)
        message = bstack1ll1ll_opy_ (u"ࠬࠦࠧီ").join(map(str, args)) + bstack1ll1ll_opy_ (u"࠭࡜࡯ࠩု")
        self._log_message(bstack1ll1ll_opy_ (u"ࠧࡊࡐࡉࡓࠬူ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧေ"): level, bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဲ"): msg})
    def _111l1l1ll1_opy_(self):
        for level, bstack111l1l1l11_opy_ in self._111l1l11l1_opy_.items():
            setattr(logging, level, self._111l1l111l_opy_(level, bstack111l1l1l11_opy_))
    def _111l1l111l_opy_(self, level, bstack111l1l1l11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1l1l11_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1l11ll_opy_
        for level, bstack111l1l1l11_opy_ in self._111l1l11l1_opy_.items():
            setattr(logging, level, bstack111l1l1l11_opy_)