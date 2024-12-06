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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11111111ll_opy_
from browserstack_sdk.bstack111l11l11_opy_ import bstack11lllll1_opy_
def _1lllll11lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1llll1ll1l1_opy_:
    def __init__(self, handler):
        self._1lllll111ll_opy_ = {}
        self._1lllll11l1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11lllll1_opy_.version()
        if bstack11111111ll_opy_(pytest_version, bstack1ll1ll_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᓥ")) >= 0:
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓦ")] = Module._register_setup_function_fixture
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓧ")] = Module._register_setup_module_fixture
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓨ")] = Class._register_setup_class_fixture
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᓩ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓪ"))
            Module._register_setup_module_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓫ"))
            Class._register_setup_class_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓬ"))
            Class._register_setup_method_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓭ"))
        else:
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᓮ")] = Module._inject_setup_function_fixture
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓯ")] = Module._inject_setup_module_fixture
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓰ")] = Class._inject_setup_class_fixture
            self._1lllll111ll_opy_[bstack1ll1ll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᓱ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓲ"))
            Module._inject_setup_module_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓳ"))
            Class._inject_setup_class_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓴ"))
            Class._inject_setup_method_fixture = self.bstack1llll1lllll_opy_(bstack1ll1ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓵ"))
    def bstack1lllll1l111_opy_(self, bstack1lllll11ll1_opy_, hook_type):
        bstack1lllll1111l_opy_ = id(bstack1lllll11ll1_opy_.__class__)
        if (bstack1lllll1111l_opy_, hook_type) in self._1lllll11l1l_opy_:
            return
        meth = getattr(bstack1lllll11ll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lllll11l1l_opy_[(bstack1lllll1111l_opy_, hook_type)] = meth
            setattr(bstack1lllll11ll1_opy_, hook_type, self.bstack1llll1lll11_opy_(hook_type, bstack1lllll1111l_opy_))
    def bstack1llll1ll1ll_opy_(self, instance, bstack1lllll1l11l_opy_):
        if bstack1lllll1l11l_opy_ == bstack1ll1ll_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᓶ"):
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᓷ"))
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᓸ"))
        if bstack1lllll1l11l_opy_ == bstack1ll1ll_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᓹ"):
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᓺ"))
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᓻ"))
        if bstack1lllll1l11l_opy_ == bstack1ll1ll_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᓼ"):
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᓽ"))
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᓾ"))
        if bstack1lllll1l11l_opy_ == bstack1ll1ll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᓿ"):
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᔀ"))
            self.bstack1lllll1l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᔁ"))
    @staticmethod
    def bstack1llll1ll11l_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᔂ"), bstack1ll1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᔃ")]:
            _1lllll11lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1llll1lll11_opy_(self, hook_type, bstack1lllll1111l_opy_):
        def bstack1lllll111l1_opy_(arg=None):
            self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᔄ"))
            result = None
            try:
                bstack1lllll11111_opy_ = self._1lllll11l1l_opy_[(bstack1lllll1111l_opy_, hook_type)]
                self.bstack1llll1ll11l_opy_(hook_type, bstack1lllll11111_opy_, (arg,))
                result = Result(result=bstack1ll1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᔅ"))
            except Exception as e:
                result = Result(result=bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᔆ"), exception=e)
                self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᔇ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᔈ"), result)
        def bstack1lllll11l11_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᔉ"))
            result = None
            exception = None
            try:
                self.bstack1llll1ll11l_opy_(hook_type, self._1lllll11l1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᔊ"))
            except Exception as e:
                result = Result(result=bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᔋ"), exception=e)
                self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᔌ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᔍ"), result)
        if hook_type in [bstack1ll1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᔎ"), bstack1ll1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᔏ")]:
            return bstack1lllll11l11_opy_
        return bstack1lllll111l1_opy_
    def bstack1llll1lllll_opy_(self, bstack1lllll1l11l_opy_):
        def bstack1llll1lll1l_opy_(this, *args, **kwargs):
            self.bstack1llll1ll1ll_opy_(this, bstack1lllll1l11l_opy_)
            self._1lllll111ll_opy_[bstack1lllll1l11l_opy_](this, *args, **kwargs)
        return bstack1llll1lll1l_opy_