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
import re
from bstack_utils.bstack1l11l11l_opy_ import bstack1ll1llll1ll_opy_
def bstack1ll1llll11l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘙ")):
        return bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᘚ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘛ")):
        return bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᘜ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘝ")):
        return bstack1ll1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᘞ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᘟ")):
        return bstack1ll1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᘠ")
def bstack1ll1lll1111_opy_(fixture_name):
    return bool(re.match(bstack1ll1ll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᘡ"), fixture_name))
def bstack1ll1llll111_opy_(fixture_name):
    return bool(re.match(bstack1ll1ll_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᘢ"), fixture_name))
def bstack1ll1lll111l_opy_(fixture_name):
    return bool(re.match(bstack1ll1ll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᘣ"), fixture_name))
def bstack1ll1ll1lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᘤ")):
        return bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᘥ"), bstack1ll1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᘦ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᘧ")):
        return bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᘨ"), bstack1ll1ll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᘩ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᘪ")):
        return bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᘫ"), bstack1ll1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᘬ")
    elif fixture_name.startswith(bstack1ll1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᘭ")):
        return bstack1ll1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᘮ"), bstack1ll1ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᘯ")
    return None, None
def bstack1ll1lll11ll_opy_(hook_name):
    if hook_name in [bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᘰ"), bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᘱ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1lll1l1l_opy_(hook_name):
    if hook_name in [bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᘲ"), bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᘳ")]:
        return bstack1ll1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᘴ")
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᘵ"), bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᘶ")]:
        return bstack1ll1ll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᘷ")
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᘸ"), bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᘹ")]:
        return bstack1ll1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᘺ")
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᘻ"), bstack1ll1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᘼ")]:
        return bstack1ll1ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᘽ")
    return hook_name
def bstack1ll1ll1llll_opy_(node, scenario):
    if hasattr(node, bstack1ll1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᘾ")):
        parts = node.nodeid.rsplit(bstack1ll1ll_opy_ (u"ࠦࡠࠨᘿ"))
        params = parts[-1]
        return bstack1ll1ll_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᙀ").format(scenario.name, params)
    return scenario.name
def bstack1ll1lll1l11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1ll_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᙁ")):
            examples = list(node.callspec.params[bstack1ll1ll_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᙂ")].values())
        return examples
    except:
        return []
def bstack1ll1lll1lll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1lll1ll1_opy_(report):
    try:
        status = bstack1ll1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᙃ")
        if report.passed or (report.failed and hasattr(report, bstack1ll1ll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᙄ"))):
            status = bstack1ll1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᙅ")
        elif report.skipped:
            status = bstack1ll1ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᙆ")
        bstack1ll1llll1ll_opy_(status)
    except:
        pass
def bstack1ll1l1ll_opy_(status):
    try:
        bstack1ll1llll1l1_opy_ = bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᙇ")
        if status == bstack1ll1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᙈ"):
            bstack1ll1llll1l1_opy_ = bstack1ll1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᙉ")
        elif status == bstack1ll1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᙊ"):
            bstack1ll1llll1l1_opy_ = bstack1ll1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᙋ")
        bstack1ll1llll1ll_opy_(bstack1ll1llll1l1_opy_)
    except:
        pass
def bstack1ll1lll11l1_opy_(item=None, report=None, summary=None, extra=None):
    return