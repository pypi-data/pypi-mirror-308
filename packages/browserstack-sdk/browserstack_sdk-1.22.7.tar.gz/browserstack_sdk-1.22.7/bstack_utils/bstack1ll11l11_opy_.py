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
import logging
import os
import threading
from bstack_utils.helper import bstack1ll111ll_opy_
from bstack_utils.constants import bstack111l11l1l1_opy_
logger = logging.getLogger(__name__)
class bstack1111llll_opy_:
    bstack1ll1ll1l1l1_opy_ = None
    @classmethod
    def bstack1ll11llll_opy_(cls):
        if cls.on():
            logger.info(
                bstack1ll1ll_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ៨").format(os.environ[bstack1ll1ll_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤ៩")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬ៪"), None) is None or os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭៫")] == bstack1ll1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ៬"):
            return False
        return True
    @classmethod
    def bstack1ll111lllll_opy_(cls, bs_config, framework=bstack1ll1ll_opy_ (u"ࠢࠣ៭")):
        if framework == bstack1ll1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ៮"):
            return bstack1ll111ll_opy_(bs_config.get(bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭៯")))
        bstack1ll111l1lll_opy_ = framework in bstack111l11l1l1_opy_
        return bstack1ll111ll_opy_(bs_config.get(bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ៰"), bstack1ll111l1lll_opy_))
    @classmethod
    def bstack1ll111ll11l_opy_(cls, framework):
        return framework in bstack111l11l1l1_opy_
    @classmethod
    def bstack1ll1l111l1l_opy_(cls, bs_config, framework):
        return cls.bstack1ll111lllll_opy_(bs_config, framework) is True and cls.bstack1ll111ll11l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ៱"), None)
    @staticmethod
    def bstack11ll111l11_opy_():
        if getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ៲"), None):
            return {
                bstack1ll1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫ៳"): bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࠬ៴"),
                bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៵"): getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭៶"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៷"), None):
            return {
                bstack1ll1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ៸"): bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ៹"),
                bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭៺"): getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ៻"), None)
            }
        return None
    @staticmethod
    def bstack1ll111ll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1111llll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1llll1l_opy_(test, hook_name=None):
        bstack1ll111lll11_opy_ = test.parent
        if hook_name in [bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭៼"), bstack1ll1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ៽"), bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ៾"), bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭៿")]:
            bstack1ll111lll11_opy_ = test
        scope = []
        while bstack1ll111lll11_opy_ is not None:
            scope.append(bstack1ll111lll11_opy_.name)
            bstack1ll111lll11_opy_ = bstack1ll111lll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll111ll111_opy_(hook_type):
        if hook_type == bstack1ll1ll_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥ᠀"):
            return bstack1ll1ll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥ᠁")
        elif hook_type == bstack1ll1ll_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦ᠂"):
            return bstack1ll1ll_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣ᠃")
    @staticmethod
    def bstack1ll111ll1l1_opy_(bstack1ll1lll111_opy_):
        try:
            if not bstack1111llll_opy_.on():
                return bstack1ll1lll111_opy_
            if os.environ.get(bstack1ll1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢ᠄"), None) == bstack1ll1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᠅"):
                tests = os.environ.get(bstack1ll1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣ᠆"), None)
                if tests is None or tests == bstack1ll1ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᠇"):
                    return bstack1ll1lll111_opy_
                bstack1ll1lll111_opy_ = tests.split(bstack1ll1ll_opy_ (u"࠭ࠬࠨ᠈"))
                return bstack1ll1lll111_opy_
        except Exception as exc:
            print(bstack1ll1ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣ᠉"), str(exc))
        return bstack1ll1lll111_opy_