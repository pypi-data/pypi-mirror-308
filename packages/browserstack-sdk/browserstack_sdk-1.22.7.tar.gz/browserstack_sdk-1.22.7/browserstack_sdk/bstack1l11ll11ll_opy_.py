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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11ll1ll11l_opy_ import bstack11ll11ll1l_opy_, bstack11ll1ll1ll_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack1111llll_opy_
from bstack_utils.helper import bstack1l1lll11_opy_, bstack1l1l11l11l_opy_, Result
from bstack_utils.bstack1l111lll11_opy_ import bstack1llll1ll_opy_
from bstack_utils.capture import bstack11ll11l1l1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l11ll11ll_opy_:
    def __init__(self):
        self.bstack11ll1l1l1l_opy_ = bstack11ll11l1l1_opy_(self.bstack11ll1l1l11_opy_)
        self.tests = {}
    @staticmethod
    def bstack11ll1l1l11_opy_(log):
        if not (log[bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧย")] and log[bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨร")].strip()):
            return
        active = bstack1111llll_opy_.bstack11ll111l11_opy_()
        log = {
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧฤ"): log[bstack1ll1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨล")],
            bstack1ll1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ฦ"): bstack1l1l11l11l_opy_(),
            bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬว"): log[bstack1ll1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ศ")],
        }
        if active:
            if active[bstack1ll1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫษ")] == bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬส"):
                log[bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨห")] = active[bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩฬ")]
            elif active[bstack1ll1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨอ")] == bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩฮ"):
                log[bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬฯ")] = active[bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ะ")]
        bstack1llll1ll_opy_.bstack1lll11l1l1_opy_([log])
    def start_test(self, attrs):
        bstack11ll1ll111_opy_ = uuid4().__str__()
        self.tests[bstack11ll1ll111_opy_] = {}
        self.bstack11ll1l1l1l_opy_.start()
        driver = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ั"), None)
        bstack11ll1ll11l_opy_ = bstack11ll1ll1ll_opy_(
            name=attrs.scenario.name,
            uuid=bstack11ll1ll111_opy_,
            bstack11ll11lll1_opy_=bstack1l1l11l11l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1ll1ll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤา"),
            framework=bstack1ll1ll_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩำ"),
            scope=[attrs.feature.name],
            bstack11ll1111ll_opy_=bstack1llll1ll_opy_.bstack11ll11l1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11ll1ll111_opy_][bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ิ")] = bstack11ll1ll11l_opy_
        threading.current_thread().current_test_uuid = bstack11ll1ll111_opy_
        bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬี"), bstack11ll1ll11l_opy_)
    def end_test(self, attrs):
        bstack11ll11l11l_opy_ = {
            bstack1ll1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥึ"): attrs.feature.name,
            bstack1ll1ll_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦื"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11ll1ll11l_opy_ = self.tests[current_test_uuid][bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣุࠪ")]
        meta = {
            bstack1ll1ll_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤู"): bstack11ll11l11l_opy_,
            bstack1ll1ll_opy_ (u"ࠤࡶࡸࡪࡶࡳฺࠣ"): bstack11ll1ll11l_opy_.meta.get(bstack1ll1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ฻"), []),
            bstack1ll1ll_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ฼"): {
                bstack1ll1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ฽"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11ll1ll11l_opy_.bstack11ll11l111_opy_(meta)
        bstack11ll1ll11l_opy_.bstack11ll1ll1l1_opy_(bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ฾"), []))
        bstack11ll1l1111_opy_, exception = self._11ll1l11l1_opy_(attrs)
        bstack11ll1l1lll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11ll1l111l_opy_=[bstack11ll1l1111_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ฿")].stop(time=bstack1l1l11l11l_opy_(), duration=int(attrs.duration)*1000, result=bstack11ll1l1lll_opy_)
        bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪเ"), self.tests[threading.current_thread().current_test_uuid][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬแ")])
    def bstack111ll11l1_opy_(self, attrs):
        bstack11ll111ll1_opy_ = {
            bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࠭โ"): uuid4().__str__(),
            bstack1ll1ll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬใ"): attrs.keyword,
            bstack1ll1ll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬไ"): [],
            bstack1ll1ll_opy_ (u"࠭ࡴࡦࡺࡷࠫๅ"): attrs.name,
            bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫๆ"): bstack1l1l11l11l_opy_(),
            bstack1ll1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ็"): bstack1ll1ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩ่ࠪ"),
            bstack1ll1ll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ้"): bstack1ll1ll_opy_ (u"๊ࠫࠬ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ๋")].add_step(bstack11ll111ll1_opy_)
        threading.current_thread().current_step_uuid = bstack11ll111ll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩ์")]
    def bstack1l111111l_opy_(self, attrs):
        current_test_id = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫํ"), None)
        current_step_uuid = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ๎"), None)
        bstack11ll1l1111_opy_, exception = self._11ll1l11l1_opy_(attrs)
        bstack11ll1l1lll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11ll1l111l_opy_=[bstack11ll1l1111_opy_])
        self.tests[current_test_id][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ๏")].bstack11ll1lll11_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11ll1l1lll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l111l11ll_opy_(self, name, attrs):
        try:
            bstack11ll1l11ll_opy_ = uuid4().__str__()
            self.tests[bstack11ll1l11ll_opy_] = {}
            self.bstack11ll1l1l1l_opy_.start()
            scopes = []
            driver = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ๐"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ๑")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11ll1l11ll_opy_)
            if name in [bstack1ll1ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ๒"), bstack1ll1ll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ๓")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ๔"), bstack1ll1ll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ๕")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll1ll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ๖")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11ll11ll1l_opy_(
                name=name,
                uuid=bstack11ll1l11ll_opy_,
                bstack11ll11lll1_opy_=bstack1l1l11l11l_opy_(),
                file_path=file_path,
                framework=bstack1ll1ll_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ๗"),
                bstack11ll1111ll_opy_=bstack1llll1ll_opy_.bstack11ll11l1ll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll1ll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ๘"),
                hook_type=name
            )
            self.tests[bstack11ll1l11ll_opy_][bstack1ll1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ๙")] = hook_data
            current_test_id = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ๚"), None)
            if current_test_id:
                hook_data.bstack11ll11ll11_opy_(current_test_id)
            if name == bstack1ll1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ๛"):
                threading.current_thread().before_all_hook_uuid = bstack11ll1l11ll_opy_
            threading.current_thread().current_hook_uuid = bstack11ll1l11ll_opy_
            bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ๜"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ๝"), name, e)
    def bstack111l111ll_opy_(self, attrs):
        bstack11ll111l1l_opy_ = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ๞"), None)
        hook_data = self.tests[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๟")]
        status = bstack1ll1ll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ๠")
        exception = None
        bstack11ll1l1111_opy_ = None
        if hook_data.name == bstack1ll1ll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ๡"):
            self.bstack11ll1l1l1l_opy_.reset()
            bstack11ll11llll_opy_ = self.tests[bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ๢"), None)][bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ๣")].result.result
            if bstack11ll11llll_opy_ == bstack1ll1ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ๤"):
                if attrs.hook_failures == 1:
                    status = bstack1ll1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ๥")
                elif attrs.hook_failures == 2:
                    status = bstack1ll1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ๦")
            elif attrs.bstack11ll111lll_opy_:
                status = bstack1ll1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ๧")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ๨") and attrs.hook_failures == 1:
                status = bstack1ll1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ๩")
            elif hasattr(attrs, bstack1ll1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ๪")) and attrs.error_message:
                status = bstack1ll1ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ๫")
            bstack11ll1l1111_opy_, exception = self._11ll1l11l1_opy_(attrs)
        bstack11ll1l1lll_opy_ = Result(result=status, exception=exception, bstack11ll1l111l_opy_=[bstack11ll1l1111_opy_])
        hook_data.stop(time=bstack1l1l11l11l_opy_(), duration=0, result=bstack11ll1l1lll_opy_)
        bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ๬"), self.tests[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๭")])
        threading.current_thread().current_hook_uuid = None
    def _11ll1l11l1_opy_(self, attrs):
        try:
            import traceback
            bstack1l1ll111l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11ll1l1111_opy_ = bstack1l1ll111l_opy_[-1] if bstack1l1ll111l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ๮"))
            bstack11ll1l1111_opy_ = None
            exception = None
        return bstack11ll1l1111_opy_, exception