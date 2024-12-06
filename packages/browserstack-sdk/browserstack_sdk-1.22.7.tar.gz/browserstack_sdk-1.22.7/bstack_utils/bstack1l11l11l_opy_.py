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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack1111l1l11l_opy_, bstack11l1ll11l_opy_, bstack1l1lll11_opy_, bstack1l1l1l1lll_opy_, \
    bstack11111lll11_opy_
def bstack11lll111_opy_(bstack1ll1l1lll11_opy_):
    for driver in bstack1ll1l1lll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l1llll_opy_(driver, status, reason=bstack1ll1ll_opy_ (u"ࠬ࠭ᙎ")):
    bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
    if bstack1l1l1l1ll_opy_.bstack11l111llll_opy_():
        return
    bstack11llll1l_opy_ = bstack1ll1l111l_opy_(bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᙏ"), bstack1ll1ll_opy_ (u"ࠧࠨᙐ"), status, reason, bstack1ll1ll_opy_ (u"ࠨࠩᙑ"), bstack1ll1ll_opy_ (u"ࠩࠪᙒ"))
    driver.execute_script(bstack11llll1l_opy_)
def bstack11l1111l_opy_(page, status, reason=bstack1ll1ll_opy_ (u"ࠪࠫᙓ")):
    try:
        if page is None:
            return
        bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
        if bstack1l1l1l1ll_opy_.bstack11l111llll_opy_():
            return
        bstack11llll1l_opy_ = bstack1ll1l111l_opy_(bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᙔ"), bstack1ll1ll_opy_ (u"ࠬ࠭ᙕ"), status, reason, bstack1ll1ll_opy_ (u"࠭ࠧᙖ"), bstack1ll1ll_opy_ (u"ࠧࠨᙗ"))
        page.evaluate(bstack1ll1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᙘ"), bstack11llll1l_opy_)
    except Exception as e:
        print(bstack1ll1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᙙ"), e)
def bstack1ll1l111l_opy_(type, name, status, reason, bstack1l1l111l11_opy_, bstack1ll11l1ll_opy_):
    bstack1lll1lll11_opy_ = {
        bstack1ll1ll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᙚ"): type,
        bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙛ"): {}
    }
    if type == bstack1ll1ll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᙜ"):
        bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᙝ")][bstack1ll1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙞ")] = bstack1l1l111l11_opy_
        bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᙟ")][bstack1ll1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧᙠ")] = json.dumps(str(bstack1ll11l1ll_opy_))
    if type == bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᙡ"):
        bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙢ")][bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙣ")] = name
    if type == bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᙤ"):
        bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᙥ")][bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙦ")] = status
        if status == bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᙧ") and str(reason) != bstack1ll1ll_opy_ (u"ࠥࠦᙨ"):
            bstack1lll1lll11_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᙩ")][bstack1ll1ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙪ")] = json.dumps(str(reason))
    bstack1lll111l1_opy_ = bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᙫ").format(json.dumps(bstack1lll1lll11_opy_))
    return bstack1lll111l1_opy_
def bstack1ll111lll_opy_(url, config, logger, bstack1lllll11l_opy_=False):
    hostname = bstack11l1ll11l_opy_(url)
    is_private = bstack1l1l1l1lll_opy_(hostname)
    try:
        if is_private or bstack1lllll11l_opy_:
            file_path = bstack1111l1l11l_opy_(bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᙬ"), bstack1ll1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ᙭"), logger)
            if os.environ.get(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ᙮")) and eval(
                    os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᙯ"))):
                return
            if (bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᙰ") in config and not config[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᙱ")]):
                os.environ[bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᙲ")] = str(True)
                bstack1ll1l1lll1l_opy_ = {bstack1ll1ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᙳ"): hostname}
                bstack11111lll11_opy_(bstack1ll1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᙴ"), bstack1ll1ll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᙵ"), bstack1ll1l1lll1l_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l1l1l1l_opy_(caps, bstack1ll1l1ll1l1_opy_):
    if bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᙶ") in caps:
        caps[bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᙷ")][bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᙸ")] = True
        if bstack1ll1l1ll1l1_opy_:
            caps[bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᙹ")][bstack1ll1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᙺ")] = bstack1ll1l1ll1l1_opy_
    else:
        caps[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᙻ")] = True
        if bstack1ll1l1ll1l1_opy_:
            caps[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᙼ")] = bstack1ll1l1ll1l1_opy_
def bstack1ll1llll1ll_opy_(bstack11l1lllll1_opy_):
    bstack1ll1l1ll1ll_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᙽ"), bstack1ll1ll_opy_ (u"ࠫࠬᙾ"))
    if bstack1ll1l1ll1ll_opy_ == bstack1ll1ll_opy_ (u"ࠬ࠭ᙿ") or bstack1ll1l1ll1ll_opy_ == bstack1ll1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ "):
        threading.current_thread().testStatus = bstack11l1lllll1_opy_
    else:
        if bstack11l1lllll1_opy_ == bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᚁ"):
            threading.current_thread().testStatus = bstack11l1lllll1_opy_