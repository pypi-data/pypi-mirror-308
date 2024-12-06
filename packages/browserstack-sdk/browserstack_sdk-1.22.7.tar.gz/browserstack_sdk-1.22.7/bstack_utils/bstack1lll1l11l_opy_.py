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
class bstack111l1l1lll_opy_(object):
  bstack1l11l1l11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"࠭ࡾࠨဌ")), bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧဍ"))
  bstack111l1ll11l_opy_ = os.path.join(bstack1l11l1l11l_opy_, bstack1ll1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨဎ"))
  bstack111l1ll1ll_opy_ = None
  perform_scan = None
  bstack1ll11lll11_opy_ = None
  bstack111111111_opy_ = None
  bstack111ll111ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫဏ")):
      cls.instance = super(bstack111l1l1lll_opy_, cls).__new__(cls)
      cls.instance.bstack111l1ll1l1_opy_()
    return cls.instance
  def bstack111l1ll1l1_opy_(self):
    try:
      with open(self.bstack111l1ll11l_opy_, bstack1ll1ll_opy_ (u"ࠪࡶࠬတ")) as bstack11llll11_opy_:
        bstack111l1lll11_opy_ = bstack11llll11_opy_.read()
        data = json.loads(bstack111l1lll11_opy_)
        if bstack1ll1ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ထ") in data:
          self.bstack111lll1l1l_opy_(data[bstack1ll1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧဒ")])
        if bstack1ll1ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧဓ") in data:
          self.bstack111ll1l11l_opy_(data[bstack1ll1ll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨန")])
    except:
      pass
  def bstack111ll1l11l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1ll1ll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ပ")]
      self.bstack1ll11lll11_opy_ = scripts[bstack1ll1ll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ဖ")]
      self.bstack111111111_opy_ = scripts[bstack1ll1ll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧဗ")]
      self.bstack111ll111ll_opy_ = scripts[bstack1ll1ll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩဘ")]
  def bstack111lll1l1l_opy_(self, bstack111l1ll1ll_opy_):
    if bstack111l1ll1ll_opy_ != None and len(bstack111l1ll1ll_opy_) != 0:
      self.bstack111l1ll1ll_opy_ = bstack111l1ll1ll_opy_
  def store(self):
    try:
      with open(self.bstack111l1ll11l_opy_, bstack1ll1ll_opy_ (u"ࠬࡽࠧမ")) as file:
        json.dump({
          bstack1ll1ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣယ"): self.bstack111l1ll1ll_opy_,
          bstack1ll1ll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣရ"): {
            bstack1ll1ll_opy_ (u"ࠣࡵࡦࡥࡳࠨလ"): self.perform_scan,
            bstack1ll1ll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨဝ"): self.bstack1ll11lll11_opy_,
            bstack1ll1ll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢသ"): self.bstack111111111_opy_,
            bstack1ll1ll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤဟ"): self.bstack111ll111ll_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll1ll111l_opy_(self, bstack111l1ll111_opy_):
    try:
      return any(command.get(bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪဠ")) == bstack111l1ll111_opy_ for command in self.bstack111l1ll1ll_opy_)
    except:
      return False
bstack1lll1l11l_opy_ = bstack111l1l1lll_opy_()