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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l1ll1l1l_opy_ import RobotHandler
from bstack_utils.capture import bstack11ll11l1l1_opy_
from bstack_utils.bstack11ll1ll11l_opy_ import bstack11l11lll1l_opy_, bstack11ll11ll1l_opy_, bstack11ll1ll1ll_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack1111llll_opy_
from bstack_utils.bstack1l111lll11_opy_ import bstack1llll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1lll11_opy_, bstack1l1l11l11l_opy_, Result, \
    bstack11l1llllll_opy_, bstack11l11l11ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ๯"): [],
        bstack1ll1ll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭๰"): [],
        bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ๱"): []
    }
    bstack11l11l1l1l_opy_ = []
    bstack11l1l111l1_opy_ = []
    @staticmethod
    def bstack11ll1l1l11_opy_(log):
        if not (log[bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๲")] and log[bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๳")].strip()):
            return
        active = bstack1111llll_opy_.bstack11ll111l11_opy_()
        log = {
            bstack1ll1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ๴"): log[bstack1ll1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ๵")],
            bstack1ll1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ๶"): bstack11l11l11ll_opy_().isoformat() + bstack1ll1ll_opy_ (u"࡛ࠧࠩ๷"),
            bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๸"): log[bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ๹")],
        }
        if active:
            if active[bstack1ll1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨ๺")] == bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ๻"):
                log[bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ๼")] = active[bstack1ll1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭๽")]
            elif active[bstack1ll1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ๾")] == bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹ࠭๿"):
                log[bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ຀")] = active[bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪກ")]
        bstack1llll1ll_opy_.bstack1lll11l1l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11l1l1l11l_opy_ = None
        self._11l1l11ll1_opy_ = None
        self._11l11ll111_opy_ = OrderedDict()
        self.bstack11ll1l1l1l_opy_ = bstack11ll11l1l1_opy_(self.bstack11ll1l1l11_opy_)
    @bstack11l1llllll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l11l1ll1_opy_()
        if not self._11l11ll111_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧຂ")), None):
            self._11l11ll111_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨ຃"))] = {}
        bstack11l1lll11l_opy_ = bstack11ll1ll1ll_opy_(
                bstack11l1ll1lll_opy_=attrs.get(bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩຄ")),
                name=name,
                bstack11ll11lll1_opy_=bstack1l1l11l11l_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ຅")], start=os.getcwd()) if attrs.get(bstack1ll1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨຆ")) != bstack1ll1ll_opy_ (u"ࠩࠪງ") else bstack1ll1ll_opy_ (u"ࠪࠫຈ"),
                framework=bstack1ll1ll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪຉ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨຊ"), None)
        self._11l11ll111_opy_[attrs.get(bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩ຋"))][bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪຌ")] = bstack11l1lll11l_opy_
    @bstack11l1llllll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l1llll11_opy_()
        self._11l1ll111l_opy_(messages)
        for bstack11ll111111_opy_ in self.bstack11l11l1l1l_opy_:
            bstack11ll111111_opy_[bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪຍ")][bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨຎ")].extend(self.store[bstack1ll1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩຏ")])
            bstack1llll1ll_opy_.bstack11l1l11l11_opy_(bstack11ll111111_opy_)
        self.bstack11l11l1l1l_opy_ = []
        self.store[bstack1ll1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪຐ")] = []
    @bstack11l1llllll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11ll1l1l1l_opy_.start()
        if not self._11l11ll111_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨຑ")), None):
            self._11l11ll111_opy_[attrs.get(bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩຒ"))] = {}
        driver = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ຓ"), None)
        bstack11ll1ll11l_opy_ = bstack11ll1ll1ll_opy_(
            bstack11l1ll1lll_opy_=attrs.get(bstack1ll1ll_opy_ (u"ࠨ࡫ࡧࠫດ")),
            name=name,
            bstack11ll11lll1_opy_=bstack1l1l11l11l_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩຕ")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1llll1l_opy_(attrs.get(bstack1ll1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪຖ"), None)),
            framework=bstack1ll1ll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪທ"),
            tags=attrs[bstack1ll1ll_opy_ (u"ࠬࡺࡡࡨࡵࠪຘ")],
            hooks=self.store[bstack1ll1ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬນ")],
            bstack11ll1111ll_opy_=bstack1llll1ll_opy_.bstack11ll11l1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1ll_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤບ").format(bstack1ll1ll_opy_ (u"ࠣࠢࠥປ").join(attrs[bstack1ll1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧຜ")]), name) if attrs[bstack1ll1ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨຝ")] else name
        )
        self._11l11ll111_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧພ"))][bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨຟ")] = bstack11ll1ll11l_opy_
        threading.current_thread().current_test_uuid = bstack11ll1ll11l_opy_.bstack11l11ll1ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩຠ"), None)
        self.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨມ"), bstack11ll1ll11l_opy_)
    @bstack11l1llllll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11ll1l1l1l_opy_.reset()
        bstack11l1lllll1_opy_ = bstack11l11llll1_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨຢ")), bstack1ll1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪຣ"))
        self._11l11ll111_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࠭຤"))][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧລ")].stop(time=bstack1l1l11l11l_opy_(), duration=int(attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪ຦"), bstack1ll1ll_opy_ (u"࠭࠰ࠨວ"))), result=Result(result=bstack11l1lllll1_opy_, exception=attrs.get(bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຨ")), bstack11ll1l111l_opy_=[attrs.get(bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຩ"))]))
        self.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫສ"), self._11l11ll111_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࠭ຫ"))][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຬ")], True)
        self.store[bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩອ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l1llllll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l11l1ll1_opy_()
        current_test_id = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨຮ"), None)
        bstack11l1ll1l11_opy_ = current_test_id if bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩຯ"), None) else bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫະ"), None)
        if attrs.get(bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧັ"), bstack1ll1ll_opy_ (u"ࠪࠫາ")).lower() in [bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪຳ"), bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧິ")]:
            hook_type = bstack11l1l1111l_opy_(attrs.get(bstack1ll1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫີ")), bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫຶ"), None))
            hook_name = bstack1ll1ll_opy_ (u"ࠨࡽࢀࠫື").format(attrs.get(bstack1ll1ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦຸࠩ"), bstack1ll1ll_opy_ (u"ູࠪࠫ")))
            if hook_type in [bstack1ll1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ຺"), bstack1ll1ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨົ")]:
                hook_name = bstack1ll1ll_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧຼ").format(bstack11l1l1l1l1_opy_.get(hook_type), attrs.get(bstack1ll1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧຽ"), bstack1ll1ll_opy_ (u"ࠨࠩ຾")))
            bstack11l1ll1111_opy_ = bstack11ll11ll1l_opy_(
                bstack11l1ll1lll_opy_=bstack11l1ll1l11_opy_ + bstack1ll1ll_opy_ (u"ࠩ࠰ࠫ຿") + attrs.get(bstack1ll1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨເ"), bstack1ll1ll_opy_ (u"ࠫࠬແ")).lower(),
                name=hook_name,
                bstack11ll11lll1_opy_=bstack1l1l11l11l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬໂ")), start=os.getcwd()),
                framework=bstack1ll1ll_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬໃ"),
                tags=attrs[bstack1ll1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬໄ")],
                scope=RobotHandler.bstack11l1llll1l_opy_(attrs.get(bstack1ll1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໅"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l1ll1111_opy_.bstack11l11ll1ll_opy_()
            threading.current_thread().current_hook_id = bstack11l1ll1l11_opy_ + bstack1ll1ll_opy_ (u"ࠩ࠰ࠫໆ") + attrs.get(bstack1ll1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨ໇"), bstack1ll1ll_opy_ (u"່ࠫࠬ")).lower()
            self.store[bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥ້ࠩ")] = [bstack11l1ll1111_opy_.bstack11l11ll1ll_opy_()]
            if bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦ໊ࠪ"), None):
                self.store[bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶ໋ࠫ")].append(bstack11l1ll1111_opy_.bstack11l11ll1ll_opy_())
            else:
                self.store[bstack1ll1ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໌")].append(bstack11l1ll1111_opy_.bstack11l11ll1ll_opy_())
            if bstack11l1ll1l11_opy_:
                self._11l11ll111_opy_[bstack11l1ll1l11_opy_ + bstack1ll1ll_opy_ (u"ࠩ࠰ࠫໍ") + attrs.get(bstack1ll1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨ໎"), bstack1ll1ll_opy_ (u"ࠫࠬ໏")).lower()] = { bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ໐"): bstack11l1ll1111_opy_ }
            bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ໑"), bstack11l1ll1111_opy_)
        else:
            bstack11ll111ll1_opy_ = {
                bstack1ll1ll_opy_ (u"ࠧࡪࡦࠪ໒"): uuid4().__str__(),
                bstack1ll1ll_opy_ (u"ࠨࡶࡨࡼࡹ࠭໓"): bstack1ll1ll_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ໔").format(attrs.get(bstack1ll1ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ໕")), attrs.get(bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ໖"), bstack1ll1ll_opy_ (u"ࠬ࠭໗"))) if attrs.get(bstack1ll1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫ໘"), []) else attrs.get(bstack1ll1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ໙")),
                bstack1ll1ll_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ໚"): attrs.get(bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ໛"), []),
                bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧໜ"): bstack1l1l11l11l_opy_(),
                bstack1ll1ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫໝ"): bstack1ll1ll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ໞ"),
                bstack1ll1ll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫໟ"): attrs.get(bstack1ll1ll_opy_ (u"ࠧࡥࡱࡦࠫ໠"), bstack1ll1ll_opy_ (u"ࠨࠩ໡"))
            }
            if attrs.get(bstack1ll1ll_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ໢"), bstack1ll1ll_opy_ (u"ࠪࠫ໣")) != bstack1ll1ll_opy_ (u"ࠫࠬ໤"):
                bstack11ll111ll1_opy_[bstack1ll1ll_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭໥")] = attrs.get(bstack1ll1ll_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ໦"))
            if not self.bstack11l1l111l1_opy_:
                self._11l11ll111_opy_[self._11l11ll11l_opy_()][bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໧")].add_step(bstack11ll111ll1_opy_)
                threading.current_thread().current_step_uuid = bstack11ll111ll1_opy_[bstack1ll1ll_opy_ (u"ࠨ࡫ࡧࠫ໨")]
            self.bstack11l1l111l1_opy_.append(bstack11ll111ll1_opy_)
    @bstack11l1llllll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l1llll11_opy_()
        self._11l1ll111l_opy_(messages)
        current_test_id = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ໩"), None)
        bstack11l1ll1l11_opy_ = current_test_id if current_test_id else bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭໪"), None)
        bstack11l1ll11l1_opy_ = bstack11l11llll1_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ໫")), bstack1ll1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭໬"))
        bstack11l1l11l1l_opy_ = attrs.get(bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໭"))
        if bstack11l1ll11l1_opy_ != bstack1ll1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ໮") and not attrs.get(bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໯")) and self._11l1l1l11l_opy_:
            bstack11l1l11l1l_opy_ = self._11l1l1l11l_opy_
        bstack11ll1l1lll_opy_ = Result(result=bstack11l1ll11l1_opy_, exception=bstack11l1l11l1l_opy_, bstack11ll1l111l_opy_=[bstack11l1l11l1l_opy_])
        if attrs.get(bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໰"), bstack1ll1ll_opy_ (u"ࠪࠫ໱")).lower() in [bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ໲"), bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ໳")]:
            bstack11l1ll1l11_opy_ = current_test_id if current_test_id else bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ໴"), None)
            if bstack11l1ll1l11_opy_:
                bstack11ll111l1l_opy_ = bstack11l1ll1l11_opy_ + bstack1ll1ll_opy_ (u"ࠢ࠮ࠤ໵") + attrs.get(bstack1ll1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭໶"), bstack1ll1ll_opy_ (u"ࠩࠪ໷")).lower()
                self._11l11ll111_opy_[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໸")].stop(time=bstack1l1l11l11l_opy_(), duration=int(attrs.get(bstack1ll1ll_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ໹"), bstack1ll1ll_opy_ (u"ࠬ࠶ࠧ໺"))), result=bstack11ll1l1lll_opy_)
                bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(bstack1ll1ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ໻"), self._11l11ll111_opy_[bstack11ll111l1l_opy_][bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໼")])
        else:
            bstack11l1ll1l11_opy_ = current_test_id if current_test_id else bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪ໽"), None)
            if bstack11l1ll1l11_opy_ and len(self.bstack11l1l111l1_opy_) == 1:
                current_step_uuid = bstack1l1lll11_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭໾"), None)
                self._11l11ll111_opy_[bstack11l1ll1l11_opy_][bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໿")].bstack11ll1lll11_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1ll_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩༀ"), bstack1ll1ll_opy_ (u"ࠬ࠶ࠧ༁"))), result=bstack11ll1l1lll_opy_)
            else:
                self.bstack11l11lll11_opy_(attrs)
            self.bstack11l1l111l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1ll_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ༂"), bstack1ll1ll_opy_ (u"ࠧ࡯ࡱࠪ༃")) == bstack1ll1ll_opy_ (u"ࠨࡻࡨࡷࠬ༄"):
                return
            self.messages.push(message)
            bstack11l1l1ll11_opy_ = []
            if bstack1111llll_opy_.bstack11ll111l11_opy_():
                bstack11l1l1ll11_opy_.append({
                    bstack1ll1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༅"): bstack1l1l11l11l_opy_(),
                    bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༆"): message.get(bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༇")),
                    bstack1ll1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༈"): message.get(bstack1ll1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༉")),
                    **bstack1111llll_opy_.bstack11ll111l11_opy_()
                })
                if len(bstack11l1l1ll11_opy_) > 0:
                    bstack1llll1ll_opy_.bstack1lll11l1l1_opy_(bstack11l1l1ll11_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1llll1ll_opy_.bstack11l1l1l111_opy_()
    def bstack11l11lll11_opy_(self, bstack11l11l1lll_opy_):
        if not bstack1111llll_opy_.bstack11ll111l11_opy_():
            return
        kwname = bstack1ll1ll_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭༊").format(bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ་")), bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ༌"), bstack1ll1ll_opy_ (u"ࠪࠫ།"))) if bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ༎"), []) else bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ༏"))
        error_message = bstack1ll1ll_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧ༐").format(kwname, bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ༑")), str(bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༒"))))
        bstack11l11ll1l1_opy_ = bstack1ll1ll_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣ༓").format(kwname, bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༔")))
        bstack11l1l1llll_opy_ = error_message if bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༕")) else bstack11l11ll1l1_opy_
        bstack11l11l1l11_opy_ = {
            bstack1ll1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༖"): self.bstack11l1l111l1_opy_[-1].get(bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ༗"), bstack1l1l11l11l_opy_()),
            bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༘"): bstack11l1l1llll_opy_,
            bstack1ll1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲ༙ࠧ"): bstack1ll1ll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ༚") if bstack11l11l1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༛")) == bstack1ll1ll_opy_ (u"ࠫࡋࡇࡉࡍࠩ༜") else bstack1ll1ll_opy_ (u"ࠬࡏࡎࡇࡑࠪ༝"),
            **bstack1111llll_opy_.bstack11ll111l11_opy_()
        }
        bstack1llll1ll_opy_.bstack1lll11l1l1_opy_([bstack11l11l1l11_opy_])
    def _11l11ll11l_opy_(self):
        for bstack11l1ll1lll_opy_ in reversed(self._11l11ll111_opy_):
            bstack11l1l111ll_opy_ = bstack11l1ll1lll_opy_
            data = self._11l11ll111_opy_[bstack11l1ll1lll_opy_][bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༞")]
            if isinstance(data, bstack11ll11ll1l_opy_):
                if not bstack1ll1ll_opy_ (u"ࠧࡆࡃࡆࡌࠬ༟") in data.bstack11l1l1ll1l_opy_():
                    return bstack11l1l111ll_opy_
            else:
                return bstack11l1l111ll_opy_
    def _11l1ll111l_opy_(self, messages):
        try:
            bstack11l11lllll_opy_ = BuiltIn().get_variable_value(bstack1ll1ll_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ༠")) in (bstack11l1lll111_opy_.DEBUG, bstack11l1lll111_opy_.TRACE)
            for message, bstack11l1ll11ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༡"))
                level = message.get(bstack1ll1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ༢"))
                if level == bstack11l1lll111_opy_.FAIL:
                    self._11l1l1l11l_opy_ = name or self._11l1l1l11l_opy_
                    self._11l1l11ll1_opy_ = bstack11l1ll11ll_opy_.get(bstack1ll1ll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ༣")) if bstack11l11lllll_opy_ and bstack11l1ll11ll_opy_ else self._11l1l11ll1_opy_
        except:
            pass
    @classmethod
    def bstack11ll1l1ll1_opy_(self, event: str, bstack11l1l11111_opy_: bstack11l11lll1l_opy_, bstack11l11l11l1_opy_=False):
        if event == bstack1ll1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ༤"):
            bstack11l1l11111_opy_.set(hooks=self.store[bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ༥")])
        if event == bstack1ll1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ༦"):
            event = bstack1ll1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ༧")
        if bstack11l11l11l1_opy_:
            bstack11l1lll1l1_opy_ = {
                bstack1ll1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭༨"): event,
                bstack11l1l11111_opy_.bstack11l1l1l1ll_opy_(): bstack11l1l11111_opy_.bstack11l1lll1ll_opy_(event)
            }
            self.bstack11l11l1l1l_opy_.append(bstack11l1lll1l1_opy_)
        else:
            bstack1llll1ll_opy_.bstack11ll1l1ll1_opy_(event, bstack11l1l11111_opy_)
class Messages:
    def __init__(self):
        self._11ll1111l1_opy_ = []
    def bstack11l11l1ll1_opy_(self):
        self._11ll1111l1_opy_.append([])
    def bstack11l1llll11_opy_(self):
        return self._11ll1111l1_opy_.pop() if self._11ll1111l1_opy_ else list()
    def push(self, message):
        self._11ll1111l1_opy_[-1].append(message) if self._11ll1111l1_opy_ else self._11ll1111l1_opy_.append([message])
class bstack11l1lll111_opy_:
    FAIL = bstack1ll1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨ༩")
    ERROR = bstack1ll1ll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ༪")
    WARNING = bstack1ll1ll_opy_ (u"ࠬ࡝ࡁࡓࡐࠪ༫")
    bstack11l1l1lll1_opy_ = bstack1ll1ll_opy_ (u"࠭ࡉࡏࡈࡒࠫ༬")
    DEBUG = bstack1ll1ll_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭༭")
    TRACE = bstack1ll1ll_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ༮")
    bstack11ll11111l_opy_ = [FAIL, ERROR]
def bstack11l1l11lll_opy_(bstack11l1ll1ll1_opy_):
    if not bstack11l1ll1ll1_opy_:
        return None
    if bstack11l1ll1ll1_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༯"), None):
        return getattr(bstack11l1ll1ll1_opy_[bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༰")], bstack1ll1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ༱"), None)
    return bstack11l1ll1ll1_opy_.get(bstack1ll1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪ༲"), None)
def bstack11l1l1111l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ༳"), bstack1ll1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ༴")]:
        return
    if hook_type.lower() == bstack1ll1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ༵ࠧ"):
        if current_test_uuid is None:
            return bstack1ll1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭༶")
        else:
            return bstack1ll1ll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ༷")
    elif hook_type.lower() == bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭༸"):
        if current_test_uuid is None:
            return bstack1ll1ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ༹")
        else:
            return bstack1ll1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ༺")