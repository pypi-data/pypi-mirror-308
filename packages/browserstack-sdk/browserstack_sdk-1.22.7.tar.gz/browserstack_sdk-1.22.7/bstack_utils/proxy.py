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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll11l1l1_opy_
bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
def bstack1lll111111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1111111_opy_(bstack1ll1lllll11_opy_, bstack1ll1llllll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1lllll11_opy_):
        with open(bstack1ll1lllll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll111111l_opy_(bstack1ll1lllll11_opy_):
        pac = get_pac(url=bstack1ll1lllll11_opy_)
    else:
        raise Exception(bstack1ll1ll_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᗳ").format(bstack1ll1lllll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1ll_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᗴ"), 80))
        bstack1lll11111l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll11111l1_opy_ = bstack1ll1ll_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᗵ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1llllll1_opy_, bstack1lll11111l1_opy_)
    return proxy_url
def bstack111lllll_opy_(config):
    return bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᗶ") in config or bstack1ll1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᗷ") in config
def bstack1llll111l1_opy_(config):
    if not bstack111lllll_opy_(config):
        return
    if config.get(bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᗸ")):
        return config.get(bstack1ll1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᗹ"))
    if config.get(bstack1ll1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᗺ")):
        return config.get(bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᗻ"))
def bstack1l11l1l1l_opy_(config, bstack1ll1llllll1_opy_):
    proxy = bstack1llll111l1_opy_(config)
    proxies = {}
    if config.get(bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᗼ")) or config.get(bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᗽ")):
        if proxy.endswith(bstack1ll1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᗾ")):
            proxies = bstack11llllll_opy_(proxy, bstack1ll1llllll1_opy_)
        else:
            proxies = {
                bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᗿ"): proxy
            }
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᘀ"), proxies)
    return proxies
def bstack11llllll_opy_(bstack1ll1lllll11_opy_, bstack1ll1llllll1_opy_):
    proxies = {}
    global bstack1ll1lllll1l_opy_
    if bstack1ll1ll_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᘁ") in globals():
        return bstack1ll1lllll1l_opy_
    try:
        proxy = bstack1lll1111111_opy_(bstack1ll1lllll11_opy_, bstack1ll1llllll1_opy_)
        if bstack1ll1ll_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᘂ") in proxy:
            proxies = {}
        elif bstack1ll1ll_opy_ (u"ࠢࡉࡖࡗࡔࠧᘃ") in proxy or bstack1ll1ll_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᘄ") in proxy or bstack1ll1ll_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᘅ") in proxy:
            bstack1ll1lllllll_opy_ = proxy.split(bstack1ll1ll_opy_ (u"ࠥࠤࠧᘆ"))
            if bstack1ll1ll_opy_ (u"ࠦ࠿࠵࠯ࠣᘇ") in bstack1ll1ll_opy_ (u"ࠧࠨᘈ").join(bstack1ll1lllllll_opy_[1:]):
                proxies = {
                    bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᘉ"): bstack1ll1ll_opy_ (u"ࠢࠣᘊ").join(bstack1ll1lllllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᘋ"): str(bstack1ll1lllllll_opy_[0]).lower() + bstack1ll1ll_opy_ (u"ࠤ࠽࠳࠴ࠨᘌ") + bstack1ll1ll_opy_ (u"ࠥࠦᘍ").join(bstack1ll1lllllll_opy_[1:])
                }
        elif bstack1ll1ll_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᘎ") in proxy:
            bstack1ll1lllllll_opy_ = proxy.split(bstack1ll1ll_opy_ (u"ࠧࠦࠢᘏ"))
            if bstack1ll1ll_opy_ (u"ࠨ࠺࠰࠱ࠥᘐ") in bstack1ll1ll_opy_ (u"ࠢࠣᘑ").join(bstack1ll1lllllll_opy_[1:]):
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᘒ"): bstack1ll1ll_opy_ (u"ࠤࠥᘓ").join(bstack1ll1lllllll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘔ"): bstack1ll1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᘕ") + bstack1ll1ll_opy_ (u"ࠧࠨᘖ").join(bstack1ll1lllllll_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᘗ"): proxy
            }
    except Exception as e:
        print(bstack1ll1ll_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᘘ"), bstack1llll11l1l1_opy_.format(bstack1ll1lllll11_opy_, str(e)))
    bstack1ll1lllll1l_opy_ = proxies
    return proxies