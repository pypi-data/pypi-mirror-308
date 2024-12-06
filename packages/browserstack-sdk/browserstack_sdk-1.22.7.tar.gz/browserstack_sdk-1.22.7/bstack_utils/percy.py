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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1l1lll1l_opy_, bstack1l1l111l1l_opy_
class bstack1ll1ll11l_opy_:
  working_dir = os.getcwd()
  bstack11lll11l1_opy_ = False
  config = {}
  binary_path = bstack1ll1ll_opy_ (u"ࠨࠩᕿ")
  bstack1llll111111_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪᖀ")
  bstack1ll1llllll_opy_ = False
  bstack1lll1l1lll1_opy_ = None
  bstack1lll1l1l111_opy_ = {}
  bstack1lll1l1ll1l_opy_ = 300
  bstack1lll11ll1l1_opy_ = False
  logger = None
  bstack1lll11l1l11_opy_ = False
  bstack11l11lll_opy_ = False
  bstack11l1111ll_opy_ = None
  bstack1lll1l111l1_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫᖁ")
  bstack1llll1111ll_opy_ = {
    bstack1ll1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᖂ") : 1,
    bstack1ll1ll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᖃ") : 2,
    bstack1ll1ll_opy_ (u"࠭ࡥࡥࡩࡨࠫᖄ") : 3,
    bstack1ll1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᖅ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lll1ll1l11_opy_(self):
    bstack1lll1l11lll_opy_ = bstack1ll1ll_opy_ (u"ࠨࠩᖆ")
    bstack1lll1ll11ll_opy_ = sys.platform
    bstack1lll1l11111_opy_ = bstack1ll1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᖇ")
    if re.match(bstack1ll1ll_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᖈ"), bstack1lll1ll11ll_opy_) != None:
      bstack1lll1l11lll_opy_ = bstack111l111111_opy_ + bstack1ll1ll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᖉ")
      self.bstack1lll1l111l1_opy_ = bstack1ll1ll_opy_ (u"ࠬࡳࡡࡤࠩᖊ")
    elif re.match(bstack1ll1ll_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᖋ"), bstack1lll1ll11ll_opy_) != None:
      bstack1lll1l11lll_opy_ = bstack111l111111_opy_ + bstack1ll1ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᖌ")
      bstack1lll1l11111_opy_ = bstack1ll1ll_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᖍ")
      self.bstack1lll1l111l1_opy_ = bstack1ll1ll_opy_ (u"ࠩࡺ࡭ࡳ࠭ᖎ")
    else:
      bstack1lll1l11lll_opy_ = bstack111l111111_opy_ + bstack1ll1ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᖏ")
      self.bstack1lll1l111l1_opy_ = bstack1ll1ll_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᖐ")
    return bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_
  def bstack1llll11111l_opy_(self):
    try:
      bstack1lll1ll1ll1_opy_ = [os.path.join(expanduser(bstack1ll1ll_opy_ (u"ࠧࢄࠢᖑ")), bstack1ll1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᖒ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll1ll1ll1_opy_:
        if(self.bstack1lll1ll1lll_opy_(path)):
          return path
      raise bstack1ll1ll_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᖓ")
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᖔ").format(e))
  def bstack1lll1ll1lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll1111l1_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_):
    try:
      bstack1llll111l11_opy_ = self.bstack1llll11111l_opy_()
      bstack1lll1ll1111_opy_ = os.path.join(bstack1llll111l11_opy_, bstack1ll1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᖕ"))
      bstack1lll1llll1l_opy_ = os.path.join(bstack1llll111l11_opy_, bstack1lll1l11111_opy_)
      if os.path.exists(bstack1lll1llll1l_opy_):
        self.logger.info(bstack1ll1ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᖖ").format(bstack1lll1llll1l_opy_))
        return bstack1lll1llll1l_opy_
      if os.path.exists(bstack1lll1ll1111_opy_):
        self.logger.info(bstack1ll1ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᖗ").format(bstack1lll1ll1111_opy_))
        return self.bstack1lll11ll11l_opy_(bstack1lll1ll1111_opy_, bstack1lll1l11111_opy_)
      self.logger.info(bstack1ll1ll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᖘ").format(bstack1lll1l11lll_opy_))
      response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"࠭ࡇࡆࡖࠪᖙ"), bstack1lll1l11lll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lll1ll1111_opy_, bstack1ll1ll_opy_ (u"ࠧࡸࡤࠪᖚ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll1ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᖛ").format(bstack1lll1ll1111_opy_))
        return self.bstack1lll11ll11l_opy_(bstack1lll1ll1111_opy_, bstack1lll1l11111_opy_)
      else:
        raise(bstack1ll1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᖜ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᖝ").format(e))
  def bstack1lll11lll11_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_):
    try:
      retry = 2
      bstack1lll1llll1l_opy_ = None
      bstack1lll1ll111l_opy_ = False
      while retry > 0:
        bstack1lll1llll1l_opy_ = self.bstack1llll1111l1_opy_(bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_)
        bstack1lll1ll111l_opy_ = self.bstack1lll11lllll_opy_(bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_, bstack1lll1llll1l_opy_)
        if bstack1lll1ll111l_opy_:
          break
        retry -= 1
      return bstack1lll1llll1l_opy_, bstack1lll1ll111l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᖞ").format(e))
    return bstack1lll1llll1l_opy_, False
  def bstack1lll11lllll_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_, bstack1lll1llll1l_opy_, bstack1lll1lll111_opy_ = 0):
    if bstack1lll1lll111_opy_ > 1:
      return False
    if bstack1lll1llll1l_opy_ == None or os.path.exists(bstack1lll1llll1l_opy_) == False:
      self.logger.warn(bstack1ll1ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᖟ"))
      return False
    bstack1lll1lll1l1_opy_ = bstack1ll1ll_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᖠ")
    command = bstack1ll1ll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᖡ").format(bstack1lll1llll1l_opy_)
    bstack1lll1llll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1lll1lll1l1_opy_, bstack1lll1llll11_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᖢ"))
      return False
  def bstack1lll11ll11l_opy_(self, bstack1lll1ll1111_opy_, bstack1lll1l11111_opy_):
    try:
      working_dir = os.path.dirname(bstack1lll1ll1111_opy_)
      shutil.unpack_archive(bstack1lll1ll1111_opy_, working_dir)
      bstack1lll1llll1l_opy_ = os.path.join(working_dir, bstack1lll1l11111_opy_)
      os.chmod(bstack1lll1llll1l_opy_, 0o755)
      return bstack1lll1llll1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᖣ"))
  def bstack1lll1lll1ll_opy_(self):
    try:
      bstack1llll111l1l_opy_ = self.config.get(bstack1ll1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᖤ"))
      bstack1lll1lll1ll_opy_ = bstack1llll111l1l_opy_ or (bstack1llll111l1l_opy_ is None and self.bstack11lll11l1_opy_)
      if not bstack1lll1lll1ll_opy_ or self.config.get(bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᖥ"), None) not in bstack111l111l11_opy_:
        return False
      self.bstack1ll1llllll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᖦ").format(e))
  def bstack1lll1l11l1l_opy_(self):
    try:
      bstack1lll1l11l1l_opy_ = self.bstack1lll1lllll1_opy_
      return bstack1lll1l11l1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᖧ").format(e))
  def init(self, bstack11lll11l1_opy_, config, logger):
    self.bstack11lll11l1_opy_ = bstack11lll11l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll1lll1ll_opy_():
      return
    self.bstack1lll1l1l111_opy_ = config.get(bstack1ll1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᖨ"), {})
    self.bstack1lll1lllll1_opy_ = config.get(bstack1ll1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᖩ"))
    try:
      bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_ = self.bstack1lll1ll1l11_opy_()
      bstack1lll1llll1l_opy_, bstack1lll1ll111l_opy_ = self.bstack1lll11lll11_opy_(bstack1lll1l11lll_opy_, bstack1lll1l11111_opy_)
      if bstack1lll1ll111l_opy_:
        self.binary_path = bstack1lll1llll1l_opy_
        thread = Thread(target=self.bstack1lll11l1l1l_opy_)
        thread.start()
      else:
        self.bstack1lll11l1l11_opy_ = True
        self.logger.error(bstack1ll1ll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᖪ").format(bstack1lll1llll1l_opy_))
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᖫ").format(e))
  def bstack1lll11l111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll1ll_opy_ (u"ࠫࡱࡵࡧࠨᖬ"), bstack1ll1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᖭ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll1ll_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᖮ").format(logfile))
      self.bstack1llll111111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᖯ").format(e))
  def bstack1lll11l1l1l_opy_(self):
    bstack1lll11l1ll1_opy_ = self.bstack1lll1l1l11l_opy_()
    if bstack1lll11l1ll1_opy_ == None:
      self.bstack1lll11l1l11_opy_ = True
      self.logger.error(bstack1ll1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᖰ"))
      return False
    command_args = [bstack1ll1ll_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᖱ") if self.bstack11lll11l1_opy_ else bstack1ll1ll_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᖲ")]
    bstack1lll1l1111l_opy_ = self.bstack1lll1ll11l1_opy_()
    if bstack1lll1l1111l_opy_ != None:
      command_args.append(bstack1ll1ll_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᖳ").format(bstack1lll1l1111l_opy_))
    env = os.environ.copy()
    env[bstack1ll1ll_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᖴ")] = bstack1lll11l1ll1_opy_
    env[bstack1ll1ll_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᖵ")] = os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᖶ"), bstack1ll1ll_opy_ (u"ࠨࠩᖷ"))
    bstack1lll11lll1l_opy_ = [self.binary_path]
    self.bstack1lll11l111l_opy_()
    self.bstack1lll1l1lll1_opy_ = self.bstack1lll11l11l1_opy_(bstack1lll11lll1l_opy_ + command_args, env)
    self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᖸ"))
    bstack1lll1lll111_opy_ = 0
    while self.bstack1lll1l1lll1_opy_.poll() == None:
      bstack1lll11l1lll_opy_ = self.bstack1lll1l1ll11_opy_()
      if bstack1lll11l1lll_opy_:
        self.logger.debug(bstack1ll1ll_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᖹ"))
        self.bstack1lll11ll1l1_opy_ = True
        return True
      bstack1lll1lll111_opy_ += 1
      self.logger.debug(bstack1ll1ll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᖺ").format(bstack1lll1lll111_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᖻ").format(bstack1lll1lll111_opy_))
    self.bstack1lll11l1l11_opy_ = True
    return False
  def bstack1lll1l1ll11_opy_(self, bstack1lll1lll111_opy_ = 0):
    if bstack1lll1lll111_opy_ > 10:
      return False
    try:
      bstack1lll11llll1_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ᖼ"), bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᖽ"))
      bstack1lll1ll1l1l_opy_ = bstack1lll11llll1_opy_ + bstack1111llllll_opy_
      response = requests.get(bstack1lll1ll1l1l_opy_)
      data = response.json()
      self.bstack11l1111ll_opy_ = data.get(bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᖾ"), {}).get(bstack1ll1ll_opy_ (u"ࠩ࡬ࡨࠬᖿ"), None)
      return True
    except:
      self.logger.debug(bstack1ll1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᗀ"))
      return False
  def bstack1lll1l1l11l_opy_(self):
    bstack1lll1l1l1l1_opy_ = bstack1ll1ll_opy_ (u"ࠫࡦࡶࡰࠨᗁ") if self.bstack11lll11l1_opy_ else bstack1ll1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᗂ")
    bstack1lll11ll111_opy_ = bstack1ll1ll_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᗃ") if self.config.get(bstack1ll1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᗄ")) is None else True
    bstack11111l1lll_opy_ = bstack1ll1ll_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᗅ").format(self.config[bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᗆ")], bstack1lll1l1l1l1_opy_, bstack1lll11ll111_opy_)
    if self.bstack1lll1lllll1_opy_:
      bstack11111l1lll_opy_ += bstack1ll1ll_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧᗇ").format(self.bstack1lll1lllll1_opy_)
    uri = bstack1l1l1lll1l_opy_(bstack11111l1lll_opy_)
    try:
      response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"ࠫࡌࡋࡔࠨᗈ"), uri, {}, {bstack1ll1ll_opy_ (u"ࠬࡧࡵࡵࡪࠪᗉ"): (self.config[bstack1ll1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᗊ")], self.config[bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᗋ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1ll1llllll_opy_ = data.get(bstack1ll1ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᗌ"))
        self.bstack1lll1lllll1_opy_ = data.get(bstack1ll1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᗍ"))
        os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᗎ")] = str(self.bstack1ll1llllll_opy_)
        os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᗏ")] = str(self.bstack1lll1lllll1_opy_)
        if bstack1lll11ll111_opy_ == bstack1ll1ll_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᗐ") and str(self.bstack1ll1llllll_opy_).lower() == bstack1ll1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᗑ"):
          self.bstack11l11lll_opy_ = True
        if bstack1ll1ll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᗒ") in data:
          return data[bstack1ll1ll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᗓ")]
        else:
          raise bstack1ll1ll_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᗔ").format(data)
      else:
        raise bstack1ll1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᗕ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᗖ").format(e))
  def bstack1lll1ll11l1_opy_(self):
    bstack1lll1llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᗗ"))
    try:
      if bstack1ll1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᗘ") not in self.bstack1lll1l1l111_opy_:
        self.bstack1lll1l1l111_opy_[bstack1ll1ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᗙ")] = 2
      with open(bstack1lll1llllll_opy_, bstack1ll1ll_opy_ (u"ࠨࡹࠪᗚ")) as fp:
        json.dump(self.bstack1lll1l1l111_opy_, fp)
      return bstack1lll1llllll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᗛ").format(e))
  def bstack1lll11l11l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1lll1l111l1_opy_ == bstack1ll1ll_opy_ (u"ࠪࡻ࡮ࡴࠧᗜ"):
        bstack1lll1l11l11_opy_ = [bstack1ll1ll_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᗝ"), bstack1ll1ll_opy_ (u"ࠬ࠵ࡣࠨᗞ")]
        cmd = bstack1lll1l11l11_opy_ + cmd
      cmd = bstack1ll1ll_opy_ (u"࠭ࠠࠨᗟ").join(cmd)
      self.logger.debug(bstack1ll1ll_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᗠ").format(cmd))
      with open(self.bstack1llll111111_opy_, bstack1ll1ll_opy_ (u"ࠣࡣࠥᗡ")) as bstack1lll1lll11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll1lll11l_opy_, text=True, stderr=bstack1lll1lll11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll11l1l11_opy_ = True
      self.logger.error(bstack1ll1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᗢ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll11ll1l1_opy_:
        self.logger.info(bstack1ll1ll_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᗣ"))
        cmd = [self.binary_path, bstack1ll1ll_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᗤ")]
        self.bstack1lll11l11l1_opy_(cmd)
        self.bstack1lll11ll1l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᗥ").format(cmd, e))
  def bstack1l111l1lll_opy_(self):
    if not self.bstack1ll1llllll_opy_:
      return
    try:
      bstack1lll11l11ll_opy_ = 0
      while not self.bstack1lll11ll1l1_opy_ and bstack1lll11l11ll_opy_ < self.bstack1lll1l1ll1l_opy_:
        if self.bstack1lll11l1l11_opy_:
          self.logger.info(bstack1ll1ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᗦ"))
          return
        time.sleep(1)
        bstack1lll11l11ll_opy_ += 1
      os.environ[bstack1ll1ll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᗧ")] = str(self.bstack1lll1l1llll_opy_())
      self.logger.info(bstack1ll1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᗨ"))
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᗩ").format(e))
  def bstack1lll1l1llll_opy_(self):
    if self.bstack11lll11l1_opy_:
      return
    try:
      bstack1lll1l11ll1_opy_ = [platform[bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗪ")].lower() for platform in self.config.get(bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᗫ"), [])]
      bstack1lll1l1l1ll_opy_ = sys.maxsize
      bstack1lll11ll1ll_opy_ = bstack1ll1ll_opy_ (u"ࠬ࠭ᗬ")
      for browser in bstack1lll1l11ll1_opy_:
        if browser in self.bstack1llll1111ll_opy_:
          bstack1lll1l111ll_opy_ = self.bstack1llll1111ll_opy_[browser]
        if bstack1lll1l111ll_opy_ < bstack1lll1l1l1ll_opy_:
          bstack1lll1l1l1ll_opy_ = bstack1lll1l111ll_opy_
          bstack1lll11ll1ll_opy_ = browser
      return bstack1lll11ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᗭ").format(e))
  @classmethod
  def bstack1l1l11ll11_opy_(self):
    return os.getenv(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᗮ"), bstack1ll1ll_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᗯ")).lower()
  @classmethod
  def bstack1l1ll1llll_opy_(self):
    return os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᗰ"), bstack1ll1ll_opy_ (u"ࠪࠫᗱ"))