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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11l11l1_opy_
from browserstack_sdk.bstack1lllllll1l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l111l1l_opy_
class bstack11lllll1_opy_:
    def __init__(self, args, logger, bstack11l1111l11_opy_, bstack11l111111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1lll111_opy_ = []
        self.bstack11l111l11l_opy_ = None
        self.bstack1l11111ll_opy_ = []
        self.bstack11l111l1ll_opy_ = self.bstack1l11lll1l_opy_()
        self.bstack1l1l1111l1_opy_ = -1
    def bstack1llll1l11_opy_(self, bstack11l11l111l_opy_):
        self.parse_args()
        self.bstack11l1111lll_opy_()
        self.bstack11l111l111_opy_(bstack11l11l111l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l11111l1_opy_():
        import importlib
        if getattr(importlib, bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬ༻"), False):
            bstack11l11l1111_opy_ = importlib.find_loader(bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ༼"))
        else:
            bstack11l11l1111_opy_ = importlib.util.find_spec(bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ༽"))
    def bstack11l1111ll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l1111l1_opy_ = -1
        if self.bstack11l111111l_opy_ and bstack1ll1ll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ༾") in self.bstack11l1111l11_opy_:
            self.bstack1l1l1111l1_opy_ = int(self.bstack11l1111l11_opy_[bstack1ll1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ༿")])
        try:
            bstack11l111lll1_opy_ = [bstack1ll1ll_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧཀ"), bstack1ll1ll_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩཁ"), bstack1ll1ll_opy_ (u"ࠧ࠮ࡲࠪག")]
            if self.bstack1l1l1111l1_opy_ >= 0:
                bstack11l111lll1_opy_.extend([bstack1ll1ll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩགྷ"), bstack1ll1ll_opy_ (u"ࠩ࠰ࡲࠬང")])
            for arg in bstack11l111lll1_opy_:
                self.bstack11l1111ll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1111lll_opy_(self):
        bstack11l111l11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l111l11l_opy_ = bstack11l111l11l_opy_
        return bstack11l111l11l_opy_
    def bstack111llll1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l11111l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l111l1l_opy_)
    def bstack11l111l111_opy_(self, bstack11l11l111l_opy_):
        bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
        if bstack11l11l111l_opy_:
            self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧཅ"))
            self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"࡙ࠫࡸࡵࡦࠩཆ"))
        if bstack1l1l1l1ll_opy_.bstack11l111llll_opy_():
            self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫཇ"))
            self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"࠭ࡔࡳࡷࡨࠫ཈"))
        self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠧ࠮ࡲࠪཉ"))
        self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ཊ"))
        self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫཋ"))
        self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪཌ"))
        if self.bstack1l1l1111l1_opy_ > 1:
            self.bstack11l111l11l_opy_.append(bstack1ll1ll_opy_ (u"ࠫ࠲ࡴࠧཌྷ"))
            self.bstack11l111l11l_opy_.append(str(self.bstack1l1l1111l1_opy_))
    def bstack11l111ll1l_opy_(self):
        bstack1l11111ll_opy_ = []
        for spec in self.bstack1ll1lll111_opy_:
            bstack1l1llll111_opy_ = [spec]
            bstack1l1llll111_opy_ += self.bstack11l111l11l_opy_
            bstack1l11111ll_opy_.append(bstack1l1llll111_opy_)
        self.bstack1l11111ll_opy_ = bstack1l11111ll_opy_
        return bstack1l11111ll_opy_
    def bstack1l11lll1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l111l1ll_opy_ = True
            return True
        except Exception as e:
            self.bstack11l111l1ll_opy_ = False
        return self.bstack11l111l1ll_opy_
    def bstack1ll1l11l1l_opy_(self, bstack11l1111l1l_opy_, bstack1llll1l11_opy_):
        bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬཎ")] = self.bstack11l1111l11_opy_
        multiprocessing.set_start_method(bstack1ll1ll_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬཏ"))
        bstack1ll1111ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1l1ll11_opy_ = manager.list()
        if bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪཐ") in self.bstack11l1111l11_opy_:
            for index, platform in enumerate(self.bstack11l1111l11_opy_[bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫད")]):
                bstack1ll1111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1111l1l_opy_,
                                                            args=(self.bstack11l111l11l_opy_, bstack1llll1l11_opy_, bstack1l1l1ll11_opy_)))
            bstack11l11111ll_opy_ = len(self.bstack11l1111l11_opy_[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬདྷ")])
        else:
            bstack1ll1111ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1111l1l_opy_,
                                                        args=(self.bstack11l111l11l_opy_, bstack1llll1l11_opy_, bstack1l1l1ll11_opy_)))
            bstack11l11111ll_opy_ = 1
        i = 0
        for t in bstack1ll1111ll_opy_:
            os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪན")] = str(i)
            if bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧཔ") in self.bstack11l1111l11_opy_:
                os.environ[bstack1ll1ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ཕ")] = json.dumps(self.bstack11l1111l11_opy_[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩབ")][i % bstack11l11111ll_opy_])
            i += 1
            t.start()
        for t in bstack1ll1111ll_opy_:
            t.join()
        return list(bstack1l1l1ll11_opy_)
    @staticmethod
    def bstack1l1l1111l_opy_(driver, bstack11l111ll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫབྷ"), None)
        if item and getattr(item, bstack1ll1ll_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪམ"), None) and not getattr(item, bstack1ll1ll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫཙ"), False):
            logger.info(
                bstack1ll1ll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤཚ"))
            bstack11l111l1l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11l11l1_opy_.bstack11ll11lll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)