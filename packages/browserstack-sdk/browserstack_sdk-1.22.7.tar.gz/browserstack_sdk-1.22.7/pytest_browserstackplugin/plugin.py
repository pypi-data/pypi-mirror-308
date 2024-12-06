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
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llll1111_opy_, bstack1l111l1ll_opy_, update, bstack11ll11ll_opy_,
                                       bstack1ll11lll1_opy_, bstack111l11ll_opy_, bstack1l11ll11_opy_, bstack1l1lll1l_opy_,
                                       bstack1lll1llll1_opy_, bstack111ll1l1_opy_, bstack1l1l1ll1l_opy_, bstack1l1l1lll1_opy_,
                                       bstack1lll1ll11l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1l1l1l11_opy_)
from browserstack_sdk.bstack111l11l11_opy_ import bstack11lllll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11ll1ll1_opy_
from bstack_utils.capture import bstack11ll11l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1l11l1_opy_, bstack11ll11111_opy_, bstack1l1lll111_opy_, \
    bstack1ll111111l_opy_
from bstack_utils.helper import bstack1l1lll11_opy_, bstack11111111l1_opy_, bstack11l11l11ll_opy_, bstack1lll11l1ll_opy_, bstack11111l11l1_opy_, bstack1l1l11l11l_opy_, \
    bstack1111llll11_opy_, \
    bstack1llllll1l11_opy_, bstack1l11llllll_opy_, bstack1l1lll1lll_opy_, bstack11111l1ll1_opy_, bstack1111l1l1l_opy_, Notset, \
    bstack1l1ll11lll_opy_, bstack111111l111_opy_, bstack11111ll11l_opy_, Result, bstack1111ll1l1l_opy_, bstack1111l11l11_opy_, bstack11l1llllll_opy_, \
    bstack11111lll1_opy_, bstack1ll11ll11_opy_, bstack1ll111ll_opy_, bstack11111ll1l1_opy_
from bstack_utils.bstack1llll1llll1_opy_ import bstack1llll1ll1l1_opy_
from bstack_utils.messages import bstack1l1111ll1_opy_, bstack1l1l1l11l_opy_, bstack1lll1l1l1_opy_, bstack1l1111l11_opy_, bstack1l111l1l_opy_, \
    bstack1lll11ll_opy_, bstack1ll1l1111l_opy_, bstack1lll1ll111_opy_, bstack111lll11l_opy_, bstack1l1l111ll_opy_, \
    bstack1l1llllll_opy_, bstack1l11l111l1_opy_
from bstack_utils.proxy import bstack1llll111l1_opy_, bstack11llllll_opy_
from bstack_utils.bstack11lll1l1l1_opy_ import bstack1ll1lll11l1_opy_, bstack1ll1lll11ll_opy_, bstack1ll1lll1l1l_opy_, bstack1ll1llll111_opy_, \
    bstack1ll1lll111l_opy_, bstack1ll1ll1llll_opy_, bstack1ll1lll1lll_opy_, bstack1ll1l1ll_opy_, bstack1ll1lll1ll1_opy_
from bstack_utils.bstack1l11l1ll1l_opy_ import bstack11llll11l1_opy_
from bstack_utils.bstack1l11l11l_opy_ import bstack1ll1l111l_opy_, bstack1ll111lll_opy_, bstack1l1l1l1l1l_opy_, \
    bstack11l1llll_opy_, bstack11l1111l_opy_
from bstack_utils.bstack11ll1ll11l_opy_ import bstack11ll1ll1ll_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack1111llll_opy_
import bstack_utils.bstack1l1l1l111_opy_ as bstack1l11l11l1_opy_
from bstack_utils.bstack1l111lll11_opy_ import bstack1llll1ll_opy_
from bstack_utils.bstack1lll1l11l_opy_ import bstack1lll1l11l_opy_
from browserstack_sdk.__init__ import bstack1lllll111_opy_
bstack11111111l_opy_ = None
bstack1l11111l1_opy_ = None
bstack11ll1l11_opy_ = None
bstack11111l1l1_opy_ = None
bstack11ll111ll_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack1l11lll111_opy_ = None
bstack1l11llll1l_opy_ = None
bstack11lll11l11_opy_ = None
bstack11ll11l1l_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1llll11l1_opy_ = None
bstack1l1111111_opy_ = None
bstack11lllllll_opy_ = bstack1ll1ll_opy_ (u"ࠨࠩ᠊")
CONFIG = {}
bstack1l1111l11l_opy_ = False
bstack1llll11111_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪ᠋")
bstack11l1lll1l_opy_ = bstack1ll1ll_opy_ (u"ࠪࠫ᠌")
bstack1l1111l1_opy_ = False
bstack11llllll1_opy_ = []
bstack1l1llll11l_opy_ = bstack1l1l11l1_opy_
bstack1ll111l11ll_opy_ = bstack1ll1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᠍")
bstack1ll11llll1_opy_ = {}
bstack1111111l1_opy_ = False
logger = bstack11ll1ll1_opy_.get_logger(__name__, bstack1l1llll11l_opy_)
store = {
    bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ᠎"): []
}
bstack1ll1111l1l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l11ll111_opy_ = {}
current_test_uuid = None
def bstack11ll1l111_opy_(page, bstack1ll1l1lll1_opy_):
    try:
        page.evaluate(bstack1ll1ll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ᠏"),
                      bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ᠐") + json.dumps(
                          bstack1ll1l1lll1_opy_) + bstack1ll1ll_opy_ (u"ࠣࡿࢀࠦ᠑"))
    except Exception as e:
        print(bstack1ll1ll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ᠒"), e)
def bstack1l11l1l1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll1ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ᠓"), bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ᠔") + json.dumps(
            message) + bstack1ll1ll_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ᠕") + json.dumps(level) + bstack1ll1ll_opy_ (u"࠭ࡽࡾࠩ᠖"))
    except Exception as e:
        print(bstack1ll1ll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ᠗"), e)
def pytest_configure(config):
    bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
    config.args = bstack1111llll_opy_.bstack1ll111ll1l1_opy_(config.args)
    bstack1l1l1l1ll_opy_.bstack1llll1l11l_opy_(bstack1ll111ll_opy_(config.getoption(bstack1ll1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ᠘"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll111l111l_opy_ = item.config.getoption(bstack1ll1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᠙"))
    plugins = item.config.getoption(bstack1ll1ll_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦ᠚"))
    report = outcome.get_result()
    bstack1ll1111l11l_opy_(item, call, report)
    if bstack1ll1ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤ᠛") not in plugins or bstack1111l1l1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1ll_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨ᠜"), None)
    page = getattr(item, bstack1ll1ll_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧ᠝"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11111ll1_opy_(item, report, summary, bstack1ll111l111l_opy_)
    if (page is not None):
        bstack1l1llllllll_opy_(item, report, summary, bstack1ll111l111l_opy_)
def bstack1ll11111ll1_opy_(item, report, summary, bstack1ll111l111l_opy_):
    if report.when == bstack1ll1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᠞") and report.skipped:
        bstack1ll1lll1ll1_opy_(report)
    if report.when in [bstack1ll1ll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ᠟"), bstack1ll1ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᠠ")]:
        return
    if not bstack11111l11l1_opy_():
        return
    try:
        if (str(bstack1ll111l111l_opy_).lower() != bstack1ll1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨᠡ")):
            item._driver.execute_script(
                bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩᠢ") + json.dumps(
                    report.nodeid) + bstack1ll1ll_opy_ (u"ࠬࢃࡽࠨᠣ"))
        os.environ[bstack1ll1ll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᠤ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢᠥ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1ll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᠦ")))
    bstack11llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠤࠥᠧ")
    bstack1ll1lll1ll1_opy_(report)
    if not passed:
        try:
            bstack11llllll11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1ll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᠨ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11llllll11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1ll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᠩ")))
        bstack11llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠧࠨᠪ")
        if not passed:
            try:
                bstack11llllll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1ll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᠫ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11llllll11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᠬ")
                    + json.dumps(bstack1ll1ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤᠭ"))
                    + bstack1ll1ll_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᠮ")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᠯ")
                    + json.dumps(str(bstack11llllll11_opy_))
                    + bstack1ll1ll_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᠰ")
                )
        except Exception as e:
            summary.append(bstack1ll1ll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥᠱ").format(e))
def bstack1ll11111111_opy_(test_name, error_message):
    try:
        bstack1l1llllll1l_opy_ = []
        bstack1ll111l1_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᠲ"), bstack1ll1ll_opy_ (u"ࠧ࠱ࠩᠳ"))
        bstack11lll11lll_opy_ = {bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᠴ"): test_name, bstack1ll1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᠵ"): error_message, bstack1ll1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᠶ"): bstack1ll111l1_opy_}
        bstack1ll111111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1ll_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᠷ"))
        if os.path.exists(bstack1ll111111l1_opy_):
            with open(bstack1ll111111l1_opy_) as f:
                bstack1l1llllll1l_opy_ = json.load(f)
        bstack1l1llllll1l_opy_.append(bstack11lll11lll_opy_)
        with open(bstack1ll111111l1_opy_, bstack1ll1ll_opy_ (u"ࠬࡽࠧᠸ")) as f:
            json.dump(bstack1l1llllll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫᠹ") + str(e))
def bstack1l1llllllll_opy_(item, report, summary, bstack1ll111l111l_opy_):
    if report.when in [bstack1ll1ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᠺ"), bstack1ll1ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᠻ")]:
        return
    if (str(bstack1ll111l111l_opy_).lower() != bstack1ll1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᠼ")):
        bstack11ll1l111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1ll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᠽ")))
    bstack11llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠦࠧᠾ")
    bstack1ll1lll1ll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11llllll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1ll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᠿ").format(e)
                )
        try:
            if passed:
                bstack11l1111l_opy_(getattr(item, bstack1ll1ll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᡀ"), None), bstack1ll1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᡁ"))
            else:
                error_message = bstack1ll1ll_opy_ (u"ࠨࠩᡂ")
                if bstack11llllll11_opy_:
                    bstack1l11l1l1l1_opy_(item._page, str(bstack11llllll11_opy_), bstack1ll1ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᡃ"))
                    bstack11l1111l_opy_(getattr(item, bstack1ll1ll_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᡄ"), None), bstack1ll1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᡅ"), str(bstack11llllll11_opy_))
                    error_message = str(bstack11llllll11_opy_)
                else:
                    bstack11l1111l_opy_(getattr(item, bstack1ll1ll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᡆ"), None), bstack1ll1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᡇ"))
                bstack1ll11111111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᡈ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1ll1ll_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᡉ"), default=bstack1ll1ll_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᡊ"), help=bstack1ll1ll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᡋ"))
    parser.addoption(bstack1ll1ll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᡌ"), default=bstack1ll1ll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᡍ"), help=bstack1ll1ll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᡎ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1ll_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᡏ"), action=bstack1ll1ll_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢᡐ"), default=bstack1ll1ll_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤᡑ"),
                         help=bstack1ll1ll_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤᡒ"))
def bstack11ll1l1l11_opy_(log):
    if not (log[bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡓ")] and log[bstack1ll1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᡔ")].strip()):
        return
    active = bstack11ll111l11_opy_()
    log = {
        bstack1ll1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᡕ"): log[bstack1ll1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᡖ")],
        bstack1ll1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᡗ"): bstack11l11l11ll_opy_().isoformat() + bstack1ll1ll_opy_ (u"ࠩ࡝ࠫᡘ"),
        bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᡙ"): log[bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡚ")],
    }
    if active:
        if active[bstack1ll1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᡛ")] == bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᡜ"):
            log[bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᡝ")] = active[bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᡞ")]
        elif active[bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᡟ")] == bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࠨᡠ"):
            log[bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᡡ")] = active[bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᡢ")]
    bstack1llll1ll_opy_.bstack1lll11l1l1_opy_([log])
def bstack11ll111l11_opy_():
    if len(store[bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᡣ")]) > 0 and store[bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᡤ")][-1]:
        return {
            bstack1ll1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᡥ"): bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᡦ"),
            bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᡧ"): store[bstack1ll1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᡨ")][-1]
        }
    if store.get(bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᡩ"), None):
        return {
            bstack1ll1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫᡪ"): bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࠬᡫ"),
            bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᡬ"): store[bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᡭ")]
        }
    return None
bstack11ll1l1l1l_opy_ = bstack11ll11l1l1_opy_(bstack11ll1l1l11_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1l1lllll11l_opy_ = True
        bstack111l1ll1_opy_ = bstack1l11l11l1_opy_.bstack1111l1l1_opy_(bstack1llllll1l11_opy_(item.own_markers))
        item._a11y_test_case = bstack111l1ll1_opy_
        if bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᡮ"), None):
            driver = getattr(item, bstack1ll1ll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᡯ"), None)
            item._a11y_started = bstack1l11l11l1_opy_.bstack1l1l11111l_opy_(driver, bstack111l1ll1_opy_)
        if not bstack1llll1ll_opy_.on() or bstack1ll111l11ll_opy_ != bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᡰ"):
            return
        global current_test_uuid, bstack11ll1l1l1l_opy_
        bstack11ll1l1l1l_opy_.start()
        bstack11l1ll1ll1_opy_ = {
            bstack1ll1ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᡱ"): uuid4().__str__(),
            bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᡲ"): bstack11l11l11ll_opy_().isoformat() + bstack1ll1ll_opy_ (u"ࠨ࡜ࠪᡳ")
        }
        current_test_uuid = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᡴ")]
        store[bstack1ll1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᡵ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᡶ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l11ll111_opy_[item.nodeid] = {**_11l11ll111_opy_[item.nodeid], **bstack11l1ll1ll1_opy_}
        bstack1ll1111ll11_opy_(item, _11l11ll111_opy_[item.nodeid], bstack1ll1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᡷ"))
    except Exception as err:
        print(bstack1ll1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨᡸ"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll1111l1l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11111l1ll1_opy_():
        atexit.register(bstack11lll111_opy_)
        if not bstack1ll1111l1l1_opy_:
            try:
                bstack1ll11111l11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11111ll1l1_opy_():
                    bstack1ll11111l11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11111l11_opy_:
                    signal.signal(s, bstack1ll11111lll_opy_)
                bstack1ll1111l1l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣ᡹") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1lll11l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᡺")
    try:
        if not bstack1llll1ll_opy_.on():
            return
        bstack11ll1l1l1l_opy_.start()
        uuid = uuid4().__str__()
        bstack11l1ll1ll1_opy_ = {
            bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᡻"): uuid,
            bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᡼"): bstack11l11l11ll_opy_().isoformat() + bstack1ll1ll_opy_ (u"ࠫ࡟࠭᡽"),
            bstack1ll1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ᡾"): bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᡿"),
            bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᢀ"): bstack1ll1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᢁ"),
            bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᢂ"): bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᢃ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᢄ")] = item
        store[bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᢅ")] = [uuid]
        if not _11l11ll111_opy_.get(item.nodeid, None):
            _11l11ll111_opy_[item.nodeid] = {bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢆ"): [], bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢇ"): []}
        _11l11ll111_opy_[item.nodeid][bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢈ")].append(bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢉ")])
        _11l11ll111_opy_[item.nodeid + bstack1ll1ll_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪᢊ")] = bstack11l1ll1ll1_opy_
        bstack1ll1111111l_opy_(item, bstack11l1ll1ll1_opy_, bstack1ll1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᢋ"))
    except Exception as err:
        print(bstack1ll1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᢌ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll11llll1_opy_
        bstack1ll111l1_opy_ = 0
        if bstack1l1111l1_opy_ is True:
            bstack1ll111l1_opy_ = int(os.environ.get(bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᢍ")))
        if bstack1ll1ll11l_opy_.bstack1l1l11ll11_opy_() == bstack1ll1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᢎ"):
            if bstack1ll1ll11l_opy_.bstack1l1ll1llll_opy_() == bstack1ll1ll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᢏ"):
                bstack1ll111l11l1_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᢐ"), None)
                bstack1l11l11111_opy_ = bstack1ll111l11l1_opy_ + bstack1ll1ll_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᢑ")
                driver = getattr(item, bstack1ll1ll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᢒ"), None)
                bstack11111llll_opy_ = getattr(item, bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢓ"), None)
                bstack11l1l11l1_opy_ = getattr(item, bstack1ll1ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᢔ"), None)
                PercySDK.screenshot(driver, bstack1l11l11111_opy_, bstack11111llll_opy_=bstack11111llll_opy_, bstack11l1l11l1_opy_=bstack11l1l11l1_opy_, bstack11lll11l1l_opy_=bstack1ll111l1_opy_)
        if getattr(item, bstack1ll1ll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧᢕ"), False):
            bstack11lllll1_opy_.bstack1l1l1111l_opy_(getattr(item, bstack1ll1ll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᢖ"), None), bstack1ll11llll1_opy_, logger, item)
        if not bstack1llll1ll_opy_.on():
            return
        bstack11l1ll1ll1_opy_ = {
            bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢗ"): uuid4().__str__(),
            bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᢘ"): bstack11l11l11ll_opy_().isoformat() + bstack1ll1ll_opy_ (u"ࠫ࡟࠭ᢙ"),
            bstack1ll1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᢚ"): bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᢛ"),
            bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᢜ"): bstack1ll1ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᢝ"),
            bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᢞ"): bstack1ll1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᢟ")
        }
        _11l11ll111_opy_[item.nodeid + bstack1ll1ll_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧᢠ")] = bstack11l1ll1ll1_opy_
        bstack1ll1111111l_opy_(item, bstack11l1ll1ll1_opy_, bstack1ll1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᢡ"))
    except Exception as err:
        print(bstack1ll1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬᢢ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1llll1ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1ll1llll111_opy_(fixturedef.argname):
        store[bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᢣ")] = request.node
    elif bstack1ll1lll111l_opy_(fixturedef.argname):
        store[bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ᢤ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1ll1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᢥ"): fixturedef.argname,
            bstack1ll1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢦ"): bstack1111llll11_opy_(outcome),
            bstack1ll1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᢧ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᢨ")]
        if not _11l11ll111_opy_.get(current_test_item.nodeid, None):
            _11l11ll111_opy_[current_test_item.nodeid] = {bstack1ll1ll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᢩ"): []}
        _11l11ll111_opy_[current_test_item.nodeid][bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢪ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ᢫"), str(err))
if bstack1111l1l1l_opy_() and bstack1llll1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l11ll111_opy_[request.node.nodeid][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ᢬")].bstack111ll11l1_opy_(id(step))
        except Exception as err:
            print(bstack1ll1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ᢭"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l11ll111_opy_[request.node.nodeid][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ᢮")].bstack11ll1lll11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ᢯"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11ll1ll11l_opy_: bstack11ll1ll1ll_opy_ = _11l11ll111_opy_[request.node.nodeid][bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᢰ")]
            bstack11ll1ll11l_opy_.bstack11ll1lll11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᢱ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111l11ll_opy_
        try:
            if not bstack1llll1ll_opy_.on() or bstack1ll111l11ll_opy_ != bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᢲ"):
                return
            global bstack11ll1l1l1l_opy_
            bstack11ll1l1l1l_opy_.start()
            driver = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᢳ"), None)
            if not _11l11ll111_opy_.get(request.node.nodeid, None):
                _11l11ll111_opy_[request.node.nodeid] = {}
            bstack11ll1ll11l_opy_ = bstack11ll1ll1ll_opy_.bstack1ll1l11l111_opy_(
                scenario, feature, request.node,
                name=bstack1ll1ll1llll_opy_(request.node, scenario),
                bstack11ll11lll1_opy_=bstack1l1l11l11l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1ll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᢴ"),
                tags=bstack1ll1lll1lll_opy_(feature, scenario),
                bstack11ll1111ll_opy_=bstack1llll1ll_opy_.bstack11ll11l1ll_opy_(driver) if driver and driver.session_id else {}
            )
            _11l11ll111_opy_[request.node.nodeid][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᢵ")] = bstack11ll1ll11l_opy_
            bstack1ll1111l111_opy_(bstack11ll1ll11l_opy_.uuid)
            bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᢶ"), bstack11ll1ll11l_opy_)
        except Exception as err:
            print(bstack1ll1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨᢷ"), str(err))
def bstack1ll1111lll1_opy_(bstack11ll1l11ll_opy_):
    if bstack11ll1l11ll_opy_ in store[bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᢸ")]:
        store[bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᢹ")].remove(bstack11ll1l11ll_opy_)
def bstack1ll1111l111_opy_(bstack11ll1ll111_opy_):
    store[bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᢺ")] = bstack11ll1ll111_opy_
    threading.current_thread().current_test_uuid = bstack11ll1ll111_opy_
@bstack1llll1ll_opy_.bstack1ll11l1l1ll_opy_
def bstack1ll1111l11l_opy_(item, call, report):
    global bstack1ll111l11ll_opy_
    bstack1lll1lll_opy_ = bstack1l1l11l11l_opy_()
    if hasattr(report, bstack1ll1ll_opy_ (u"ࠪࡷࡹࡵࡰࠨᢻ")):
        bstack1lll1lll_opy_ = bstack1111ll1l1l_opy_(report.stop)
    elif hasattr(report, bstack1ll1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᢼ")):
        bstack1lll1lll_opy_ = bstack1111ll1l1l_opy_(report.start)
    try:
        if getattr(report, bstack1ll1ll_opy_ (u"ࠬࡽࡨࡦࡰࠪᢽ"), bstack1ll1ll_opy_ (u"࠭ࠧᢾ")) == bstack1ll1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᢿ"):
            bstack11ll1l1l1l_opy_.reset()
        if getattr(report, bstack1ll1ll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᣀ"), bstack1ll1ll_opy_ (u"ࠩࠪᣁ")) == bstack1ll1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᣂ"):
            if bstack1ll111l11ll_opy_ == bstack1ll1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᣃ"):
                _11l11ll111_opy_[item.nodeid][bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᣄ")] = bstack1lll1lll_opy_
                bstack1ll1111ll11_opy_(item, _11l11ll111_opy_[item.nodeid], bstack1ll1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᣅ"), report, call)
                store[bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᣆ")] = None
            elif bstack1ll111l11ll_opy_ == bstack1ll1ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᣇ"):
                bstack11ll1ll11l_opy_ = _11l11ll111_opy_[item.nodeid][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᣈ")]
                bstack11ll1ll11l_opy_.set(hooks=_11l11ll111_opy_[item.nodeid].get(bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᣉ"), []))
                exception, bstack11ll1l111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11ll1l111l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1ll_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪᣊ"), bstack1ll1ll_opy_ (u"ࠬ࠭ᣋ"))]
                bstack11ll1ll11l_opy_.stop(time=bstack1lll1lll_opy_, result=Result(result=getattr(report, bstack1ll1ll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᣌ"), bstack1ll1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᣍ")), exception=exception, bstack11ll1l111l_opy_=bstack11ll1l111l_opy_))
                bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᣎ"), _11l11ll111_opy_[item.nodeid][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᣏ")])
        elif getattr(report, bstack1ll1ll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᣐ"), bstack1ll1ll_opy_ (u"ࠫࠬᣑ")) in [bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᣒ"), bstack1ll1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᣓ")]:
            bstack11ll111l1l_opy_ = item.nodeid + bstack1ll1ll_opy_ (u"ࠧ࠮ࠩᣔ") + getattr(report, bstack1ll1ll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᣕ"), bstack1ll1ll_opy_ (u"ࠩࠪᣖ"))
            if getattr(report, bstack1ll1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᣗ"), False):
                hook_type = bstack1ll1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᣘ") if getattr(report, bstack1ll1ll_opy_ (u"ࠬࡽࡨࡦࡰࠪᣙ"), bstack1ll1ll_opy_ (u"࠭ࠧᣚ")) == bstack1ll1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᣛ") else bstack1ll1ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᣜ")
                _11l11ll111_opy_[bstack11ll111l1l_opy_] = {
                    bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᣝ"): uuid4().__str__(),
                    bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᣞ"): bstack1lll1lll_opy_,
                    bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᣟ"): hook_type
                }
            _11l11ll111_opy_[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᣠ")] = bstack1lll1lll_opy_
            bstack1ll1111lll1_opy_(_11l11ll111_opy_[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᣡ")])
            bstack1ll1111111l_opy_(item, _11l11ll111_opy_[bstack11ll111l1l_opy_], bstack1ll1ll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᣢ"), report, call)
            if getattr(report, bstack1ll1ll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᣣ"), bstack1ll1ll_opy_ (u"ࠩࠪᣤ")) == bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᣥ"):
                if getattr(report, bstack1ll1ll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᣦ"), bstack1ll1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᣧ")) == bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᣨ"):
                    bstack11l1ll1ll1_opy_ = {
                        bstack1ll1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᣩ"): uuid4().__str__(),
                        bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᣪ"): bstack1l1l11l11l_opy_(),
                        bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣫ"): bstack1l1l11l11l_opy_()
                    }
                    _11l11ll111_opy_[item.nodeid] = {**_11l11ll111_opy_[item.nodeid], **bstack11l1ll1ll1_opy_}
                    bstack1ll1111ll11_opy_(item, _11l11ll111_opy_[item.nodeid], bstack1ll1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᣬ"))
                    bstack1ll1111ll11_opy_(item, _11l11ll111_opy_[item.nodeid], bstack1ll1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᣭ"), report, call)
    except Exception as err:
        print(bstack1ll1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᣮ"), str(err))
def bstack1ll111111ll_opy_(test, bstack11l1ll1ll1_opy_, result=None, call=None, bstack1111l11l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11ll1ll11l_opy_ = {
        bstack1ll1ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᣯ"): bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᣰ")],
        bstack1ll1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᣱ"): bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺࠧᣲ"),
        bstack1ll1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᣳ"): test.name,
        bstack1ll1ll_opy_ (u"ࠫࡧࡵࡤࡺࠩᣴ"): {
            bstack1ll1ll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᣵ"): bstack1ll1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭᣶"),
            bstack1ll1ll_opy_ (u"ࠧࡤࡱࡧࡩࠬ᣷"): inspect.getsource(test.obj)
        },
        bstack1ll1ll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᣸"): test.name,
        bstack1ll1ll_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ᣹"): test.name,
        bstack1ll1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ᣺"): bstack1111llll_opy_.bstack11l1llll1l_opy_(test),
        bstack1ll1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ᣻"): file_path,
        bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ᣼"): file_path,
        bstack1ll1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᣽"): bstack1ll1ll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ᣾"),
        bstack1ll1ll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭᣿"): file_path,
        bstack1ll1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᤀ"): bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᤁ")],
        bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᤂ"): bstack1ll1ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᤃ"),
        bstack1ll1ll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᤄ"): {
            bstack1ll1ll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᤅ"): test.nodeid
        },
        bstack1ll1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᤆ"): bstack1llllll1l11_opy_(test.own_markers)
    }
    if bstack1111l11l1_opy_ in [bstack1ll1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᤇ"), bstack1ll1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᤈ")]:
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᤉ")] = {
            bstack1ll1ll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᤊ"): bstack11l1ll1ll1_opy_.get(bstack1ll1ll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᤋ"), [])
        }
    if bstack1111l11l1_opy_ == bstack1ll1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᤌ"):
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᤍ")] = bstack1ll1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᤎ")
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᤏ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᤐ")]
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᤑ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᤒ")]
    if result:
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᤓ")] = result.outcome
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᤔ")] = result.duration * 1000
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᤕ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᤖ")]
        if result.failed:
            bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᤗ")] = bstack1llll1ll_opy_.bstack111llllll1_opy_(call.excinfo.typename)
            bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᤘ")] = bstack1llll1ll_opy_.bstack1ll11ll1111_opy_(call.excinfo, result)
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᤙ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᤚ")]
    if outcome:
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᤛ")] = bstack1111llll11_opy_(outcome)
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᤜ")] = 0
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᤝ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᤞ")]
        if bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᤟")] == bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᤠ"):
            bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᤡ")] = bstack1ll1ll_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩᤢ")  # bstack1l1lllll1l1_opy_
            bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᤣ")] = [{bstack1ll1ll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᤤ"): [bstack1ll1ll_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᤥ")]}]
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᤦ")] = bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᤧ")]
    return bstack11ll1ll11l_opy_
def bstack1ll1111llll_opy_(test, bstack11l1ll1111_opy_, bstack1111l11l1_opy_, result, call, outcome, bstack1ll111l1l11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᤨ")]
    hook_name = bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᤩ")]
    hook_data = {
        bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᤪ"): bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᤫ")],
        bstack1ll1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ᤬"): bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ᤭"),
        bstack1ll1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᤮"): bstack1ll1ll_opy_ (u"ࠧࡼࡿࠪ᤯").format(bstack1ll1lll11ll_opy_(hook_name)),
        bstack1ll1ll_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᤰ"): {
            bstack1ll1ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᤱ"): bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᤲ"),
            bstack1ll1ll_opy_ (u"ࠫࡨࡵࡤࡦࠩᤳ"): None
        },
        bstack1ll1ll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᤴ"): test.name,
        bstack1ll1ll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᤵ"): bstack1111llll_opy_.bstack11l1llll1l_opy_(test, hook_name),
        bstack1ll1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᤶ"): file_path,
        bstack1ll1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᤷ"): file_path,
        bstack1ll1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᤸ"): bstack1ll1ll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪ᤹ࠫ"),
        bstack1ll1ll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ᤺"): file_path,
        bstack1ll1ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵ᤻ࠩ"): bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᤼")],
        bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ᤽"): bstack1ll1ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ᤾") if bstack1ll111l11ll_opy_ == bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭᤿") else bstack1ll1ll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ᥀"),
        bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ᥁"): hook_type
    }
    bstack1ll1l1ll11l_opy_ = bstack11l1l11lll_opy_(_11l11ll111_opy_.get(test.nodeid, None))
    if bstack1ll1l1ll11l_opy_:
        hook_data[bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ᥂")] = bstack1ll1l1ll11l_opy_
    if result:
        hook_data[bstack1ll1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᥃")] = result.outcome
        hook_data[bstack1ll1ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ᥄")] = result.duration * 1000
        hook_data[bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᥅")] = bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᥆")]
        if result.failed:
            hook_data[bstack1ll1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ᥇")] = bstack1llll1ll_opy_.bstack111llllll1_opy_(call.excinfo.typename)
            hook_data[bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᥈")] = bstack1llll1ll_opy_.bstack1ll11ll1111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᥉")] = bstack1111llll11_opy_(outcome)
        hook_data[bstack1ll1ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ᥊")] = 100
        hook_data[bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᥋")] = bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᥌")]
        if hook_data[bstack1ll1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᥍")] == bstack1ll1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᥎"):
            hook_data[bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ᥏")] = bstack1ll1ll_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᥐ")  # bstack1l1lllll1l1_opy_
            hook_data[bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᥑ")] = [{bstack1ll1ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᥒ"): [bstack1ll1ll_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᥓ")]}]
    if bstack1ll111l1l11_opy_:
        hook_data[bstack1ll1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᥔ")] = bstack1ll111l1l11_opy_.result
        hook_data[bstack1ll1ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᥕ")] = bstack111111l111_opy_(bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᥖ")], bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᥗ")])
        hook_data[bstack1ll1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᥘ")] = bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᥙ")]
        if hook_data[bstack1ll1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᥚ")] == bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᥛ"):
            hook_data[bstack1ll1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᥜ")] = bstack1llll1ll_opy_.bstack111llllll1_opy_(bstack1ll111l1l11_opy_.exception_type)
            hook_data[bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᥝ")] = [{bstack1ll1ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᥞ"): bstack11111ll11l_opy_(bstack1ll111l1l11_opy_.exception)}]
    return hook_data
def bstack1ll1111ll11_opy_(test, bstack11l1ll1ll1_opy_, bstack1111l11l1_opy_, result=None, call=None, outcome=None):
    bstack11ll1ll11l_opy_ = bstack1ll111111ll_opy_(test, bstack11l1ll1ll1_opy_, result, call, bstack1111l11l1_opy_, outcome)
    driver = getattr(test, bstack1ll1ll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᥟ"), None)
    if bstack1111l11l1_opy_ == bstack1ll1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᥠ") and driver:
        bstack11ll1ll11l_opy_[bstack1ll1ll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᥡ")] = bstack1llll1ll_opy_.bstack11ll11l1ll_opy_(driver)
    if bstack1111l11l1_opy_ == bstack1ll1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᥢ"):
        bstack1111l11l1_opy_ = bstack1ll1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᥣ")
    bstack11l1lll1l1_opy_ = {
        bstack1ll1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᥤ"): bstack1111l11l1_opy_,
        bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᥥ"): bstack11ll1ll11l_opy_
    }
    bstack1llll1ll_opy_.bstack11l1l11l11_opy_(bstack11l1lll1l1_opy_)
def bstack1ll1111111l_opy_(test, bstack11l1ll1ll1_opy_, bstack1111l11l1_opy_, result=None, call=None, outcome=None, bstack1ll111l1l11_opy_=None):
    hook_data = bstack1ll1111llll_opy_(test, bstack11l1ll1ll1_opy_, bstack1111l11l1_opy_, result, call, outcome, bstack1ll111l1l11_opy_)
    bstack11l1lll1l1_opy_ = {
        bstack1ll1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᥦ"): bstack1111l11l1_opy_,
        bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᥧ"): hook_data
    }
    bstack1llll1ll_opy_.bstack11l1l11l11_opy_(bstack11l1lll1l1_opy_)
def bstack11l1l11lll_opy_(bstack11l1ll1ll1_opy_):
    if not bstack11l1ll1ll1_opy_:
        return None
    if bstack11l1ll1ll1_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᥨ"), None):
        return getattr(bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᥩ")], bstack1ll1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᥪ"), None)
    return bstack11l1ll1ll1_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᥫ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1llll1ll_opy_.on():
            return
        places = [bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᥬ"), bstack1ll1ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᥭ"), bstack1ll1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ᥮")]
        bstack11l1l1ll11_opy_ = []
        for bstack1ll111l1l1l_opy_ in places:
            records = caplog.get_records(bstack1ll111l1l1l_opy_)
            bstack1ll11111l1l_opy_ = bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᥯") if bstack1ll111l1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠩࡦࡥࡱࡲࠧᥰ") else bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᥱ")
            bstack1l1lllll111_opy_ = request.node.nodeid + (bstack1ll1ll_opy_ (u"ࠫࠬᥲ") if bstack1ll111l1l1l_opy_ == bstack1ll1ll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᥳ") else bstack1ll1ll_opy_ (u"࠭࠭ࠨᥴ") + bstack1ll111l1l1l_opy_)
            bstack11ll1ll111_opy_ = bstack11l1l11lll_opy_(_11l11ll111_opy_.get(bstack1l1lllll111_opy_, None))
            if not bstack11ll1ll111_opy_:
                continue
            for record in records:
                if bstack1111l11l11_opy_(record.message):
                    continue
                bstack11l1l1ll11_opy_.append({
                    bstack1ll1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᥵"): bstack11111111l1_opy_(record.created).isoformat() + bstack1ll1ll_opy_ (u"ࠨ࡜ࠪ᥶"),
                    bstack1ll1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᥷"): record.levelname,
                    bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᥸"): record.message,
                    bstack1ll11111l1l_opy_: bstack11ll1ll111_opy_
                })
        if len(bstack11l1l1ll11_opy_) > 0:
            bstack1llll1ll_opy_.bstack1lll11l1l1_opy_(bstack11l1l1ll11_opy_)
    except Exception as err:
        print(bstack1ll1ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ᥹"), str(err))
def bstack1111111ll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1111111l1_opy_
    bstack1l11lll1ll_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᥺"), None) and bstack1l1lll11_opy_(
            threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᥻"), None)
    bstack11lll1111l_opy_ = getattr(driver, bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ᥼"), None) != None and getattr(driver, bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ᥽"), None) == True
    if sequence == bstack1ll1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ᥾") and driver != None:
      if not bstack1111111l1_opy_ and bstack11111l11l1_opy_() and bstack1ll1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᥿") in CONFIG and CONFIG[bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᦀ")] == True and bstack1lll1l11l_opy_.bstack1ll1ll111l_opy_(driver_command) and (bstack11lll1111l_opy_ or bstack1l11lll1ll_opy_) and not bstack1l1l1l1l11_opy_(args):
        try:
          bstack1111111l1_opy_ = True
          logger.debug(bstack1ll1ll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧᦁ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1ll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫᦂ").format(str(err)))
        bstack1111111l1_opy_ = False
    if sequence == bstack1ll1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᦃ"):
        if driver_command == bstack1ll1ll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᦄ"):
            bstack1llll1ll_opy_.bstack1llllllll_opy_({
                bstack1ll1ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᦅ"): response[bstack1ll1ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩᦆ")],
                bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᦇ"): store[bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᦈ")]
            })
def bstack11lll111_opy_():
    global bstack11llllll1_opy_
    bstack11ll1ll1_opy_.bstack111l11111_opy_()
    logging.shutdown()
    bstack1llll1ll_opy_.bstack11l1l1l111_opy_()
    for driver in bstack11llllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11111lll_opy_(*args):
    global bstack11llllll1_opy_
    bstack1llll1ll_opy_.bstack11l1l1l111_opy_()
    for driver in bstack11llllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l111111_opy_(self, *args, **kwargs):
    bstack1lll1l11ll_opy_ = bstack11111111l_opy_(self, *args, **kwargs)
    bstack1llll1ll_opy_.bstack1ll1l1ll1_opy_(self)
    return bstack1lll1l11ll_opy_
def bstack1l1ll1l1ll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1l1l1ll_opy_ = Config.bstack1ll111l11_opy_()
    if bstack1l1l1l1ll_opy_.get_property(bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪᦉ")):
        return
    bstack1l1l1l1ll_opy_.bstack111ll1l1l_opy_(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫᦊ"), True)
    global bstack11lllllll_opy_
    global bstack1lllll1111_opy_
    bstack11lllllll_opy_ = framework_name
    logger.info(bstack1l11l111l1_opy_.format(bstack11lllllll_opy_.split(bstack1ll1ll_opy_ (u"ࠨ࠯ࠪᦋ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11111l11l1_opy_():
            Service.start = bstack1l11ll11_opy_
            Service.stop = bstack1l1lll1l_opy_
            webdriver.Remote.__init__ = bstack1lll1111ll_opy_
            webdriver.Remote.get = bstack1l1ll1l1l_opy_
            if not isinstance(os.getenv(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪᦌ")), str):
                return
            WebDriver.close = bstack1lll1llll1_opy_
            WebDriver.quit = bstack111ll111l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack11111l11l1_opy_() and bstack1llll1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1l111111_opy_
        bstack1lllll1111_opy_ = True
    except Exception as e:
        pass
    bstack1ll11ll1l1_opy_()
    if os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨᦍ")):
        bstack1lllll1111_opy_ = eval(os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᦎ")))
    if not bstack1lllll1111_opy_:
        bstack1l1l1ll1l_opy_(bstack1ll1ll_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢᦏ"), bstack1l1llllll_opy_)
    if bstack1l1llllll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1llll1l1ll_opy_ = bstack1l1ll11ll_opy_
        except Exception as e:
            logger.error(bstack1lll11ll_opy_.format(str(e)))
    if bstack1ll1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᦐ") in str(framework_name).lower():
        if not bstack11111l11l1_opy_():
            return
        try:
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
def bstack111ll111l_opy_(self):
    global bstack11lllllll_opy_
    global bstack1lll11111_opy_
    global bstack1l11111l1_opy_
    try:
        if bstack1ll1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᦑ") in bstack11lllllll_opy_ and self.session_id != None and bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᦒ"), bstack1ll1ll_opy_ (u"ࠩࠪᦓ")) != bstack1ll1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᦔ"):
            bstack1llll11lll_opy_ = bstack1ll1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᦕ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᦖ")
            bstack1ll11ll11_opy_(logger, True)
            if self != None:
                bstack11l1llll_opy_(self, bstack1llll11lll_opy_, bstack1ll1ll_opy_ (u"࠭ࠬࠡࠩᦗ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᦘ"), None)
        if item is not None and bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᦙ"), None):
            bstack11lllll1_opy_.bstack1l1l1111l_opy_(self, bstack1ll11llll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1ll_opy_ (u"ࠩࠪᦚ")
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦᦛ") + str(e))
    bstack1l11111l1_opy_(self)
    self.session_id = None
def bstack1lll1111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll11111_opy_
    global bstack1llll1lll_opy_
    global bstack1l1111l1_opy_
    global bstack11lllllll_opy_
    global bstack11111111l_opy_
    global bstack11llllll1_opy_
    global bstack1llll11111_opy_
    global bstack11l1lll1l_opy_
    global bstack1ll11llll1_opy_
    CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᦜ")] = str(bstack11lllllll_opy_) + str(__version__)
    command_executor = bstack1l1lll1lll_opy_(bstack1llll11111_opy_, CONFIG)
    logger.debug(bstack1l1111l11_opy_.format(command_executor))
    proxy = bstack1lll1ll11l_opy_(CONFIG, proxy)
    bstack1ll111l1_opy_ = 0
    try:
        if bstack1l1111l1_opy_ is True:
            bstack1ll111l1_opy_ = int(os.environ.get(bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᦝ")))
    except:
        bstack1ll111l1_opy_ = 0
    bstack1ll1llll1l_opy_ = bstack1llll1111_opy_(CONFIG, bstack1ll111l1_opy_)
    logger.debug(bstack1lll1ll111_opy_.format(str(bstack1ll1llll1l_opy_)))
    bstack1ll11llll1_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᦞ"))[bstack1ll111l1_opy_]
    if bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᦟ") in CONFIG and CONFIG[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᦠ")]:
        bstack1l1l1l1l1l_opy_(bstack1ll1llll1l_opy_, bstack11l1lll1l_opy_)
    if bstack1l11l11l1_opy_.bstack1lllll1l1l_opy_(CONFIG, bstack1ll111l1_opy_) and bstack1l11l11l1_opy_.bstack1l11l1l11_opy_(bstack1ll1llll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack1l11l11l1_opy_.set_capabilities(bstack1ll1llll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack1111lll11_opy_ = bstack1l111l1ll_opy_(desired_capabilities)
        bstack1111lll11_opy_[bstack1ll1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᦡ")] = bstack1l1ll11lll_opy_(CONFIG)
        bstack1l1l1lll_opy_ = bstack1llll1111_opy_(bstack1111lll11_opy_)
        if bstack1l1l1lll_opy_:
            bstack1ll1llll1l_opy_ = update(bstack1l1l1lll_opy_, bstack1ll1llll1l_opy_)
        desired_capabilities = None
    if options:
        bstack111ll1l1_opy_(options, bstack1ll1llll1l_opy_)
    if not options:
        options = bstack11ll11ll_opy_(bstack1ll1llll1l_opy_)
    if proxy and bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᦢ")):
        options.proxy(proxy)
    if options and bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᦣ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l11llllll_opy_() < version.parse(bstack1ll1ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᦤ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1llll1l_opy_)
    logger.info(bstack1lll1l1l1_opy_)
    if bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᦥ")):
        bstack11111111l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᦦ")):
        bstack11111111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᦧ")):
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
        bstack111l1lll1_opy_ = bstack1ll1ll_opy_ (u"ࠩࠪᦨ")
        if bstack1l11llllll_opy_() >= version.parse(bstack1ll1ll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫᦩ")):
            bstack111l1lll1_opy_ = self.caps.get(bstack1ll1ll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᦪ"))
        else:
            bstack111l1lll1_opy_ = self.capabilities.get(bstack1ll1ll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᦫ"))
        if bstack111l1lll1_opy_:
            bstack11111lll1_opy_(bstack111l1lll1_opy_)
            if bstack1l11llllll_opy_() <= version.parse(bstack1ll1ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭᦬")):
                self.command_executor._url = bstack1ll1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᦭") + bstack1llll11111_opy_ + bstack1ll1ll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ᦮")
            else:
                self.command_executor._url = bstack1ll1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᦯") + bstack111l1lll1_opy_ + bstack1ll1ll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᦰ")
            logger.debug(bstack1l1l1l11l_opy_.format(bstack111l1lll1_opy_))
        else:
            logger.debug(bstack1l1111ll1_opy_.format(bstack1ll1ll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᦱ")))
    except Exception as e:
        logger.debug(bstack1l1111ll1_opy_.format(e))
    bstack1lll11111_opy_ = self.session_id
    if bstack1ll1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᦲ") in bstack11lllllll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᦳ"), None)
        if item:
            bstack1l1llllll11_opy_ = getattr(item, bstack1ll1ll_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬᦴ"), False)
            if not getattr(item, bstack1ll1ll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᦵ"), None) and bstack1l1llllll11_opy_:
                setattr(store[bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᦶ")], bstack1ll1ll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᦷ"), self)
        bstack1llll1ll_opy_.bstack1ll1l1ll1_opy_(self)
    bstack11llllll1_opy_.append(self)
    if bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᦸ") in CONFIG and bstack1ll1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᦹ") in CONFIG[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᦺ")][bstack1ll111l1_opy_]:
        bstack1llll1lll_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᦻ")][bstack1ll111l1_opy_][bstack1ll1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᦼ")]
    logger.debug(bstack1l1l111ll_opy_.format(bstack1lll11111_opy_))
def bstack1l1ll1l1l_opy_(self, url):
    global bstack11lll11l11_opy_
    global CONFIG
    try:
        bstack1ll111lll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111lll11l_opy_.format(str(err)))
    try:
        bstack11lll11l11_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1lll11l_opy_ = str(e)
            if any(err_msg in bstack1l1lll11l_opy_ for err_msg in bstack1l1lll111_opy_):
                bstack1ll111lll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111lll11l_opy_.format(str(err)))
        raise e
def bstack1llll1llll_opy_(item, when):
    global bstack1llll11l1_opy_
    try:
        bstack1llll11l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll1l1ll1_opy_(item, call, rep):
    global bstack1l1111111_opy_
    global bstack11llllll1_opy_
    name = bstack1ll1ll_opy_ (u"ࠩࠪᦽ")
    try:
        if rep.when == bstack1ll1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᦾ"):
            bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
            bstack1ll111l111l_opy_ = item.config.getoption(bstack1ll1ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᦿ"))
            try:
                if (str(bstack1ll111l111l_opy_).lower() != bstack1ll1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪᧀ")):
                    name = str(rep.nodeid)
                    bstack11llll1l_opy_ = bstack1ll1l111l_opy_(bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᧁ"), name, bstack1ll1ll_opy_ (u"ࠧࠨᧂ"), bstack1ll1ll_opy_ (u"ࠨࠩᧃ"), bstack1ll1ll_opy_ (u"ࠩࠪᧄ"), bstack1ll1ll_opy_ (u"ࠪࠫᧅ"))
                    os.environ[bstack1ll1ll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᧆ")] = name
                    for driver in bstack11llllll1_opy_:
                        if bstack1lll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack11llll1l_opy_)
            except Exception as e:
                logger.debug(bstack1ll1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬᧇ").format(str(e)))
            try:
                bstack1ll1l1ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᧈ"):
                    status = bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᧉ") if rep.outcome.lower() == bstack1ll1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᧊") else bstack1ll1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᧋")
                    reason = bstack1ll1ll_opy_ (u"ࠪࠫ᧌")
                    if status == bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᧍"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1ll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ᧎") if status == bstack1ll1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᧏") else bstack1ll1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᧐")
                    data = name + bstack1ll1ll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ᧑") if status == bstack1ll1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᧒") else name + bstack1ll1ll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭᧓") + reason
                    bstack111l1l11l_opy_ = bstack1ll1l111l_opy_(bstack1ll1ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭᧔"), bstack1ll1ll_opy_ (u"ࠬ࠭᧕"), bstack1ll1ll_opy_ (u"࠭ࠧ᧖"), bstack1ll1ll_opy_ (u"ࠧࠨ᧗"), level, data)
                    for driver in bstack11llllll1_opy_:
                        if bstack1lll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack111l1l11l_opy_)
            except Exception as e:
                logger.debug(bstack1ll1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ᧘").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭᧙").format(str(e)))
    bstack1l1111111_opy_(item, call, rep)
notset = Notset()
def bstack1llll1ll1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll111ll1_opy_
    if str(name).lower() == bstack1ll1ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ᧚"):
        return bstack1ll1ll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ᧛")
    else:
        return bstack1ll111ll1_opy_(self, name, default, skip)
def bstack1l1ll11ll_opy_(self):
    global CONFIG
    global bstack1l11lll111_opy_
    try:
        proxy = bstack1llll111l1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1ll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ᧜")):
                proxies = bstack11llllll_opy_(proxy, bstack1l1lll1lll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1l111l_opy_ = proxies.popitem()
                    if bstack1ll1ll_opy_ (u"ࠨ࠺࠰࠱ࠥ᧝") in bstack1l1l111l_opy_:
                        return bstack1l1l111l_opy_
                    else:
                        return bstack1ll1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᧞") + bstack1l1l111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ᧟").format(str(e)))
    return bstack1l11lll111_opy_(self)
def bstack1l1llllll1_opy_():
    return (bstack1ll1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᧠") in CONFIG or bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᧡") in CONFIG) and bstack1lll11l1ll_opy_() and bstack1l11llllll_opy_() >= version.parse(
        bstack11ll11111_opy_)
def bstack11lll1ll11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1llll1lll_opy_
    global bstack1l1111l1_opy_
    global bstack11lllllll_opy_
    CONFIG[bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᧢")] = str(bstack11lllllll_opy_) + str(__version__)
    bstack1ll111l1_opy_ = 0
    try:
        if bstack1l1111l1_opy_ is True:
            bstack1ll111l1_opy_ = int(os.environ.get(bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᧣")))
    except:
        bstack1ll111l1_opy_ = 0
    CONFIG[bstack1ll1ll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ᧤")] = True
    bstack1ll1llll1l_opy_ = bstack1llll1111_opy_(CONFIG, bstack1ll111l1_opy_)
    logger.debug(bstack1lll1ll111_opy_.format(str(bstack1ll1llll1l_opy_)))
    if CONFIG.get(bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᧥")):
        bstack1l1l1l1l1l_opy_(bstack1ll1llll1l_opy_, bstack11l1lll1l_opy_)
    if bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᧦") in CONFIG and bstack1ll1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᧧") in CONFIG[bstack1ll1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᧨")][bstack1ll111l1_opy_]:
        bstack1llll1lll_opy_ = CONFIG[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᧩")][bstack1ll111l1_opy_][bstack1ll1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᧪")]
    import urllib
    import json
    if bstack1ll1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᧫") in CONFIG and str(CONFIG[bstack1ll1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᧬")]).lower() != bstack1ll1ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ᧭"):
        bstack1l111ll1_opy_ = bstack1lllll111_opy_()
        bstack1llllll11_opy_ = bstack1l111ll1_opy_ + urllib.parse.quote(json.dumps(bstack1ll1llll1l_opy_))
    else:
        bstack1llllll11_opy_ = bstack1ll1ll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ᧮") + urllib.parse.quote(json.dumps(bstack1ll1llll1l_opy_))
    browser = self.connect(bstack1llllll11_opy_)
    return browser
def bstack1ll11ll1l1_opy_():
    global bstack1lllll1111_opy_
    global bstack11lllllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111111ll_opy_
        if not bstack11111l11l1_opy_():
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
def bstack1ll1111ll1l_opy_():
    global CONFIG
    global bstack1l1111l11l_opy_
    global bstack1llll11111_opy_
    global bstack11l1lll1l_opy_
    global bstack1l1111l1_opy_
    global bstack1l1llll11l_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ᧯")))
    bstack1l1111l11l_opy_ = eval(os.environ.get(bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ᧰")))
    bstack1llll11111_opy_ = os.environ.get(bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ᧱"))
    bstack1l1l1lll1_opy_(CONFIG, bstack1l1111l11l_opy_)
    bstack1l1llll11l_opy_ = bstack11ll1ll1_opy_.bstack111lll1l1_opy_(CONFIG, bstack1l1llll11l_opy_)
    global bstack11111111l_opy_
    global bstack1l11111l1_opy_
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
    except Exception as e:
        pass
    if (bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᧲") in CONFIG or bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᧳") in CONFIG) and bstack1lll11l1ll_opy_():
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
        logger.debug(bstack1ll1ll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ᧴"))
    bstack11l1lll1l_opy_ = CONFIG.get(bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭᧵"), {}).get(bstack1ll1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᧶"))
    bstack1l1111l1_opy_ = True
    bstack1l1ll1l1ll_opy_(bstack1ll111111l_opy_)
if (bstack11111l1ll1_opy_()):
    bstack1ll1111ll1l_opy_()
@bstack11l1llllll_opy_(class_method=False)
def bstack1l1lllll1ll_opy_(hook_name, event, bstack1ll111l1111_opy_=None):
    if hook_name not in [bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ᧷"), bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ᧸"), bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ᧹"), bstack1ll1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ᧺"), bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭᧻"), bstack1ll1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ᧼"), bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ᧽"), bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᧾")]:
        return
    node = store[bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᧿")]
    if hook_name in [bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᨀ"), bstack1ll1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᨁ")]:
        node = store[bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᨂ")]
    elif hook_name in [bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᨃ"), bstack1ll1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᨄ")]:
        node = store[bstack1ll1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᨅ")]
    if event == bstack1ll1ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᨆ"):
        hook_type = bstack1ll1lll1l1l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l1ll1111_opy_ = {
            bstack1ll1ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᨇ"): uuid,
            bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᨈ"): bstack1l1l11l11l_opy_(),
            bstack1ll1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᨉ"): bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᨊ"),
            bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᨋ"): hook_type,
            bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᨌ"): hook_name
        }
        store[bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᨍ")].append(uuid)
        bstack1ll111l1ll1_opy_ = node.nodeid
        if hook_type == bstack1ll1ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᨎ"):
            if not _11l11ll111_opy_.get(bstack1ll111l1ll1_opy_, None):
                _11l11ll111_opy_[bstack1ll111l1ll1_opy_] = {bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᨏ"): []}
            _11l11ll111_opy_[bstack1ll111l1ll1_opy_][bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᨐ")].append(bstack11l1ll1111_opy_[bstack1ll1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᨑ")])
        _11l11ll111_opy_[bstack1ll111l1ll1_opy_ + bstack1ll1ll_opy_ (u"ࠪ࠱ࠬᨒ") + hook_name] = bstack11l1ll1111_opy_
        bstack1ll1111111l_opy_(node, bstack11l1ll1111_opy_, bstack1ll1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᨓ"))
    elif event == bstack1ll1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᨔ"):
        bstack11ll111l1l_opy_ = node.nodeid + bstack1ll1ll_opy_ (u"࠭࠭ࠨᨕ") + hook_name
        _11l11ll111_opy_[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᨖ")] = bstack1l1l11l11l_opy_()
        bstack1ll1111lll1_opy_(_11l11ll111_opy_[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᨗ")])
        bstack1ll1111111l_opy_(node, _11l11ll111_opy_[bstack11ll111l1l_opy_], bstack1ll1ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧᨘࠫ"), bstack1ll111l1l11_opy_=bstack1ll111l1111_opy_)
def bstack1ll1111l1ll_opy_():
    global bstack1ll111l11ll_opy_
    if bstack1111l1l1l_opy_():
        bstack1ll111l11ll_opy_ = bstack1ll1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᨙ")
    else:
        bstack1ll111l11ll_opy_ = bstack1ll1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᨚ")
@bstack1llll1ll_opy_.bstack1ll11l1l1ll_opy_
def bstack1l1lllllll1_opy_():
    bstack1ll1111l1ll_opy_()
    if bstack1lll11l1ll_opy_():
        bstack11llll11l1_opy_(bstack1111111ll_opy_)
    try:
        bstack1llll1ll1l1_opy_(bstack1l1lllll1ll_opy_)
    except Exception as e:
        logger.debug(bstack1ll1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᨛ").format(e))
bstack1l1lllllll1_opy_()