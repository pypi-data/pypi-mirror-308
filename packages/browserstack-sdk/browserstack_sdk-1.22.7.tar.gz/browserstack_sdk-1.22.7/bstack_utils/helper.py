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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111l1111ll_opy_, bstack1l11l1ll_opy_, bstack1l11ll11l_opy_, bstack1ll11l1l1l_opy_,
                                    bstack111l11ll1l_opy_, bstack111l111lll_opy_, bstack111l11l111_opy_, bstack111l11111l_opy_)
from bstack_utils.messages import bstack1ll1111l1_opy_, bstack1lll11ll_opy_
from bstack_utils.proxy import bstack1l11l1l1l_opy_, bstack1llll111l1_opy_
bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
logger = logging.getLogger(__name__)
def bstack111lll1l11_opy_(config):
    return config[bstack1ll1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጘ")]
def bstack111ll11ll1_opy_(config):
    return config[bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጙ")]
def bstack1l1l11ll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1111lllll1_opy_(obj):
    values = []
    bstack1lllllll1l1_opy_ = re.compile(bstack1ll1ll_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣጚ"), re.I)
    for key in obj.keys():
        if bstack1lllllll1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111lll1l1_opy_(config):
    tags = []
    tags.extend(bstack1111lllll1_opy_(os.environ))
    tags.extend(bstack1111lllll1_opy_(config))
    return tags
def bstack1llllll1l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1lllll1l1ll_opy_(bstack1111l11l1l_opy_):
    if not bstack1111l11l1l_opy_:
        return bstack1ll1ll_opy_ (u"ࠬ࠭ጛ")
    return bstack1ll1ll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢጜ").format(bstack1111l11l1l_opy_.name, bstack1111l11l1l_opy_.email)
def bstack111lll1ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1lllllll111_opy_ = repo.common_dir
        info = {
            bstack1ll1ll_opy_ (u"ࠢࡴࡪࡤࠦጝ"): repo.head.commit.hexsha,
            bstack1ll1ll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦጞ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1ll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤጟ"): repo.active_branch.name,
            bstack1ll1ll_opy_ (u"ࠥࡸࡦ࡭ࠢጠ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢጡ"): bstack1lllll1l1ll_opy_(repo.head.commit.committer),
            bstack1ll1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨጢ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1ll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨጣ"): bstack1lllll1l1ll_opy_(repo.head.commit.author),
            bstack1ll1ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧጤ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1ll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤጥ"): repo.head.commit.message,
            bstack1ll1ll_opy_ (u"ࠤࡵࡳࡴࡺࠢጦ"): repo.git.rev_parse(bstack1ll1ll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧጧ")),
            bstack1ll1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧጨ"): bstack1lllllll111_opy_,
            bstack1ll1ll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣጩ"): subprocess.check_output([bstack1ll1ll_opy_ (u"ࠨࡧࡪࡶࠥጪ"), bstack1ll1ll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥጫ"), bstack1ll1ll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦጬ")]).strip().decode(
                bstack1ll1ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨጭ")),
            bstack1ll1ll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧጮ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨጯ"): repo.git.rev_list(
                bstack1ll1ll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧጰ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111ll111_opy_ = []
        for remote in remotes:
            bstack1111l11lll_opy_ = {
                bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጱ"): remote.name,
                bstack1ll1ll_opy_ (u"ࠢࡶࡴ࡯ࠦጲ"): remote.url,
            }
            bstack11111ll111_opy_.append(bstack1111l11lll_opy_)
        bstack11111l1l1l_opy_ = {
            bstack1ll1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨጳ"): bstack1ll1ll_opy_ (u"ࠤࡪ࡭ࡹࠨጴ"),
            **info,
            bstack1ll1ll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦጵ"): bstack11111ll111_opy_
        }
        bstack11111l1l1l_opy_ = bstack1111ll11ll_opy_(bstack11111l1l1l_opy_)
        return bstack11111l1l1l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢጶ").format(err))
        return {}
def bstack1111ll11ll_opy_(bstack11111l1l1l_opy_):
    bstack1llllllllll_opy_ = bstack11111lll1l_opy_(bstack11111l1l1l_opy_)
    if bstack1llllllllll_opy_ and bstack1llllllllll_opy_ > bstack111l11ll1l_opy_:
        bstack1111l1l1l1_opy_ = bstack1llllllllll_opy_ - bstack111l11ll1l_opy_
        bstack1111l1ll1l_opy_ = bstack1111lll111_opy_(bstack11111l1l1l_opy_[bstack1ll1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨጷ")], bstack1111l1l1l1_opy_)
        bstack11111l1l1l_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢጸ")] = bstack1111l1ll1l_opy_
        logger.info(bstack1ll1ll_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤጹ")
                    .format(bstack11111lll1l_opy_(bstack11111l1l1l_opy_) / 1024))
    return bstack11111l1l1l_opy_
def bstack11111lll1l_opy_(bstack1l1ll1lll1_opy_):
    try:
        if bstack1l1ll1lll1_opy_:
            bstack1111lll1ll_opy_ = json.dumps(bstack1l1ll1lll1_opy_)
            bstack1llllll11l1_opy_ = sys.getsizeof(bstack1111lll1ll_opy_)
            return bstack1llllll11l1_opy_
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣጺ").format(e))
    return -1
def bstack1111lll111_opy_(field, bstack1111l111l1_opy_):
    try:
        bstack1111111lll_opy_ = len(bytes(bstack111l111lll_opy_, bstack1ll1ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨጻ")))
        bstack1lllll1lll1_opy_ = bytes(field, bstack1ll1ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩጼ"))
        bstack1111lll11l_opy_ = len(bstack1lllll1lll1_opy_)
        bstack1lllllll11l_opy_ = ceil(bstack1111lll11l_opy_ - bstack1111l111l1_opy_ - bstack1111111lll_opy_)
        if bstack1lllllll11l_opy_ > 0:
            bstack1llllllll1l_opy_ = bstack1lllll1lll1_opy_[:bstack1lllllll11l_opy_].decode(bstack1ll1ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪጽ"), errors=bstack1ll1ll_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬጾ")) + bstack111l111lll_opy_
            return bstack1llllllll1l_opy_
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦጿ").format(e))
    return field
def bstack1l111llll_opy_():
    env = os.environ
    if (bstack1ll1ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧፀ") in env and len(env[bstack1ll1ll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨፁ")]) > 0) or (
            bstack1ll1ll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣፂ") in env and len(env[bstack1ll1ll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤፃ")]) > 0):
        return {
            bstack1ll1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤፄ"): bstack1ll1ll_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨፅ"),
            bstack1ll1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤፆ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥፇ")),
            bstack1ll1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥፈ"): env.get(bstack1ll1ll_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦፉ")),
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤፊ"): env.get(bstack1ll1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥፋ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠧࡉࡉࠣፌ")) == bstack1ll1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦፍ") and bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤፎ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨፏ"): bstack1ll1ll_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦፐ"),
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨፑ"): env.get(bstack1ll1ll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢፒ")),
            bstack1ll1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢፓ"): env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥፔ")),
            bstack1ll1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨፕ"): env.get(bstack1ll1ll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦፖ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠤࡆࡍࠧፗ")) == bstack1ll1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣፘ") and bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦፙ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥፚ"): bstack1ll1ll_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ፛"),
            bstack1ll1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ፜"): env.get(bstack1ll1ll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ፝")),
            bstack1ll1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ፞"): env.get(bstack1ll1ll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ፟")),
            bstack1ll1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፠"): env.get(bstack1ll1ll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ፡"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡊࠤ።")) == bstack1ll1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧ፣") and env.get(bstack1ll1ll_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤ፤")) == bstack1ll1ll_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦ፥"):
        return {
            bstack1ll1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ፦"): bstack1ll1ll_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ፧"),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፨"): None,
            bstack1ll1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ፩"): None,
            bstack1ll1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፪"): None
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ፫")) and env.get(bstack1ll1ll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ፬")):
        return {
            bstack1ll1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ፭"): bstack1ll1ll_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ፮"),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፯"): env.get(bstack1ll1ll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ፰")),
            bstack1ll1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፱"): None,
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ፲"): env.get(bstack1ll1ll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ፳"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠥࡇࡎࠨ፴")) == bstack1ll1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ፵") and bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦ፶"))):
        return {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ፷"): bstack1ll1ll_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ፸"),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ፹"): env.get(bstack1ll1ll_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ፺")),
            bstack1ll1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፻"): None,
            bstack1ll1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፼"): env.get(bstack1ll1ll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ፽"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡊࠤ፾")) == bstack1ll1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧ፿") and bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᎀ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎁ"): bstack1ll1ll_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᎂ"),
            bstack1ll1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᎃ"): env.get(bstack1ll1ll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᎄ")),
            bstack1ll1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎅ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᎆ")),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎇ"): env.get(bstack1ll1ll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᎈ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠥࡇࡎࠨᎉ")) == bstack1ll1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᎊ") and bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᎋ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎌ"): bstack1ll1ll_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᎍ"),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎎ"): env.get(bstack1ll1ll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᎏ")),
            bstack1ll1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᎐"): env.get(bstack1ll1ll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᎑")),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᎒"): env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤ᎓"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠢࡄࡋࠥ᎔")) == bstack1ll1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᎕") and bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧ᎖"))):
        return {
            bstack1ll1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᎗"): bstack1ll1ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢ᎘"),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᎙"): env.get(bstack1ll1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᎚")),
            bstack1ll1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᎛"): env.get(bstack1ll1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥ᎜")) or env.get(bstack1ll1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ᎝")),
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᎞"): env.get(bstack1ll1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᎟"))
        }
    if bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᎠ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎡ"): bstack1ll1ll_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᎢ"),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎣ"): bstack1ll1ll_opy_ (u"ࠤࡾࢁࢀࢃࠢᎤ").format(env.get(bstack1ll1ll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭Ꭵ")), env.get(bstack1ll1ll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᎦ"))),
            bstack1ll1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎧ"): env.get(bstack1ll1ll_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᎨ")),
            bstack1ll1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎩ"): env.get(bstack1ll1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᎪ"))
        }
    if bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᎫ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᎬ"): bstack1ll1ll_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᎭ"),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎮ"): bstack1ll1ll_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᎯ").format(env.get(bstack1ll1ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭Ꮀ")), env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᎱ")), env.get(bstack1ll1ll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᎲ")), env.get(bstack1ll1ll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᎳ"))),
            bstack1ll1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎴ"): env.get(bstack1ll1ll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᎵ")),
            bstack1ll1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎶ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᎷ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᎸ")) and env.get(bstack1ll1ll_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᎹ")):
        return {
            bstack1ll1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᎺ"): bstack1ll1ll_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᎻ"),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎼ"): bstack1ll1ll_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᎽ").format(env.get(bstack1ll1ll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᎾ")), env.get(bstack1ll1ll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭Ꮏ")), env.get(bstack1ll1ll_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᏀ"))),
            bstack1ll1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏁ"): env.get(bstack1ll1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᏂ")),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏃ"): env.get(bstack1ll1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᏄ"))
        }
    if any([env.get(bstack1ll1ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᏅ")), env.get(bstack1ll1ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᏆ")), env.get(bstack1ll1ll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᏇ"))]):
        return {
            bstack1ll1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᏈ"): bstack1ll1ll_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᏉ"),
            bstack1ll1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏊ"): env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᏋ")),
            bstack1ll1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏌ"): env.get(bstack1ll1ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᏍ")),
            bstack1ll1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏎ"): env.get(bstack1ll1ll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᏏ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᏐ")):
        return {
            bstack1ll1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏑ"): bstack1ll1ll_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᏒ"),
            bstack1ll1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏓ"): env.get(bstack1ll1ll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᏔ")),
            bstack1ll1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏕ"): env.get(bstack1ll1ll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᏖ")),
            bstack1ll1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏗ"): env.get(bstack1ll1ll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᏘ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᏙ")) or env.get(bstack1ll1ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏚ")):
        return {
            bstack1ll1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᏛ"): bstack1ll1ll_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᏜ"),
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏝ"): env.get(bstack1ll1ll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᏞ")),
            bstack1ll1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏟ"): bstack1ll1ll_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᏠ") if env.get(bstack1ll1ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏡ")) else None,
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏢ"): env.get(bstack1ll1ll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᏣ"))
        }
    if any([env.get(bstack1ll1ll_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᏤ")), env.get(bstack1ll1ll_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᏥ")), env.get(bstack1ll1ll_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᏦ"))]):
        return {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏧ"): bstack1ll1ll_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᏨ"),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᏩ"): None,
            bstack1ll1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏪ"): env.get(bstack1ll1ll_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᏫ")),
            bstack1ll1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏬ"): env.get(bstack1ll1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᏭ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᏮ")):
        return {
            bstack1ll1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏯ"): bstack1ll1ll_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᏰ"),
            bstack1ll1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᏱ"): env.get(bstack1ll1ll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᏲ")),
            bstack1ll1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏳ"): bstack1ll1ll_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᏴ").format(env.get(bstack1ll1ll_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᏵ"))) if env.get(bstack1ll1ll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᏶")) else None,
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᏷"): env.get(bstack1ll1ll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᏸ"))
        }
    if bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᏹ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏺ"): bstack1ll1ll_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᏻ"),
            bstack1ll1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᏼ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᏽ")),
            bstack1ll1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᏾"): env.get(bstack1ll1ll_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ᏿")),
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᐀"): env.get(bstack1ll1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐁ"))
        }
    if bstack1ll111ll_opy_(env.get(bstack1ll1ll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᐂ"))):
        return {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐃ"): bstack1ll1ll_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᐄ"),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐅ"): bstack1ll1ll_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᐆ").format(env.get(bstack1ll1ll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᐇ")), env.get(bstack1ll1ll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᐈ")), env.get(bstack1ll1ll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᐉ"))),
            bstack1ll1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐊ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᐋ")),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐌ"): env.get(bstack1ll1ll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᐍ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠥࡇࡎࠨᐎ")) == bstack1ll1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᐏ") and env.get(bstack1ll1ll_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᐐ")) == bstack1ll1ll_opy_ (u"ࠨ࠱ࠣᐑ"):
        return {
            bstack1ll1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐒ"): bstack1ll1ll_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᐓ"),
            bstack1ll1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐔ"): bstack1ll1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᐕ").format(env.get(bstack1ll1ll_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᐖ"))),
            bstack1ll1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᐗ"): None,
            bstack1ll1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐘ"): None,
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᐙ")):
        return {
            bstack1ll1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᐚ"): bstack1ll1ll_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᐛ"),
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᐜ"): None,
            bstack1ll1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐝ"): env.get(bstack1ll1ll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᐞ")),
            bstack1ll1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐟ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᐠ"))
        }
    if any([env.get(bstack1ll1ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᐡ")), env.get(bstack1ll1ll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᐢ")), env.get(bstack1ll1ll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᐣ")), env.get(bstack1ll1ll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᐤ"))]):
        return {
            bstack1ll1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᐥ"): bstack1ll1ll_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᐦ"),
            bstack1ll1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᐧ"): None,
            bstack1ll1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐨ"): env.get(bstack1ll1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᐩ")) or None,
            bstack1ll1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐪ"): env.get(bstack1ll1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐫ"), 0)
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᐬ")):
        return {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐭ"): bstack1ll1ll_opy_ (u"ࠢࡈࡱࡆࡈࠧᐮ"),
            bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐯ"): None,
            bstack1ll1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᐰ"): env.get(bstack1ll1ll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᐱ")),
            bstack1ll1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᐲ"): env.get(bstack1ll1ll_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᐳ"))
        }
    if env.get(bstack1ll1ll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᐴ")):
        return {
            bstack1ll1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐵ"): bstack1ll1ll_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᐶ"),
            bstack1ll1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐷ"): env.get(bstack1ll1ll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᐸ")),
            bstack1ll1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐹ"): env.get(bstack1ll1ll_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᐺ")),
            bstack1ll1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐻ"): env.get(bstack1ll1ll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᐼ"))
        }
    return {bstack1ll1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐽ"): None}
def get_host_info():
    return {
        bstack1ll1ll_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᐾ"): platform.node(),
        bstack1ll1ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᐿ"): platform.system(),
        bstack1ll1ll_opy_ (u"ࠦࡹࡿࡰࡦࠤᑀ"): platform.machine(),
        bstack1ll1ll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᑁ"): platform.version(),
        bstack1ll1ll_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᑂ"): platform.architecture()[0]
    }
def bstack1lll11l1ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l1llll_opy_():
    if bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᑃ")):
        return bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᑄ")
    return bstack1ll1ll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᑅ")
def bstack111111l1ll_opy_(driver):
    info = {
        bstack1ll1ll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᑆ"): driver.capabilities,
        bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᑇ"): driver.session_id,
        bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᑈ"): driver.capabilities.get(bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᑉ"), None),
        bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᑊ"): driver.capabilities.get(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᑋ"), None),
        bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᑌ"): driver.capabilities.get(bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᑍ"), None),
    }
    if bstack1111l1llll_opy_() == bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᑎ"):
        if bstack11lll11l1_opy_():
            info[bstack1ll1ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᑏ")] = bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑐ")
        elif driver.capabilities.get(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑑ"), {}).get(bstack1ll1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᑒ"), False):
            info[bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᑓ")] = bstack1ll1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᑔ")
        else:
            info[bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᑕ")] = bstack1ll1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᑖ")
    return info
def bstack11lll11l1_opy_():
    if bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑗ")):
        return True
    if bstack1ll111ll_opy_(os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᑘ"), None)):
        return True
    return False
def bstack1l1l111l1l_opy_(bstack1111l1l1ll_opy_, url, data, config):
    headers = config.get(bstack1ll1ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᑙ"), None)
    proxies = bstack1l11l1l1l_opy_(config, url)
    auth = config.get(bstack1ll1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᑚ"), None)
    response = requests.request(
            bstack1111l1l1ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1llll1l_opy_(bstack1l11111l_opy_, size):
    bstack1l111l1ll1_opy_ = []
    while len(bstack1l11111l_opy_) > size:
        bstack11ll1ll11_opy_ = bstack1l11111l_opy_[:size]
        bstack1l111l1ll1_opy_.append(bstack11ll1ll11_opy_)
        bstack1l11111l_opy_ = bstack1l11111l_opy_[size:]
    bstack1l111l1ll1_opy_.append(bstack1l11111l_opy_)
    return bstack1l111l1ll1_opy_
def bstack1111ll11l1_opy_(message, bstack1111l1111l_opy_=False):
    os.write(1, bytes(message, bstack1ll1ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᑛ")))
    os.write(1, bytes(bstack1ll1ll_opy_ (u"ࠫࡡࡴࠧᑜ"), bstack1ll1ll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᑝ")))
    if bstack1111l1111l_opy_:
        with open(bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᑞ") + os.environ[bstack1ll1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑟ")] + bstack1ll1ll_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ᑠ"), bstack1ll1ll_opy_ (u"ࠩࡤࠫᑡ")) as f:
            f.write(message + bstack1ll1ll_opy_ (u"ࠪࡠࡳ࠭ᑢ"))
def bstack11111l11l1_opy_():
    return os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᑣ")].lower() == bstack1ll1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪᑤ")
def bstack1l1l1lll1l_opy_(bstack11111l1lll_opy_):
    return bstack1ll1ll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᑥ").format(bstack111l1111ll_opy_, bstack11111l1lll_opy_)
def bstack1l1l11l11l_opy_():
    return bstack11l11l11ll_opy_().replace(tzinfo=None).isoformat() + bstack1ll1ll_opy_ (u"࡛ࠧࠩᑦ")
def bstack111111l111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1ll_opy_ (u"ࠨ࡜ࠪᑧ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1ll_opy_ (u"ࠩ࡝ࠫᑨ")))).total_seconds() * 1000
def bstack1111ll1l1l_opy_(timestamp):
    return bstack11111111l1_opy_(timestamp).isoformat() + bstack1ll1ll_opy_ (u"ࠪ࡞ࠬᑩ")
def bstack1111111ll1_opy_(bstack1111ll1ll1_opy_):
    date_format = bstack1ll1ll_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᑪ")
    bstack1lllllll1ll_opy_ = datetime.datetime.strptime(bstack1111ll1ll1_opy_, date_format)
    return bstack1lllllll1ll_opy_.isoformat() + bstack1ll1ll_opy_ (u"ࠬࡠࠧᑫ")
def bstack1111llll11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑬ")
    else:
        return bstack1ll1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑭ")
def bstack1ll111ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᑮ")
def bstack1lllll1llll_opy_(val):
    return val.__str__().lower() == bstack1ll1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᑯ")
def bstack11l1llllll_opy_(bstack1111llll1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111llll1l_opy_ as e:
                print(bstack1ll1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᑰ").format(func.__name__, bstack1111llll1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111111l1l1_opy_(bstack11111l111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111l111l_opy_(cls, *args, **kwargs)
            except bstack1111llll1l_opy_ as e:
                print(bstack1ll1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᑱ").format(bstack11111l111l_opy_.__name__, bstack1111llll1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111111l1l1_opy_
    else:
        return decorator
def bstack11111lll_opy_(bstack11l1111l11_opy_):
    if bstack1ll1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᑲ") in bstack11l1111l11_opy_ and bstack1lllll1llll_opy_(bstack11l1111l11_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᑳ")]):
        return False
    if bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᑴ") in bstack11l1111l11_opy_ and bstack1lllll1llll_opy_(bstack11l1111l11_opy_[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᑵ")]):
        return False
    return True
def bstack1111l1l1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1lll1lll_opy_(hub_url, CONFIG):
    if bstack1l11llllll_opy_() <= version.parse(bstack1ll1ll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᑶ")):
        if hub_url != bstack1ll1ll_opy_ (u"ࠪࠫᑷ"):
            return bstack1ll1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᑸ") + hub_url + bstack1ll1ll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᑹ")
        return bstack1l11ll11l_opy_
    if hub_url != bstack1ll1ll_opy_ (u"࠭ࠧᑺ"):
        return bstack1ll1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᑻ") + hub_url + bstack1ll1ll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᑼ")
    return bstack1ll11l1l1l_opy_
def bstack11111l1ll1_opy_():
    return isinstance(os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᑽ")), str)
def bstack11l1ll11l_opy_(url):
    return urlparse(url).hostname
def bstack1l1l1l1lll_opy_(hostname):
    for bstack1ll1l1l1l_opy_ in bstack1l11l1ll_opy_:
        regex = re.compile(bstack1ll1l1l1l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111l1l11l_opy_(bstack1lllll1ll11_opy_, file_name, logger):
    bstack1l11l1l11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠪࢂࠬᑾ")), bstack1lllll1ll11_opy_)
    try:
        if not os.path.exists(bstack1l11l1l11l_opy_):
            os.makedirs(bstack1l11l1l11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"ࠫࢃ࠭ᑿ")), bstack1lllll1ll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1ll_opy_ (u"ࠬࡽࠧᒀ")):
                pass
            with open(file_path, bstack1ll1ll_opy_ (u"ࠨࡷࠬࠤᒁ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1111l1_opy_.format(str(e)))
def bstack11111lll11_opy_(file_name, key, value, logger):
    file_path = bstack1111l1l11l_opy_(bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᒂ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1l11_opy_ = json.load(open(file_path, bstack1ll1ll_opy_ (u"ࠨࡴࡥࠫᒃ")))
        else:
            bstack1lll1l11_opy_ = {}
        bstack1lll1l11_opy_[key] = value
        with open(file_path, bstack1ll1ll_opy_ (u"ࠤࡺ࠯ࠧᒄ")) as outfile:
            json.dump(bstack1lll1l11_opy_, outfile)
def bstack1l11111ll1_opy_(file_name, logger):
    file_path = bstack1111l1l11l_opy_(bstack1ll1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᒅ"), file_name, logger)
    bstack1lll1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1ll_opy_ (u"ࠫࡷ࠭ᒆ")) as bstack11llll11_opy_:
            bstack1lll1l11_opy_ = json.load(bstack11llll11_opy_)
    return bstack1lll1l11_opy_
def bstack11l111l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᒇ") + file_path + bstack1ll1ll_opy_ (u"࠭ࠠࠨᒈ") + str(e))
def bstack1l11llllll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1ll_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᒉ")
def bstack1l1ll11lll_opy_(config):
    if bstack1ll1ll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᒊ") in config:
        del (config[bstack1ll1ll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᒋ")])
        return False
    if bstack1l11llllll_opy_() < version.parse(bstack1ll1ll_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᒌ")):
        return False
    if bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᒍ")):
        return True
    if bstack1ll1ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᒎ") in config and config[bstack1ll1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᒏ")] is False:
        return False
    else:
        return True
def bstack111l1111_opy_(args_list, bstack1111l1lll1_opy_):
    index = -1
    for value in bstack1111l1lll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11ll1l111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11ll1l111l_opy_ = bstack11ll1l111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒐ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒑ"), exception=exception)
    def bstack111llllll1_opy_(self):
        if self.result != bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒒ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᒓ") in self.exception_type:
            return bstack1ll1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᒔ")
        return bstack1ll1ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᒕ")
    def bstack1111ll1lll_opy_(self):
        if self.result != bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒖ"):
            return None
        if self.bstack11ll1l111l_opy_:
            return self.bstack11ll1l111l_opy_
        return bstack11111ll11l_opy_(self.exception)
def bstack11111ll11l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l11l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1lll11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lllllll1_opy_(config, logger):
    try:
        import playwright
        bstack11111l11ll_opy_ = playwright.__file__
        bstack1lllllllll1_opy_ = os.path.split(bstack11111l11ll_opy_)
        bstack1111ll111l_opy_ = bstack1lllllllll1_opy_[0] + bstack1ll1ll_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᒗ")
        os.environ[bstack1ll1ll_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᒘ")] = bstack1llll111l1_opy_(config)
        with open(bstack1111ll111l_opy_, bstack1ll1ll_opy_ (u"ࠩࡵࠫᒙ")) as f:
            bstack1ll11ll1l_opy_ = f.read()
            bstack1llllllll11_opy_ = bstack1ll1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᒚ")
            bstack1llllll1ll1_opy_ = bstack1ll11ll1l_opy_.find(bstack1llllllll11_opy_)
            if bstack1llllll1ll1_opy_ == -1:
              process = subprocess.Popen(bstack1ll1ll_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᒛ"), shell=True, cwd=bstack1lllllllll1_opy_[0])
              process.wait()
              bstack111111111l_opy_ = bstack1ll1ll_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᒜ")
              bstack1111l11111_opy_ = bstack1ll1ll_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᒝ")
              bstack11111llll1_opy_ = bstack1ll11ll1l_opy_.replace(bstack111111111l_opy_, bstack1111l11111_opy_)
              with open(bstack1111ll111l_opy_, bstack1ll1ll_opy_ (u"ࠧࡸࠩᒞ")) as f:
                f.write(bstack11111llll1_opy_)
    except Exception as e:
        logger.error(bstack1lll11ll_opy_.format(str(e)))
def bstack111lll111_opy_():
  try:
    bstack111111lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᒟ"))
    bstack111111l11l_opy_ = []
    if os.path.exists(bstack111111lll1_opy_):
      with open(bstack111111lll1_opy_) as f:
        bstack111111l11l_opy_ = json.load(f)
      os.remove(bstack111111lll1_opy_)
    return bstack111111l11l_opy_
  except:
    pass
  return []
def bstack11111lll1_opy_(bstack111l1lll1_opy_):
  try:
    bstack111111l11l_opy_ = []
    bstack111111lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᒠ"))
    if os.path.exists(bstack111111lll1_opy_):
      with open(bstack111111lll1_opy_) as f:
        bstack111111l11l_opy_ = json.load(f)
    bstack111111l11l_opy_.append(bstack111l1lll1_opy_)
    with open(bstack111111lll1_opy_, bstack1ll1ll_opy_ (u"ࠪࡻࠬᒡ")) as f:
        json.dump(bstack111111l11l_opy_, f)
  except:
    pass
def bstack1ll11ll11_opy_(logger, bstack111111ll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᒢ"), bstack1ll1ll_opy_ (u"ࠬ࠭ᒣ"))
    if test_name == bstack1ll1ll_opy_ (u"࠭ࠧᒤ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᒥ"), bstack1ll1ll_opy_ (u"ࠨࠩᒦ"))
    bstack11111ll1ll_opy_ = bstack1ll1ll_opy_ (u"ࠩ࠯ࠤࠬᒧ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111111ll1l_opy_:
        bstack1ll111l1_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒨ"), bstack1ll1ll_opy_ (u"ࠫ࠵࠭ᒩ"))
        bstack11lll11lll_opy_ = {bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒪ"): test_name, bstack1ll1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᒫ"): bstack11111ll1ll_opy_, bstack1ll1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᒬ"): bstack1ll111l1_opy_}
        bstack1111l11ll1_opy_ = []
        bstack1111l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᒭ"))
        if os.path.exists(bstack1111l111ll_opy_):
            with open(bstack1111l111ll_opy_) as f:
                bstack1111l11ll1_opy_ = json.load(f)
        bstack1111l11ll1_opy_.append(bstack11lll11lll_opy_)
        with open(bstack1111l111ll_opy_, bstack1ll1ll_opy_ (u"ࠩࡺࠫᒮ")) as f:
            json.dump(bstack1111l11ll1_opy_, f)
    else:
        bstack11lll11lll_opy_ = {bstack1ll1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᒯ"): test_name, bstack1ll1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᒰ"): bstack11111ll1ll_opy_, bstack1ll1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᒱ"): str(multiprocessing.current_process().name)}
        if bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᒲ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11lll11lll_opy_)
  except Exception as e:
      logger.warn(bstack1ll1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᒳ").format(e))
def bstack1ll11l1lll_opy_(error_message, test_name, index, logger):
  try:
    bstack1111111l11_opy_ = []
    bstack11lll11lll_opy_ = {bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᒴ"): test_name, bstack1ll1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᒵ"): error_message, bstack1ll1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᒶ"): index}
    bstack1111111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᒷ"))
    if os.path.exists(bstack1111111l1l_opy_):
        with open(bstack1111111l1l_opy_) as f:
            bstack1111111l11_opy_ = json.load(f)
    bstack1111111l11_opy_.append(bstack11lll11lll_opy_)
    with open(bstack1111111l1l_opy_, bstack1ll1ll_opy_ (u"ࠬࡽࠧᒸ")) as f:
        json.dump(bstack1111111l11_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᒹ").format(e))
def bstack1l1ll111l1_opy_(bstack1l11ll1ll_opy_, name, logger):
  try:
    bstack11lll11lll_opy_ = {bstack1ll1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒺ"): name, bstack1ll1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᒻ"): bstack1l11ll1ll_opy_, bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᒼ"): str(threading.current_thread()._name)}
    return bstack11lll11lll_opy_
  except Exception as e:
    logger.warn(bstack1ll1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᒽ").format(e))
  return
def bstack11111ll1l1_opy_():
    return platform.system() == bstack1ll1ll_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᒾ")
def bstack1ll1111ll1_opy_(bstack11111l1111_opy_, config, logger):
    bstack111111ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11111l1111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᒿ").format(e))
    return bstack111111ll11_opy_
def bstack11111111ll_opy_(bstack111111llll_opy_, bstack1llllll111l_opy_):
    bstack1111111111_opy_ = version.parse(bstack111111llll_opy_)
    bstack1llllll1111_opy_ = version.parse(bstack1llllll111l_opy_)
    if bstack1111111111_opy_ > bstack1llllll1111_opy_:
        return 1
    elif bstack1111111111_opy_ < bstack1llllll1111_opy_:
        return -1
    else:
        return 0
def bstack11l11l11ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11111111l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1ll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11llll1111_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1ll1ll_opy_ (u"࠭ࡧࡦࡶࠪᓀ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1llll1_opy_ = caps.get(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓁ"))
    bstack1lllll1ll1l_opy_ = True
    if bstack1lllll1llll_opy_(caps.get(bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᓂ"))) or bstack1lllll1llll_opy_(caps.get(bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᓃ"))):
        bstack1lllll1ll1l_opy_ = False
    if bstack1l1ll11lll_opy_({bstack1ll1ll_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᓄ"): bstack1lllll1ll1l_opy_}):
        bstack11l1llll1_opy_ = bstack11l1llll1_opy_ or {}
        bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᓅ")] = bstack1111l1ll11_opy_(framework)
        bstack11l1llll1_opy_[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓆ")] = bstack11111l11l1_opy_()
        if getattr(options, bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᓇ"), None):
            options.set_capability(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓈ"), bstack11l1llll1_opy_)
        else:
            options[bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᓉ")] = bstack11l1llll1_opy_
    else:
        if getattr(options, bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᓊ"), None):
            options.set_capability(bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᓋ"), bstack1111l1ll11_opy_(framework))
            options.set_capability(bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᓌ"), bstack11111l11l1_opy_())
        else:
            options[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᓍ")] = bstack1111l1ll11_opy_(framework)
            options[bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᓎ")] = bstack11111l11l1_opy_()
    return options
def bstack1llllll1l1l_opy_(bstack11111lllll_opy_, framework):
    if bstack11111lllll_opy_ and len(bstack11111lllll_opy_.split(bstack1ll1ll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᓏ"))) > 1:
        ws_url = bstack11111lllll_opy_.split(bstack1ll1ll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᓐ"))[0]
        if bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᓑ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111l1l111_opy_ = json.loads(urllib.parse.unquote(bstack11111lllll_opy_.split(bstack1ll1ll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᓒ"))[1]))
            bstack1111l1l111_opy_ = bstack1111l1l111_opy_ or {}
            bstack1111l1l111_opy_[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᓓ")] = str(framework) + str(__version__)
            bstack1111l1l111_opy_[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓔ")] = bstack11111l11l1_opy_()
            bstack11111lllll_opy_ = bstack11111lllll_opy_.split(bstack1ll1ll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᓕ"))[0] + bstack1ll1ll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᓖ") + urllib.parse.quote(json.dumps(bstack1111l1l111_opy_))
    return bstack11111lllll_opy_
def bstack1ll1lll11_opy_():
    global bstack1l1l1lllll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1lllll_opy_ = BrowserType.connect
    return bstack1l1l1lllll_opy_
def bstack1ll1l1111_opy_(framework_name):
    global bstack11lllllll_opy_
    bstack11lllllll_opy_ = framework_name
    return framework_name
def bstack1l111111ll_opy_(self, *args, **kwargs):
    global bstack1l1l1lllll_opy_
    try:
        global bstack11lllllll_opy_
        if bstack1ll1ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᓗ") in kwargs:
            kwargs[bstack1ll1ll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᓘ")] = bstack1llllll1l1l_opy_(
                kwargs.get(bstack1ll1ll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᓙ"), None),
                bstack11lllllll_opy_
            )
    except Exception as e:
        logger.error(bstack1ll1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᓚ").format(str(e)))
    return bstack1l1l1lllll_opy_(self, *args, **kwargs)
def bstack1llllll1lll_opy_(bstack1lllll1l1l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l11l1l1l_opy_(bstack1lllll1l1l1_opy_, bstack1ll1ll_opy_ (u"ࠧࠨᓛ"))
        if proxies and proxies.get(bstack1ll1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᓜ")):
            parsed_url = urlparse(proxies.get(bstack1ll1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᓝ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᓞ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᓟ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᓠ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᓡ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111ll11l_opy_(bstack1lllll1l1l1_opy_):
    bstack11111l1l11_opy_ = {
        bstack111l11111l_opy_[bstack1111ll1111_opy_]: bstack1lllll1l1l1_opy_[bstack1111ll1111_opy_]
        for bstack1111ll1111_opy_ in bstack1lllll1l1l1_opy_
        if bstack1111ll1111_opy_ in bstack111l11111l_opy_
    }
    bstack11111l1l11_opy_[bstack1ll1ll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᓢ")] = bstack1llllll1lll_opy_(bstack1lllll1l1l1_opy_, bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᓣ")))
    bstack1llllll11ll_opy_ = [element.lower() for element in bstack111l11l111_opy_]
    bstack1111ll1l11_opy_(bstack11111l1l11_opy_, bstack1llllll11ll_opy_)
    return bstack11111l1l11_opy_
def bstack1111ll1l11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1ll_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᓤ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111ll1l11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111ll1l11_opy_(item, keys)