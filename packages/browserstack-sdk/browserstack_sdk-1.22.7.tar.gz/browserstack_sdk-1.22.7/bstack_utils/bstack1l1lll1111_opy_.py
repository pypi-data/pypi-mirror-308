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
import threading
import logging
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11l11l1_opy_
from bstack_utils.helper import bstack1l1lll11_opy_
logger = logging.getLogger(__name__)
def bstack1l111ll111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l11lll11_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1ll_opy_ (u"࠭ࡴࡢࡩࡶࠫအ"), [])
    bstack111l1ll1_opy_ = bstack1l11l11l1_opy_.bstack1111l1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack111l1ll1_opy_
    try:
      bstack11lllll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll111_opy_(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ဢ")) else context.browser
      if bstack11lllll1l1_opy_ and bstack11lllll1l1_opy_.session_id and bstack111l1ll1_opy_ and bstack1l1lll11_opy_(
              threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဣ"), None):
          threading.current_thread().isA11yTest = bstack1l11l11l1_opy_.bstack1l1l11111l_opy_(bstack11lllll1l1_opy_, bstack111l1ll1_opy_)
    except Exception as e:
       logger.debug(bstack1ll1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩဤ").format(str(e)))
def bstack1ll1ll111_opy_(bstack11lllll1l1_opy_):
    if bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧဥ"), None) and bstack1l1lll11_opy_(
      threading.current_thread(), bstack1ll1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪဦ"), None) and not bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨဧ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11l11l1_opy_.bstack11ll11lll_opy_(bstack11lllll1l1_opy_, name=bstack1ll1ll_opy_ (u"ࠨࠢဨ"), path=bstack1ll1ll_opy_ (u"ࠢࠣဩ"))