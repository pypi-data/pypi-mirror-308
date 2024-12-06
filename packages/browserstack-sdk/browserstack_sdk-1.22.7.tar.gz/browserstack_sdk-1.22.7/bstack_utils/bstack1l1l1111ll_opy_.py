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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111lll1ll1_opy_, bstack1l111llll_opy_, get_host_info, bstack1111lll1l1_opy_, \
 bstack11111lll_opy_, bstack1l1lll11_opy_, bstack11l1llllll_opy_, bstack1111ll11l1_opy_, bstack1l1l11l11l_opy_
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11l11l1_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack1111llll_opy_
from bstack_utils.percy import bstack1ll1ll11l_opy_
from bstack_utils.config import Config
bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll1ll11l_opy_()
@bstack11l1llllll_opy_(class_method=False)
def bstack1ll11l1l11l_opy_(bs_config, bstack1ll1l1l1l1_opy_):
  try:
    data = {
        bstack1ll1ll_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪឪ"): bstack1ll1ll_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩឫ"),
        bstack1ll1ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫឬ"): bs_config.get(bstack1ll1ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫឭ"), bstack1ll1ll_opy_ (u"ࠧࠨឮ")),
        bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ឯ"): bs_config.get(bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬឰ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ឱ"): bs_config.get(bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ឲ")),
        bstack1ll1ll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪឳ"): bs_config.get(bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ឴"), bstack1ll1ll_opy_ (u"ࠧࠨ឵")),
        bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬា"): bstack1l1l11l11l_opy_(),
        bstack1ll1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧិ"): bstack1111lll1l1_opy_(bs_config),
        bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭ី"): get_host_info(),
        bstack1ll1ll_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬឹ"): bstack1l111llll_opy_(),
        bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬឺ"): os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬុ")),
        bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬូ"): os.environ.get(bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ួ"), False),
        bstack1ll1ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫើ"): bstack111lll1ll1_opy_(),
        bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪឿ"): bstack1ll111lll1l_opy_(),
        bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨៀ"): bstack1ll11l111ll_opy_(bstack1ll1l1l1l1_opy_),
        bstack1ll1ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪេ"): bstack1l11l11l1l_opy_(bs_config, bstack1ll1l1l1l1_opy_.get(bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧែ"), bstack1ll1ll_opy_ (u"ࠧࠨៃ"))),
        bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪោ"): bstack11111lll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥៅ").format(str(error)))
    return None
def bstack1ll11l111ll_opy_(framework):
  return {
    bstack1ll1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪំ"): framework.get(bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬះ"), bstack1ll1ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬៈ")),
    bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ៉"): framework.get(bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ៊")),
    bstack1ll1ll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ់"): framework.get(bstack1ll1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ៌")),
    bstack1ll1ll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ៍"): bstack1ll1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ៎"),
    bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ៏"): framework.get(bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭័"))
  }
def bstack1l11l11l1l_opy_(bs_config, framework):
  bstack1l111lllll_opy_ = False
  bstack1l111lll_opy_ = False
  bstack1ll11l11ll1_opy_ = False
  if bstack1ll1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ៑") in bs_config:
    bstack1ll11l11ll1_opy_ = True
  elif bstack1ll1ll_opy_ (u"ࠨࡣࡳࡴ្ࠬ") in bs_config:
    bstack1l111lllll_opy_ = True
  else:
    bstack1l111lll_opy_ = True
  bstack11l1l11ll_opy_ = {
    bstack1ll1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ៓"): bstack1111llll_opy_.bstack1ll111lllll_opy_(bs_config, framework),
    bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ។"): bstack1l11l11l1_opy_.bstack111llll1l1_opy_(bs_config),
    bstack1ll1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ៕"): bs_config.get(bstack1ll1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ៖"), False),
    bstack1ll1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨៗ"): bstack1l111lll_opy_,
    bstack1ll1ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭៘"): bstack1l111lllll_opy_,
    bstack1ll1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ៙"): bstack1ll11l11ll1_opy_
  }
  return bstack11l1l11ll_opy_
@bstack11l1llllll_opy_(class_method=False)
def bstack1ll111lll1l_opy_():
  try:
    bstack1ll11l11l11_opy_ = json.loads(os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ៚"), bstack1ll1ll_opy_ (u"ࠪࡿࢂ࠭៛")))
    return {
        bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ៜ"): bstack1ll11l11l11_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ៝").format(str(error)))
    return {}
def bstack1ll11llll1l_opy_(array, bstack1ll11l11111_opy_, bstack1ll11l11l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll11l11111_opy_]
    result[key] = o[bstack1ll11l11l1l_opy_]
  return result
def bstack1ll11ll11ll_opy_(bstack1111l11l1_opy_=bstack1ll1ll_opy_ (u"࠭ࠧ៞")):
  bstack1ll11l11lll_opy_ = bstack1l11l11l1_opy_.on()
  bstack1ll11l111l1_opy_ = bstack1111llll_opy_.on()
  bstack1ll111llll1_opy_ = percy.bstack1l1l11ll11_opy_()
  if bstack1ll111llll1_opy_ and not bstack1ll11l111l1_opy_ and not bstack1ll11l11lll_opy_:
    return bstack1111l11l1_opy_ not in [bstack1ll1ll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ៟"), bstack1ll1ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ០")]
  elif bstack1ll11l11lll_opy_ and not bstack1ll11l111l1_opy_:
    return bstack1111l11l1_opy_ not in [bstack1ll1ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ១"), bstack1ll1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ២"), bstack1ll1ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ៣")]
  return bstack1ll11l11lll_opy_ or bstack1ll11l111l1_opy_ or bstack1ll111llll1_opy_
@bstack11l1llllll_opy_(class_method=False)
def bstack1ll1l111111_opy_(bstack1111l11l1_opy_, test=None):
  bstack1ll11l1111l_opy_ = bstack1l11l11l1_opy_.on()
  if not bstack1ll11l1111l_opy_ or bstack1111l11l1_opy_ not in [bstack1ll1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ៤")] or test == None:
    return None
  return {
    bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭៥"): bstack1ll11l1111l_opy_ and bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭៦"), None) == True and bstack1l11l11l1_opy_.bstack1111l1l1_opy_(test[bstack1ll1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭៧")])
  }