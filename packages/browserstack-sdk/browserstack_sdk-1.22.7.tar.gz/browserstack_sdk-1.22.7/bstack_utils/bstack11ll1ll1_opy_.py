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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l111ll1_opy_, bstack111l11l111_opy_
import tempfile
import json
bstack1llll11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᔐ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1ll_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᔑ"),
      datefmt=bstack1ll1ll_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᔒ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll1l1111_opy_():
  global bstack1llll11lll1_opy_
  if os.path.exists(bstack1llll11lll1_opy_):
    os.remove(bstack1llll11lll1_opy_)
def bstack111l11111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack111lll1l1_opy_(config, log_level):
  bstack1llll11l1ll_opy_ = log_level
  if bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᔓ") in config and config[bstack1ll1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᔔ")] in bstack111l111ll1_opy_:
    bstack1llll11l1ll_opy_ = bstack111l111ll1_opy_[config[bstack1ll1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᔕ")]]
  if config.get(bstack1ll1ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᔖ"), False):
    logging.getLogger().setLevel(bstack1llll11l1ll_opy_)
    return bstack1llll11l1ll_opy_
  global bstack1llll11lll1_opy_
  bstack111l11111_opy_()
  bstack1llll1l1ll1_opy_ = logging.Formatter(
    fmt=bstack1ll1ll_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᔗ"),
    datefmt=bstack1ll1ll_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᔘ")
  )
  bstack1llll1l1l1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1llll11lll1_opy_)
  file_handler.setFormatter(bstack1llll1l1ll1_opy_)
  bstack1llll1l1l1l_opy_.setFormatter(bstack1llll1l1ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llll1l1l1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᔙ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llll1l1l1l_opy_.setLevel(bstack1llll11l1ll_opy_)
  logging.getLogger().addHandler(bstack1llll1l1l1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llll11l1ll_opy_
def bstack1llll11ll11_opy_(config):
  try:
    bstack1llll1l1l11_opy_ = set(bstack111l11l111_opy_)
    bstack1llll1l11l1_opy_ = bstack1ll1ll_opy_ (u"ࠬ࠭ᔚ")
    with open(bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᔛ")) as bstack1llll1l11ll_opy_:
      bstack1llll1l111l_opy_ = bstack1llll1l11ll_opy_.read()
      bstack1llll1l11l1_opy_ = re.sub(bstack1ll1ll_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᔜ"), bstack1ll1ll_opy_ (u"ࠨࠩᔝ"), bstack1llll1l111l_opy_, flags=re.M)
      bstack1llll1l11l1_opy_ = re.sub(
        bstack1ll1ll_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᔞ") + bstack1ll1ll_opy_ (u"ࠪࢀࠬᔟ").join(bstack1llll1l1l11_opy_) + bstack1ll1ll_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᔠ"),
        bstack1ll1ll_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᔡ"),
        bstack1llll1l11l1_opy_, flags=re.M | re.I
      )
    def bstack1llll11llll_opy_(dic):
      bstack1llll1l1lll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llll1l1l11_opy_:
          bstack1llll1l1lll_opy_[key] = bstack1ll1ll_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᔢ")
        else:
          if isinstance(value, dict):
            bstack1llll1l1lll_opy_[key] = bstack1llll11llll_opy_(value)
          else:
            bstack1llll1l1lll_opy_[key] = value
      return bstack1llll1l1lll_opy_
    bstack1llll1l1lll_opy_ = bstack1llll11llll_opy_(config)
    return {
      bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᔣ"): bstack1llll1l11l1_opy_,
      bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᔤ"): json.dumps(bstack1llll1l1lll_opy_)
    }
  except Exception as e:
    return {}
def bstack1lll11l1l1_opy_(config):
  global bstack1llll11lll1_opy_
  try:
    if config.get(bstack1ll1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᔥ"), False):
      return
    uuid = os.getenv(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᔦ"))
    if not uuid or uuid == bstack1ll1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᔧ"):
      return
    bstack1llll11ll1l_opy_ = [bstack1ll1ll_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᔨ"), bstack1ll1ll_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᔩ"), bstack1ll1ll_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᔪ"), bstack1llll11lll1_opy_]
    bstack111l11111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧᔫ") + uuid + bstack1ll1ll_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᔬ"))
    with tarfile.open(output_file, bstack1ll1ll_opy_ (u"ࠥࡻ࠿࡭ࡺࠣᔭ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llll11ll1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llll11ll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llll1ll111_opy_ = data.encode()
        tarinfo.size = len(bstack1llll1ll111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llll1ll111_opy_))
    bstack1l11111l11_opy_ = MultipartEncoder(
      fields= {
        bstack1ll1ll_opy_ (u"ࠫࡩࡧࡴࡢࠩᔮ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1ll_opy_ (u"ࠬࡸࡢࠨᔯ")), bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫᔰ")),
        bstack1ll1ll_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᔱ"): uuid
      }
    )
    response = requests.post(
      bstack1ll1ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᔲ"),
      data=bstack1l11111l11_opy_,
      headers={bstack1ll1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᔳ"): bstack1l11111l11_opy_.content_type},
      auth=(config[bstack1ll1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᔴ")], config[bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᔵ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫᔶ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬᔷ") + str(e))
  finally:
    try:
      bstack1llll1l1111_opy_()
    except:
      pass