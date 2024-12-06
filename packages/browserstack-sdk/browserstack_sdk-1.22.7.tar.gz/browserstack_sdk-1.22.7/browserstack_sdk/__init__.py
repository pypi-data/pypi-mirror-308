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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack111l11l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll111ll1l_opy_ import bstack1llllll1ll_opy_
import time
import requests
def bstack11l11l1ll_opy_():
  global CONFIG
  headers = {
        bstack1ll1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l11l1l1l_opy_(CONFIG, bstack1ll1l11111_opy_)
  try:
    response = requests.get(bstack1ll1l11111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1l1l11l1_opy_ = response.json()[bstack1ll1ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l111l111l_opy_.format(response.json()))
      return bstack1l1l1l11l1_opy_
    else:
      logger.debug(bstack1llll11ll1_opy_.format(bstack1ll1ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1llll11ll1_opy_.format(e))
def bstack11l1l1ll1_opy_(hub_url):
  global CONFIG
  url = bstack1ll1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll1ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l11l1l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1111l1l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l11l1l1_opy_.format(hub_url, e))
def bstack11lll1l1l_opy_():
  try:
    global bstack1llll11111_opy_
    bstack1l1l1l11l1_opy_ = bstack11l11l1ll_opy_()
    bstack1ll1lll1l1_opy_ = []
    results = []
    for bstack1ll1l1l11_opy_ in bstack1l1l1l11l1_opy_:
      bstack1ll1lll1l1_opy_.append(bstack111111ll1_opy_(target=bstack11l1l1ll1_opy_,args=(bstack1ll1l1l11_opy_,)))
    for t in bstack1ll1lll1l1_opy_:
      t.start()
    for t in bstack1ll1lll1l1_opy_:
      results.append(t.join())
    bstack1lllll11l1_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll1ll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1ll1ll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1lllll11l1_opy_[hub_url] = latency
    bstack11l1ll1ll_opy_ = min(bstack1lllll11l1_opy_, key= lambda x: bstack1lllll11l1_opy_[x])
    bstack1llll11111_opy_ = bstack11l1ll1ll_opy_
    logger.debug(bstack1llll11l_opy_.format(bstack11l1ll1ll_opy_))
  except Exception as e:
    logger.debug(bstack1111l1ll1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack11ll1ll1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1ll1111ll1_opy_, bstack1l1l111l1l_opy_, bstack1l1l1lll1l_opy_, bstack1l1lll11_opy_, bstack11111lll_opy_, \
  Notset, bstack1l1ll11lll_opy_, \
  bstack1l11111ll1_opy_, bstack11l111l1l_opy_, bstack111l1111_opy_, bstack1l111llll_opy_, bstack1111l1l1l_opy_, bstack1lll11l1ll_opy_, \
  bstack1l1l11ll1_opy_, \
  bstack1lllllll1_opy_, bstack111lll111_opy_, bstack11111lll1_opy_, bstack1l1ll111l1_opy_, \
  bstack1ll11ll11_opy_, bstack1ll11l1lll_opy_, bstack1ll111ll_opy_, bstack1111ll11l_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack1l11lllll_opy_
from bstack_utils.bstack1l11l1ll1l_opy_ import bstack11llll11l1_opy_
from bstack_utils.bstack1l11l11l_opy_ import bstack11l1llll_opy_, bstack11l1111l_opy_
from bstack_utils.bstack1l111lll11_opy_ import bstack1llll1ll_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack1111llll_opy_
from bstack_utils.bstack1lll1l11l_opy_ import bstack1lll1l11l_opy_
from bstack_utils.proxy import bstack11llllll_opy_, bstack1l11l1l1l_opy_, bstack1llll111l1_opy_, bstack111lllll_opy_
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11l11l1_opy_
from browserstack_sdk.bstack111l11l11_opy_ import *
from browserstack_sdk.bstack1lllllll1l_opy_ import *
from bstack_utils.bstack11lll1l1l1_opy_ import bstack1ll1l1ll_opy_
from browserstack_sdk.bstack1l11ll11ll_opy_ import *
import requests
from bstack_utils.constants import *
def bstack1ll11l11l_opy_():
    global bstack1llll11111_opy_
    try:
        bstack1l1l1l1ll1_opy_ = bstack1l1111ll1l_opy_()
        bstack1111ll1l_opy_(bstack1l1l1l1ll1_opy_)
        hub_url = bstack1l1l1l1ll1_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1ll1ll_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1ll1ll_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1ll1ll_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1ll1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1llll11111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1111ll1l_opy_():
    global CONFIG
    bstack1l1lll111l_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1ll1ll_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1ll1ll_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l1lll111l_opy_, str):
        raise ValueError(bstack1ll1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l1l1l1ll1_opy_ = bstack1111lll1_opy_(bstack1l1lll111l_opy_)
        return bstack1l1l1l1ll1_opy_
    except Exception as e:
        logger.error(bstack1ll1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1111lll1_opy_(bstack1l1lll111l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1ll1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1ll1ll_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1lll1l1lll_opy_ + bstack1l1lll111l_opy_
        auth = (CONFIG[bstack1ll1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1ll1111l11_opy_ = json.loads(response.text)
            return bstack1ll1111l11_opy_
    except ValueError as ve:
        logger.error(bstack1ll1ll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1ll1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1111ll1l_opy_(bstack1ll1ll1lll_opy_):
    global CONFIG
    if bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1ll1ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1ll1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1ll1ll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1ll1ll1lll_opy_:
        bstack11l111111_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1ll1ll_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11l111111_opy_)
        bstack1ll111l1ll_opy_ = bstack1ll1ll1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11l1l1ll_opy_ = bstack1ll1ll_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1ll111l1ll_opy_)
        logger.debug(bstack1ll1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11l1l1ll_opy_)
        bstack1l1ll1ll11_opy_ = {
            bstack1ll1ll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1ll1ll_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1ll1ll_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1ll1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1ll1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11l1l1ll_opy_
        }
        bstack11l111111_opy_.update(bstack1l1ll1ll11_opy_)
        logger.debug(bstack1ll1ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11l111111_opy_)
        CONFIG[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11l111111_opy_
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1lllll111_opy_():
    bstack1l1l1l1ll1_opy_ = bstack1l1111ll1l_opy_()
    if not bstack1l1l1l1ll1_opy_[bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1ll1ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l1l1l1ll1_opy_[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1ll1ll_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
def bstack1l1l1l11ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1ll1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1ll1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1lllll1l11_opy_
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1ll1ll_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1ll1ll_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l111lll1l_opy_ = json.loads(response.text)
                bstack1l11l11l11_opy_ = bstack1l111lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l11l11l11_opy_:
                    bstack1l111ll1l_opy_ = bstack1l11l11l11_opy_[0]
                    bstack1l1ll1l11_opy_ = bstack1l111ll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11111111_opy_ = bstack1l1l11ll_opy_ + bstack1l1ll1l11_opy_
                    result.extend([bstack1l1ll1l11_opy_, bstack11111111_opy_])
                    logger.info(bstack1l111ll1ll_opy_.format(bstack11111111_opy_))
                    bstack1l1l1l1l_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l1l1l1l_opy_ += bstack1ll1ll_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l1l1l1l_opy_ != bstack1l111ll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l1l1l1111_opy_.format(bstack1l111ll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l1l1l1l_opy_))
                    return result
                else:
                    logger.debug(bstack1ll1ll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1ll1ll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1ll1ll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack1l1l1111ll_opy_ as bstack1ll1l111l1_opy_
import bstack_utils.bstack1l1lll1111_opy_ as bstack1ll1l1l1ll_opy_
bstack11l11111_opy_ = bstack1ll1ll_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࢹ")
bstack11l1l111l_opy_ = bstack1ll1ll_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࢺ")
from ._version import __version__
bstack11lll1llll_opy_ = None
CONFIG = {}
bstack1ll11l11ll_opy_ = {}
bstack1l11ll1l_opy_ = {}
bstack1lll11111_opy_ = None
bstack1l11ll1l11_opy_ = None
bstack1llll1lll_opy_ = None
bstack1l111l111_opy_ = -1
bstack1lll11lll1_opy_ = 0
bstack1l1llll11l_opy_ = bstack1l1l11l1_opy_
bstack11l11ll1l_opy_ = 1
bstack1l1111l1_opy_ = False
bstack11l1ll1l1_opy_ = False
bstack11lllllll_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪࢻ")
bstack11l1lll1l_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫࢼ")
bstack1l1111l11l_opy_ = False
bstack1llll111l_opy_ = True
bstack1lllll11_opy_ = bstack1ll1ll_opy_ (u"ࠫࠬࢽ")
bstack11llllll1_opy_ = []
bstack1llll11111_opy_ = bstack1ll1ll_opy_ (u"ࠬ࠭ࢾ")
bstack1lllll1111_opy_ = False
bstack1lllllllll_opy_ = None
bstack11l11l1l1_opy_ = None
bstack1l11llll_opy_ = None
bstack1lllll11ll_opy_ = -1
bstack1llllll1l_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"࠭ࡾࠨࢿ")), bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣀ"), bstack1ll1ll_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣁ"))
bstack1111lllll_opy_ = 0
bstack11ll1lll1_opy_ = 0
bstack1lll1111_opy_ = []
bstack1lll1l1l11_opy_ = []
bstack1lll1l111_opy_ = []
bstack1l1ll1l1_opy_ = []
bstack1lll11l11l_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪࣂ")
bstack1lll11l11_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫࣃ")
bstack1ll1llll11_opy_ = False
bstack111lll1l_opy_ = False
bstack1ll11llll1_opy_ = {}
bstack11111111l_opy_ = None
bstack1l11111l1_opy_ = None
bstack11111l11_opy_ = None
bstack11llll111l_opy_ = None
bstack1l1l111lll_opy_ = None
bstack1l11ll1l1l_opy_ = None
bstack11ll1l11_opy_ = None
bstack11111l1l1_opy_ = None
bstack1l1ll1ll1l_opy_ = None
bstack11ll111ll_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack1l11lll111_opy_ = None
bstack1l11llll1l_opy_ = None
bstack11lll11l11_opy_ = None
bstack11ll11l1l_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1llll11l1_opy_ = None
bstack111111l1_opy_ = None
bstack1l1111111_opy_ = None
bstack1111l111l_opy_ = None
bstack1lll11ll11_opy_ = None
bstack1l1l1lllll_opy_ = None
bstack1111111l1_opy_ = False
bstack1ll1ll1l1l_opy_ = bstack1ll1ll_opy_ (u"ࠦࠧࣄ")
logger = bstack11ll1ll1_opy_.get_logger(__name__, bstack1l1llll11l_opy_)
bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
percy = bstack1ll1ll11l_opy_()
bstack1ll1llllll_opy_ = bstack1llllll1ll_opy_()
bstack1ll1ll11ll_opy_ = bstack1l11ll11ll_opy_()
def bstack11lll1ll1l_opy_():
  global CONFIG
  global bstack1ll1llll11_opy_
  global bstack1l1l1l1ll_opy_
  bstack11lll111ll_opy_ = bstack1l1ll1l111_opy_(CONFIG)
  if bstack11111lll_opy_(CONFIG):
    if (bstack1ll1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࣅ") in bstack11lll111ll_opy_ and str(bstack11lll111ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣆ")]).lower() == bstack1ll1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬࣇ")):
      bstack1ll1llll11_opy_ = True
    bstack1l1l1l1ll_opy_.bstack1llll1l11l_opy_(bstack11lll111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬࣈ"), False))
  else:
    bstack1ll1llll11_opy_ = True
    bstack1l1l1l1ll_opy_.bstack1llll1l11l_opy_(True)
def bstack1lll1l11l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11llllll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1111l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1ll_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨࣉ") == args[i].lower() or bstack1ll1ll_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦ࣊") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lllll11_opy_
      bstack1lllll11_opy_ += bstack1ll1ll_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩ࣋") + path
      return path
  return None
bstack11lllll1l_opy_ = re.compile(bstack1ll1ll_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿ࠣ࣌"))
def bstack1l1l1111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11lllll1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll1ll_opy_ (u"ࠨࠤࡼࠤ࣍") + group + bstack1ll1ll_opy_ (u"ࠢࡾࠤ࣎"), os.environ.get(group))
  return value
def bstack11lll1l1_opy_():
  bstack1lll11111l_opy_ = bstack1111l1111_opy_()
  if bstack1lll11111l_opy_ and os.path.exists(os.path.abspath(bstack1lll11111l_opy_)):
    fileName = bstack1lll11111l_opy_
  if bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉ࣏ࠬ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࣐࠭")])) and not bstack1ll1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩ࣑ࠬ") in locals():
    fileName = os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")]
  if bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫࣓ࠧ") in locals():
    bstack1l11l11_opy_ = os.path.abspath(fileName)
  else:
    bstack1l11l11_opy_ = bstack1ll1ll_opy_ (u"࠭ࠧࣔ")
  bstack11lll1ll1_opy_ = os.getcwd()
  bstack1l111l1111_opy_ = bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣕ")
  bstack1lll1ll1l1_opy_ = bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣖ")
  while (not os.path.exists(bstack1l11l11_opy_)) and bstack11lll1ll1_opy_ != bstack1ll1ll_opy_ (u"ࠤࠥࣗ"):
    bstack1l11l11_opy_ = os.path.join(bstack11lll1ll1_opy_, bstack1l111l1111_opy_)
    if not os.path.exists(bstack1l11l11_opy_):
      bstack1l11l11_opy_ = os.path.join(bstack11lll1ll1_opy_, bstack1lll1ll1l1_opy_)
    if bstack11lll1ll1_opy_ != os.path.dirname(bstack11lll1ll1_opy_):
      bstack11lll1ll1_opy_ = os.path.dirname(bstack11lll1ll1_opy_)
    else:
      bstack11lll1ll1_opy_ = bstack1ll1ll_opy_ (u"ࠥࠦࣘ")
  if not os.path.exists(bstack1l11l11_opy_):
    bstack1llllll11l_opy_(
      bstack11lllll11l_opy_.format(os.getcwd()))
  try:
    with open(bstack1l11l11_opy_, bstack1ll1ll_opy_ (u"ࠫࡷ࠭ࣙ")) as stream:
      yaml.add_implicit_resolver(bstack1ll1ll_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣚ"), bstack11lllll1l_opy_)
      yaml.add_constructor(bstack1ll1ll_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࣛ"), bstack1l1l1111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l11l11_opy_, bstack1ll1ll_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1llllll11l_opy_(bstack1l11l1llll_opy_.format(str(exc)))
def bstack1l11111111_opy_(config):
  bstack1l1l111111_opy_ = bstack1llllll1l1_opy_(config)
  for option in list(bstack1l1l111111_opy_):
    if option.lower() in bstack1l1ll11ll1_opy_ and option != bstack1l1ll11ll1_opy_[option.lower()]:
      bstack1l1l111111_opy_[bstack1l1ll11ll1_opy_[option.lower()]] = bstack1l1l111111_opy_[option]
      del bstack1l1l111111_opy_[option]
  return config
def bstack11ll1lll_opy_():
  global bstack1l11ll1l_opy_
  for key, bstack1l11l1ll1_opy_ in bstack1ll11111l_opy_.items():
    if isinstance(bstack1l11l1ll1_opy_, list):
      for var in bstack1l11l1ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11ll1l_opy_[key] = os.environ[var]
          break
    elif bstack1l11l1ll1_opy_ in os.environ and os.environ[bstack1l11l1ll1_opy_] and str(os.environ[bstack1l11l1ll1_opy_]).strip():
      bstack1l11ll1l_opy_[key] = os.environ[bstack1l11l1ll1_opy_]
  if bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣝ") in os.environ:
    bstack1l11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣞ")] = {}
    bstack1l11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣟ")][bstack1ll1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")] = os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡")]
def bstack1lll1lllll_opy_():
  global bstack1ll11l11ll_opy_
  global bstack1lllll11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1ll1ll_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣢").lower() == val.lower():
      bstack1ll11l11ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")] = {}
      bstack1ll11l11ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣤ")][bstack1ll1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣥ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1ll11111_opy_ in bstack1l11l1l1ll_opy_.items():
    if isinstance(bstack1ll11111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1ll11111_opy_:
          if idx < len(sys.argv) and bstack1ll1ll_opy_ (u"ࠪ࠱࠲ࣦ࠭") + var.lower() == val.lower() and not key in bstack1ll11l11ll_opy_:
            bstack1ll11l11ll_opy_[key] = sys.argv[idx + 1]
            bstack1lllll11_opy_ += bstack1ll1ll_opy_ (u"ࠫࠥ࠳࠭ࠨࣧ") + var + bstack1ll1ll_opy_ (u"ࠬࠦࠧࣨ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1ll1ll_opy_ (u"࠭࠭࠮ࣩࠩ") + bstack1ll11111_opy_.lower() == val.lower() and not key in bstack1ll11l11ll_opy_:
          bstack1ll11l11ll_opy_[key] = sys.argv[idx + 1]
          bstack1lllll11_opy_ += bstack1ll1ll_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + bstack1ll11111_opy_ + bstack1ll1ll_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l111l1ll_opy_(config):
  bstack1l11l1111_opy_ = config.keys()
  for bstack1ll1111111_opy_, bstack11llll1ll1_opy_ in bstack11lll11111_opy_.items():
    if bstack11llll1ll1_opy_ in bstack1l11l1111_opy_:
      config[bstack1ll1111111_opy_] = config[bstack11llll1ll1_opy_]
      del config[bstack11llll1ll1_opy_]
  for bstack1ll1111111_opy_, bstack11llll1ll1_opy_ in bstack1l11llll11_opy_.items():
    if isinstance(bstack11llll1ll1_opy_, list):
      for bstack1l111ll11_opy_ in bstack11llll1ll1_opy_:
        if bstack1l111ll11_opy_ in bstack1l11l1111_opy_:
          config[bstack1ll1111111_opy_] = config[bstack1l111ll11_opy_]
          del config[bstack1l111ll11_opy_]
          break
    elif bstack11llll1ll1_opy_ in bstack1l11l1111_opy_:
      config[bstack1ll1111111_opy_] = config[bstack11llll1ll1_opy_]
      del config[bstack11llll1ll1_opy_]
  for bstack1l111ll11_opy_ in list(config):
    for bstack1l11l111ll_opy_ in bstack111ll1ll1_opy_:
      if bstack1l111ll11_opy_.lower() == bstack1l11l111ll_opy_.lower() and bstack1l111ll11_opy_ != bstack1l11l111ll_opy_:
        config[bstack1l11l111ll_opy_] = config[bstack1l111ll11_opy_]
        del config[bstack1l111ll11_opy_]
  bstack1llll1l111_opy_ = [{}]
  if not config.get(bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࣬")):
    config[bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࣭࠭")] = [{}]
  bstack1llll1l111_opy_ = config[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ࣮ࠧ")]
  for platform in bstack1llll1l111_opy_:
    for bstack1l111ll11_opy_ in list(platform):
      for bstack1l11l111ll_opy_ in bstack111ll1ll1_opy_:
        if bstack1l111ll11_opy_.lower() == bstack1l11l111ll_opy_.lower() and bstack1l111ll11_opy_ != bstack1l11l111ll_opy_:
          platform[bstack1l11l111ll_opy_] = platform[bstack1l111ll11_opy_]
          del platform[bstack1l111ll11_opy_]
  for bstack1ll1111111_opy_, bstack11llll1ll1_opy_ in bstack1l11llll11_opy_.items():
    for platform in bstack1llll1l111_opy_:
      if isinstance(bstack11llll1ll1_opy_, list):
        for bstack1l111ll11_opy_ in bstack11llll1ll1_opy_:
          if bstack1l111ll11_opy_ in platform:
            platform[bstack1ll1111111_opy_] = platform[bstack1l111ll11_opy_]
            del platform[bstack1l111ll11_opy_]
            break
      elif bstack11llll1ll1_opy_ in platform:
        platform[bstack1ll1111111_opy_] = platform[bstack11llll1ll1_opy_]
        del platform[bstack11llll1ll1_opy_]
  for bstack1lll111ll1_opy_ in bstack1l111ll11l_opy_:
    if bstack1lll111ll1_opy_ in config:
      if not bstack1l111ll11l_opy_[bstack1lll111ll1_opy_] in config:
        config[bstack1l111ll11l_opy_[bstack1lll111ll1_opy_]] = {}
      config[bstack1l111ll11l_opy_[bstack1lll111ll1_opy_]].update(config[bstack1lll111ll1_opy_])
      del config[bstack1lll111ll1_opy_]
  for platform in bstack1llll1l111_opy_:
    for bstack1lll111ll1_opy_ in bstack1l111ll11l_opy_:
      if bstack1lll111ll1_opy_ in list(platform):
        if not bstack1l111ll11l_opy_[bstack1lll111ll1_opy_] in platform:
          platform[bstack1l111ll11l_opy_[bstack1lll111ll1_opy_]] = {}
        platform[bstack1l111ll11l_opy_[bstack1lll111ll1_opy_]].update(platform[bstack1lll111ll1_opy_])
        del platform[bstack1lll111ll1_opy_]
  config = bstack1l11111111_opy_(config)
  return config
def bstack1l11l111_opy_(config):
  global bstack11l1lll1l_opy_
  bstack1l1ll1l1l1_opy_ = False
  if bstack1ll1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦ࣯ࠩ") in config and str(config[bstack1ll1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࣰࠪ")]).lower() != bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪࣱ࠭"):
    if bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࣲࠬ") not in config or str(config[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ࣳ")]).lower() == bstack1ll1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
      config[bstack1ll1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࣵ")] = False
    else:
      bstack1l1l1l1ll1_opy_ = bstack1l1111ll1l_opy_()
      if bstack1ll1ll_opy_ (u"ࠬ࡯ࡳࡕࡴ࡬ࡥࡱࡍࡲࡪࡦࣶࠪ") in bstack1l1l1l1ll1_opy_:
        if not bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࣷ") in config:
          config[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣸ")] = {}
        config[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣹࠬ")][bstack1ll1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣺࠫ")] = bstack1ll1ll_opy_ (u"ࠪࡥࡹࡹ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩࣻ")
        bstack1l1ll1l1l1_opy_ = True
        bstack11l1lll1l_opy_ = config[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")].get(bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ"))
  if bstack11111lll_opy_(config) and bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣾ") in config and str(config[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ")]).lower() != bstack1ll1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ") and not bstack1l1ll1l1l1_opy_:
    if not bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
      config[bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
    if not config[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")].get(bstack1ll1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩऄ")) and not bstack1ll1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨअ") in config[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")]:
      bstack1l1l11l11l_opy_ = datetime.datetime.now()
      bstack111llll1_opy_ = bstack1l1l11l11l_opy_.strftime(bstack1ll1ll_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬइ"))
      hostname = socket.gethostname()
      bstack111l1ll1l_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪई").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1ll_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬउ").format(bstack111llll1_opy_, hostname, bstack111l1ll1l_opy_)
      config[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")][bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऋ")] = identifier
    bstack11l1lll1l_opy_ = config[bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack1ll1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  return config
def bstack1ll1lll1ll_opy_():
  bstack11l1l1l1l_opy_ =  bstack1l111llll_opy_()[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠧऎ")]
  return bstack11l1l1l1l_opy_ if bstack11l1l1l1l_opy_ else -1
def bstack1ll1lllll1_opy_(bstack11l1l1l1l_opy_):
  global CONFIG
  if not bstack1ll1ll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫए") in CONFIG[bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ")]:
    return
  CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ")] = CONFIG[bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ")].replace(
    bstack1ll1ll_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ"),
    str(bstack11l1l1l1l_opy_)
  )
def bstack1ll1lll1l_opy_():
  global CONFIG
  if not bstack1ll1ll_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭औ") in CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")]:
    return
  bstack1l1l11l11l_opy_ = datetime.datetime.now()
  bstack111llll1_opy_ = bstack1l1l11l11l_opy_.strftime(bstack1ll1ll_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧख"))
  CONFIG[bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग")] = CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")].replace(
    bstack1ll1ll_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫङ"),
    bstack111llll1_opy_
  )
def bstack1lll111ll_opy_():
  global CONFIG
  if bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच") in CONFIG and not bool(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")]):
    del CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")]
    return
  if not bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG:
    CONFIG[bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = bstack1ll1ll_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧट")
  if bstack1ll1ll_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫठ") in CONFIG[bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")]:
    bstack1ll1lll1l_opy_()
    os.environ[bstack1ll1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫढ")] = CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण")]
  if not bstack1ll1ll_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫत") in CONFIG[bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    return
  bstack11l1l1l1l_opy_ = bstack1ll1ll_opy_ (u"ࠫࠬद")
  bstack1llll1lll1_opy_ = bstack1ll1lll1ll_opy_()
  if bstack1llll1lll1_opy_ != -1:
    bstack11l1l1l1l_opy_ = bstack1ll1ll_opy_ (u"ࠬࡉࡉࠡࠩध") + str(bstack1llll1lll1_opy_)
  if bstack11l1l1l1l_opy_ == bstack1ll1ll_opy_ (u"࠭ࠧन"):
    bstack1l1lll1ll_opy_ = bstack11lll1lll_opy_(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪऩ")])
    if bstack1l1lll1ll_opy_ != -1:
      bstack11l1l1l1l_opy_ = str(bstack1l1lll1ll_opy_)
  if bstack11l1l1l1l_opy_:
    bstack1ll1lllll1_opy_(bstack11l1l1l1l_opy_)
    os.environ[bstack1ll1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬप")] = CONFIG[bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
def bstack1l1lllll11_opy_(bstack1llll1111l_opy_, bstack111lll1ll_opy_, path):
  bstack1l1ll1lll1_opy_ = {
    bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧब"): bstack111lll1ll_opy_
  }
  if os.path.exists(path):
    bstack1lll1l11_opy_ = json.load(open(path, bstack1ll1ll_opy_ (u"ࠫࡷࡨࠧभ")))
  else:
    bstack1lll1l11_opy_ = {}
  bstack1lll1l11_opy_[bstack1llll1111l_opy_] = bstack1l1ll1lll1_opy_
  with open(path, bstack1ll1ll_opy_ (u"ࠧࡽࠫࠣम")) as outfile:
    json.dump(bstack1lll1l11_opy_, outfile)
def bstack11lll1lll_opy_(bstack1llll1111l_opy_):
  bstack1llll1111l_opy_ = str(bstack1llll1111l_opy_)
  bstack1l11l1l11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"࠭ࡾࠨय")), bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧर"))
  try:
    if not os.path.exists(bstack1l11l1l11l_opy_):
      os.makedirs(bstack1l11l1l11l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠨࢀࠪऱ")), bstack1ll1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩल"), bstack1ll1ll_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬळ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1ll_opy_ (u"ࠫࡼ࠭ऴ")):
        pass
      with open(file_path, bstack1ll1ll_opy_ (u"ࠧࡽࠫࠣव")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1ll_opy_ (u"࠭ࡲࠨश")) as bstack11llll11_opy_:
      bstack1111ll1l1_opy_ = json.load(bstack11llll11_opy_)
    if bstack1llll1111l_opy_ in bstack1111ll1l1_opy_:
      bstack1l1l11lll_opy_ = bstack1111ll1l1_opy_[bstack1llll1111l_opy_][bstack1ll1ll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫष")]
      bstack1lll1llll_opy_ = int(bstack1l1l11lll_opy_) + 1
      bstack1l1lllll11_opy_(bstack1llll1111l_opy_, bstack1lll1llll_opy_, file_path)
      return bstack1lll1llll_opy_
    else:
      bstack1l1lllll11_opy_(bstack1llll1111l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1111l1_opy_.format(str(e)))
    return -1
def bstack1l111lll1_opy_(config):
  if not config[bstack1ll1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪस")] or not config[bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬह")]:
    return True
  else:
    return False
def bstack1111ll111_opy_(config, index=0):
  global bstack1l1111l11l_opy_
  bstack11l1llll1_opy_ = {}
  caps = bstack1ll1l1ll1l_opy_ + bstack1ll1l1ll11_opy_
  if config.get(bstack1ll1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧऺ"), False):
    bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨऻ")] = True
    bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")] = config.get(bstack1ll1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪऽ"), {})
  if bstack1l1111l11l_opy_:
    caps += bstack1ll111l1l1_opy_
  for key in config:
    if key in caps + [bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪा")]:
      continue
    bstack11l1llll1_opy_[key] = config[key]
  if bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫि") in config:
    for bstack1ll11l1ll1_opy_ in config[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬी")][index]:
      if bstack1ll11l1ll1_opy_ in caps:
        continue
      bstack11l1llll1_opy_[bstack1ll11l1ll1_opy_] = config[bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")][index][bstack1ll11l1ll1_opy_]
  bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ू")] = socket.gethostname()
  if bstack1ll1ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ृ") in bstack11l1llll1_opy_:
    del (bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧॄ")])
  return bstack11l1llll1_opy_
def bstack1lll11l1l_opy_(config):
  global bstack1l1111l11l_opy_
  bstack11l11lll1_opy_ = {}
  caps = bstack1ll1l1ll11_opy_
  if bstack1l1111l11l_opy_:
    caps += bstack1ll111l1l1_opy_
  for key in caps:
    if key in config:
      bstack11l11lll1_opy_[key] = config[key]
  return bstack11l11lll1_opy_
def bstack1l1lll11ll_opy_(bstack11l1llll1_opy_, bstack11l11lll1_opy_):
  bstack11111l11l_opy_ = {}
  for key in bstack11l1llll1_opy_.keys():
    if key in bstack11lll11111_opy_:
      bstack11111l11l_opy_[bstack11lll11111_opy_[key]] = bstack11l1llll1_opy_[key]
    else:
      bstack11111l11l_opy_[key] = bstack11l1llll1_opy_[key]
  for key in bstack11l11lll1_opy_:
    if key in bstack11lll11111_opy_:
      bstack11111l11l_opy_[bstack11lll11111_opy_[key]] = bstack11l11lll1_opy_[key]
    else:
      bstack11111l11l_opy_[key] = bstack11l11lll1_opy_[key]
  return bstack11111l11l_opy_
def bstack1llll1111_opy_(config, index=0):
  global bstack1l1111l11l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11llllllll_opy_ = bstack1ll1111ll1_opy_(bstack1l11ll1ll1_opy_, config, logger)
  bstack11l11lll1_opy_ = bstack1lll11l1l_opy_(config)
  bstack1l1ll11l11_opy_ = bstack1ll1l1ll11_opy_
  bstack1l1ll11l11_opy_ += bstack11l111l1_opy_
  bstack11l11lll1_opy_ = update(bstack11l11lll1_opy_, bstack11llllllll_opy_)
  if bstack1l1111l11l_opy_:
    bstack1l1ll11l11_opy_ += bstack1ll111l1l1_opy_
  if bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ") in config:
    if bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॆ") in config[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")][index]:
      caps[bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨै")] = config[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index][bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ")]
    if bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧो") in config[bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index]:
      caps[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯्ࠩ")] = str(config[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ")])
    bstack1l1llll11_opy_ = bstack1ll1111ll1_opy_(bstack1l11ll1ll1_opy_, config[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index], logger)
    bstack1l1ll11l11_opy_ += list(bstack1l1llll11_opy_.keys())
    for bstack1l1l11lll1_opy_ in bstack1l1ll11l11_opy_:
      if bstack1l1l11lll1_opy_ in config[bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
        if bstack1l1l11lll1_opy_ == bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॒"):
          try:
            bstack1l1llll11_opy_[bstack1l1l11lll1_opy_] = str(config[bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1l1l11lll1_opy_] * 1.0)
          except:
            bstack1l1llll11_opy_[bstack1l1l11lll1_opy_] = str(config[bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index][bstack1l1l11lll1_opy_])
        else:
          bstack1l1llll11_opy_[bstack1l1l11lll1_opy_] = config[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index][bstack1l1l11lll1_opy_]
        del (config[bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l1l11lll1_opy_])
    bstack11l11lll1_opy_ = update(bstack11l11lll1_opy_, bstack1l1llll11_opy_)
  bstack11l1llll1_opy_ = bstack1111ll111_opy_(config, index)
  for bstack1l111ll11_opy_ in bstack1ll1l1ll11_opy_ + list(bstack11llllllll_opy_.keys()):
    if bstack1l111ll11_opy_ in bstack11l1llll1_opy_:
      bstack11l11lll1_opy_[bstack1l111ll11_opy_] = bstack11l1llll1_opy_[bstack1l111ll11_opy_]
      del (bstack11l1llll1_opy_[bstack1l111ll11_opy_])
  if bstack1l1ll11lll_opy_(config):
    bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫॗ")] = True
    caps.update(bstack11l11lll1_opy_)
    caps[bstack1ll1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭क़")] = bstack11l1llll1_opy_
  else:
    bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ख़")] = False
    caps.update(bstack1l1lll11ll_opy_(bstack11l1llll1_opy_, bstack11l11lll1_opy_))
    if bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬग़") in caps:
      caps[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩज़")] = caps[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")]
      del (caps[bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")])
    if bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़") in caps:
      caps[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧय़")] = caps[bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧॠ")]
      del (caps[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ")])
  return caps
def bstack1l1lll1lll_opy_():
  global bstack1llll11111_opy_
  global CONFIG
  if bstack1l11llllll_opy_() <= version.parse(bstack1ll1ll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨॢ")):
    if bstack1llll11111_opy_ != bstack1ll1ll_opy_ (u"ࠩࠪॣ"):
      return bstack1ll1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ।") + bstack1llll11111_opy_ + bstack1ll1ll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ॥")
    return bstack1l11ll11l_opy_
  if bstack1llll11111_opy_ != bstack1ll1ll_opy_ (u"ࠬ࠭०"):
    return bstack1ll1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ१") + bstack1llll11111_opy_ + bstack1ll1ll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ२")
  return bstack1ll11l1l1l_opy_
def bstack1lll1lll1l_opy_(options):
  return hasattr(options, bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ३"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11lll1_opy_(options, bstack1ll11111l1_opy_):
  for bstack1l1111ll11_opy_ in bstack1ll11111l1_opy_:
    if bstack1l1111ll11_opy_ in [bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ४"), bstack1ll1ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ५")]:
      continue
    if bstack1l1111ll11_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1111ll11_opy_] = update(options._experimental_options[bstack1l1111ll11_opy_],
                                                         bstack1ll11111l1_opy_[bstack1l1111ll11_opy_])
    else:
      options.add_experimental_option(bstack1l1111ll11_opy_, bstack1ll11111l1_opy_[bstack1l1111ll11_opy_])
  if bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ६") in bstack1ll11111l1_opy_:
    for arg in bstack1ll11111l1_opy_[bstack1ll1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪ७")]:
      options.add_argument(arg)
    del (bstack1ll11111l1_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫ८")])
  if bstack1ll1ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९") in bstack1ll11111l1_opy_:
    for ext in bstack1ll11111l1_opy_[bstack1ll1ll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ॰")]:
      options.add_extension(ext)
    del (bstack1ll11111l1_opy_[bstack1ll1ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॱ")])
def bstack111l1l1l1_opy_(options, bstack111l1l1l_opy_):
  if bstack1ll1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॲ") in bstack111l1l1l_opy_:
    for bstack111l1l111_opy_ in bstack111l1l1l_opy_[bstack1ll1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪॳ")]:
      if bstack111l1l111_opy_ in options._preferences:
        options._preferences[bstack111l1l111_opy_] = update(options._preferences[bstack111l1l111_opy_], bstack111l1l1l_opy_[bstack1ll1ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॴ")][bstack111l1l111_opy_])
      else:
        options.set_preference(bstack111l1l111_opy_, bstack111l1l1l_opy_[bstack1ll1ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ")][bstack111l1l111_opy_])
  if bstack1ll1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack111l1l1l_opy_:
    for arg in bstack111l1l1l_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
def bstack1ll1l11l_opy_(options, bstack1l1llll1l1_opy_):
  if bstack1ll1ll_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪॸ") in bstack1l1llll1l1_opy_:
    options.use_webview(bool(bstack1l1llll1l1_opy_[bstack1ll1ll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫॹ")]))
  bstack1l11lll1_opy_(options, bstack1l1llll1l1_opy_)
def bstack1ll11111ll_opy_(options, bstack11ll1ll1l_opy_):
  for bstack1ll111l111_opy_ in bstack11ll1ll1l_opy_:
    if bstack1ll111l111_opy_ in [bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨॺ"), bstack1ll1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      continue
    options.set_capability(bstack1ll111l111_opy_, bstack11ll1ll1l_opy_[bstack1ll111l111_opy_])
  if bstack1ll1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack11ll1ll1l_opy_:
    for arg in bstack11ll1ll1l_opy_[bstack1ll1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
  if bstack1ll1ll_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ") in bstack11ll1ll1l_opy_:
    options.bstack11lll111l_opy_(bool(bstack11ll1ll1l_opy_[bstack1ll1ll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ॿ")]))
def bstack111l1lll_opy_(options, bstack1lllllll11_opy_):
  for bstack1lllll111l_opy_ in bstack1lllllll11_opy_:
    if bstack1lllll111l_opy_ in [bstack1ll1ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧঀ"), bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      continue
    options._options[bstack1lllll111l_opy_] = bstack1lllllll11_opy_[bstack1lllll111l_opy_]
  if bstack1ll1ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩং") in bstack1lllllll11_opy_:
    for bstack111l1l1ll_opy_ in bstack1lllllll11_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ")]:
      options.bstack1ll11l1l11_opy_(
        bstack111l1l1ll_opy_, bstack1lllllll11_opy_[bstack1ll1ll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄")][bstack111l1l1ll_opy_])
  if bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack1lllllll11_opy_:
    for arg in bstack1lllllll11_opy_[bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
def bstack1lllll1lll_opy_(options, caps):
  if not hasattr(options, bstack1ll1ll_opy_ (u"ࠪࡏࡊ࡟ࠧই")):
    return
  if options.KEY == bstack1ll1ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঈ") and options.KEY in caps:
    bstack1l11lll1_opy_(options, caps[bstack1ll1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪউ")])
  elif options.KEY == bstack1ll1ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঊ") and options.KEY in caps:
    bstack111l1l1l1_opy_(options, caps[bstack1ll1ll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঋ")])
  elif options.KEY == bstack1ll1ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঌ") and options.KEY in caps:
    bstack1ll11111ll_opy_(options, caps[bstack1ll1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঍")])
  elif options.KEY == bstack1ll1ll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ঎") and options.KEY in caps:
    bstack1ll1l11l_opy_(options, caps[bstack1ll1ll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬএ")])
  elif options.KEY == bstack1ll1ll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঐ") and options.KEY in caps:
    bstack111l1lll_opy_(options, caps[bstack1ll1ll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ঑")])
def bstack11ll11ll_opy_(caps):
  global bstack1l1111l11l_opy_
  if isinstance(os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ঒")), str):
    bstack1l1111l11l_opy_ = eval(os.getenv(bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩও")))
  if bstack1l1111l11l_opy_:
    if bstack1lll1l11l1_opy_() < version.parse(bstack1ll1ll_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঔ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪক")
    if bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ") in caps:
      browser = caps[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ")]
    elif bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧঘ") in caps:
      browser = caps[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨঙ")]
    browser = str(browser).lower()
    if browser == bstack1ll1ll_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨচ") or browser == bstack1ll1ll_opy_ (u"ࠩ࡬ࡴࡦࡪࠧছ"):
      browser = bstack1ll1ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪজ")
    if browser == bstack1ll1ll_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬঝ"):
      browser = bstack1ll1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬঞ")
    if browser not in [bstack1ll1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট"), bstack1ll1ll_opy_ (u"ࠧࡦࡦࡪࡩࠬঠ"), bstack1ll1ll_opy_ (u"ࠨ࡫ࡨࠫড"), bstack1ll1ll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩঢ"), bstack1ll1ll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫণ")]:
      return None
    try:
      package = bstack1ll1ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ত").format(browser)
      name = bstack1ll1ll_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll1lll1l_opy_(options):
        return None
      for bstack1l111ll11_opy_ in caps.keys():
        options.set_capability(bstack1l111ll11_opy_, caps[bstack1l111ll11_opy_])
      bstack1lllll1lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll1l1_opy_(options, bstack1ll1llll1l_opy_):
  if not bstack1lll1lll1l_opy_(options):
    return
  for bstack1l111ll11_opy_ in bstack1ll1llll1l_opy_.keys():
    if bstack1l111ll11_opy_ in bstack11l111l1_opy_:
      continue
    if bstack1l111ll11_opy_ in options._caps and type(options._caps[bstack1l111ll11_opy_]) in [dict, list]:
      options._caps[bstack1l111ll11_opy_] = update(options._caps[bstack1l111ll11_opy_], bstack1ll1llll1l_opy_[bstack1l111ll11_opy_])
    else:
      options.set_capability(bstack1l111ll11_opy_, bstack1ll1llll1l_opy_[bstack1l111ll11_opy_])
  bstack1lllll1lll_opy_(options, bstack1ll1llll1l_opy_)
  if bstack1ll1ll_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬদ") in options._caps:
    if options._caps[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬধ")] and options._caps[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ন")].lower() != bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ঩"):
      del options._caps[bstack1ll1ll_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ")]
def bstack11llllll1l_opy_(proxy_config):
  if bstack1ll1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨফ") in proxy_config:
    proxy_config[bstack1ll1ll_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧব")] = proxy_config[bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪভ")]
    del (proxy_config[bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম")])
  if bstack1ll1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫয") in proxy_config and proxy_config[bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬর")].lower() != bstack1ll1ll_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ঱"):
    proxy_config[bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল")] = bstack1ll1ll_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬ঳")
  if bstack1ll1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ঴") in proxy_config:
    proxy_config[bstack1ll1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack1ll1ll_opy_ (u"ࠨࡲࡤࡧࠬশ")
  return proxy_config
def bstack1lll1ll11l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨষ") in config:
    return proxy
  config[bstack1ll1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩস")] = bstack11llllll1l_opy_(config[bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪহ")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺")])
  return proxy
def bstack1l1ll11ll_opy_(self):
  global CONFIG
  global bstack1l11lll111_opy_
  try:
    proxy = bstack1llll111l1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1ll_opy_ (u"࠭࠮ࡱࡣࡦࠫ঻")):
        proxies = bstack11llllll_opy_(proxy, bstack1l1lll1lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1l111l_opy_ = proxies.popitem()
          if bstack1ll1ll_opy_ (u"ࠢ࠻࠱࠲়ࠦ") in bstack1l1l111l_opy_:
            return bstack1l1l111l_opy_
          else:
            return bstack1ll1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤঽ") + bstack1l1l111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨা").format(str(e)))
  return bstack1l11lll111_opy_(self)
def bstack1l1llllll1_opy_():
  global CONFIG
  return bstack111lllll_opy_(CONFIG) and bstack1lll11l1ll_opy_() and bstack1l11llllll_opy_() >= version.parse(bstack11ll11111_opy_)
def bstack1ll11l111l_opy_():
  global CONFIG
  return (bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ি") in CONFIG or bstack1ll1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in CONFIG) and bstack1l1l11ll1_opy_()
def bstack1llllll1l1_opy_(config):
  bstack1l1l111111_opy_ = {}
  if bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩু") in config:
    bstack1l1l111111_opy_ = config[bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪূ")]
  if bstack1ll1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৃ") in config:
    bstack1l1l111111_opy_ = config[bstack1ll1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৄ")]
  proxy = bstack1llll111l1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")) and os.path.isfile(proxy):
      bstack1l1l111111_opy_[bstack1ll1ll_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৆")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1ll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩে")):
        proxies = bstack1l11l1l1l_opy_(config, bstack1l1lll1lll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1l111l_opy_ = proxies.popitem()
          if bstack1ll1ll_opy_ (u"ࠧࡀ࠯࠰ࠤৈ") in bstack1l1l111l_opy_:
            parsed_url = urlparse(bstack1l1l111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1ll_opy_ (u"ࠨ࠺࠰࠱ࠥ৉") + bstack1l1l111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1l111111_opy_[bstack1ll1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৊")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1l111111_opy_[bstack1ll1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫো")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1l111111_opy_[bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৌ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1l111111_opy_[bstack1ll1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ্࠭")] = str(parsed_url.password)
  return bstack1l1l111111_opy_
def bstack1l1ll1l111_opy_(config):
  if bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৎ") in config:
    return config[bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৏")]
  return {}
def bstack1l1l1l1l1l_opy_(caps):
  global bstack11l1lll1l_opy_
  if bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৐") in caps:
    caps[bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৑")][bstack1ll1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ৒")] = True
    if bstack11l1lll1l_opy_:
      caps[bstack1ll1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓")][bstack1ll1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔")] = bstack11l1lll1l_opy_
  else:
    caps[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৕")] = True
    if bstack11l1lll1l_opy_:
      caps[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৖")] = bstack11l1lll1l_opy_
def bstack11llll1ll_opy_():
  global CONFIG
  if not bstack11111lll_opy_(CONFIG):
    return
  if bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪৗ") in CONFIG and bstack1ll111ll_opy_(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৘")]):
    if (
      bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৙") in CONFIG
      and bstack1ll111ll_opy_(CONFIG[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৚")].get(bstack1ll1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৛")))
    ):
      logger.debug(bstack1ll1ll_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧড়"))
      return
    bstack1l1l111111_opy_ = bstack1llllll1l1_opy_(CONFIG)
    bstack11l111lll_opy_(CONFIG[bstack1ll1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨঢ়")], bstack1l1l111111_opy_)
def bstack11l111lll_opy_(key, bstack1l1l111111_opy_):
  global bstack11lll1llll_opy_
  logger.info(bstack11lll1l111_opy_)
  try:
    bstack11lll1llll_opy_ = Local()
    bstack1lll1111l1_opy_ = {bstack1ll1ll_opy_ (u"࠭࡫ࡦࡻࠪ৞"): key}
    bstack1lll1111l1_opy_.update(bstack1l1l111111_opy_)
    logger.debug(bstack1llll111ll_opy_.format(str(bstack1lll1111l1_opy_)))
    bstack11lll1llll_opy_.start(**bstack1lll1111l1_opy_)
    if bstack11lll1llll_opy_.isRunning():
      logger.info(bstack1l1lllll_opy_)
  except Exception as e:
    bstack1llllll11l_opy_(bstack11lllllll1_opy_.format(str(e)))
def bstack111l111l_opy_():
  global bstack11lll1llll_opy_
  if bstack11lll1llll_opy_.isRunning():
    logger.info(bstack1l1l11llll_opy_)
    bstack11lll1llll_opy_.stop()
  bstack11lll1llll_opy_ = None
def bstack11l1lllll_opy_(bstack1llllllll1_opy_=[]):
  global CONFIG
  bstack1ll1lll1_opy_ = []
  bstack1ll11l11l1_opy_ = [bstack1ll1ll_opy_ (u"ࠧࡰࡵࠪয়"), bstack1ll1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫৠ"), bstack1ll1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ৡ"), bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬৢ"), bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩৣ"), bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৤")]
  try:
    for err in bstack1llllllll1_opy_:
      bstack11llll1l1_opy_ = {}
      for k in bstack1ll11l11l1_opy_:
        val = CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৥")][int(err[bstack1ll1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭০")])].get(k)
        if val:
          bstack11llll1l1_opy_[k] = val
      if(err[bstack1ll1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ১")] != bstack1ll1ll_opy_ (u"ࠩࠪ২")):
        bstack11llll1l1_opy_[bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ৩")] = {
          err[bstack1ll1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ৪")]: err[bstack1ll1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")]
        }
        bstack1ll1lll1_opy_.append(bstack11llll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ৬") + str(e))
  finally:
    return bstack1ll1lll1_opy_
def bstack1ll1ll1ll_opy_(file_name):
  bstack1l1ll1111l_opy_ = []
  try:
    bstack111ll11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111ll11l_opy_):
      with open(bstack111ll11l_opy_) as f:
        bstack1l1111ll_opy_ = json.load(f)
        bstack1l1ll1111l_opy_ = bstack1l1111ll_opy_
      os.remove(bstack111ll11l_opy_)
    return bstack1l1ll1111l_opy_
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡪࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡯࡭ࡸࡺ࠺ࠡࠩ৭") + str(e))
    return bstack1l1ll1111l_opy_
def bstack11lll111_opy_():
  global bstack1ll1ll1l1l_opy_
  global bstack11llllll1_opy_
  global bstack1lll1111_opy_
  global bstack1lll1l1l11_opy_
  global bstack1lll1l111_opy_
  global bstack1lll11l11_opy_
  global CONFIG
  bstack11111l111_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ৮"))
  if bstack11111l111_opy_ in [bstack1ll1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ৯"), bstack1ll1ll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩৰ")]:
    bstack111l11lll_opy_()
  percy.shutdown()
  if bstack1ll1ll1l1l_opy_:
    logger.warning(bstack1lll11ll1_opy_.format(str(bstack1ll1ll1l1l_opy_)))
  else:
    try:
      bstack1lll1l11_opy_ = bstack1l11111ll1_opy_(bstack1ll1ll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪৱ"), logger)
      if bstack1lll1l11_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ৲")) and bstack1lll1l11_opy_.get(bstack1ll1ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ৳")).get(bstack1ll1ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ৴")):
        logger.warning(bstack1lll11ll1_opy_.format(str(bstack1lll1l11_opy_[bstack1ll1ll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭৵")][bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ৶")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1l11ll111_opy_)
  global bstack11lll1llll_opy_
  if bstack11lll1llll_opy_:
    bstack111l111l_opy_()
  try:
    for driver in bstack11llllll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1l1l11l_opy_)
  if bstack1lll11l11_opy_ == bstack1ll1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ৷"):
    bstack1lll1l111_opy_ = bstack1ll1ll1ll_opy_(bstack1ll1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ৸"))
  if bstack1lll11l11_opy_ == bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৹") and len(bstack1lll1l1l11_opy_) == 0:
    bstack1lll1l1l11_opy_ = bstack1ll1ll1ll_opy_(bstack1ll1ll_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ৺"))
    if len(bstack1lll1l1l11_opy_) == 0:
      bstack1lll1l1l11_opy_ = bstack1ll1ll1ll_opy_(bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭৻"))
  bstack111ll1lll_opy_ = bstack1ll1ll_opy_ (u"ࠨࠩৼ")
  if len(bstack1lll1111_opy_) > 0:
    bstack111ll1lll_opy_ = bstack11l1lllll_opy_(bstack1lll1111_opy_)
  elif len(bstack1lll1l1l11_opy_) > 0:
    bstack111ll1lll_opy_ = bstack11l1lllll_opy_(bstack1lll1l1l11_opy_)
  elif len(bstack1lll1l111_opy_) > 0:
    bstack111ll1lll_opy_ = bstack11l1lllll_opy_(bstack1lll1l111_opy_)
  elif len(bstack1l1ll1l1_opy_) > 0:
    bstack111ll1lll_opy_ = bstack11l1lllll_opy_(bstack1l1ll1l1_opy_)
  if bool(bstack111ll1lll_opy_):
    bstack1ll11lll1l_opy_(bstack111ll1lll_opy_)
  else:
    bstack1ll11lll1l_opy_()
  bstack11l111l1l_opy_(bstack11lll11l_opy_, logger)
  bstack11ll1ll1_opy_.bstack1lll11l1l1_opy_(CONFIG)
  if len(bstack1lll1l111_opy_) > 0:
    sys.exit(len(bstack1lll1l111_opy_))
def bstack1l1ll11l_opy_(bstack11l1l1l1_opy_, frame):
  global bstack1l1l1l1ll_opy_
  logger.error(bstack1111llll1_opy_)
  bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ৽"), bstack11l1l1l1_opy_)
  if hasattr(signal, bstack1ll1ll_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫ৾")):
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫ৿"), signal.Signals(bstack11l1l1l1_opy_).name)
  else:
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਀"), bstack1ll1ll_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਁ"))
  bstack11111l111_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਂ"))
  if bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ"):
    bstack1llll1ll_opy_.stop(bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ਄")))
  bstack11lll111_opy_()
  sys.exit(1)
def bstack1llllll11l_opy_(err):
  logger.critical(bstack1ll111lll1_opy_.format(str(err)))
  bstack1ll11lll1l_opy_(bstack1ll111lll1_opy_.format(str(err)), True)
  atexit.unregister(bstack11lll111_opy_)
  bstack111l11lll_opy_()
  sys.exit(1)
def bstack1l1l1ll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll11lll1l_opy_(message, True)
  atexit.unregister(bstack11lll111_opy_)
  bstack111l11lll_opy_()
  sys.exit(1)
def bstack1lllll1l1_opy_():
  global CONFIG
  global bstack1ll11l11ll_opy_
  global bstack1l11ll1l_opy_
  global bstack1llll111l_opy_
  CONFIG = bstack11lll1l1_opy_()
  load_dotenv(CONFIG.get(bstack1ll1ll_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਅ")))
  bstack11ll1lll_opy_()
  bstack1lll1lllll_opy_()
  CONFIG = bstack1l111l1ll_opy_(CONFIG)
  update(CONFIG, bstack1l11ll1l_opy_)
  update(CONFIG, bstack1ll11l11ll_opy_)
  CONFIG = bstack1l11l111_opy_(CONFIG)
  bstack1llll111l_opy_ = bstack11111lll_opy_(CONFIG)
  os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧਆ")] = bstack1llll111l_opy_.__str__()
  bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਇ"), bstack1llll111l_opy_)
  if (bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਈ") in CONFIG and bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਉ") in bstack1ll11l11ll_opy_) or (
          bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਊ") in CONFIG and bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ਋") not in bstack1l11ll1l_opy_):
    if os.getenv(bstack1ll1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ਌")):
      CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭਍")] = os.getenv(bstack1ll1ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਎"))
    else:
      bstack1lll111ll_opy_()
  elif (bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਏ") not in CONFIG and bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਐ") in CONFIG) or (
          bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਑") in bstack1l11ll1l_opy_ and bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ਒") not in bstack1ll11l11ll_opy_):
    del (CONFIG[bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਓ")])
  if bstack1l111lll1_opy_(CONFIG):
    bstack1llllll11l_opy_(bstack1l11l11lll_opy_)
  bstack1ll1ll1l_opy_()
  bstack1ll11ll1ll_opy_()
  if bstack1l1111l11l_opy_:
    CONFIG[bstack1ll1ll_opy_ (u"ࠫࡦࡶࡰࠨਔ")] = bstack1l11ll1l1_opy_(CONFIG)
    logger.info(bstack1l1ll11l1l_opy_.format(CONFIG[bstack1ll1ll_opy_ (u"ࠬࡧࡰࡱࠩਕ")]))
  if not bstack1llll111l_opy_:
    CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਖ")] = [{}]
def bstack1l1l1lll1_opy_(config, bstack11lll11l1_opy_):
  global CONFIG
  global bstack1l1111l11l_opy_
  CONFIG = config
  bstack1l1111l11l_opy_ = bstack11lll11l1_opy_
def bstack1ll11ll1ll_opy_():
  global CONFIG
  global bstack1l1111l11l_opy_
  if bstack1ll1ll_opy_ (u"ࠧࡢࡲࡳࠫਗ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1l11llll1_opy_)
    bstack1l1111l11l_opy_ = True
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧਘ"), True)
def bstack1l11ll1l1_opy_(config):
  bstack11l11ll11_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪਙ")
  app = config[bstack1ll1ll_opy_ (u"ࠪࡥࡵࡶࠧਚ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1l1l_opy_:
      if os.path.exists(app):
        bstack11l11ll11_opy_ = bstack1lll1ll1_opy_(config, app)
      elif bstack1ll1l11l11_opy_(app):
        bstack11l11ll11_opy_ = app
      else:
        bstack1llllll11l_opy_(bstack1lll1l1l1l_opy_.format(app))
    else:
      if bstack1ll1l11l11_opy_(app):
        bstack11l11ll11_opy_ = app
      elif os.path.exists(app):
        bstack11l11ll11_opy_ = bstack1lll1ll1_opy_(app)
      else:
        bstack1llllll11l_opy_(bstack1lll111lll_opy_)
  else:
    if len(app) > 2:
      bstack1llllll11l_opy_(bstack1l1lllll1_opy_)
    elif len(app) == 2:
      if bstack1ll1ll_opy_ (u"ࠫࡵࡧࡴࡩࠩਛ") in app and bstack1ll1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨਜ") in app:
        if os.path.exists(app[bstack1ll1ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫਝ")]):
          bstack11l11ll11_opy_ = bstack1lll1ll1_opy_(config, app[bstack1ll1ll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬਞ")], app[bstack1ll1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫਟ")])
        else:
          bstack1llllll11l_opy_(bstack1lll1l1l1l_opy_.format(app))
      else:
        bstack1llllll11l_opy_(bstack1l1lllll1_opy_)
    else:
      for key in app:
        if key in bstack11lll1ll_opy_:
          if key == bstack1ll1ll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧਠ"):
            if os.path.exists(app[key]):
              bstack11l11ll11_opy_ = bstack1lll1ll1_opy_(config, app[key])
            else:
              bstack1llllll11l_opy_(bstack1lll1l1l1l_opy_.format(app))
          else:
            bstack11l11ll11_opy_ = app[key]
        else:
          bstack1llllll11l_opy_(bstack1l1l1llll1_opy_)
  return bstack11l11ll11_opy_
def bstack1ll1l11l11_opy_(bstack11l11ll11_opy_):
  import re
  bstack11lllll1ll_opy_ = re.compile(bstack1ll1ll_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥਡ"))
  bstack1l1ll11111_opy_ = re.compile(bstack1ll1ll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣਢ"))
  if bstack1ll1ll_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫਣ") in bstack11l11ll11_opy_ or re.fullmatch(bstack11lllll1ll_opy_, bstack11l11ll11_opy_) or re.fullmatch(bstack1l1ll11111_opy_, bstack11l11ll11_opy_):
    return True
  else:
    return False
def bstack1lll1ll1_opy_(config, path, bstack1l11lll11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1ll_opy_ (u"࠭ࡲࡣࠩਤ")).read()).hexdigest()
  bstack1111111l_opy_ = bstack1ll1111lll_opy_(md5_hash)
  bstack11l11ll11_opy_ = None
  if bstack1111111l_opy_:
    logger.info(bstack11l11l11_opy_.format(bstack1111111l_opy_, md5_hash))
    return bstack1111111l_opy_
  bstack1l11111l11_opy_ = MultipartEncoder(
    fields={
      bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࠬਥ"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1ll_opy_ (u"ࠨࡴࡥࠫਦ")), bstack1ll1ll_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ਧ")),
      bstack1ll1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ਨ"): bstack1l11lll11l_opy_
    }
  )
  response = requests.post(bstack1ll1l1lll_opy_, data=bstack1l11111l11_opy_,
                           headers={bstack1ll1ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ਩"): bstack1l11111l11_opy_.content_type},
                           auth=(config[bstack1ll1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਪ")], config[bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩਫ")]))
  try:
    res = json.loads(response.text)
    bstack11l11ll11_opy_ = res[bstack1ll1ll_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨਬ")]
    logger.info(bstack1l111l1l1l_opy_.format(bstack11l11ll11_opy_))
    bstack11lll1111_opy_(md5_hash, bstack11l11ll11_opy_)
  except ValueError as err:
    bstack1llllll11l_opy_(bstack111l11l1l_opy_.format(str(err)))
  return bstack11l11ll11_opy_
def bstack1ll1ll1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l11ll1l_opy_
  bstack1llll11ll_opy_ = 1
  bstack1l1ll1111_opy_ = 1
  if bstack1ll1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨਭ") in CONFIG:
    bstack1l1ll1111_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩਮ")]
  else:
    bstack1l1ll1111_opy_ = bstack1l1l1lll11_opy_(framework_name, args) or 1
  if bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG:
    bstack1llll11ll_opy_ = len(CONFIG[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")])
  bstack11l11ll1l_opy_ = int(bstack1l1ll1111_opy_) * int(bstack1llll11ll_opy_)
def bstack1l1l1lll11_opy_(framework_name, args):
  if framework_name == bstack1l1l111ll1_opy_ and args and bstack1ll1ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ਱") in args:
      bstack11l11111l_opy_ = args.index(bstack1ll1ll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫਲ"))
      return int(args[bstack11l11111l_opy_ + 1]) or 1
  return 1
def bstack1ll1111lll_opy_(md5_hash):
  bstack1l11111lll_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠧࡿࠩਲ਼")), bstack1ll1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ਴"), bstack1ll1ll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪਵ"))
  if os.path.exists(bstack1l11111lll_opy_):
    bstack1l1lll1l11_opy_ = json.load(open(bstack1l11111lll_opy_, bstack1ll1ll_opy_ (u"ࠪࡶࡧ࠭ਸ਼")))
    if md5_hash in bstack1l1lll1l11_opy_:
      bstack11lllll111_opy_ = bstack1l1lll1l11_opy_[md5_hash]
      bstack1lll1lll_opy_ = datetime.datetime.now()
      bstack111l1ll11_opy_ = datetime.datetime.strptime(bstack11lllll111_opy_[bstack1ll1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ਷")], bstack1ll1ll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩਸ"))
      if (bstack1lll1lll_opy_ - bstack111l1ll11_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11lllll111_opy_[bstack1ll1ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫਹ")]):
        return None
      return bstack11lllll111_opy_[bstack1ll1ll_opy_ (u"ࠧࡪࡦࠪ਺")]
  else:
    return None
def bstack11lll1111_opy_(md5_hash, bstack11l11ll11_opy_):
  bstack1l11l1l11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠨࢀࠪ਻")), bstack1ll1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬਼ࠩ"))
  if not os.path.exists(bstack1l11l1l11l_opy_):
    os.makedirs(bstack1l11l1l11l_opy_)
  bstack1l11111lll_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠪࢂࠬ਽")), bstack1ll1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਾ"), bstack1ll1ll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ਿ"))
  bstack11l11l1l_opy_ = {
    bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩੀ"): bstack11l11ll11_opy_,
    bstack1ll1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪੁ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1ll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬੂ")),
    bstack1ll1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੃"): str(__version__)
  }
  if os.path.exists(bstack1l11111lll_opy_):
    bstack1l1lll1l11_opy_ = json.load(open(bstack1l11111lll_opy_, bstack1ll1ll_opy_ (u"ࠪࡶࡧ࠭੄")))
  else:
    bstack1l1lll1l11_opy_ = {}
  bstack1l1lll1l11_opy_[md5_hash] = bstack11l11l1l_opy_
  with open(bstack1l11111lll_opy_, bstack1ll1ll_opy_ (u"ࠦࡼ࠱ࠢ੅")) as outfile:
    json.dump(bstack1l1lll1l11_opy_, outfile)
def bstack1l11ll11_opy_(self):
  return
def bstack1l1lll1l_opy_(self):
  return
def bstack1lll1llll1_opy_(self):
  global bstack1l11llll1l_opy_
  bstack1l11llll1l_opy_(self)
def bstack11l1ll111_opy_():
  global bstack1l11llll_opy_
  bstack1l11llll_opy_ = True
def bstack111ll111l_opy_(self):
  global bstack11lllllll_opy_
  global bstack1lll11111_opy_
  global bstack1l11111l1_opy_
  try:
    if bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ੆") in bstack11lllllll_opy_ and self.session_id != None and bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੇ"), bstack1ll1ll_opy_ (u"ࠧࠨੈ")) != bstack1ll1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ੉"):
      bstack1llll11lll_opy_ = bstack1ll1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੊") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੋ")
      if bstack1llll11lll_opy_ == bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫੌ"):
        bstack1ll11ll11_opy_(logger)
      if self != None:
        bstack11l1llll_opy_(self, bstack1llll11lll_opy_, bstack1ll1ll_opy_ (u"ࠬ࠲ࠠࠨ੍").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll1ll_opy_ (u"࠭ࠧ੎")
    if bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੏") in bstack11lllllll_opy_ and getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੐"), None):
      bstack11lllll1_opy_.bstack1l1l1111l_opy_(self, bstack1ll11llll1_opy_, logger, wait=True)
    if bstack1ll1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩੑ") in bstack11lllllll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11l1llll_opy_(self, bstack1ll1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੒"))
      bstack1ll1l1l1ll_opy_.bstack1ll1ll111_opy_(self)
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੓") + str(e))
  bstack1l11111l1_opy_(self)
  self.session_id = None
def bstack1l11ll111l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11llll1111_opy_
    global bstack11lllllll_opy_
    command_executor = kwargs.get(bstack1ll1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੔"), bstack1ll1ll_opy_ (u"࠭ࠧ੕"))
    bstack1111ll11_opy_ = False
    if type(command_executor) == str and bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ੖") in command_executor:
      bstack1111ll11_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ੗") in str(getattr(command_executor, bstack1ll1ll_opy_ (u"ࠩࡢࡹࡷࡲࠧ੘"), bstack1ll1ll_opy_ (u"ࠪࠫਖ਼"))):
      bstack1111ll11_opy_ = True
    else:
      return bstack11111111l_opy_(self, *args, **kwargs)
    if bstack1111ll11_opy_:
      if kwargs.get(bstack1ll1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬਗ਼")):
        kwargs[bstack1ll1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ਜ਼")] = bstack11llll1111_opy_(kwargs[bstack1ll1ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧੜ")], bstack11lllllll_opy_)
      elif kwargs.get(bstack1ll1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ੝")):
        kwargs[bstack1ll1ll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨਫ਼")] = bstack11llll1111_opy_(kwargs[bstack1ll1ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ੟")], bstack11lllllll_opy_)
  except Exception as e:
    logger.error(bstack1ll1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ੠").format(str(e)))
  return bstack11111111l_opy_(self, *args, **kwargs)
def bstack1l111111_opy_(self, command_executor=bstack1ll1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ੡"), *args, **kwargs):
  bstack1lll1l11ll_opy_ = bstack1l11ll111l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1111llll_opy_.on():
    return bstack1lll1l11ll_opy_
  try:
    logger.debug(bstack1ll1ll_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ੢").format(str(command_executor)))
    logger.debug(bstack1ll1ll_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ੣").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ੤") in command_executor._url:
      bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ੥"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ੦") in command_executor):
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ੧"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1llll1ll_opy_.bstack1ll1l1ll1_opy_(self)
  return bstack1lll1l11ll_opy_
def bstack1l1l1l1l11_opy_(args):
  return bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ੨") in str(args)
def bstack1ll1l111ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1111l111l_opy_
  global bstack1111111l1_opy_
  bstack1l11lll1ll_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ੩"), None) and bstack1l1lll11_opy_(
          threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ੪"), None)
  bstack11lll1111l_opy_ = getattr(self, bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ੫"), None) != None and getattr(self, bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ੬"), None) == True
  if not bstack1111111l1_opy_ and bstack1llll111l_opy_ and bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ੭") in CONFIG and CONFIG[bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ੮")] == True and bstack1lll1l11l_opy_.bstack1ll1ll111l_opy_(driver_command) and (bstack11lll1111l_opy_ or bstack1l11lll1ll_opy_) and not bstack1l1l1l1l11_opy_(args):
    try:
      bstack1111111l1_opy_ = True
      logger.debug(bstack1ll1ll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭੯").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1ll1ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪੰ").format(str(err)))
    bstack1111111l1_opy_ = False
  response = bstack1111l111l_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੱ") in str(bstack11lllllll_opy_).lower() or bstack1ll1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧੲ") in str(bstack11lllllll_opy_).lower()) and bstack1111llll_opy_.on():
    try:
      if driver_command == bstack1ll1ll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬੳ"):
        bstack1llll1ll_opy_.bstack1llllllll_opy_({
            bstack1ll1ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨੴ"): response[bstack1ll1ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩੵ")],
            bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ੶"): bstack1llll1ll_opy_.current_test_uuid() if bstack1llll1ll_opy_.current_test_uuid() else bstack1111llll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1lll1111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1lll11111_opy_
  global bstack1l111l111_opy_
  global bstack1llll1lll_opy_
  global bstack1l1111l1_opy_
  global bstack11l1ll1l1_opy_
  global bstack11lllllll_opy_
  global bstack11111111l_opy_
  global bstack11llllll1_opy_
  global bstack1lllll11ll_opy_
  global bstack1ll11llll1_opy_
  CONFIG[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੷")] = str(bstack11lllllll_opy_) + str(__version__)
  command_executor = bstack1l1lll1lll_opy_()
  logger.debug(bstack1l1111l11_opy_.format(command_executor))
  proxy = bstack1lll1ll11l_opy_(CONFIG, proxy)
  bstack1ll111l1_opy_ = 0 if bstack1l111l111_opy_ < 0 else bstack1l111l111_opy_
  try:
    if bstack1l1111l1_opy_ is True:
      bstack1ll111l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1ll1l1_opy_ is True:
      bstack1ll111l1_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll111l1_opy_ = 0
  bstack1ll1llll1l_opy_ = bstack1llll1111_opy_(CONFIG, bstack1ll111l1_opy_)
  logger.debug(bstack1lll1ll111_opy_.format(str(bstack1ll1llll1l_opy_)))
  if bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੸") in CONFIG and bstack1ll111ll_opy_(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ੹")]):
    bstack1l1l1l1l1l_opy_(bstack1ll1llll1l_opy_)
  if bstack1l11l11l1_opy_.bstack1lllll1l1l_opy_(CONFIG, bstack1ll111l1_opy_) and bstack1l11l11l1_opy_.bstack1l11l1l11_opy_(bstack1ll1llll1l_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1l11l11l1_opy_.set_capabilities(bstack1ll1llll1l_opy_, CONFIG)
  if desired_capabilities:
    bstack1111lll11_opy_ = bstack1l111l1ll_opy_(desired_capabilities)
    bstack1111lll11_opy_[bstack1ll1ll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ੺")] = bstack1l1ll11lll_opy_(CONFIG)
    bstack1l1l1lll_opy_ = bstack1llll1111_opy_(bstack1111lll11_opy_)
    if bstack1l1l1lll_opy_:
      bstack1ll1llll1l_opy_ = update(bstack1l1l1lll_opy_, bstack1ll1llll1l_opy_)
    desired_capabilities = None
  if options:
    bstack111ll1l1_opy_(options, bstack1ll1llll1l_opy_)
  if not options:
    options = bstack11ll11ll_opy_(bstack1ll1llll1l_opy_)
  bstack1ll11llll1_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੻"))[bstack1ll111l1_opy_]
  if proxy and bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ੼")):
    options.proxy(proxy)
  if options and bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ੽")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l11llllll_opy_() < version.parse(bstack1ll1ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ੾")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1llll1l_opy_)
  logger.info(bstack1lll1l1l1_opy_)
  if bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭੿")):
    bstack11111111l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭઀")):
    bstack11111111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨઁ")):
    bstack11111111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11111111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack111l1lll1_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪં")
    if bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫઃ")):
      bstack111l1lll1_opy_ = self.caps.get(bstack1ll1ll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ઄"))
    else:
      bstack111l1lll1_opy_ = self.capabilities.get(bstack1ll1ll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧઅ"))
    if bstack111l1lll1_opy_:
      bstack11111lll1_opy_(bstack111l1lll1_opy_)
      if bstack1l11llllll_opy_() <= version.parse(bstack1ll1ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭આ")):
        self.command_executor._url = bstack1ll1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣઇ") + bstack1llll11111_opy_ + bstack1ll1ll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧઈ")
      else:
        self.command_executor._url = bstack1ll1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦઉ") + bstack111l1lll1_opy_ + bstack1ll1ll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦઊ")
      logger.debug(bstack1l1l1l11l_opy_.format(bstack111l1lll1_opy_))
    else:
      logger.debug(bstack1l1111ll1_opy_.format(bstack1ll1ll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧઋ")))
  except Exception as e:
    logger.debug(bstack1l1111ll1_opy_.format(e))
  if bstack1ll1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫઌ") in bstack11lllllll_opy_:
    bstack11lll1l1ll_opy_(bstack1l111l111_opy_, bstack1lllll11ll_opy_)
  bstack1lll11111_opy_ = self.session_id
  if bstack1ll1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ઍ") in bstack11lllllll_opy_ or bstack1ll1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ઎") in bstack11lllllll_opy_ or bstack1ll1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧએ") in bstack11lllllll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1llll1ll_opy_.bstack1ll1l1ll1_opy_(self)
  bstack11llllll1_opy_.append(self)
  if bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઐ") in CONFIG and bstack1ll1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઑ") in CONFIG[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ઒")][bstack1ll111l1_opy_]:
    bstack1llll1lll_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨઓ")][bstack1ll111l1_opy_][bstack1ll1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઔ")]
  logger.debug(bstack1l1l111ll_opy_.format(bstack1lll11111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1lllll111_opy_
    def bstack1ll1llll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1lllll1111_opy_
      if(bstack1ll1ll_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤક") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠨࢀࠪખ")), bstack1ll1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"), bstack1ll1ll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬઘ")), bstack1ll1ll_opy_ (u"ࠫࡼ࠭ઙ")) as fp:
          fp.write(bstack1ll1ll_opy_ (u"ࠧࠨચ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1ll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣછ")))):
          with open(args[1], bstack1ll1ll_opy_ (u"ࠧࡳࠩજ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1ll_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧઝ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l11111_opy_)
            if bstack1ll1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ઞ") in CONFIG and str(CONFIG[bstack1ll1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧટ")]).lower() != bstack1ll1ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪઠ"):
                bstack1llllll11_opy_ = bstack1lllll111_opy_()
                bstack11l1l111l_opy_ = bstack1ll1ll_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࠢࠣࡸࡷࡿࠠࡼࡽࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠌࠣࠤࠥࠦࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࠽ࠍࠤࠥࢃࡽࠡࡥࡤࡸࡨ࡮ࠠࠩࡧࡻ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡩ࡯࡯ࡵࡲࡰࡪ࠴ࡥࡳࡴࡲࡶ࠭ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠣ࠮ࠣࡩࡽ࠯࠻ࠋࠢࠣࢁࢂࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࡿࢀ࠿ࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧડ").format(bstack1llllll11_opy_=bstack1llllll11_opy_)
            lines.insert(1, bstack11l1l111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1ll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣઢ")), bstack1ll1ll_opy_ (u"ࠧࡸࠩણ")) as bstack1ll11lll_opy_:
              bstack1ll11lll_opy_.writelines(lines)
        CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪત")] = str(bstack11lllllll_opy_) + str(__version__)
        bstack1ll111l1_opy_ = 0 if bstack1l111l111_opy_ < 0 else bstack1l111l111_opy_
        try:
          if bstack1l1111l1_opy_ is True:
            bstack1ll111l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l1ll1l1_opy_ is True:
            bstack1ll111l1_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll111l1_opy_ = 0
        CONFIG[bstack1ll1ll_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤથ")] = False
        CONFIG[bstack1ll1ll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤદ")] = True
        bstack1ll1llll1l_opy_ = bstack1llll1111_opy_(CONFIG, bstack1ll111l1_opy_)
        logger.debug(bstack1lll1ll111_opy_.format(str(bstack1ll1llll1l_opy_)))
        if CONFIG.get(bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨધ")):
          bstack1l1l1l1l1l_opy_(bstack1ll1llll1l_opy_)
        if bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨન") in CONFIG and bstack1ll1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ઩") in CONFIG[bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪપ")][bstack1ll111l1_opy_]:
          bstack1llll1lll_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫફ")][bstack1ll111l1_opy_][bstack1ll1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧબ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠪࢂࠬભ")), bstack1ll1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫમ"), bstack1ll1ll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧય")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll1llll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1ll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣર"))
      bstack1lllll1111_opy_ = True
      return bstack11ll11l1l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11lll1ll11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l111l111_opy_
    global bstack1llll1lll_opy_
    global bstack1l1111l1_opy_
    global bstack11l1ll1l1_opy_
    global bstack11lllllll_opy_
    CONFIG[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ઱")] = str(bstack11lllllll_opy_) + str(__version__)
    bstack1ll111l1_opy_ = 0 if bstack1l111l111_opy_ < 0 else bstack1l111l111_opy_
    try:
      if bstack1l1111l1_opy_ is True:
        bstack1ll111l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l1ll1l1_opy_ is True:
        bstack1ll111l1_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll111l1_opy_ = 0
    CONFIG[bstack1ll1ll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢલ")] = True
    bstack1ll1llll1l_opy_ = bstack1llll1111_opy_(CONFIG, bstack1ll111l1_opy_)
    logger.debug(bstack1lll1ll111_opy_.format(str(bstack1ll1llll1l_opy_)))
    if CONFIG.get(bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ળ")):
      bstack1l1l1l1l1l_opy_(bstack1ll1llll1l_opy_)
    if bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭઴") in CONFIG and bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩવ") in CONFIG[bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ")][bstack1ll111l1_opy_]:
      bstack1llll1lll_opy_ = CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩષ")][bstack1ll111l1_opy_][bstack1ll1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬસ")]
    import urllib
    import json
    if bstack1ll1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬહ") in CONFIG and str(CONFIG[bstack1ll1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭઺")]).lower() != bstack1ll1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ઻"):
        bstack1l111ll1_opy_ = bstack1lllll111_opy_()
        bstack1llllll11_opy_ = bstack1l111ll1_opy_ + urllib.parse.quote(json.dumps(bstack1ll1llll1l_opy_))
    else:
        bstack1llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ઼࠭") + urllib.parse.quote(json.dumps(bstack1ll1llll1l_opy_))
    browser = self.connect(bstack1llllll11_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll11ll1l1_opy_():
    global bstack1lllll1111_opy_
    global bstack11lllllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111111ll_opy_
        if not bstack1llll111l_opy_:
          global bstack1l1l1lllll_opy_
          if not bstack1l1l1lllll_opy_:
            from bstack_utils.helper import bstack1ll1lll11_opy_, bstack1ll1l1111_opy_
            bstack1l1l1lllll_opy_ = bstack1ll1lll11_opy_()
            bstack1ll1l1111_opy_(bstack11lllllll_opy_)
          BrowserType.connect = bstack1l111111ll_opy_
          return
        BrowserType.launch = bstack11lll1ll11_opy_
        bstack1lllll1111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1llll1_opy_
      bstack1lllll1111_opy_ = True
    except Exception as e:
      pass
def bstack11ll1l111_opy_(context, bstack1ll1l1lll1_opy_):
  try:
    context.page.evaluate(bstack1ll1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨઽ"), bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪા")+ json.dumps(bstack1ll1l1lll1_opy_) + bstack1ll1ll_opy_ (u"ࠢࡾࡿࠥિ"))
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨી"), e)
def bstack1l11l1l1l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll1ll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥુ"), bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨૂ") + json.dumps(message) + bstack1ll1ll_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧૃ") + json.dumps(level) + bstack1ll1ll_opy_ (u"ࠬࢃࡽࠨૄ"))
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤૅ"), e)
def bstack1l1ll1l1l_opy_(self, url):
  global bstack11lll11l11_opy_
  try:
    bstack1ll111lll_opy_(url)
  except Exception as err:
    logger.debug(bstack111lll11l_opy_.format(str(err)))
  try:
    bstack11lll11l11_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1lll11l_opy_ = str(e)
      if any(err_msg in bstack1l1lll11l_opy_ for err_msg in bstack1l1lll111_opy_):
        bstack1ll111lll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111lll11l_opy_.format(str(err)))
    raise e
def bstack1l111l11l_opy_(self):
  global bstack11l11l1l1_opy_
  bstack11l11l1l1_opy_ = self
  return
def bstack1llll1l1_opy_(self):
  global bstack1lllllllll_opy_
  bstack1lllllllll_opy_ = self
  return
def bstack1llll1l1l1_opy_(test_name, bstack1ll1l1llll_opy_):
  global CONFIG
  if percy.bstack1l1l11ll11_opy_() == bstack1ll1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧ૆"):
    bstack1ll11l111_opy_ = os.path.relpath(bstack1ll1l1llll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll11l111_opy_)
    bstack1l11111l1l_opy_ = suite_name + bstack1ll1ll_opy_ (u"ࠣ࠯ࠥે") + test_name
    threading.current_thread().percySessionName = bstack1l11111l1l_opy_
def bstack1ll1l11ll1_opy_(self, test, *args, **kwargs):
  global bstack11111l11_opy_
  test_name = None
  bstack1ll1l1llll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll1l1llll_opy_ = str(test.source)
  bstack1llll1l1l1_opy_(test_name, bstack1ll1l1llll_opy_)
  bstack11111l11_opy_(self, test, *args, **kwargs)
def bstack1l1l1ll1l1_opy_(driver, bstack1l11111l1l_opy_):
  if not bstack1ll1llll11_opy_ and bstack1l11111l1l_opy_:
      bstack1lll1lll11_opy_ = {
          bstack1ll1ll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩૈ"): bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫૉ"),
          bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ૊"): {
              bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪો"): bstack1l11111l1l_opy_
          }
      }
      bstack1lll111l1_opy_ = bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫૌ").format(json.dumps(bstack1lll1lll11_opy_))
      driver.execute_script(bstack1lll111l1_opy_)
  if bstack1l11ll1l11_opy_:
      bstack1ll1l1l1_opy_ = {
          bstack1ll1ll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴ્ࠧ"): bstack1ll1ll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ૎"),
          bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ૏"): {
              bstack1ll1ll_opy_ (u"ࠪࡨࡦࡺࡡࠨૐ"): bstack1l11111l1l_opy_ + bstack1ll1ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭૑"),
              bstack1ll1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ૒"): bstack1ll1ll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ૓")
          }
      }
      if bstack1l11ll1l11_opy_.status == bstack1ll1ll_opy_ (u"ࠧࡑࡃࡖࡗࠬ૔"):
          bstack11lll1l11l_opy_ = bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭૕").format(json.dumps(bstack1ll1l1l1_opy_))
          driver.execute_script(bstack11lll1l11l_opy_)
          bstack11l1llll_opy_(driver, bstack1ll1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ૖"))
      elif bstack1l11ll1l11_opy_.status == bstack1ll1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨ૗"):
          reason = bstack1ll1ll_opy_ (u"ࠦࠧ૘")
          bstack1111ll1ll_opy_ = bstack1l11111l1l_opy_ + bstack1ll1ll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭૙")
          if bstack1l11ll1l11_opy_.message:
              reason = str(bstack1l11ll1l11_opy_.message)
              bstack1111ll1ll_opy_ = bstack1111ll1ll_opy_ + bstack1ll1ll_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭૚") + reason
          bstack1ll1l1l1_opy_[bstack1ll1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ૛")] = {
              bstack1ll1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ૜"): bstack1ll1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ૝"),
              bstack1ll1ll_opy_ (u"ࠪࡨࡦࡺࡡࠨ૞"): bstack1111ll1ll_opy_
          }
          bstack11lll1l11l_opy_ = bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ૟").format(json.dumps(bstack1ll1l1l1_opy_))
          driver.execute_script(bstack11lll1l11l_opy_)
          bstack11l1llll_opy_(driver, bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬૠ"), reason)
          bstack1ll11l1lll_opy_(reason, str(bstack1l11ll1l11_opy_), str(bstack1l111l111_opy_), logger)
def bstack1ll1l111_opy_(driver, test):
  if percy.bstack1l1l11ll11_opy_() == bstack1ll1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦૡ") and percy.bstack1l1ll1llll_opy_() == bstack1ll1ll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤૢ"):
      bstack1l11l11111_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫૣ"), None)
      bstack1l111ll1l1_opy_(driver, bstack1l11l11111_opy_, test)
  if bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭૤"), None) and bstack1l1lll11_opy_(
          threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ૥"), None):
      logger.info(bstack1ll1ll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦ૦"))
      bstack1l11l11l1_opy_.bstack11ll11lll_opy_(driver, name=test.name, path=test.source)
def bstack1l1l1ll11l_opy_(test, bstack1l11111l1l_opy_):
    try:
      data = {}
      if test:
        data[bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ૧")] = bstack1l11111l1l_opy_
      if bstack1l11ll1l11_opy_:
        if bstack1l11ll1l11_opy_.status == bstack1ll1ll_opy_ (u"࠭ࡐࡂࡕࡖࠫ૨"):
          data[bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૩")] = bstack1ll1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ૪")
        elif bstack1l11ll1l11_opy_.status == bstack1ll1ll_opy_ (u"ࠩࡉࡅࡎࡒࠧ૫"):
          data[bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ૬")] = bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૭")
          if bstack1l11ll1l11_opy_.message:
            data[bstack1ll1ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ૮")] = str(bstack1l11ll1l11_opy_.message)
      user = CONFIG[bstack1ll1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ૯")]
      key = CONFIG[bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ૰")]
      url = bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭૱").format(user, key, bstack1lll11111_opy_)
      headers = {
        bstack1ll1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ૲"): bstack1ll1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭૳"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1111l11ll_opy_.format(str(e)))
def bstack1ll11l1l1_opy_(test, bstack1l11111l1l_opy_):
  global CONFIG
  global bstack1lllllllll_opy_
  global bstack11l11l1l1_opy_
  global bstack1lll11111_opy_
  global bstack1l11ll1l11_opy_
  global bstack1llll1lll_opy_
  global bstack11llll111l_opy_
  global bstack1l1l111lll_opy_
  global bstack1l11ll1l1l_opy_
  global bstack1lll11ll11_opy_
  global bstack11llllll1_opy_
  global bstack1ll11llll1_opy_
  try:
    if not bstack1lll11111_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠫࢃ࠭૴")), bstack1ll1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ૵"), bstack1ll1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ૶"))) as f:
        bstack1lll111l11_opy_ = json.loads(bstack1ll1ll_opy_ (u"ࠢࡼࠤ૷") + f.read().strip() + bstack1ll1ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ૸") + bstack1ll1ll_opy_ (u"ࠤࢀࠦૹ"))
        bstack1lll11111_opy_ = bstack1lll111l11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11llllll1_opy_:
    for driver in bstack11llllll1_opy_:
      if bstack1lll11111_opy_ == driver.session_id:
        if test:
          bstack1ll1l111_opy_(driver, test)
        bstack1l1l1ll1l1_opy_(driver, bstack1l11111l1l_opy_)
  elif bstack1lll11111_opy_:
    bstack1l1l1ll11l_opy_(test, bstack1l11111l1l_opy_)
  if bstack1lllllllll_opy_:
    bstack1l1l111lll_opy_(bstack1lllllllll_opy_)
  if bstack11l11l1l1_opy_:
    bstack1l11ll1l1l_opy_(bstack11l11l1l1_opy_)
  if bstack1l11llll_opy_:
    bstack1lll11ll11_opy_()
def bstack111ll1111_opy_(self, test, *args, **kwargs):
  bstack1l11111l1l_opy_ = None
  if test:
    bstack1l11111l1l_opy_ = str(test.name)
  bstack1ll11l1l1_opy_(test, bstack1l11111l1l_opy_)
  bstack11llll111l_opy_(self, test, *args, **kwargs)
def bstack11lll111l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1l11_opy_
  global CONFIG
  global bstack11llllll1_opy_
  global bstack1lll11111_opy_
  bstack11lllll1l1_opy_ = None
  try:
    if bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩૺ"), None):
      try:
        if not bstack1lll11111_opy_:
          with open(os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠫࢃ࠭ૻ")), bstack1ll1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬૼ"), bstack1ll1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ૽"))) as f:
            bstack1lll111l11_opy_ = json.loads(bstack1ll1ll_opy_ (u"ࠢࡼࠤ૾") + f.read().strip() + bstack1ll1ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ૿") + bstack1ll1ll_opy_ (u"ࠤࢀࠦ଀"))
            bstack1lll11111_opy_ = bstack1lll111l11_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11llllll1_opy_:
        for driver in bstack11llllll1_opy_:
          if bstack1lll11111_opy_ == driver.session_id:
            bstack11lllll1l1_opy_ = driver
    bstack111l1ll1_opy_ = bstack1l11l11l1_opy_.bstack1111l1l1_opy_(test.tags)
    if bstack11lllll1l1_opy_:
      threading.current_thread().isA11yTest = bstack1l11l11l1_opy_.bstack1l1l11111l_opy_(bstack11lllll1l1_opy_, bstack111l1ll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111l1ll1_opy_
  except:
    pass
  bstack11ll1l11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11ll1l11_opy_
  bstack1l11ll1l11_opy_ = self._test
def bstack11l1lll1_opy_():
  global bstack1llllll1l_opy_
  try:
    if os.path.exists(bstack1llllll1l_opy_):
      os.remove(bstack1llllll1l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ଁ") + str(e))
def bstack1l1111llll_opy_():
  global bstack1llllll1l_opy_
  bstack1lll1l11_opy_ = {}
  try:
    if not os.path.isfile(bstack1llllll1l_opy_):
      with open(bstack1llllll1l_opy_, bstack1ll1ll_opy_ (u"ࠫࡼ࠭ଂ")):
        pass
      with open(bstack1llllll1l_opy_, bstack1ll1ll_opy_ (u"ࠧࡽࠫࠣଃ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1llllll1l_opy_):
      bstack1lll1l11_opy_ = json.load(open(bstack1llllll1l_opy_, bstack1ll1ll_opy_ (u"࠭ࡲࡣࠩ଄")))
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩଅ") + str(e))
  finally:
    return bstack1lll1l11_opy_
def bstack11lll1l1ll_opy_(platform_index, item_index):
  global bstack1llllll1l_opy_
  try:
    bstack1lll1l11_opy_ = bstack1l1111llll_opy_()
    bstack1lll1l11_opy_[item_index] = platform_index
    with open(bstack1llllll1l_opy_, bstack1ll1ll_opy_ (u"ࠣࡹ࠮ࠦଆ")) as outfile:
      json.dump(bstack1lll1l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧଇ") + str(e))
def bstack1l11l1111l_opy_(bstack1ll1ll11l1_opy_):
  global CONFIG
  bstack111ll1ll_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫଈ")
  if not bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଉ") in CONFIG:
    logger.info(bstack1ll1ll_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩଊ"))
  try:
    platform = CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଋ")][bstack1ll1ll11l1_opy_]
    if bstack1ll1ll_opy_ (u"ࠧࡰࡵࠪଌ") in platform:
      bstack111ll1ll_opy_ += str(platform[bstack1ll1ll_opy_ (u"ࠨࡱࡶࠫ଍")]) + bstack1ll1ll_opy_ (u"ࠩ࠯ࠤࠬ଎")
    if bstack1ll1ll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଏ") in platform:
      bstack111ll1ll_opy_ += str(platform[bstack1ll1ll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧଐ")]) + bstack1ll1ll_opy_ (u"ࠬ࠲ࠠࠨ଑")
    if bstack1ll1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ଒") in platform:
      bstack111ll1ll_opy_ += str(platform[bstack1ll1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫଓ")]) + bstack1ll1ll_opy_ (u"ࠨ࠮ࠣࠫଔ")
    if bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫକ") in platform:
      bstack111ll1ll_opy_ += str(platform[bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬଖ")]) + bstack1ll1ll_opy_ (u"ࠫ࠱ࠦࠧଗ")
    if bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଘ") in platform:
      bstack111ll1ll_opy_ += str(platform[bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଙ")]) + bstack1ll1ll_opy_ (u"ࠧ࠭ࠢࠪଚ")
    if bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଛ") in platform:
      bstack111ll1ll_opy_ += str(platform[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪଜ")]) + bstack1ll1ll_opy_ (u"ࠪ࠰ࠥ࠭ଝ")
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫଞ") + str(e))
  finally:
    if bstack111ll1ll_opy_[len(bstack111ll1ll_opy_) - 2:] == bstack1ll1ll_opy_ (u"ࠬ࠲ࠠࠨଟ"):
      bstack111ll1ll_opy_ = bstack111ll1ll_opy_[:-2]
    return bstack111ll1ll_opy_
def bstack1l1l11l1l_opy_(path, bstack111ll1ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll1ll11_opy_ = ET.parse(path)
    bstack1lll11llll_opy_ = bstack1ll1ll11_opy_.getroot()
    bstack1lll11l1_opy_ = None
    for suite in bstack1lll11llll_opy_.iter(bstack1ll1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬଠ")):
      if bstack1ll1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧଡ") in suite.attrib:
        suite.attrib[bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ଢ")] += bstack1ll1ll_opy_ (u"ࠩࠣࠫଣ") + bstack111ll1ll_opy_
        bstack1lll11l1_opy_ = suite
    bstack1ll1llll_opy_ = None
    for robot in bstack1lll11llll_opy_.iter(bstack1ll1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩତ")):
      bstack1ll1llll_opy_ = robot
    bstack111111l11_opy_ = len(bstack1ll1llll_opy_.findall(bstack1ll1ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪଥ")))
    if bstack111111l11_opy_ == 1:
      bstack1ll1llll_opy_.remove(bstack1ll1llll_opy_.findall(bstack1ll1ll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫଦ"))[0])
      bstack1l1l11l111_opy_ = ET.Element(bstack1ll1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬଧ"), attrib={bstack1ll1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬନ"): bstack1ll1ll_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨ଩"), bstack1ll1ll_opy_ (u"ࠩ࡬ࡨࠬପ"): bstack1ll1ll_opy_ (u"ࠪࡷ࠵࠭ଫ")})
      bstack1ll1llll_opy_.insert(1, bstack1l1l11l111_opy_)
      bstack1llll11l11_opy_ = None
      for suite in bstack1ll1llll_opy_.iter(bstack1ll1ll_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪବ")):
        bstack1llll11l11_opy_ = suite
      bstack1llll11l11_opy_.append(bstack1lll11l1_opy_)
      bstack111llllll_opy_ = None
      for status in bstack1lll11l1_opy_.iter(bstack1ll1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଭ")):
        bstack111llllll_opy_ = status
      bstack1llll11l11_opy_.append(bstack111llllll_opy_)
    bstack1ll1ll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫମ") + str(e))
def bstack111llll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111111l1_opy_
  global CONFIG
  if bstack1ll1ll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦଯ") in options:
    del options[bstack1ll1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧର")]
  bstack1l1ll1lll1_opy_ = bstack1l1111llll_opy_()
  for bstack1l11l11ll1_opy_ in bstack1l1ll1lll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠩ଱"), str(bstack1l11l11ll1_opy_), bstack1ll1ll_opy_ (u"ࠪࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠧଲ"))
    bstack1l1l11l1l_opy_(path, bstack1l11l1111l_opy_(bstack1l1ll1lll1_opy_[bstack1l11l11ll1_opy_]))
  bstack11l1lll1_opy_()
  return bstack111111l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll1ll1ll1_opy_(self, ff_profile_dir):
  global bstack11111l1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack11111l1l1_opy_(self, ff_profile_dir)
def bstack1ll111l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1lll1l_opy_
  bstack11l1lll11_opy_ = []
  if bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଳ") in CONFIG:
    bstack11l1lll11_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଴")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢଵ")],
      pabot_args[bstack1ll1ll_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣଶ")],
      argfile,
      pabot_args.get(bstack1ll1ll_opy_ (u"ࠣࡪ࡬ࡺࡪࠨଷ")),
      pabot_args[bstack1ll1ll_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧସ")],
      platform[0],
      bstack11l1lll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1ll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥହ")] or [(bstack1ll1ll_opy_ (u"ࠦࠧ଺"), None)]
    for platform in enumerate(bstack11l1lll11_opy_)
  ]
def bstack1l1ll111ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11111ll1_opy_=bstack1ll1ll_opy_ (u"ࠬ࠭଻")):
  global bstack11ll111ll_opy_
  self.platform_index = platform_index
  self.bstack1l1l111l1_opy_ = bstack11111ll1_opy_
  bstack11ll111ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1lll11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1llll1ll_opy_
  global bstack1lllll11_opy_
  bstack11l1l1l11_opy_ = copy.deepcopy(item)
  if not bstack1ll1ll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ଼") in item.options:
    bstack11l1l1l11_opy_.options[bstack1ll1ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩଽ")] = []
  bstack1lll1111l_opy_ = bstack11l1l1l11_opy_.options[bstack1ll1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪା")].copy()
  for v in bstack11l1l1l11_opy_.options[bstack1ll1ll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫି")]:
    if bstack1ll1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩୀ") in v:
      bstack1lll1111l_opy_.remove(v)
    if bstack1ll1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫୁ") in v:
      bstack1lll1111l_opy_.remove(v)
    if bstack1ll1ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩୂ") in v:
      bstack1lll1111l_opy_.remove(v)
  bstack1lll1111l_opy_.insert(0, bstack1ll1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜࠿ࢁࡽࠨୃ").format(bstack11l1l1l11_opy_.platform_index))
  bstack1lll1111l_opy_.insert(0, bstack1ll1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧୄ").format(bstack11l1l1l11_opy_.bstack1l1l111l1_opy_))
  bstack11l1l1l11_opy_.options[bstack1ll1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ୅")] = bstack1lll1111l_opy_
  if bstack1lllll11_opy_:
    bstack11l1l1l11_opy_.options[bstack1ll1ll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ୆")].insert(0, bstack1ll1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ࠽ࡿࢂ࠭େ").format(bstack1lllll11_opy_))
  return bstack1l1llll1ll_opy_(caller_id, datasources, is_last, bstack11l1l1l11_opy_, outs_dir)
def bstack11ll11ll1_opy_(command, item_index):
  if bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬୈ")):
    os.environ[bstack1ll1ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭୉")] = json.dumps(CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୊")][item_index % bstack1lll11lll1_opy_])
  global bstack1lllll11_opy_
  if bstack1lllll11_opy_:
    command[0] = command[0].replace(bstack1ll1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ୋ"), bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬୌ") + str(
      item_index) + bstack1ll1ll_opy_ (u"୍ࠩࠣࠫ") + bstack1lllll11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ୎"),
                                    bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ୏") + str(item_index), 1)
def bstack11l1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1ll1ll1l_opy_
  bstack11ll11ll1_opy_(command, item_index)
  return bstack1l1ll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l111llll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1ll1ll1l_opy_
  bstack11ll11ll1_opy_(command, item_index)
  return bstack1l1ll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1ll1ll1l_opy_
  bstack11ll11ll1_opy_(command, item_index)
  return bstack1l1ll1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1llll1ll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll11lllll_opy_
  bstack1l1111lll1_opy_ = bstack1ll11lllll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll1ll_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡠࡣࡵࡶࠬ୐")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1ll_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰࡥࡡࡳࡴࠪ୑")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1111lll1_opy_
def bstack111111lll_opy_(runner, hook_name, context, element, bstack1111l1ll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1ll11ll_opy_.bstack1l111l11ll_opy_(hook_name, element)
    bstack1111l1ll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1ll11ll_opy_.bstack111l111ll_opy_(element)
      if hook_name not in [bstack1ll1ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ୒"), bstack1ll1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫ୓")] and args and hasattr(args[0], bstack1ll1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩ୔")):
        args[0].error_message = bstack1ll1ll_opy_ (u"ࠪࠫ୕")
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡩࡣࡱࡨࡱ࡫ࠠࡩࡱࡲ࡯ࡸࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ୖ").format(str(e)))
def bstack1l1ll1ll_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    if runner.hooks.get(bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤୗ")).__name__ != bstack1ll1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ୘"):
      bstack111111lll_opy_(runner, name, context, runner, bstack1111l1ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l111ll111_opy_(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭୙")) else context.browser
      runner.driver_initialised = bstack1ll1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ୚")
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭୛").format(str(e)))
def bstack1l1111111l_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    bstack111111lll_opy_(runner, name, context, context.feature, bstack1111l1ll_opy_, *args)
    try:
      if not bstack1ll1llll11_opy_:
        bstack11lllll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll111_opy_(bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଡ଼")) else context.browser
        if is_driver_active(bstack11lllll1l1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧଢ଼")
          bstack1ll1l1lll1_opy_ = str(runner.feature.name)
          bstack11ll1l111_opy_(context, bstack1ll1l1lll1_opy_)
          bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ୞") + json.dumps(bstack1ll1l1lll1_opy_) + bstack1ll1ll_opy_ (u"࠭ࡽࡾࠩୟ"))
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧୠ").format(str(e)))
def bstack1l1111lll_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    if hasattr(context, bstack1ll1ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪୡ")):
        bstack1ll1ll11ll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1ll1ll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫୢ")) else context.feature
    bstack111111lll_opy_(runner, name, context, target, bstack1111l1ll_opy_, *args)
def bstack1lll1ll1ll_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1ll11ll_opy_.start_test(context)
    bstack111111lll_opy_(runner, name, context, context.scenario, bstack1111l1ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll1l1l1ll_opy_.bstack1l11lll11_opy_(context, *args)
    try:
      bstack11lllll1l1_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩୣ"), context.browser)
      if is_driver_active(bstack11lllll1l1_opy_):
        bstack1llll1ll_opy_.bstack1ll1l1ll1_opy_(bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ୤"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ୥")
        if (not bstack1ll1llll11_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1l1lll1_opy_ = str(runner.feature.name)
          bstack1ll1l1lll1_opy_ = feature_name + bstack1ll1ll_opy_ (u"࠭ࠠ࠮ࠢࠪ୦") + scenario_name
          if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୧"):
            bstack11ll1l111_opy_(context, bstack1ll1l1lll1_opy_)
            bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭୨") + json.dumps(bstack1ll1l1lll1_opy_) + bstack1ll1ll_opy_ (u"ࠩࢀࢁࠬ୩"))
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ୪").format(str(e)))
def bstack1l1l1ll111_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    bstack111111lll_opy_(runner, name, context, args[0], bstack1111l1ll_opy_, *args)
    try:
      bstack11lllll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll111_opy_(bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ୫")) else context.browser
      if is_driver_active(bstack11lllll1l1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ୬")
        bstack1ll1ll11ll_opy_.bstack111ll11l1_opy_(args[0])
        if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ୭"):
          feature_name = bstack1ll1l1lll1_opy_ = str(runner.feature.name)
          bstack1ll1l1lll1_opy_ = feature_name + bstack1ll1ll_opy_ (u"ࠧࠡ࠯ࠣࠫ୮") + context.scenario.name
          bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭୯") + json.dumps(bstack1ll1l1lll1_opy_) + bstack1ll1ll_opy_ (u"ࠩࢀࢁࠬ୰"))
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧୱ").format(str(e)))
def bstack11l1l1111_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
  bstack1ll1ll11ll_opy_.bstack1l111111l_opy_(args[0])
  try:
    bstack1111lll1l_opy_ = args[0].status.name
    bstack11lllll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ୲") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11lllll1l1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll1ll_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ୳")
        feature_name = bstack1ll1l1lll1_opy_ = str(runner.feature.name)
        bstack1ll1l1lll1_opy_ = feature_name + bstack1ll1ll_opy_ (u"࠭ࠠ࠮ࠢࠪ୴") + context.scenario.name
        bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ୵") + json.dumps(bstack1ll1l1lll1_opy_) + bstack1ll1ll_opy_ (u"ࠨࡿࢀࠫ୶"))
    if str(bstack1111lll1l_opy_).lower() == bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୷"):
      bstack11llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫ୸")
      bstack1lll11l111_opy_ = bstack1ll1ll_opy_ (u"ࠫࠬ୹")
      bstack11l1ll11_opy_ = bstack1ll1ll_opy_ (u"ࠬ࠭୺")
      try:
        import traceback
        bstack11llllll11_opy_ = runner.exception.__class__.__name__
        bstack1l1ll111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll11l111_opy_ = bstack1ll1ll_opy_ (u"࠭ࠠࠨ୻").join(bstack1l1ll111l_opy_)
        bstack11l1ll11_opy_ = bstack1l1ll111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1ll11l1_opy_.format(str(e)))
      bstack11llllll11_opy_ += bstack11l1ll11_opy_
      bstack1l11l1l1l1_opy_(context, json.dumps(str(args[0].name) + bstack1ll1ll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ୼") + str(bstack1lll11l111_opy_)),
                          bstack1ll1ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ୽"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ୾"):
        bstack11l1111l_opy_(getattr(context, bstack1ll1ll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ୿"), None), bstack1ll1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ஀"), bstack11llllll11_opy_)
        bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ஁") + json.dumps(str(args[0].name) + bstack1ll1ll_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧஂ") + str(bstack1lll11l111_opy_)) + bstack1ll1ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧஃ"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ஄"):
        bstack11l1llll_opy_(bstack11lllll1l1_opy_, bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஅ"), bstack1ll1ll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢஆ") + str(bstack11llllll11_opy_))
    else:
      bstack1l11l1l1l1_opy_(context, bstack1ll1ll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧஇ"), bstack1ll1ll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥஈ"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦஉ"):
        bstack11l1111l_opy_(getattr(context, bstack1ll1ll_opy_ (u"ࠧࡱࡣࡪࡩࠬஊ"), None), bstack1ll1ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ஋"))
      bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ஌") + json.dumps(str(args[0].name) + bstack1ll1ll_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ஍")) + bstack1ll1ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪஎ"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥஏ"):
        bstack11l1llll_opy_(bstack11lllll1l1_opy_, bstack1ll1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨஐ"))
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭஑").format(str(e)))
  bstack111111lll_opy_(runner, name, context, args[0], bstack1111l1ll_opy_, *args)
def bstack1ll1111l_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
  bstack1ll1ll11ll_opy_.end_test(args[0])
  try:
    bstack1l1ll1l11l_opy_ = args[0].status.name
    bstack11lllll1l1_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧஒ"), context.browser)
    bstack1ll1l1l1ll_opy_.bstack1ll1ll111_opy_(bstack11lllll1l1_opy_)
    if str(bstack1l1ll1l11l_opy_).lower() == bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஓ"):
      bstack11llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫஔ")
      bstack1lll11l111_opy_ = bstack1ll1ll_opy_ (u"ࠫࠬக")
      bstack11l1ll11_opy_ = bstack1ll1ll_opy_ (u"ࠬ࠭஖")
      try:
        import traceback
        bstack11llllll11_opy_ = runner.exception.__class__.__name__
        bstack1l1ll111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll11l111_opy_ = bstack1ll1ll_opy_ (u"࠭ࠠࠨ஗").join(bstack1l1ll111l_opy_)
        bstack11l1ll11_opy_ = bstack1l1ll111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1ll11l1_opy_.format(str(e)))
      bstack11llllll11_opy_ += bstack11l1ll11_opy_
      bstack1l11l1l1l1_opy_(context, json.dumps(str(args[0].name) + bstack1ll1ll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ஘") + str(bstack1lll11l111_opy_)),
                          bstack1ll1ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢங"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦச") or runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ஛"):
        bstack11l1111l_opy_(getattr(context, bstack1ll1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩஜ"), None), bstack1ll1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ஝"), bstack11llllll11_opy_)
        bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫஞ") + json.dumps(str(args[0].name) + bstack1ll1ll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨட") + str(bstack1lll11l111_opy_)) + bstack1ll1ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ஠"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ஡") or runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ஢"):
        bstack11l1llll_opy_(bstack11lllll1l1_opy_, bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫண"), bstack1ll1ll_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤத") + str(bstack11llllll11_opy_))
    else:
      bstack1l11l1l1l1_opy_(context, bstack1ll1ll_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ஥"), bstack1ll1ll_opy_ (u"ࠢࡪࡰࡩࡳࠧ஦"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ஧") or runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩந"):
        bstack11l1111l_opy_(getattr(context, bstack1ll1ll_opy_ (u"ࠪࡴࡦ࡭ࡥࠨன"), None), bstack1ll1ll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦப"))
      bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ஫") + json.dumps(str(args[0].name) + bstack1ll1ll_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥ஬")) + bstack1ll1ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭஭"))
      if runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥம") or runner.driver_initialised == bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩய"):
        bstack11l1llll_opy_(bstack11lllll1l1_opy_, bstack1ll1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥர"))
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ற").format(str(e)))
  bstack111111lll_opy_(runner, name, context, context.scenario, bstack1111l1ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1lllll1ll1_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1ll1ll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧல")) else context.feature
    bstack111111lll_opy_(runner, name, context, target, bstack1111l1ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11llll111_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    try:
      bstack11lllll1l1_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬள"), context.browser)
      if context.failed is True:
        bstack11lllll11_opy_ = []
        bstack11lll1l11_opy_ = []
        bstack1ll1lll11l_opy_ = []
        bstack1l11ll1ll_opy_ = bstack1ll1ll_opy_ (u"ࠧࠨழ")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11lllll11_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1ll111l_opy_ = traceback.format_tb(exc_tb)
            bstack1lll11lll_opy_ = bstack1ll1ll_opy_ (u"ࠨࠢࠪவ").join(bstack1l1ll111l_opy_)
            bstack11lll1l11_opy_.append(bstack1lll11lll_opy_)
            bstack1ll1lll11l_opy_.append(bstack1l1ll111l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1ll11l1_opy_.format(str(e)))
        bstack11llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪஶ")
        for i in range(len(bstack11lllll11_opy_)):
          bstack11llllll11_opy_ += bstack11lllll11_opy_[i] + bstack1ll1lll11l_opy_[i] + bstack1ll1ll_opy_ (u"ࠪࡠࡳ࠭ஷ")
        bstack1l11ll1ll_opy_ = bstack1ll1ll_opy_ (u"ࠫࠥ࠭ஸ").join(bstack11lll1l11_opy_)
        if runner.driver_initialised in [bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨஹ"), bstack1ll1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ஺")]:
          bstack1l11l1l1l1_opy_(context, bstack1l11ll1ll_opy_, bstack1ll1ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ஻"))
          bstack11l1111l_opy_(getattr(context, bstack1ll1ll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭஼"), None), bstack1ll1ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ஽"), bstack11llllll11_opy_)
          bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨா") + json.dumps(bstack1l11ll1ll_opy_) + bstack1ll1ll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫி"))
          bstack11l1llll_opy_(bstack11lllll1l1_opy_, bstack1ll1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧீ"), bstack1ll1ll_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦு") + str(bstack11llllll11_opy_))
          bstack11lll11lll_opy_ = bstack1l1ll111l1_opy_(bstack1l11ll1ll_opy_, runner.feature.name, logger)
          if (bstack11lll11lll_opy_ != None):
            bstack1l1ll1l1_opy_.append(bstack11lll11lll_opy_)
      else:
        if runner.driver_initialised in [bstack1ll1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣூ"), bstack1ll1ll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ௃")]:
          bstack1l11l1l1l1_opy_(context, bstack1ll1ll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ௄") + str(runner.feature.name) + bstack1ll1ll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ௅"), bstack1ll1ll_opy_ (u"ࠦ࡮ࡴࡦࡰࠤெ"))
          bstack11l1111l_opy_(getattr(context, bstack1ll1ll_opy_ (u"ࠬࡶࡡࡨࡧࠪே"), None), bstack1ll1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨை"))
          bstack11lllll1l1_opy_.execute_script(bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௉") + json.dumps(bstack1ll1ll_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦொ") + str(runner.feature.name) + bstack1ll1ll_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦோ")) + bstack1ll1ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩௌ"))
          bstack11l1llll_opy_(bstack11lllll1l1_opy_, bstack1ll1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧ்ࠫ"))
          bstack11lll11lll_opy_ = bstack1l1ll111l1_opy_(bstack1l11ll1ll_opy_, runner.feature.name, logger)
          if (bstack11lll11lll_opy_ != None):
            bstack1l1ll1l1_opy_.append(bstack11lll11lll_opy_)
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ௎").format(str(e)))
    bstack111111lll_opy_(runner, name, context, context.feature, bstack1111l1ll_opy_, *args)
def bstack1lllll1ll_opy_(runner, name, context, bstack1111l1ll_opy_, *args):
    bstack111111lll_opy_(runner, name, context, runner, bstack1111l1ll_opy_, *args)
def bstack1lll11ll1l_opy_(self, name, context, *args):
  if bstack1llll111l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1lll11lll1_opy_
    bstack1111l1lll_opy_ = CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௏")][platform_index]
    os.environ[bstack1ll1ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨௐ")] = json.dumps(bstack1111l1lll_opy_)
  global bstack1111l1ll_opy_
  if not hasattr(self, bstack1ll1ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࡩ࠭௑")):
    self.driver_initialised = None
  bstack1ll1111l1l_opy_ = {
      bstack1ll1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭௒"): bstack1l1ll1ll_opy_,
      bstack1ll1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ௓"): bstack1l1111111l_opy_,
      bstack1ll1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡹࡧࡧࠨ௔"): bstack1l1111lll_opy_,
      bstack1ll1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௕"): bstack1lll1ll1ll_opy_,
      bstack1ll1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠫ௖"): bstack1l1l1ll111_opy_,
      bstack1ll1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫௗ"): bstack11l1l1111_opy_,
      bstack1ll1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ௘"): bstack1ll1111l_opy_,
      bstack1ll1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡶࡤ࡫ࠬ௙"): bstack1lllll1ll1_opy_,
      bstack1ll1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪ௚"): bstack11llll111_opy_,
      bstack1ll1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ௛"): bstack1lllll1ll_opy_
  }
  handler = bstack1ll1111l1l_opy_.get(name, bstack1111l1ll_opy_)
  handler(self, name, context, bstack1111l1ll_opy_, *args)
  if name in [bstack1ll1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ௜"), bstack1ll1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௝"), bstack1ll1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ௞")]:
    try:
      bstack11lllll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll111_opy_(bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௟")) else context.browser
      bstack1ll11ll111_opy_ = (
        (name == bstack1ll1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ௠") and self.driver_initialised == bstack1ll1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ௡")) or
        (name == bstack1ll1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫ௢") and self.driver_initialised == bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ௣")) or
        (name == bstack1ll1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௤") and self.driver_initialised in [bstack1ll1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ௥"), bstack1ll1ll_opy_ (u"ࠣ࡫ࡱࡷࡹ࡫ࡰࠣ௦")]) or
        (name == bstack1ll1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡷࡩࡵ࠭௧") and self.driver_initialised == bstack1ll1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௨"))
      )
      if bstack1ll11ll111_opy_:
        self.driver_initialised = None
        bstack11lllll1l1_opy_.quit()
    except Exception:
      pass
def bstack1ll11lll1_opy_(config, startdir):
  return bstack1ll1ll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤ௩").format(bstack1ll1ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ௪"))
notset = Notset()
def bstack1llll1ll1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll111ll1_opy_
  if str(name).lower() == bstack1ll1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭௫"):
    return bstack1ll1ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ௬")
  else:
    return bstack1ll111ll1_opy_(self, name, default, skip)
def bstack1llll1llll_opy_(item, when):
  global bstack1llll11l1_opy_
  try:
    bstack1llll11l1_opy_(item, when)
  except Exception as e:
    pass
def bstack111l11ll_opy_():
  return
def bstack1ll1l111l_opy_(type, name, status, reason, bstack1l1l111l11_opy_, bstack1ll11l1ll_opy_):
  bstack1lll1lll11_opy_ = {
    bstack1ll1ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ௭"): type,
    bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ௮"): {}
  }
  if type == bstack1ll1ll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ௯"):
    bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ௰")][bstack1ll1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ௱")] = bstack1l1l111l11_opy_
    bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ௲")][bstack1ll1ll_opy_ (u"ࠧࡥࡣࡷࡥࠬ௳")] = json.dumps(str(bstack1ll11l1ll_opy_))
  if type == bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௴"):
    bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ௵")][bstack1ll1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ௶")] = name
  if type == bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ௷"):
    bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ௸")][bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭௹")] = status
    if status == bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ௺"):
      bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ௻")][bstack1ll1ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ௼")] = json.dumps(str(reason))
  bstack1lll111l1_opy_ = bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ௽").format(json.dumps(bstack1lll1lll11_opy_))
  return bstack1lll111l1_opy_
def bstack1111111ll_opy_(driver_command, response):
    if driver_command == bstack1ll1ll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ௾"):
        bstack1llll1ll_opy_.bstack1llllllll_opy_({
            bstack1ll1ll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ௿"): response[bstack1ll1ll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬఀ")],
            bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧఁ"): bstack1llll1ll_opy_.current_test_uuid()
        })
def bstack1lll1l1ll1_opy_(item, call, rep):
  global bstack1l1111111_opy_
  global bstack11llllll1_opy_
  global bstack1ll1llll11_opy_
  name = bstack1ll1ll_opy_ (u"ࠨࠩం")
  try:
    if rep.when == bstack1ll1ll_opy_ (u"ࠩࡦࡥࡱࡲࠧః"):
      bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1llll11_opy_:
          name = str(rep.nodeid)
          bstack11llll1l_opy_ = bstack1ll1l111l_opy_(bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫఄ"), name, bstack1ll1ll_opy_ (u"ࠫࠬఅ"), bstack1ll1ll_opy_ (u"ࠬ࠭ఆ"), bstack1ll1ll_opy_ (u"࠭ࠧఇ"), bstack1ll1ll_opy_ (u"ࠧࠨఈ"))
          threading.current_thread().bstack111lllll1_opy_ = name
          for driver in bstack11llllll1_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack11llll1l_opy_)
      except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨఉ").format(str(e)))
      try:
        bstack1ll1l1ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪఊ"):
          status = bstack1ll1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఋ") if rep.outcome.lower() == bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫఌ") else bstack1ll1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ఍")
          reason = bstack1ll1ll_opy_ (u"࠭ࠧఎ")
          if status == bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఏ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ఐ") if status == bstack1ll1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ఑") else bstack1ll1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩఒ")
          data = name + bstack1ll1ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ఓ") if status == bstack1ll1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఔ") else name + bstack1ll1ll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩక") + reason
          bstack111l1l11l_opy_ = bstack1ll1l111l_opy_(bstack1ll1ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩఖ"), bstack1ll1ll_opy_ (u"ࠨࠩగ"), bstack1ll1ll_opy_ (u"ࠩࠪఘ"), bstack1ll1ll_opy_ (u"ࠪࠫఙ"), level, data)
          for driver in bstack11llllll1_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack111l1l11l_opy_)
      except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨచ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩఛ").format(str(e)))
  bstack1l1111111_opy_(item, call, rep)
def bstack1l111ll1l1_opy_(driver, bstack11ll1l1l1_opy_, test=None):
  global bstack1l111l111_opy_
  if test != None:
    bstack11111llll_opy_ = getattr(test, bstack1ll1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫజ"), None)
    bstack11l1l11l1_opy_ = getattr(test, bstack1ll1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬఝ"), None)
    PercySDK.screenshot(driver, bstack11ll1l1l1_opy_, bstack11111llll_opy_=bstack11111llll_opy_, bstack11l1l11l1_opy_=bstack11l1l11l1_opy_, bstack11lll11l1l_opy_=bstack1l111l111_opy_)
  else:
    PercySDK.screenshot(driver, bstack11ll1l1l1_opy_)
def bstack11lll11ll1_opy_(driver):
  if bstack1ll1llllll_opy_.bstack1l11ll11l1_opy_() is True or bstack1ll1llllll_opy_.capturing() is True:
    return
  bstack1ll1llllll_opy_.bstack1l1lll1l1_opy_()
  while not bstack1ll1llllll_opy_.bstack1l11ll11l1_opy_():
    bstack1l1ll111_opy_ = bstack1ll1llllll_opy_.bstack1l1l11111_opy_()
    bstack1l111ll1l1_opy_(driver, bstack1l1ll111_opy_)
  bstack1ll1llllll_opy_.bstack111l111l1_opy_()
def bstack1l11l1ll11_opy_(sequence, driver_command, response = None, bstack111ll11ll_opy_ = None, args = None):
    try:
      if sequence != bstack1ll1ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨఞ"):
        return
      if percy.bstack1l1l11ll11_opy_() == bstack1ll1ll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣట"):
        return
      bstack1l1ll111_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఠ"), None)
      for command in bstack111ll111_opy_:
        if command == driver_command:
          for driver in bstack11llllll1_opy_:
            bstack11lll11ll1_opy_(driver)
      bstack1l11lllll1_opy_ = percy.bstack1l1ll1llll_opy_()
      if driver_command in bstack1ll11l1111_opy_[bstack1l11lllll1_opy_]:
        bstack1ll1llllll_opy_.bstack1l1l1l11_opy_(bstack1l1ll111_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1ll1l1ll_opy_(framework_name):
  if bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨడ")):
      return
  bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩఢ"), True)
  global bstack11lllllll_opy_
  global bstack1lllll1111_opy_
  global bstack111lll1l_opy_
  bstack11lllllll_opy_ = framework_name
  logger.info(bstack1l11l111l1_opy_.format(bstack11lllllll_opy_.split(bstack1ll1ll_opy_ (u"࠭࠭ࠨణ"))[0]))
  bstack11lll1ll1l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1llll111l_opy_:
      Service.start = bstack1l11ll11_opy_
      Service.stop = bstack1l1lll1l_opy_
      webdriver.Remote.get = bstack1l1ll1l1l_opy_
      WebDriver.close = bstack1lll1llll1_opy_
      WebDriver.quit = bstack111ll111l_opy_
      webdriver.Remote.__init__ = bstack1lll1111ll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1llll111l_opy_:
        webdriver.Remote.__init__ = bstack1l111111_opy_
    WebDriver.execute = bstack1ll1l111ll_opy_
    bstack1lllll1111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1llll111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11l1ll111_opy_
  except Exception as e:
    pass
  bstack1ll11ll1l1_opy_()
  if not bstack1lllll1111_opy_:
    bstack1l1l1ll1l_opy_(bstack1ll1ll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤత"), bstack1l1llllll_opy_)
  if bstack1l1llllll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1llll1l1ll_opy_ = bstack1l1ll11ll_opy_
    except Exception as e:
      logger.error(bstack1lll11ll_opy_.format(str(e)))
  if bstack1ll11l111l_opy_():
    bstack1lllllll1_opy_(CONFIG, logger)
  if (bstack1ll1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧథ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1l1l11ll11_opy_() == bstack1ll1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢద"):
          bstack11llll11l1_opy_(bstack1l11l1ll11_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll1ll1ll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1llll1l1_opy_
      except Exception as e:
        logger.warn(bstack1llll111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1lll1lll1_opy_
        bstack1lll1lll1_opy_.close = bstack1l111l11l_opy_
      except Exception as e:
        logger.debug(bstack11l111l11_opy_ + str(e))
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1llll111_opy_)
    Output.start_test = bstack1ll1l11ll1_opy_
    Output.end_test = bstack111ll1111_opy_
    TestStatus.__init__ = bstack11lll111l1_opy_
    QueueItem.__init__ = bstack1l1ll111ll_opy_
    pabot._create_items = bstack1ll111l1l_opy_
    try:
      from pabot import __version__ as bstack11ll11l11_opy_
      if version.parse(bstack11ll11l11_opy_) >= version.parse(bstack1ll1ll_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪధ")):
        pabot._run = bstack1l1l11l11_opy_
      elif version.parse(bstack11ll11l11_opy_) >= version.parse(bstack1ll1ll_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫన")):
        pabot._run = bstack1l111llll1_opy_
      else:
        pabot._run = bstack11l1l1lll_opy_
    except Exception as e:
      pabot._run = bstack11l1l1lll_opy_
    pabot._create_command_for_execution = bstack1l1lll11l1_opy_
    pabot._report_results = bstack111llll11_opy_
  if bstack1ll1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ఩") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1l11ll1111_opy_)
    Runner.run_hook = bstack1lll11ll1l_opy_
    Step.run = bstack1llll1ll1_opy_
  if bstack1ll1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ప") in str(framework_name).lower():
    if not bstack1llll111l_opy_:
      return
    try:
      if percy.bstack1l1l11ll11_opy_() == bstack1ll1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧఫ"):
          bstack11llll11l1_opy_(bstack1l11l1ll11_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll11lll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111l11ll_opy_
      Config.getoption = bstack1llll1ll1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lll1l1ll1_opy_
    except Exception as e:
      pass
def bstack11111l1ll_opy_():
  global CONFIG
  if bstack1ll1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨబ") in CONFIG and int(CONFIG[bstack1ll1ll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩభ")]) > 1:
    logger.warn(bstack111ll1l11_opy_)
def bstack111l11ll1_opy_(arg, bstack1llll1l11_opy_, bstack1l1ll1111l_opy_=None):
  global CONFIG
  global bstack1llll11111_opy_
  global bstack1l1111l11l_opy_
  global bstack1llll111l_opy_
  global bstack1l1l1l1ll_opy_
  bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪమ")
  if bstack1llll1l11_opy_ and isinstance(bstack1llll1l11_opy_, str):
    bstack1llll1l11_opy_ = eval(bstack1llll1l11_opy_)
  CONFIG = bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫయ")]
  bstack1llll11111_opy_ = bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ర")]
  bstack1l1111l11l_opy_ = bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨఱ")]
  bstack1llll111l_opy_ = bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪల")]
  bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩళ"), bstack1llll111l_opy_)
  os.environ[bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫఴ")] = bstack11111l111_opy_
  os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩవ")] = json.dumps(CONFIG)
  os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫశ")] = bstack1llll11111_opy_
  os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ష")] = str(bstack1l1111l11l_opy_)
  os.environ[bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬస")] = str(True)
  if bstack111l1111_opy_(arg, [bstack1ll1ll_opy_ (u"ࠧ࠮ࡰࠪహ"), bstack1ll1ll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ఺")]) != -1:
    os.environ[bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ఻")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll11l1l_opy_)
    return
  bstack11llll1l1l_opy_()
  global bstack11l11ll1l_opy_
  global bstack1l111l111_opy_
  global bstack11l1lll1l_opy_
  global bstack1lllll11_opy_
  global bstack1lll1l1l11_opy_
  global bstack111lll1l_opy_
  global bstack1l1111l1_opy_
  arg.append(bstack1ll1ll_opy_ (u"ࠥ࠱࡜ࠨ఼"))
  arg.append(bstack1ll1ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢఽ"))
  arg.append(bstack1ll1ll_opy_ (u"ࠧ࠳ࡗࠣా"))
  arg.append(bstack1ll1ll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧి"))
  global bstack11111111l_opy_
  global bstack1l11111l1_opy_
  global bstack1111l111l_opy_
  global bstack11ll1l11_opy_
  global bstack11111l1l1_opy_
  global bstack11ll111ll_opy_
  global bstack1l1llll1ll_opy_
  global bstack1l11llll1l_opy_
  global bstack11lll11l11_opy_
  global bstack1l11lll111_opy_
  global bstack1ll111ll1_opy_
  global bstack1llll11l1_opy_
  global bstack1l1111111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11111111l_opy_ = webdriver.Remote.__init__
    bstack1l11111l1_opy_ = WebDriver.quit
    bstack1l11llll1l_opy_ = WebDriver.close
    bstack11lll11l11_opy_ = WebDriver.get
    bstack1111l111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111lllll_opy_(CONFIG) and bstack1lll11l1ll_opy_():
    if bstack1l11llllll_opy_() < version.parse(bstack11ll11111_opy_):
      logger.error(bstack1ll1l1111l_opy_.format(bstack1l11llllll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l11lll111_opy_ = RemoteConnection._1llll1l1ll_opy_
      except Exception as e:
        logger.error(bstack1lll11ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll111ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1llll11l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l111l1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1111111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll1ll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨీ"))
  bstack11l1lll1l_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬు"), {}).get(bstack1ll1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫూ"))
  bstack1l1111l1_opy_ = True
  bstack1l1ll1l1ll_opy_(bstack1ll111111l_opy_)
  os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫృ")] = CONFIG[bstack1ll1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ౄ")]
  os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ౅")] = CONFIG[bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩె")]
  os.environ[bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪే")] = bstack1llll111l_opy_.__str__()
  from _pytest.config import main as bstack1ll1ll1111_opy_
  bstack111111ll_opy_ = []
  try:
    bstack1l111111l1_opy_ = bstack1ll1ll1111_opy_(arg)
    if bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬై") in multiprocessing.current_process().__dict__.keys():
      for bstack11l11l11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111111ll_opy_.append(bstack11l11l11l_opy_)
    try:
      bstack1l1l1l111l_opy_ = (bstack111111ll_opy_, int(bstack1l111111l1_opy_))
      bstack1l1ll1111l_opy_.append(bstack1l1l1l111l_opy_)
    except:
      bstack1l1ll1111l_opy_.append((bstack111111ll_opy_, bstack1l111111l1_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack111111ll_opy_.append({bstack1ll1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౉"): bstack1ll1ll_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬొ") + os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫో")), bstack1ll1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫౌ"): traceback.format_exc(), bstack1ll1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ్ࠬ"): int(os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ౎")))})
    bstack1l1ll1111l_opy_.append((bstack111111ll_opy_, 1))
def bstack1l11l1l1_opy_(arg):
  global bstack11ll1lll1_opy_
  bstack1l1ll1l1ll_opy_(bstack11llll11ll_opy_)
  os.environ[bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ౏")] = str(bstack1l1111l11l_opy_)
  from behave.__main__ import main as bstack1l1l1l1l1_opy_
  status_code = bstack1l1l1l1l1_opy_(arg)
  if status_code != 0:
    bstack11ll1lll1_opy_ = status_code
def bstack1lll111111_opy_():
  logger.info(bstack1lll1ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ౐"), help=bstack1ll1ll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ౑"))
  parser.add_argument(bstack1ll1ll_opy_ (u"ࠫ࠲ࡻࠧ౒"), bstack1ll1ll_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ౓"), help=bstack1ll1ll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ౔"))
  parser.add_argument(bstack1ll1ll_opy_ (u"ࠧ࠮࡭ౕࠪ"), bstack1ll1ll_opy_ (u"ࠨ࠯࠰࡯ࡪࡿౖࠧ"), help=bstack1ll1ll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ౗"))
  parser.add_argument(bstack1ll1ll_opy_ (u"ࠪ࠱࡫࠭ౘ"), bstack1ll1ll_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩౙ"), help=bstack1ll1ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫౚ"))
  bstack1lll1l1111_opy_ = parser.parse_args()
  try:
    bstack1ll111ll11_opy_ = bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ౛")
    if bstack1lll1l1111_opy_.framework and bstack1lll1l1111_opy_.framework not in (bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౜"), bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩౝ")):
      bstack1ll111ll11_opy_ = bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ౞")
    bstack11ll1lllll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll111ll11_opy_)
    bstack11ll1111l_opy_ = open(bstack11ll1lllll_opy_, bstack1ll1ll_opy_ (u"ࠪࡶࠬ౟"))
    bstack1llll11l1l_opy_ = bstack11ll1111l_opy_.read()
    bstack11ll1111l_opy_.close()
    if bstack1lll1l1111_opy_.username:
      bstack1llll11l1l_opy_ = bstack1llll11l1l_opy_.replace(bstack1ll1ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫౠ"), bstack1lll1l1111_opy_.username)
    if bstack1lll1l1111_opy_.key:
      bstack1llll11l1l_opy_ = bstack1llll11l1l_opy_.replace(bstack1ll1ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧౡ"), bstack1lll1l1111_opy_.key)
    if bstack1lll1l1111_opy_.framework:
      bstack1llll11l1l_opy_ = bstack1llll11l1l_opy_.replace(bstack1ll1ll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧౢ"), bstack1lll1l1111_opy_.framework)
    file_name = bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪౣ")
    file_path = os.path.abspath(file_name)
    bstack1lll111l1l_opy_ = open(file_path, bstack1ll1ll_opy_ (u"ࠨࡹࠪ౤"))
    bstack1lll111l1l_opy_.write(bstack1llll11l1l_opy_)
    bstack1lll111l1l_opy_.close()
    logger.info(bstack11ll1l11l_opy_)
    try:
      os.environ[bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ౥")] = bstack1lll1l1111_opy_.framework if bstack1lll1l1111_opy_.framework != None else bstack1ll1ll_opy_ (u"ࠥࠦ౦")
      config = yaml.safe_load(bstack1llll11l1l_opy_)
      config[bstack1ll1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ౧")] = bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫ౨")
      bstack1l111l11l1_opy_(bstack1l11lll1l1_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll1ll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11l1lll1_opy_.format(str(e)))
def bstack1l111l11l1_opy_(bstack1111l11l1_opy_, config, bstack1l1lllll1l_opy_={}):
  global bstack1llll111l_opy_
  global bstack1lll11l11_opy_
  global bstack1l1l1l1ll_opy_
  if not config:
    return
  bstack11l11l111_opy_ = bstack1l1111l1l1_opy_ if not bstack1llll111l_opy_ else (
    bstack1l1llll1_opy_ if bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲࠪ౩") in config else (
        bstack111l1l11_opy_ if config.get(bstack1ll1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ౪")) else bstack1ll11ll1_opy_
    )
)
  bstack1l111lllll_opy_ = False
  bstack1l111lll_opy_ = False
  if bstack1llll111l_opy_ is True:
      if bstack1ll1ll_opy_ (u"ࠨࡣࡳࡴࠬ౫") in config:
          bstack1l111lllll_opy_ = True
      else:
          bstack1l111lll_opy_ = True
  bstack11l1l11ll_opy_ = bstack1ll1l111l1_opy_.bstack1l11l11l1l_opy_(config, bstack1lll11l11_opy_)
  data = {
    bstack1ll1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ౬"): config[bstack1ll1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ౭")],
    bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ౮"): config[bstack1ll1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ౯")],
    bstack1ll1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ౰"): bstack1111l11l1_opy_,
    bstack1ll1ll_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ౱"): os.environ.get(bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ౲"), bstack1lll11l11_opy_),
    bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ౳"): bstack1lll11l11l_opy_,
    bstack1ll1ll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬ౴"): bstack111lll111_opy_(),
    bstack1ll1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ౵"): {
      bstack1ll1ll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౶"): str(config[bstack1ll1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭౷")]) if bstack1ll1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ౸") in config else bstack1ll1ll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ౹"),
      bstack1ll1ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ౺"): sys.version,
      bstack1ll1ll_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ౻"): bstack1l11l1l111_opy_(os.getenv(bstack1ll1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨ౼"), bstack1ll1ll_opy_ (u"ࠧࠨ౽"))),
      bstack1ll1ll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ౾"): bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౿"),
      bstack1ll1ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩಀ"): bstack11l11l111_opy_,
      bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧಁ"): bstack11l1l11ll_opy_,
      bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩಂ"): os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩಃ")],
      bstack1ll1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ಄"): bstack1l11lllll_opy_(os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಅ"), bstack1lll11l11_opy_)),
      bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪಆ"): config[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಇ")] if config[bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬಈ")] else bstack1ll1ll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦಉ"),
      bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಊ"): str(config[bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಋ")]) if bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಌ") in config else bstack1ll1ll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ಍"),
      bstack1ll1ll_opy_ (u"ࠨࡱࡶࠫಎ"): sys.platform,
      bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫಏ"): socket.gethostname(),
      bstack1ll1ll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬಐ"): bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭಑"))
    }
  }
  if not bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬಒ")) is None:
    data[bstack1ll1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩಓ")][bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪಔ")] = {
      bstack1ll1ll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨಕ"): bstack1ll1ll_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧಖ"),
      bstack1ll1ll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪಗ"): bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫಘ")),
      bstack1ll1ll_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫಙ"): bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩಚ"))
    }
  if bstack1111l11l1_opy_ == bstack1llllll111_opy_:
    data[bstack1ll1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪಛ")][bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭ಜ")] = bstack1111ll11l_opy_(config)
    data[bstack1ll1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಝ")][bstack1ll1ll_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨಞ")] = percy.bstack11l11lll_opy_
    data[bstack1ll1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧಟ")][bstack1ll1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫಠ")] = percy.bstack11l1111ll_opy_
  update(data[bstack1ll1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩಡ")], bstack1l1lllll1l_opy_)
  try:
    response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"ࠧࡑࡑࡖࡘࠬಢ"), bstack1l1l1lll1l_opy_(bstack1l1111l1ll_opy_), data, {
      bstack1ll1ll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ಣ"): (config[bstack1ll1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫತ")], config[bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಥ")])
    })
    if response:
      logger.debug(bstack1l1lll1l1l_opy_.format(bstack1111l11l1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1l11ll1l_opy_.format(str(e)))
def bstack1l11l1l111_opy_(framework):
  return bstack1ll1ll_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣದ").format(str(framework), __version__) if framework else bstack1ll1ll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨಧ").format(
    __version__)
def bstack11llll1l1l_opy_():
  global CONFIG
  global bstack1l1llll11l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1lllll1l1_opy_()
    logger.debug(bstack1ll111l11l_opy_.format(str(CONFIG)))
    bstack1l1llll11l_opy_ = bstack11ll1ll1_opy_.bstack111lll1l1_opy_(CONFIG, bstack1l1llll11l_opy_)
    bstack11lll1ll1l_opy_()
  except Exception as e:
    logger.error(bstack1ll1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥನ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l1ll1ll_opy_
  atexit.register(bstack11lll111_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll11l_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll11l_opy_)
def bstack1l1l1ll1ll_opy_(exctype, value, traceback):
  global bstack11llllll1_opy_
  try:
    for driver in bstack11llllll1_opy_:
      bstack11l1llll_opy_(driver, bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ಩"), bstack1ll1ll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦಪ") + str(value))
  except Exception:
    pass
  bstack1ll11lll1l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll11lll1l_opy_(message=bstack1ll1ll_opy_ (u"ࠩࠪಫ"), bstack11l1l11l_opy_ = False):
  global CONFIG
  bstack1ll1lllll_opy_ = bstack1ll1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬಬ") if bstack11l1l11l_opy_ else bstack1ll1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪಭ")
  try:
    if message:
      bstack1l1lllll1l_opy_ = {
        bstack1ll1lllll_opy_ : str(message)
      }
      bstack1l111l11l1_opy_(bstack1llllll111_opy_, CONFIG, bstack1l1lllll1l_opy_)
    else:
      bstack1l111l11l1_opy_(bstack1llllll111_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l1ll1l_opy_.format(str(e)))
def bstack1l1llll1l_opy_(bstack1l11111l_opy_, size):
  bstack1l111l1ll1_opy_ = []
  while len(bstack1l11111l_opy_) > size:
    bstack11ll1ll11_opy_ = bstack1l11111l_opy_[:size]
    bstack1l111l1ll1_opy_.append(bstack11ll1ll11_opy_)
    bstack1l11111l_opy_ = bstack1l11111l_opy_[size:]
  bstack1l111l1ll1_opy_.append(bstack1l11111l_opy_)
  return bstack1l111l1ll1_opy_
def bstack1ll111111_opy_(args):
  if bstack1ll1ll_opy_ (u"ࠬ࠳࡭ࠨಮ") in args and bstack1ll1ll_opy_ (u"࠭ࡰࡥࡤࠪಯ") in args:
    return True
  return False
def run_on_browserstack(bstack1lll1l1ll_opy_=None, bstack1l1ll1111l_opy_=None, bstack11ll1111_opy_=False):
  global CONFIG
  global bstack1llll11111_opy_
  global bstack1l1111l11l_opy_
  global bstack1lll11l11_opy_
  global bstack1l1l1l1ll_opy_
  bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠧࠨರ")
  bstack11l111l1l_opy_(bstack11lll11l_opy_, logger)
  if bstack1lll1l1ll_opy_ and isinstance(bstack1lll1l1ll_opy_, str):
    bstack1lll1l1ll_opy_ = eval(bstack1lll1l1ll_opy_)
  if bstack1lll1l1ll_opy_:
    CONFIG = bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨಱ")]
    bstack1llll11111_opy_ = bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪಲ")]
    bstack1l1111l11l_opy_ = bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬಳ")]
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭಴"), bstack1l1111l11l_opy_)
    bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬವ")
  bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨಶ"), uuid4().__str__())
  logger.debug(bstack1ll1ll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪಷ") + bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪಸ")))
  if not bstack11ll1111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll11l1l_opy_)
      return
    if sys.argv[1] == bstack1ll1ll_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬಹ") or sys.argv[1] == bstack1ll1ll_opy_ (u"ࠪ࠱ࡻ࠭಺"):
      logger.info(bstack1ll1ll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫ಻").format(__version__))
      return
    if sys.argv[1] == bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳ಼ࠫ"):
      bstack1lll111111_opy_()
      return
  args = sys.argv
  bstack11llll1l1l_opy_()
  global bstack11l11ll1l_opy_
  global bstack1lll11lll1_opy_
  global bstack1l1111l1_opy_
  global bstack11l1ll1l1_opy_
  global bstack1l111l111_opy_
  global bstack11l1lll1l_opy_
  global bstack1lllll11_opy_
  global bstack1lll1111_opy_
  global bstack1lll1l1l11_opy_
  global bstack111lll1l_opy_
  global bstack1111lllll_opy_
  bstack1lll11lll1_opy_ = len(CONFIG.get(bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಽ"), []))
  if not bstack11111l111_opy_:
    if args[1] == bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧಾ") or args[1] == bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩಿ"):
      bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೀ")
      args = args[2:]
    elif args[1] == bstack1ll1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩು"):
      bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪೂ")
      args = args[2:]
    elif args[1] == bstack1ll1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫೃ"):
      bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬೄ")
      args = args[2:]
    elif args[1] == bstack1ll1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೅"):
      bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩೆ")
      args = args[2:]
    elif args[1] == bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩೇ"):
      bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೈ")
      args = args[2:]
    elif args[1] == bstack1ll1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ೉"):
      bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬೊ")
      args = args[2:]
    else:
      if not bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩೋ") in CONFIG or str(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪೌ")]).lower() in [bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ್"), bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ೎")]:
        bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ೏")
        args = args[1:]
      elif str(CONFIG[bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ೐")]).lower() == bstack1ll1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೑"):
        bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೒")
        args = args[1:]
      elif str(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೓")]).lower() == bstack1ll1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ೔"):
        bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨೕ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ೖ")]).lower() == bstack1ll1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ೗"):
        bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ೘")
        args = args[1:]
      elif str(CONFIG[bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೙")]).lower() == bstack1ll1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ೚"):
        bstack11111l111_opy_ = bstack1ll1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೛")
        args = args[1:]
      else:
        os.environ[bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೜")] = bstack11111l111_opy_
        bstack1llllll11l_opy_(bstack111111l1l_opy_)
  os.environ[bstack1ll1ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫೝ")] = bstack11111l111_opy_
  bstack1lll11l11_opy_ = bstack11111l111_opy_
  global bstack11ll11l1l_opy_
  global bstack1l1l1lllll_opy_
  if bstack1lll1l1ll_opy_:
    try:
      os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ೞ")] = bstack11111l111_opy_
      bstack1l111l11l1_opy_(bstack11ll1l1ll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1lll111l_opy_.format(str(e)))
  global bstack11111111l_opy_
  global bstack1l11111l1_opy_
  global bstack11111l11_opy_
  global bstack11llll111l_opy_
  global bstack1l11ll1l1l_opy_
  global bstack1l1l111lll_opy_
  global bstack11ll1l11_opy_
  global bstack11111l1l1_opy_
  global bstack1l1ll1ll1l_opy_
  global bstack11ll111ll_opy_
  global bstack1l1llll1ll_opy_
  global bstack1l11llll1l_opy_
  global bstack1111l1ll_opy_
  global bstack1ll11lllll_opy_
  global bstack11lll11l11_opy_
  global bstack1l11lll111_opy_
  global bstack1ll111ll1_opy_
  global bstack1llll11l1_opy_
  global bstack111111l1_opy_
  global bstack1l1111111_opy_
  global bstack1111l111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11111111l_opy_ = webdriver.Remote.__init__
    bstack1l11111l1_opy_ = WebDriver.quit
    bstack1l11llll1l_opy_ = WebDriver.close
    bstack11lll11l11_opy_ = WebDriver.get
    bstack1111l111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11ll11l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll1lll11_opy_
    bstack1l1l1lllll_opy_ = bstack1ll1lll11_opy_()
  except Exception as e:
    pass
  try:
    global bstack1lll11ll11_opy_
    from QWeb.keywords import browser
    bstack1lll11ll11_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111lllll_opy_(CONFIG) and bstack1lll11l1ll_opy_():
    if bstack1l11llllll_opy_() < version.parse(bstack11ll11111_opy_):
      logger.error(bstack1ll1l1111l_opy_.format(bstack1l11llllll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l11lll111_opy_ = RemoteConnection._1llll1l1ll_opy_
      except Exception as e:
        logger.error(bstack1lll11ll_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll1ll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ೟"), False) and not bstack1lll1l1ll_opy_:
    logger.info(bstack1ll1ll1l11_opy_)
  if bstack1ll1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪೠ") in CONFIG and str(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫೡ")]).lower() != bstack1ll1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧೢ"):
    bstack1ll11l11l_opy_()
  elif bstack11111l111_opy_ != bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೣ") or (bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ೤") and not bstack1lll1l1ll_opy_):
    bstack11lll1l1l_opy_()
  if (bstack11111l111_opy_ in [bstack1ll1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ೥"), bstack1ll1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೦"), bstack1ll1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ೧")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll1ll1ll1_opy_
        bstack1l1l111lll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1llll111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1lll1lll1_opy_
        bstack1l11ll1l1l_opy_ = bstack1lll1lll1_opy_.close
      except Exception as e:
        logger.debug(bstack11l111l11_opy_ + str(e))
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1llll111_opy_)
    if bstack11111l111_opy_ != bstack1ll1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೨"):
      bstack11l1lll1_opy_()
    bstack11111l11_opy_ = Output.start_test
    bstack11llll111l_opy_ = Output.end_test
    bstack11ll1l11_opy_ = TestStatus.__init__
    bstack1l1ll1ll1l_opy_ = pabot._run
    bstack11ll111ll_opy_ = QueueItem.__init__
    bstack1l1llll1ll_opy_ = pabot._create_command_for_execution
    bstack111111l1_opy_ = pabot._report_results
  if bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೩"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1l11ll1111_opy_)
    bstack1111l1ll_opy_ = Runner.run_hook
    bstack1ll11lllll_opy_ = Step.run
  if bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೪"):
    try:
      from _pytest.config import Config
      bstack1ll111ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1llll11l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l111l1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1111111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ೫"))
  try:
    framework_name = bstack1ll1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೬") if bstack11111l111_opy_ in [bstack1ll1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೭"), bstack1ll1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೮"), bstack1ll1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೯")] else bstack11l11ll1_opy_(bstack11111l111_opy_)
    bstack1ll1l1l1l1_opy_ = {
      bstack1ll1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ೰"): bstack1ll1ll_opy_ (u"ࠩࡾ࠴ࢂ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨೱ").format(framework_name) if bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೲ") and bstack1111l1l1l_opy_() else framework_name,
      bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨೳ"): bstack1l11lllll_opy_(framework_name),
      bstack1ll1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ೴"): __version__,
      bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ೵"): bstack11111l111_opy_
    }
    if bstack11111l111_opy_ in bstack1lll1l111l_opy_:
      if bstack1llll111l_opy_ and bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ೶") in CONFIG and CONFIG[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ೷")] == True:
        if bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ೸") in CONFIG:
          os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ೹")] = os.getenv(bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ೺"), json.dumps(CONFIG[bstack1ll1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ೻")]))
          CONFIG[bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭೼")].pop(bstack1ll1ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ೽"), None)
          CONFIG[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ೾")].pop(bstack1ll1ll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ೿"), None)
        bstack1ll1l1l1l1_opy_[bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪഀ")] = {
          bstack1ll1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഁ"): bstack1ll1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧം"),
          bstack1ll1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧഃ"): str(bstack1l11llllll_opy_())
        }
    if bstack11111l111_opy_ not in [bstack1ll1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨഄ")]:
      bstack1l11l11ll_opy_ = bstack1llll1ll_opy_.launch(CONFIG, bstack1ll1l1l1l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11l1_opy_.format(bstack1ll1ll_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩഅ"), str(e)))
  if bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩആ"):
    bstack1l1111l1_opy_ = True
    if bstack1lll1l1ll_opy_ and bstack11ll1111_opy_:
      bstack11l1lll1l_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧഇ"), {}).get(bstack1ll1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഈ"))
      bstack1l1ll1l1ll_opy_(bstack1l11l1lll_opy_)
    elif bstack1lll1l1ll_opy_:
      bstack11l1lll1l_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩഉ"), {}).get(bstack1ll1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഊ"))
      global bstack11llllll1_opy_
      try:
        if bstack1ll111111_opy_(bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪഋ")]) and multiprocessing.current_process().name == bstack1ll1ll_opy_ (u"ࠨ࠲ࠪഌ"):
          bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ഍")].remove(bstack1ll1ll_opy_ (u"ࠪ࠱ࡲ࠭എ"))
          bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧഏ")].remove(bstack1ll1ll_opy_ (u"ࠬࡶࡤࡣࠩഐ"))
          bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ഑")] = bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪഒ")][0]
          with open(bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫഓ")], bstack1ll1ll_opy_ (u"ࠩࡵࠫഔ")) as f:
            bstack1ll11ll1l_opy_ = f.read()
          bstack11l111ll_opy_ = bstack1ll1ll_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨക").format(str(bstack1lll1l1ll_opy_))
          bstack1l1lllllll_opy_ = bstack11l111ll_opy_ + bstack1ll11ll1l_opy_
          bstack1l1l1llll_opy_ = bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧഖ")] + bstack1ll1ll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧഗ")
          with open(bstack1l1l1llll_opy_, bstack1ll1ll_opy_ (u"࠭ࡷࠨഘ")):
            pass
          with open(bstack1l1l1llll_opy_, bstack1ll1ll_opy_ (u"ࠢࡸ࠭ࠥങ")) as f:
            f.write(bstack1l1lllllll_opy_)
          import subprocess
          bstack1l111l11_opy_ = subprocess.run([bstack1ll1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣച"), bstack1l1l1llll_opy_])
          if os.path.exists(bstack1l1l1llll_opy_):
            os.unlink(bstack1l1l1llll_opy_)
          os._exit(bstack1l111l11_opy_.returncode)
        else:
          if bstack1ll111111_opy_(bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬഛ")]):
            bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ജ")].remove(bstack1ll1ll_opy_ (u"ࠫ࠲ࡳࠧഝ"))
            bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨഞ")].remove(bstack1ll1ll_opy_ (u"࠭ࡰࡥࡤࠪട"))
            bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪഠ")] = bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫഡ")][0]
          bstack1l1ll1l1ll_opy_(bstack1l11l1lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬഢ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1ll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬണ")] = bstack1ll1ll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ത")
          mod_globals[bstack1ll1ll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧഥ")] = os.path.abspath(bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩദ")])
          exec(open(bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪധ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1ll_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨന").format(str(e)))
          for driver in bstack11llllll1_opy_:
            bstack1l1ll1111l_opy_.append({
              bstack1ll1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഩ"): bstack1lll1l1ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭പ")],
              bstack1ll1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪഫ"): str(e),
              bstack1ll1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫബ"): multiprocessing.current_process().name
            })
            bstack11l1llll_opy_(driver, bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ഭ"), bstack1ll1ll_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥമ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11llllll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1111l11l_opy_, CONFIG, logger)
      bstack11llll1ll_opy_()
      bstack11111l1ll_opy_()
      bstack1llll1l11_opy_ = {
        bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫയ"): args[0],
        bstack1ll1ll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩര"): CONFIG,
        bstack1ll1ll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫറ"): bstack1llll11111_opy_,
        bstack1ll1ll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ല"): bstack1l1111l11l_opy_
      }
      percy.bstack1l111l1lll_opy_()
      if bstack1ll1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨള") in CONFIG:
        bstack1ll1111ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1l1ll11_opy_ = manager.list()
        if bstack1ll111111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഴ")]):
            if index == 0:
              bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪവ")] = args
            bstack1ll1111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll1l11_opy_, bstack1l1l1ll11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫശ")]):
            bstack1ll1111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll1l11_opy_, bstack1l1l1ll11_opy_)))
        for t in bstack1ll1111ll_opy_:
          t.start()
        for t in bstack1ll1111ll_opy_:
          t.join()
        bstack1lll1111_opy_ = list(bstack1l1l1ll11_opy_)
      else:
        if bstack1ll111111_opy_(args):
          bstack1llll1l11_opy_[bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬഷ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1llll1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1ll1l1ll_opy_(bstack1l11l1lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1ll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬസ")] = bstack1ll1ll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ഹ")
          mod_globals[bstack1ll1ll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧഺ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸ഻ࠬ") or bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ഼࠭"):
    percy.init(bstack1l1111l11l_opy_, CONFIG, logger)
    percy.bstack1l111l1lll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1llll111_opy_)
    bstack11llll1ll_opy_()
    bstack1l1ll1l1ll_opy_(bstack1l1l111ll1_opy_)
    if bstack1llll111l_opy_:
      bstack1ll1ll1l_opy_(bstack1l1l111ll1_opy_, args)
      if bstack1ll1ll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ഽ") in args:
        i = args.index(bstack1ll1ll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧാ"))
        args.pop(i)
        args.pop(i)
      if bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ി") not in CONFIG:
        CONFIG[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧീ")] = [{}]
        bstack1lll11lll1_opy_ = 1
      if bstack11l11ll1l_opy_ == 0:
        bstack11l11ll1l_opy_ = 1
      args.insert(0, str(bstack11l11ll1l_opy_))
      args.insert(0, str(bstack1ll1ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪു")))
    if bstack1llll1ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack111l1llll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll111llll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll1ll_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨൂ"),
        ).parse_args(bstack111l1llll_opy_)
        bstack11llll11l_opy_ = args.index(bstack111l1llll_opy_[0]) if len(bstack111l1llll_opy_) > 0 else len(args)
        args.insert(bstack11llll11l_opy_, str(bstack1ll1ll_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫൃ")))
        args.insert(bstack11llll11l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬൄ"))))
        if bstack1ll111ll_opy_(os.environ.get(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ൅"))) and str(os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧെ"), bstack1ll1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩേ"))) != bstack1ll1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪൈ"):
          for bstack11l111ll1_opy_ in bstack1ll111llll_opy_:
            args.remove(bstack11l111ll1_opy_)
          bstack1l1lll1ll1_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ൉")).split(bstack1ll1ll_opy_ (u"ࠧ࠭ࠩൊ"))
          for bstack1ll1l1l111_opy_ in bstack1l1lll1ll1_opy_:
            args.append(bstack1ll1l1l111_opy_)
      except Exception as e:
        logger.error(bstack1ll1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࠦോ").format(e))
    pabot.main(args)
  elif bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪൌ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1llll111_opy_)
    for a in args:
      if bstack1ll1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ്࡙ࠩ") in a:
        bstack1l111l111_opy_ = int(a.split(bstack1ll1ll_opy_ (u"ࠫ࠿࠭ൎ"))[1])
      if bstack1ll1ll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ൏") in a:
        bstack11l1lll1l_opy_ = str(a.split(bstack1ll1ll_opy_ (u"࠭࠺ࠨ൐"))[1])
      if bstack1ll1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ൑") in a:
        bstack1lllll11_opy_ = str(a.split(bstack1ll1ll_opy_ (u"ࠨ࠼ࠪ൒"))[1])
    bstack1l1111l1l_opy_ = None
    if bstack1ll1ll_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ൓") in args:
      i = args.index(bstack1ll1ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩൔ"))
      args.pop(i)
      bstack1l1111l1l_opy_ = args.pop(i)
    if bstack1l1111l1l_opy_ is not None:
      global bstack1lllll11ll_opy_
      bstack1lllll11ll_opy_ = bstack1l1111l1l_opy_
    bstack1l1ll1l1ll_opy_(bstack1l1l111ll1_opy_)
    run_cli(args)
    if bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨൕ") in multiprocessing.current_process().__dict__.keys():
      for bstack11l11l11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1ll1111l_opy_.append(bstack11l11l11l_opy_)
  elif bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬൖ"):
    percy.init(bstack1l1111l11l_opy_, CONFIG, logger)
    percy.bstack1l111l1lll_opy_()
    bstack11lll11ll_opy_ = bstack11lllll1_opy_(args, logger, CONFIG, bstack1llll111l_opy_)
    bstack11lll11ll_opy_.bstack111llll1l_opy_()
    bstack11llll1ll_opy_()
    bstack11l1ll1l1_opy_ = True
    bstack111lll1l_opy_ = bstack11lll11ll_opy_.bstack1l11lll1l_opy_()
    bstack11lll11ll_opy_.bstack1llll1l11_opy_(bstack1ll1llll11_opy_)
    bstack1111l11l_opy_ = bstack11lll11ll_opy_.bstack1ll1l11l1l_opy_(bstack111l11ll1_opy_, {
      bstack1ll1ll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧൗ"): bstack1llll11111_opy_,
      bstack1ll1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൘"): bstack1l1111l11l_opy_,
      bstack1ll1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ൙"): bstack1llll111l_opy_
    })
    try:
      bstack111111ll_opy_, bstack11llll1l11_opy_ = map(list, zip(*bstack1111l11l_opy_))
      bstack1lll1l1l11_opy_ = bstack111111ll_opy_[0]
      for status_code in bstack11llll1l11_opy_:
        if status_code != 0:
          bstack1111lllll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢ൚").format(str(e)))
  elif bstack11111l111_opy_ == bstack1ll1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൛"):
    try:
      from behave.__main__ import main as bstack1l1l1l1l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l1ll1l_opy_(e, bstack1l11ll1111_opy_)
    bstack11llll1ll_opy_()
    bstack11l1ll1l1_opy_ = True
    bstack1l1l1111l1_opy_ = 1
    if bstack1ll1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ൜") in CONFIG:
      bstack1l1l1111l1_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ൝")]
    if bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൞") in CONFIG:
      bstack11lll1lll1_opy_ = int(bstack1l1l1111l1_opy_) * int(len(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪൟ")]))
    else:
      bstack11lll1lll1_opy_ = int(bstack1l1l1111l1_opy_)
    config = Configuration(args)
    bstack1ll1l11ll_opy_ = config.paths
    if len(bstack1ll1l11ll_opy_) == 0:
      import glob
      pattern = bstack1ll1ll_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧൠ")
      bstack1l1111l111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1111l111_opy_)
      config = Configuration(args)
      bstack1ll1l11ll_opy_ = config.paths
    bstack1ll1lll111_opy_ = [os.path.normpath(item) for item in bstack1ll1l11ll_opy_]
    bstack11111ll11_opy_ = [os.path.normpath(item) for item in args]
    bstack1l111l1l11_opy_ = [item for item in bstack11111ll11_opy_ if item not in bstack1ll1lll111_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1ll_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪൡ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1lll111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack111l1111l_opy_)))
                    for bstack111l1111l_opy_ in bstack1ll1lll111_opy_]
    bstack1l11111ll_opy_ = []
    for spec in bstack1ll1lll111_opy_:
      bstack1l1llll111_opy_ = []
      bstack1l1llll111_opy_ += bstack1l111l1l11_opy_
      bstack1l1llll111_opy_.append(spec)
      bstack1l11111ll_opy_.append(bstack1l1llll111_opy_)
    execution_items = []
    for bstack1l1llll111_opy_ in bstack1l11111ll_opy_:
      if bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ൢ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧൣ")]):
          item = {}
          item[bstack1ll1ll_opy_ (u"ࠬࡧࡲࡨࠩ൤")] = bstack1ll1ll_opy_ (u"࠭ࠠࠨ൥").join(bstack1l1llll111_opy_)
          item[bstack1ll1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭൦")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࠬ൧")] = bstack1ll1ll_opy_ (u"ࠩࠣࠫ൨").join(bstack1l1llll111_opy_)
        item[bstack1ll1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ൩")] = 0
        execution_items.append(item)
    bstack11l1111l1_opy_ = bstack1l1llll1l_opy_(execution_items, bstack11lll1lll1_opy_)
    for execution_item in bstack11l1111l1_opy_:
      bstack1ll1111ll_opy_ = []
      for item in execution_item:
        bstack1ll1111ll_opy_.append(bstack111111ll1_opy_(name=str(item[bstack1ll1ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ൪")]),
                                             target=bstack1l11l1l1_opy_,
                                             args=(item[bstack1ll1ll_opy_ (u"ࠬࡧࡲࡨࠩ൫")],)))
      for t in bstack1ll1111ll_opy_:
        t.start()
      for t in bstack1ll1111ll_opy_:
        t.join()
  else:
    bstack1llllll11l_opy_(bstack111111l1l_opy_)
  if not bstack1lll1l1ll_opy_:
    bstack111l11lll_opy_()
  bstack11ll1ll1_opy_.bstack111l11111_opy_()
def browserstack_initialize(bstack1l1ll1ll1_opy_=None):
  run_on_browserstack(bstack1l1ll1ll1_opy_, None, True)
def bstack111l11lll_opy_():
  global CONFIG
  global bstack1lll11l11_opy_
  global bstack1111lllll_opy_
  global bstack11ll1lll1_opy_
  global bstack1l1l1l1ll_opy_
  bstack1llll1ll_opy_.stop()
  bstack1111llll_opy_.bstack1ll11llll_opy_()
  if bstack1ll1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ൬") in CONFIG and str(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ൭")]).lower() != bstack1ll1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ൮"):
    bstack1l1l11l1ll_opy_, bstack11111111_opy_ = bstack1l1l1l11ll_opy_()
  else:
    bstack1l1l11l1ll_opy_, bstack11111111_opy_ = get_build_link()
  bstack1l1l1ll1_opy_(bstack1l1l11l1ll_opy_)
  if bstack1l1l11l1ll_opy_ is not None and bstack1ll1lll1ll_opy_() != -1:
    sessions = bstack11ll11l1_opy_(bstack1l1l11l1ll_opy_)
    bstack11ll111l1_opy_(sessions, bstack11111111_opy_)
  if bstack1lll11l11_opy_ == bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൯") and bstack1111lllll_opy_ != 0:
    sys.exit(bstack1111lllll_opy_)
  if bstack1lll11l11_opy_ == bstack1ll1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൰") and bstack11ll1lll1_opy_ != 0:
    sys.exit(bstack11ll1lll1_opy_)
def bstack1l1l1ll1_opy_(new_id):
    global bstack1lll11l11l_opy_
    bstack1lll11l11l_opy_ = new_id
def bstack11l11ll1_opy_(bstack1l11ll1lll_opy_):
  if bstack1l11ll1lll_opy_:
    return bstack1l11ll1lll_opy_.capitalize()
  else:
    return bstack1ll1ll_opy_ (u"ࠫࠬ൱")
def bstack1l1ll1lll_opy_(bstack111lll11_opy_):
  if bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ൲") in bstack111lll11_opy_ and bstack111lll11_opy_[bstack1ll1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൳")] != bstack1ll1ll_opy_ (u"ࠧࠨ൴"):
    return bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭൵")]
  else:
    bstack1l11111l1l_opy_ = bstack1ll1ll_opy_ (u"ࠤࠥ൶")
    if bstack1ll1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ൷") in bstack111lll11_opy_ and bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ൸")] != None:
      bstack1l11111l1l_opy_ += bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ൹")] + bstack1ll1ll_opy_ (u"ࠨࠬࠡࠤൺ")
      if bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠧࡰࡵࠪൻ")] == bstack1ll1ll_opy_ (u"ࠣ࡫ࡲࡷࠧർ"):
        bstack1l11111l1l_opy_ += bstack1ll1ll_opy_ (u"ࠤ࡬ࡓࡘࠦࠢൽ")
      bstack1l11111l1l_opy_ += (bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧൾ")] or bstack1ll1ll_opy_ (u"ࠫࠬൿ"))
      return bstack1l11111l1l_opy_
    else:
      bstack1l11111l1l_opy_ += bstack11l11ll1_opy_(bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭඀")]) + bstack1ll1ll_opy_ (u"ࠨࠠࠣඁ") + (
              bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩං")] or bstack1ll1ll_opy_ (u"ࠨࠩඃ")) + bstack1ll1ll_opy_ (u"ࠤ࠯ࠤࠧ඄")
      if bstack111lll11_opy_[bstack1ll1ll_opy_ (u"ࠪࡳࡸ࠭අ")] == bstack1ll1ll_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧආ"):
        bstack1l11111l1l_opy_ += bstack1ll1ll_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥඇ")
      bstack1l11111l1l_opy_ += bstack111lll11_opy_[bstack1ll1ll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪඈ")] or bstack1ll1ll_opy_ (u"ࠧࠨඉ")
      return bstack1l11111l1l_opy_
def bstack11111ll1l_opy_(bstack11ll1l1l_opy_):
  if bstack11ll1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠣࡦࡲࡲࡪࠨඊ"):
    return bstack1ll1ll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬඋ")
  elif bstack11ll1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥඌ"):
    return bstack1ll1ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧඍ")
  elif bstack11ll1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧඎ"):
    return bstack1ll1ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ඏ")
  elif bstack11ll1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨඐ"):
    return bstack1ll1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪඑ")
  elif bstack11ll1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥඒ"):
    return bstack1ll1ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨඓ")
  elif bstack11ll1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧඔ"):
    return bstack1ll1ll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ඕ")
  else:
    return bstack1ll1ll_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪඖ") + bstack11l11ll1_opy_(
      bstack11ll1l1l_opy_) + bstack1ll1ll_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭඗")
def bstack11111l1l_opy_(session):
  return bstack1ll1ll_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨ඘").format(
    session[bstack1ll1ll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭඙")], bstack1l1ll1lll_opy_(session), bstack11111ll1l_opy_(session[bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩක")]),
    bstack11111ll1l_opy_(session[bstack1ll1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫඛ")]),
    bstack11l11ll1_opy_(session[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ග")] or session[bstack1ll1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ඝ")] or bstack1ll1ll_opy_ (u"ࠧࠨඞ")) + bstack1ll1ll_opy_ (u"ࠣࠢࠥඟ") + (session[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫච")] or bstack1ll1ll_opy_ (u"ࠪࠫඡ")),
    session[bstack1ll1ll_opy_ (u"ࠫࡴࡹࠧජ")] + bstack1ll1ll_opy_ (u"ࠧࠦࠢඣ") + session[bstack1ll1ll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪඤ")], session[bstack1ll1ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩඥ")] or bstack1ll1ll_opy_ (u"ࠨࠩඦ"),
    session[bstack1ll1ll_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ට")] if session[bstack1ll1ll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧඨ")] else bstack1ll1ll_opy_ (u"ࠫࠬඩ"))
def bstack11ll111l1_opy_(sessions, bstack11111111_opy_):
  try:
    bstack1l11l111l_opy_ = bstack1ll1ll_opy_ (u"ࠧࠨඪ")
    if not os.path.exists(bstack11l11llll_opy_):
      os.mkdir(bstack11l11llll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1ll_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫණ")), bstack1ll1ll_opy_ (u"ࠧࡳࠩඬ")) as f:
      bstack1l11l111l_opy_ = f.read()
    bstack1l11l111l_opy_ = bstack1l11l111l_opy_.replace(bstack1ll1ll_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬත"), str(len(sessions)))
    bstack1l11l111l_opy_ = bstack1l11l111l_opy_.replace(bstack1ll1ll_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩථ"), bstack11111111_opy_)
    bstack1l11l111l_opy_ = bstack1l11l111l_opy_.replace(bstack1ll1ll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫද"),
                                              sessions[0].get(bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨධ")) if sessions[0] else bstack1ll1ll_opy_ (u"ࠬ࠭න"))
    with open(os.path.join(bstack11l11llll_opy_, bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ඲")), bstack1ll1ll_opy_ (u"ࠧࡸࠩඳ")) as stream:
      stream.write(bstack1l11l111l_opy_.split(bstack1ll1ll_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬප"))[0])
      for session in sessions:
        stream.write(bstack11111l1l_opy_(session))
      stream.write(bstack1l11l111l_opy_.split(bstack1ll1ll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ඵ"))[1])
    logger.info(bstack1ll1ll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭බ").format(bstack11l11llll_opy_));
  except Exception as e:
    logger.debug(bstack11ll1llll_opy_.format(str(e)))
def bstack11ll11l1_opy_(bstack1l1l11l1ll_opy_):
  global CONFIG
  try:
    host = bstack1ll1ll_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧභ") if bstack1ll1ll_opy_ (u"ࠬࡧࡰࡱࠩම") in CONFIG else bstack1ll1ll_opy_ (u"࠭ࡡࡱ࡫ࠪඹ")
    user = CONFIG[bstack1ll1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩය")]
    key = CONFIG[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫර")]
    bstack1lll1ll11_opy_ = bstack1ll1ll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ඼") if bstack1ll1ll_opy_ (u"ࠪࡥࡵࡶࠧල") in CONFIG else (bstack1ll1ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ඾") if CONFIG.get(bstack1ll1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ඿")) else bstack1ll1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨව"))
    url = bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬශ").format(user, key, host, bstack1lll1ll11_opy_,
                                                                                bstack1l1l11l1ll_opy_)
    headers = {
      bstack1ll1ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧෂ"): bstack1ll1ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬස"),
    }
    proxies = bstack1l11l1l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll1ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨහ")], response.json()))
  except Exception as e:
    logger.debug(bstack11ll111l_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1lll11l11l_opy_
  try:
    if bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧළ") in CONFIG:
      host = bstack1ll1ll_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨෆ") if bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲࠪ෇") in CONFIG else bstack1ll1ll_opy_ (u"ࠧࡢࡲ࡬ࠫ෈")
      user = CONFIG[bstack1ll1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ෉")]
      key = CONFIG[bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽ්ࠬ")]
      bstack1lll1ll11_opy_ = bstack1ll1ll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ෋") if bstack1ll1ll_opy_ (u"ࠫࡦࡶࡰࠨ෌") in CONFIG else bstack1ll1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ෍")
      url = bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭෎").format(user, key, host, bstack1lll1ll11_opy_)
      headers = {
        bstack1ll1ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ා"): bstack1ll1ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫැ"),
      }
      if bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෑ") in CONFIG:
        params = {bstack1ll1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨි"): CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧී")], bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨු"): CONFIG[bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෕")]}
      else:
        params = {bstack1ll1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬූ"): CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ෗")]}
      proxies = bstack1l11l1l1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1ll1l1_opy_ = response.json()[0][bstack1ll1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬෘ")]
        if bstack1ll1ll1l1_opy_:
          bstack11111111_opy_ = bstack1ll1ll1l1_opy_[bstack1ll1ll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧෙ")].split(bstack1ll1ll_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪේ"))[0] + bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ෛ") + bstack1ll1ll1l1_opy_[
            bstack1ll1ll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩො")]
          logger.info(bstack1l111ll1ll_opy_.format(bstack11111111_opy_))
          bstack1lll11l11l_opy_ = bstack1ll1ll1l1_opy_[bstack1ll1ll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪෝ")]
          bstack1l1l1l1l_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫෞ")]
          if bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෟ") in CONFIG:
            bstack1l1l1l1l_opy_ += bstack1ll1ll_opy_ (u"ࠪࠤࠬ෠") + CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭෡")]
          if bstack1l1l1l1l_opy_ != bstack1ll1ll1l1_opy_[bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෢")]:
            logger.debug(bstack1l1l1l1111_opy_.format(bstack1ll1ll1l1_opy_[bstack1ll1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෣")], bstack1l1l1l1l_opy_))
          return [bstack1ll1ll1l1_opy_[bstack1ll1ll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ෤")], bstack11111111_opy_]
    else:
      logger.warn(bstack1ll11ll11l_opy_)
  except Exception as e:
    logger.debug(bstack11l1l111_opy_.format(str(e)))
  return [None, None]
def bstack1ll111lll_opy_(url, bstack1lllll11l_opy_=False):
  global CONFIG
  global bstack1ll1ll1l1l_opy_
  if not bstack1ll1ll1l1l_opy_:
    hostname = bstack11l1ll11l_opy_(url)
    is_private = bstack1l1l1l1lll_opy_(hostname)
    if (bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ෥") in CONFIG and not bstack1ll111ll_opy_(CONFIG[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭෦")])) and (is_private or bstack1lllll11l_opy_):
      bstack1ll1ll1l1l_opy_ = hostname
def bstack11l1ll11l_opy_(url):
  return urlparse(url).hostname
def bstack1l1l1l1lll_opy_(hostname):
  for bstack1ll1l1l1l_opy_ in bstack1l11l1ll_opy_:
    regex = re.compile(bstack1ll1l1l1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l111ll111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l111l111_opy_
  bstack1111l111_opy_ = not (bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ෧"), None) and bstack1l1lll11_opy_(
          threading.current_thread(), bstack1ll1ll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෨"), None))
  bstack11llll1lll_opy_ = getattr(driver, bstack1ll1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ෩"), None) != True
  if not bstack1l11l11l1_opy_.bstack1lllll1l1l_opy_(CONFIG, bstack1l111l111_opy_) or (bstack11llll1lll_opy_ and bstack1111l111_opy_):
    logger.warning(bstack1ll1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ෪"))
    return {}
  try:
    logger.debug(bstack1ll1ll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ෫"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1lll1l11l_opy_.bstack1ll11lll11_opy_)
    return results
  except Exception:
    logger.error(bstack1ll1ll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ෬"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l111l111_opy_
  bstack1111l111_opy_ = not (bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭෭"), None) and bstack1l1lll11_opy_(
          threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ෮"), None))
  bstack11llll1lll_opy_ = getattr(driver, bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ෯"), None) != True
  if not bstack1l11l11l1_opy_.bstack1lllll1l1l_opy_(CONFIG, bstack1l111l111_opy_) or (bstack11llll1lll_opy_ and bstack1111l111_opy_):
    logger.warning(bstack1ll1ll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ෰"))
    return {}
  try:
    logger.debug(bstack1ll1ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫ෱"))
    logger.debug(perform_scan(driver))
    bstack1llll1l1l_opy_ = driver.execute_async_script(bstack1lll1l11l_opy_.bstack111111111_opy_)
    return bstack1llll1l1l_opy_
  except Exception:
    logger.error(bstack1ll1ll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣෲ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l111l111_opy_
  bstack1111l111_opy_ = not (bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬෳ"), None) and bstack1l1lll11_opy_(
          threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ෴"), None))
  bstack11llll1lll_opy_ = getattr(driver, bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ෵"), None) != True
  if not bstack1l11l11l1_opy_.bstack1lllll1l1l_opy_(CONFIG, bstack1l111l111_opy_) or (bstack11llll1lll_opy_ and bstack1111l111_opy_):
    logger.warning(bstack1ll1ll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨ෶"))
    return {}
  try:
    bstack1ll1l11lll_opy_ = driver.execute_async_script(bstack1lll1l11l_opy_.perform_scan, {bstack1ll1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ෷"): kwargs.get(bstack1ll1ll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ෸"), None) or bstack1ll1ll_opy_ (u"ࠧࠨ෹")})
    return bstack1ll1l11lll_opy_
  except Exception:
    logger.error(bstack1ll1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ෺"))
    return {}