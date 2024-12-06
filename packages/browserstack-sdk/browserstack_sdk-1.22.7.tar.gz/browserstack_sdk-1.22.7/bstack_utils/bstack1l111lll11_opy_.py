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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack111lll1l11_opy_, bstack111ll11ll1_opy_, bstack1l1l111l1l_opy_, bstack11l1llllll_opy_, bstack1111l1llll_opy_, bstack111111l1ll_opy_, bstack1111ll11l1_opy_, bstack1l1l11l11l_opy_
from bstack_utils.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1ll1l_opy_
import bstack_utils.bstack1l1l1111ll_opy_ as bstack1ll1l111l1_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack1111llll_opy_
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11l11l1_opy_
from bstack_utils.bstack1lll1l11l_opy_ import bstack1lll1l11l_opy_
from bstack_utils.bstack11ll1ll11l_opy_ import bstack11l11lll1l_opy_
bstack1ll11l1ll11_opy_ = bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᛁ")
logger = logging.getLogger(__name__)
class bstack1llll1ll_opy_:
    bstack1ll1ll1l1l1_opy_ = None
    bs_config = None
    bstack1ll1l1l1l1_opy_ = None
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1ll1l1l1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll1l1l1l1_opy_ = bstack1ll1l1l1l1_opy_
        try:
            cls.bstack1ll11lll11l_opy_()
            bstack111ll111l1_opy_ = bstack111lll1l11_opy_(bs_config)
            bstack111ll1ll1l_opy_ = bstack111ll11ll1_opy_(bs_config)
            data = bstack1ll1l111l1_opy_.bstack1ll11l1l11l_opy_(bs_config, bstack1ll1l1l1l1_opy_)
            config = {
                bstack1ll1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᛂ"): (bstack111ll111l1_opy_, bstack111ll1ll1l_opy_),
                bstack1ll1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᛃ"): cls.default_headers()
            }
            response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"ࠫࡕࡕࡓࡕࠩᛄ"), cls.request_url(bstack1ll1ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬᛅ")), data, config)
            if response.status_code != 200:
                bstack1ll1l1111ll_opy_ = response.json()
                if bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᛆ")] == False:
                    cls.bstack1ll11ll111l_opy_(bstack1ll1l1111ll_opy_)
                    return
                cls.bstack1ll11lll111_opy_(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᛇ")])
                cls.bstack1ll11l1ll1l_opy_(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛈ")])
                return None
            bstack1ll1l111ll1_opy_ = cls.bstack1ll11lllll1_opy_(response)
            return bstack1ll1l111ll1_opy_
        except Exception as error:
            logger.error(bstack1ll1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢᛉ").format(str(error)))
            return None
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def stop(cls, bstack1ll11ll1ll1_opy_=None):
        if not bstack1111llll_opy_.on() and not bstack1l11l11l1_opy_.on():
            return
        if os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛊ")) == bstack1ll1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛋ") or os.environ.get(bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛌ")) == bstack1ll1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛍ"):
            logger.error(bstack1ll1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᛎ"))
            return {
                bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᛏ"): bstack1ll1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᛐ"),
                bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᛑ"): bstack1ll1ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᛒ")
            }
        try:
            cls.bstack1ll1ll1l1l1_opy_.shutdown()
            data = {
                bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛓ"): bstack1l1l11l11l_opy_()
            }
            if not bstack1ll11ll1ll1_opy_ is None:
                data[bstack1ll1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪᛔ")] = [{
                    bstack1ll1ll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᛕ"): bstack1ll1ll_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ᛖ"),
                    bstack1ll1ll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩᛗ"): bstack1ll11ll1ll1_opy_
                }]
            config = {
                bstack1ll1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᛘ"): cls.default_headers()
            }
            bstack11111l1lll_opy_ = bstack1ll1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬᛙ").format(os.environ[bstack1ll1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥᛚ")])
            bstack1ll11l1l111_opy_ = cls.request_url(bstack11111l1lll_opy_)
            response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"࠭ࡐࡖࡖࠪᛛ"), bstack1ll11l1l111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll1ll_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨᛜ"))
        except Exception as error:
            logger.error(bstack1ll1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧᛝ") + str(error))
            return {
                bstack1ll1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᛞ"): bstack1ll1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᛟ"),
                bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᛠ"): str(error)
            }
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def bstack1ll11lllll1_opy_(cls, response):
        bstack1ll1l1111ll_opy_ = response.json()
        bstack1ll1l111ll1_opy_ = {}
        if bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡰࡷࡵࠩᛡ")) is None:
            os.environ[bstack1ll1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛢ")] = bstack1ll1ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛣ")
        else:
            os.environ[bstack1ll1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛤ")] = bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠩ࡭ࡻࡹ࠭ᛥ"), bstack1ll1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛦ"))
        os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛧ")] = bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᛨ"), bstack1ll1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛩ"))
        if bstack1111llll_opy_.bstack1ll1l111l1l_opy_(cls.bs_config, cls.bstack1ll1l1l1l1_opy_.get(bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᛪ"), bstack1ll1ll_opy_ (u"ࠨࠩ᛫"))) is True:
            bstack1ll11ll1l1l_opy_, bstack1l1ll1l11_opy_, bstack1ll11ll11l1_opy_ = cls.bstack1ll1l1111l1_opy_(bstack1ll1l1111ll_opy_)
            if bstack1ll11ll1l1l_opy_ != None and bstack1l1ll1l11_opy_ != None:
                bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᛬")] = {
                    bstack1ll1ll_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭᛭"): bstack1ll11ll1l1l_opy_,
                    bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᛮ"): bstack1l1ll1l11_opy_,
                    bstack1ll1ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᛯ"): bstack1ll11ll11l1_opy_
                }
            else:
                bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᛰ")] = {}
        else:
            bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᛱ")] = {}
        if bstack1l11l11l1_opy_.bstack111llll1l1_opy_(cls.bs_config) is True:
            bstack1ll11lll1ll_opy_, bstack1l1ll1l11_opy_ = cls.bstack1ll11ll1l11_opy_(bstack1ll1l1111ll_opy_)
            if bstack1ll11lll1ll_opy_ != None and bstack1l1ll1l11_opy_ != None:
                bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛲ")] = {
                    bstack1ll1ll_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭ᛳ"): bstack1ll11lll1ll_opy_,
                    bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᛴ"): bstack1l1ll1l11_opy_,
                }
            else:
                bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛵ")] = {}
        else:
            bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᛶ")] = {}
        if bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᛷ")].get(bstack1ll1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᛸ")) != None or bstack1ll1l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᛹")].get(bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ᛺")) != None:
            cls.bstack1ll11llllll_opy_(bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠪ࡮ࡼࡺࠧ᛻")), bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᛼")))
        return bstack1ll1l111ll1_opy_
    @classmethod
    def bstack1ll1l1111l1_opy_(cls, bstack1ll1l1111ll_opy_):
        if bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᛽")) == None:
            cls.bstack1ll11lll111_opy_()
            return [None, None, None]
        if bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᛾")][bstack1ll1ll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ᛿")] != True:
            cls.bstack1ll11lll111_opy_(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᜀ")])
            return [None, None, None]
        logger.debug(bstack1ll1ll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᜁ"))
        os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᜂ")] = bstack1ll1ll_opy_ (u"ࠫࡹࡸࡵࡦࠩᜃ")
        if bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡰࡷࡵࠩᜄ")):
            os.environ[bstack1ll1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᜅ")] = bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠧ࡫ࡹࡷࠫᜆ")]
            os.environ[bstack1ll1ll_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᜇ")] = json.dumps({
                bstack1ll1ll_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᜈ"): bstack111lll1l11_opy_(cls.bs_config),
                bstack1ll1ll_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᜉ"): bstack111ll11ll1_opy_(cls.bs_config)
            })
        if bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᜊ")):
            os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᜋ")] = bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᜌ")]
        if bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᜍ")].get(bstack1ll1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜎ"), {}).get(bstack1ll1ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᜏ")):
            os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᜐ")] = str(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᜑ")][bstack1ll1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜒ")][bstack1ll1ll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᜓ")])
        return [bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠧ࡫ࡹࡷ᜔ࠫ")], bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ᜕ࠪ")], os.environ[bstack1ll1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ᜖")]]
    @classmethod
    def bstack1ll11ll1l11_opy_(cls, bstack1ll1l1111ll_opy_):
        if bstack1ll1l1111ll_opy_.get(bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᜗")) == None:
            cls.bstack1ll11l1ll1l_opy_()
            return [None, None]
        if bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᜘")][bstack1ll1ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭᜙")] != True:
            cls.bstack1ll11l1ll1l_opy_(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᜚")])
            return [None, None]
        if bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᜛")].get(bstack1ll1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᜜")):
            logger.debug(bstack1ll1ll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭᜝"))
            parsed = json.loads(os.getenv(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ᜞"), bstack1ll1ll_opy_ (u"ࠫࢀࢃࠧᜟ")))
            capabilities = bstack1ll1l111l1_opy_.bstack1ll11llll1l_opy_(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜠ")][bstack1ll1ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᜡ")][bstack1ll1ll_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜢ")], bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᜣ"), bstack1ll1ll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᜤ"))
            bstack1ll11lll1ll_opy_ = capabilities[bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᜥ")]
            os.environ[bstack1ll1ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᜦ")] = bstack1ll11lll1ll_opy_
            parsed[bstack1ll1ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜧ")] = capabilities[bstack1ll1ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᜨ")]
            os.environ[bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᜩ")] = json.dumps(parsed)
            scripts = bstack1ll1l111l1_opy_.bstack1ll11llll1l_opy_(bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜪ")][bstack1ll1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᜫ")][bstack1ll1ll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᜬ")], bstack1ll1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᜭ"), bstack1ll1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭ᜮ"))
            bstack1lll1l11l_opy_.bstack111ll1l11l_opy_(scripts)
            commands = bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᜯ")][bstack1ll1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᜰ")][bstack1ll1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩᜱ")].get(bstack1ll1ll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᜲ"))
            bstack1lll1l11l_opy_.bstack111lll1l1l_opy_(commands)
            bstack1lll1l11l_opy_.store()
        return [bstack1ll11lll1ll_opy_, bstack1ll1l1111ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᜳ")]]
    @classmethod
    def bstack1ll11lll111_opy_(cls, response=None):
        os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅ᜴ࠩ")] = bstack1ll1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᜵")
        os.environ[bstack1ll1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬ᜶")] = bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᜷")
        os.environ[bstack1ll1ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᜸")] = bstack1ll1ll_opy_ (u"ࠩࡱࡹࡱࡲࠧ᜹")
        os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫ᜺")] = bstack1ll1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ᜻")
        os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ᜼")] = bstack1ll1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ᜽")
        os.environ[bstack1ll1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ᜾")] = bstack1ll1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ᜿")
        cls.bstack1ll11ll111l_opy_(response, bstack1ll1ll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᝀ"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l1ll1l_opy_(cls, response=None):
        os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᝁ")] = bstack1ll1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᝂ")
        os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᝃ")] = bstack1ll1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᝄ")
        os.environ[bstack1ll1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᝅ")] = bstack1ll1ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᝆ")
        cls.bstack1ll11ll111l_opy_(response, bstack1ll1ll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᝇ"))
        return [None, None, None]
    @classmethod
    def bstack1ll11llllll_opy_(cls, bstack1ll1l11111l_opy_, bstack1l1ll1l11_opy_):
        os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᝈ")] = bstack1ll1l11111l_opy_
        os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᝉ")] = bstack1l1ll1l11_opy_
    @classmethod
    def bstack1ll11ll111l_opy_(cls, response=None, product=bstack1ll1ll_opy_ (u"ࠧࠨᝊ")):
        if response == None:
            logger.error(product + bstack1ll1ll_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᝋ"))
        for error in response[bstack1ll1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᝌ")]:
            bstack1111llll1l_opy_ = error[bstack1ll1ll_opy_ (u"ࠨ࡭ࡨࡽࠬᝍ")]
            error_message = error[bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᝎ")]
            if error_message:
                if bstack1111llll1l_opy_ == bstack1ll1ll_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤᝏ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll1ll_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧᝐ") + product + bstack1ll1ll_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᝑ"))
    @classmethod
    def bstack1ll11lll11l_opy_(cls):
        if cls.bstack1ll1ll1l1l1_opy_ is not None:
            return
        cls.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1ll1l_opy_(cls.bstack1ll1l111l11_opy_)
        cls.bstack1ll1ll1l1l1_opy_.start()
    @classmethod
    def bstack11l1l1l111_opy_(cls):
        if cls.bstack1ll1ll1l1l1_opy_ is None:
            return
        cls.bstack1ll1ll1l1l1_opy_.shutdown()
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def bstack1ll1l111l11_opy_(cls, bstack11l1l11111_opy_, bstack1ll11llll11_opy_=bstack1ll1ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᝒ")):
        config = {
            bstack1ll1ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᝓ"): cls.default_headers()
        }
        response = bstack1l1l111l1l_opy_(bstack1ll1ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭᝔"), cls.request_url(bstack1ll11llll11_opy_), bstack11l1l11111_opy_, config)
        bstack111lll11ll_opy_ = response.json()
    @classmethod
    def bstack11l1l11l11_opy_(cls, bstack11l1l11111_opy_, bstack1ll11llll11_opy_=bstack1ll1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ᝕")):
        if not bstack1ll1l111l1_opy_.bstack1ll11ll11ll_opy_(bstack11l1l11111_opy_[bstack1ll1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ᝖")]):
            return
        bstack11l1l11ll_opy_ = bstack1ll1l111l1_opy_.bstack1ll1l111111_opy_(bstack11l1l11111_opy_[bstack1ll1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ᝗")], bstack11l1l11111_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ᝘")))
        if bstack11l1l11ll_opy_ != None:
            if bstack11l1l11111_opy_.get(bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ᝙")) != None:
                bstack11l1l11111_opy_[bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ᝚")][bstack1ll1ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭᝛")] = bstack11l1l11ll_opy_
            else:
                bstack11l1l11111_opy_[bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ᝜")] = bstack11l1l11ll_opy_
        if bstack1ll11llll11_opy_ == bstack1ll1ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ᝝"):
            cls.bstack1ll11lll11l_opy_()
            cls.bstack1ll1ll1l1l1_opy_.add(bstack11l1l11111_opy_)
        elif bstack1ll11llll11_opy_ == bstack1ll1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ᝞"):
            cls.bstack1ll1l111l11_opy_([bstack11l1l11111_opy_], bstack1ll11llll11_opy_)
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def bstack1lll11l1l1_opy_(cls, bstack11l1l1ll11_opy_):
        bstack1ll11l1l1l1_opy_ = []
        for log in bstack11l1l1ll11_opy_:
            bstack1ll11l1llll_opy_ = {
                bstack1ll1ll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᝟"): bstack1ll1ll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᝠ"),
                bstack1ll1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᝡ"): log[bstack1ll1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᝢ")],
                bstack1ll1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᝣ"): log[bstack1ll1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᝤ")],
                bstack1ll1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᝥ"): {},
                bstack1ll1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᝦ"): log[bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᝧ")],
            }
            if bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᝨ") in log:
                bstack1ll11l1llll_opy_[bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᝩ")] = log[bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᝪ")]
            elif bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᝫ") in log:
                bstack1ll11l1llll_opy_[bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᝬ")] = log[bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝭")]
            bstack1ll11l1l1l1_opy_.append(bstack1ll11l1llll_opy_)
        cls.bstack11l1l11l11_opy_({
            bstack1ll1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᝮ"): bstack1ll1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᝯ"),
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᝰ"): bstack1ll11l1l1l1_opy_
        })
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def bstack1ll11lll1l1_opy_(cls, steps):
        bstack1ll11ll1lll_opy_ = []
        for step in steps:
            bstack1ll11l1lll1_opy_ = {
                bstack1ll1ll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ᝱"): bstack1ll1ll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ᝲ"),
                bstack1ll1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᝳ"): step[bstack1ll1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᝴")],
                bstack1ll1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ᝵"): step[bstack1ll1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᝶")],
                bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᝷"): step[bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᝸")],
                bstack1ll1ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ᝹"): step[bstack1ll1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭᝺")]
            }
            if bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝻") in step:
                bstack1ll11l1lll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᝼")] = step[bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᝽")]
            elif bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝾") in step:
                bstack1ll11l1lll1_opy_[bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᝿")] = step[bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪក")]
            bstack1ll11ll1lll_opy_.append(bstack1ll11l1lll1_opy_)
        cls.bstack11l1l11l11_opy_({
            bstack1ll1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨខ"): bstack1ll1ll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩគ"),
            bstack1ll1ll_opy_ (u"࠭࡬ࡰࡩࡶࠫឃ"): bstack1ll11ll1lll_opy_
        })
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def bstack1llllllll_opy_(cls, screenshot):
        cls.bstack11l1l11l11_opy_({
            bstack1ll1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫង"): bstack1ll1ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬច"),
            bstack1ll1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧឆ"): [{
                bstack1ll1ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨជ"): bstack1ll1ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ឈ"),
                bstack1ll1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨញ"): datetime.datetime.utcnow().isoformat() + bstack1ll1ll_opy_ (u"࡚࠭ࠨដ"),
                bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨឋ"): screenshot[bstack1ll1ll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧឌ")],
                bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩឍ"): screenshot[bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪណ")]
            }]
        }, bstack1ll11llll11_opy_=bstack1ll1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩត"))
    @classmethod
    @bstack11l1llllll_opy_(class_method=True)
    def bstack1ll1l1ll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1l11l11_opy_({
            bstack1ll1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩថ"): bstack1ll1ll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪទ"),
            bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩធ"): {
                bstack1ll1ll_opy_ (u"ࠣࡷࡸ࡭ࡩࠨន"): cls.current_test_uuid(),
                bstack1ll1ll_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣប"): cls.bstack11ll11l1ll_opy_(driver)
            }
        })
    @classmethod
    def bstack11ll1l1ll1_opy_(cls, event: str, bstack11l1l11111_opy_: bstack11l11lll1l_opy_):
        bstack11l1lll1l1_opy_ = {
            bstack1ll1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧផ"): event,
            bstack11l1l11111_opy_.bstack11l1l1l1ll_opy_(): bstack11l1l11111_opy_.bstack11l1lll1ll_opy_(event)
        }
        cls.bstack11l1l11l11_opy_(bstack11l1lll1l1_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬព"), None) is None or os.environ[bstack1ll1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ភ")] == bstack1ll1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦម")) and (os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬយ"), None) is None or os.environ[bstack1ll1ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭រ")] == bstack1ll1ll_opy_ (u"ࠤࡱࡹࡱࡲࠢល")):
            return False
        return True
    @staticmethod
    def bstack1ll11l1l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩវ"): bstack1ll1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧឝ"),
            bstack1ll1ll_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨឞ"): bstack1ll1ll_opy_ (u"࠭ࡴࡳࡷࡨࠫស")
        }
        if os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨហ"), None):
            headers[bstack1ll1ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨឡ")] = bstack1ll1ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬអ").format(os.environ[bstack1ll1ll_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦឣ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll1ll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪឤ").format(bstack1ll11l1ll11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩឥ"), None)
    @staticmethod
    def bstack11ll11l1ll_opy_(driver):
        return {
            bstack1111l1llll_opy_(): bstack111111l1ll_opy_(driver)
        }
    @staticmethod
    def bstack1ll11ll1111_opy_(exception_info, report):
        return [{bstack1ll1ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩឦ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111llllll1_opy_(typename):
        if bstack1ll1ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥឧ") in typename:
            return bstack1ll1ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤឨ")
        return bstack1ll1ll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥឩ")