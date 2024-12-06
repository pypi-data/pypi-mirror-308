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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack111l1llll1_opy_ as bstack111llll111_opy_
from bstack_utils.bstack1lll1l11l_opy_ import bstack1lll1l11l_opy_
from bstack_utils.helper import bstack1l1l11l11l_opy_, bstack11l11l11ll_opy_, bstack11111lll_opy_, bstack111lll1l11_opy_, bstack111ll11ll1_opy_, bstack1l111llll_opy_, get_host_info, bstack111lll1ll1_opy_, bstack1l1l111l1l_opy_, bstack11l1llllll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11l1llllll_opy_(class_method=False)
def _111ll1lll1_opy_(driver, bstack11l111ll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1ll_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪའ"): caps.get(bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩཡ"), None),
        bstack1ll1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨར"): bstack11l111ll11_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨལ"), None),
        bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬཤ"): caps.get(bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬཥ"), None),
        bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪས"): caps.get(bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪཧ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧཨ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཀྵ"), None) is None or os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪཪ")] == bstack1ll1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦཫ"):
        return False
    return True
def bstack111llll1l1_opy_(config):
  return config.get(bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧཬ"), False) or any([p.get(bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ཭"), False) == True for p in config.get(bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ཮"), [])])
def bstack1lllll1l1l_opy_(config, bstack1ll111l1_opy_):
  try:
    if not bstack11111lll_opy_(config):
      return False
    bstack111l1lllll_opy_ = config.get(bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ཯"), False)
    if int(bstack1ll111l1_opy_) < len(config.get(bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ཰"), [])) and config[bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཱ")][bstack1ll111l1_opy_]:
      bstack111lllll11_opy_ = config[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴིࠩ")][bstack1ll111l1_opy_].get(bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿཱིࠧ"), None)
    else:
      bstack111lllll11_opy_ = config.get(bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨུ"), None)
    if bstack111lllll11_opy_ != None:
      bstack111l1lllll_opy_ = bstack111lllll11_opy_
    bstack111ll1l111_opy_ = os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜ཱུ࡚ࠧ")) is not None and len(os.getenv(bstack1ll1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨྲྀ"))) > 0 and os.getenv(bstack1ll1ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཷ")) != bstack1ll1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪླྀ")
    return bstack111l1lllll_opy_ and bstack111ll1l111_opy_
  except Exception as error:
    logger.debug(bstack1ll1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ཹ") + str(error))
  return False
def bstack1111l1l1_opy_(test_tags):
  bstack111ll1111l_opy_ = os.getenv(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨེ"))
  if bstack111ll1111l_opy_ is None:
    return True
  bstack111ll1111l_opy_ = json.loads(bstack111ll1111l_opy_)
  try:
    include_tags = bstack111ll1111l_opy_[bstack1ll1ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪཻ࠭")] if bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ོࠧ") in bstack111ll1111l_opy_ and isinstance(bstack111ll1111l_opy_[bstack1ll1ll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨཽ")], list) else []
    exclude_tags = bstack111ll1111l_opy_[bstack1ll1ll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩཾ")] if bstack1ll1ll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪཿ") in bstack111ll1111l_opy_ and isinstance(bstack111ll1111l_opy_[bstack1ll1ll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨྀࠫ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ཱྀࠦࠢ") + str(error))
  return False
def bstack111ll1llll_opy_(config, bstack111ll11lll_opy_, bstack111ll11111_opy_, bstack111ll11l11_opy_):
  bstack111ll111l1_opy_ = bstack111lll1l11_opy_(config)
  bstack111ll1ll1l_opy_ = bstack111ll11ll1_opy_(config)
  if bstack111ll111l1_opy_ is None or bstack111ll1ll1l_opy_ is None:
    logger.error(bstack1ll1ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩྂ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪྃ"), bstack1ll1ll_opy_ (u"ࠪࡿࢂ྄࠭")))
    data = {
        bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ྅"): config[bstack1ll1ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ྆")],
        bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ྇"): config.get(bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪྈ"), os.path.basename(os.getcwd())),
        bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫྉ"): bstack1l1l11l11l_opy_(),
        bstack1ll1ll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧྊ"): config.get(bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ྋ"), bstack1ll1ll_opy_ (u"ࠫࠬྌ")),
        bstack1ll1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྍ"): {
            bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ྎ"): bstack111ll11lll_opy_,
            bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪྏ"): bstack111ll11111_opy_,
            bstack1ll1ll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬྐ"): __version__,
            bstack1ll1ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫྑ"): bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪྒ"),
            bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫྒྷ"): bstack1ll1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧྔ"),
            bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ྕ"): bstack111ll11l11_opy_
        },
        bstack1ll1ll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩྖ"): settings,
        bstack1ll1ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩྗ"): bstack111lll1ll1_opy_(),
        bstack1ll1ll_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ྘"): bstack1l111llll_opy_(),
        bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬྙ"): get_host_info(),
        bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ྚ"): bstack11111lll_opy_(config)
    }
    headers = {
        bstack1ll1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫྛ"): bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩྜ"),
    }
    config = {
        bstack1ll1ll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬྜྷ"): (bstack111ll111l1_opy_, bstack111ll1ll1l_opy_),
        bstack1ll1ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩྞ"): headers
    }
    response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧྟ"), bstack111llll111_opy_ + bstack1ll1ll_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪྠ"), data, config)
    bstack111lll11ll_opy_ = response.json()
    if bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬྡ")]:
      parsed = json.loads(os.getenv(bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ྡྷ"), bstack1ll1ll_opy_ (u"࠭ࡻࡾࠩྣ")))
      parsed[bstack1ll1ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྤ")] = bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ྥ")][bstack1ll1ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪྦ")]
      os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫྦྷ")] = json.dumps(parsed)
      bstack1lll1l11l_opy_.bstack111ll1l11l_opy_(bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠫࡩࡧࡴࡢࠩྨ")][bstack1ll1ll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ྩ")])
      bstack1lll1l11l_opy_.bstack111lll1l1l_opy_(bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫྪ")][bstack1ll1ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩྫ")])
      bstack1lll1l11l_opy_.store()
      return bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ྫྷ")][bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧྭ")], bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡨࡦࡺࡡࠨྮ")][bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧྯ")]
    else:
      logger.error(bstack1ll1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ྰ") + bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྱ")])
      if bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྲ")] == bstack1ll1ll_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪླ"):
        for bstack111lll111l_opy_ in bstack111lll11ll_opy_[bstack1ll1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩྴ")]:
          logger.error(bstack111lll111l_opy_[bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྵ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧྶ") +  str(error))
    return None, None
def bstack111ll1l1ll_opy_():
  if os.getenv(bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪྷ")) is None:
    return {
        bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྸ"): bstack1ll1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ྐྵ"),
        bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྺ"): bstack1ll1ll_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨྻ")
    }
  data = {bstack1ll1ll_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫྼ"): bstack1l1l11l11l_opy_()}
  headers = {
      bstack1ll1ll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ྽"): bstack1ll1ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭྾") + os.getenv(bstack1ll1ll_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ྿")),
      bstack1ll1ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭࿀"): bstack1ll1ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ࿁")
  }
  response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"ࠩࡓ࡙࡙࠭࿂"), bstack111llll111_opy_ + bstack1ll1ll_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬ࿃"), data, { bstack1ll1ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ࿄"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨ࿅") + bstack11l11l11ll_opy_().isoformat() + bstack1ll1ll_opy_ (u"࡚࠭ࠨ࿆"))
      return {bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿇"): bstack1ll1ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ࿈"), bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿉"): bstack1ll1ll_opy_ (u"ࠪࠫ࿊")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ࿋") + str(error))
    return {
        bstack1ll1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿌"): bstack1ll1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ࿍"),
        bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿎"): str(error)
    }
def bstack1l11l1l11_opy_(caps, options, desired_capabilities={}):
  try:
    bstack111lll11l1_opy_ = caps.get(bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿏"), {}).get(bstack1ll1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭࿐"), caps.get(bstack1ll1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ࿑"), bstack1ll1ll_opy_ (u"ࠫࠬ࿒")))
    if bstack111lll11l1_opy_:
      logger.warn(bstack1ll1ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ࿓"))
      return False
    if options:
      bstack111ll1ll11_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack111ll1ll11_opy_ = desired_capabilities
    else:
      bstack111ll1ll11_opy_ = {}
    browser = caps.get(bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ࿔"), bstack1ll1ll_opy_ (u"ࠧࠨ࿕")).lower() or bstack111ll1ll11_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭࿖"), bstack1ll1ll_opy_ (u"ࠩࠪ࿗")).lower()
    if browser != bstack1ll1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ࿘"):
      logger.warn(bstack1ll1ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ࿙"))
      return False
    browser_version = caps.get(bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿚")) or caps.get(bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ࿛")) or bstack111ll1ll11_opy_.get(bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࿜")) or bstack111ll1ll11_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿝"), {}).get(bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ࿞")) or bstack111ll1ll11_opy_.get(bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ࿟"), {}).get(bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࿠"))
    if browser_version and browser_version != bstack1ll1ll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ࿡") and int(browser_version.split(bstack1ll1ll_opy_ (u"࠭࠮ࠨ࿢"))[0]) <= 98:
      logger.warn(bstack1ll1ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧ࿣"))
      return False
    if not options:
      bstack111ll11l1l_opy_ = caps.get(bstack1ll1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭࿤")) or bstack111ll1ll11_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ࿥"), {})
      if bstack1ll1ll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ࿦") in bstack111ll11l1l_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿧"), []):
        logger.warn(bstack1ll1ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢ࿨"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1ll1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣ࿩") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack111lll1111_opy_ = config.get(bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ࿪"), {})
    bstack111lll1111_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ࿫")] = os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ࿬"))
    bstack111ll1l1l1_opy_ = json.loads(os.getenv(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ࿭"), bstack1ll1ll_opy_ (u"ࠫࢀࢃࠧ࿮"))).get(bstack1ll1ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿯"))
    caps[bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭࿰")] = True
    if bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ࿱") in caps:
      caps[bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿲")][bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࿳")] = bstack111lll1111_opy_
      caps[bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ࿴")][bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ࿵")][bstack1ll1ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿶")] = bstack111ll1l1l1_opy_
    else:
      caps[bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ࿷")] = bstack111lll1111_opy_
      caps[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭࿸")][bstack1ll1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ࿹")] = bstack111ll1l1l1_opy_
  except Exception as error:
    logger.debug(bstack1ll1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥ࿺") +  str(error))
def bstack1l1l11111l_opy_(driver, bstack111lll1lll_opy_):
  try:
    setattr(driver, bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ࿻"), True)
    session = driver.session_id
    if session:
      bstack111llll1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111llll1ll_opy_ = False
      bstack111llll1ll_opy_ = url.scheme in [bstack1ll1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࠤ࿼"), bstack1ll1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ࿽")]
      if bstack111llll1ll_opy_:
        if bstack111lll1lll_opy_:
          logger.info(bstack1ll1ll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨ࿾"))
      return bstack111lll1lll_opy_
  except Exception as e:
    logger.error(bstack1ll1ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ࿿") + str(e))
    return False
def bstack11ll11lll_opy_(driver, name, path):
  try:
    bstack111llll11l_opy_ = {
        bstack1ll1ll_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨက"): threading.current_thread().current_test_uuid,
        bstack1ll1ll_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧခ"): os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨဂ"), bstack1ll1ll_opy_ (u"ࠫࠬဃ")),
        bstack1ll1ll_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩင"): os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧစ"), bstack1ll1ll_opy_ (u"ࠧࠨဆ"))
    }
    logger.debug(bstack1ll1ll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫဇ"))
    logger.debug(driver.execute_async_script(bstack1lll1l11l_opy_.perform_scan, {bstack1ll1ll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤဈ"): name}))
    logger.debug(driver.execute_async_script(bstack1lll1l11l_opy_.bstack111ll111ll_opy_, bstack111llll11l_opy_))
    logger.info(bstack1ll1ll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨဉ"))
  except Exception as bstack111l1lll1l_opy_:
    logger.error(bstack1ll1ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨည") + str(path) + bstack1ll1ll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢဋ") + str(bstack111l1lll1l_opy_))