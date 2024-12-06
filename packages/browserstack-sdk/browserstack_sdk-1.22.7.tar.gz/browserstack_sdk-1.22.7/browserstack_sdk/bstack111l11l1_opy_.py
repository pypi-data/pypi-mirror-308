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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llll11ll_opy_ = {}
        bstack11ll1llll1_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ෻"), bstack1ll1ll_opy_ (u"ࠪࠫ෼"))
        if not bstack11ll1llll1_opy_:
            return bstack1llll11ll_opy_
        try:
            bstack11ll1lll1l_opy_ = json.loads(bstack11ll1llll1_opy_)
            if bstack1ll1ll_opy_ (u"ࠦࡴࡹࠢ෽") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡵࡳࠣ෾")] = bstack11ll1lll1l_opy_[bstack1ll1ll_opy_ (u"ࠨ࡯ࡴࠤ෿")]
            if bstack1ll1ll_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ฀") in bstack11ll1lll1l_opy_ or bstack1ll1ll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦก") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧข")] = bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢฃ"), bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢค")))
            if bstack1ll1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨฅ") in bstack11ll1lll1l_opy_ or bstack1ll1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦฆ") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧง")] = bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤจ"), bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢฉ")))
            if bstack1ll1ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧช") in bstack11ll1lll1l_opy_ or bstack1ll1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧซ") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨฌ")] = bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣญ"), bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣฎ")))
            if bstack1ll1ll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣฏ") in bstack11ll1lll1l_opy_ or bstack1ll1ll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨฐ") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢฑ")] = bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦฒ"), bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤณ")))
            if bstack1ll1ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣด") in bstack11ll1lll1l_opy_ or bstack1ll1ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨต") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢถ")] = bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦท"), bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤธ")))
            if bstack1ll1ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢน") in bstack11ll1lll1l_opy_ or bstack1ll1ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢบ") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣป")] = bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥผ"), bstack11ll1lll1l_opy_.get(bstack1ll1ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥฝ")))
            if bstack1ll1ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦพ") in bstack11ll1lll1l_opy_:
                bstack1llll11ll_opy_[bstack1ll1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧฟ")] = bstack11ll1lll1l_opy_[bstack1ll1ll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨภ")]
        except Exception as error:
            logger.error(bstack1ll1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦม") +  str(error))
        return bstack1llll11ll_opy_