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
from uuid import uuid4
from bstack_utils.helper import bstack1l1l11l11l_opy_, bstack111111l111_opy_
from bstack_utils.bstack11lll1l1l1_opy_ import bstack1ll1lll1l11_opy_
class bstack11l11lll1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11ll11lll1_opy_=None, framework=None, tags=[], scope=[], bstack1ll1l11lll1_opy_=None, bstack1ll1l1l1111_opy_=True, bstack1ll1l1l1l1l_opy_=None, bstack1111l11l1_opy_=None, result=None, duration=None, bstack11l1ll1lll_opy_=None, meta={}):
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1l1l1111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11ll11lll1_opy_ = bstack11ll11lll1_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1l11lll1_opy_ = bstack1ll1l11lll1_opy_
        self.bstack1ll1l1l1l1l_opy_ = bstack1ll1l1l1l1l_opy_
        self.bstack1111l11l1_opy_ = bstack1111l11l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l11ll1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11ll11l111_opy_(self, meta):
        self.meta = meta
    def bstack11ll1ll1l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1l11llll_opy_(self):
        bstack1ll1l1l1lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᚂ"): bstack1ll1l1l1lll_opy_,
            bstack1ll1ll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᚃ"): bstack1ll1l1l1lll_opy_,
            bstack1ll1ll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᚄ"): bstack1ll1l1l1lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1ll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧᚅ") + key)
            setattr(self, key, val)
    def bstack1ll1l11l1ll_opy_(self):
        return {
            bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᚆ"): self.name,
            bstack1ll1ll_opy_ (u"࠭ࡢࡰࡦࡼࠫᚇ"): {
                bstack1ll1ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᚈ"): bstack1ll1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᚉ"),
                bstack1ll1ll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᚊ"): self.code
            },
            bstack1ll1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᚋ"): self.scope,
            bstack1ll1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩᚌ"): self.tags,
            bstack1ll1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᚍ"): self.framework,
            bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᚎ"): self.bstack11ll11lll1_opy_
        }
    def bstack1ll1l11ll1l_opy_(self):
        return {
         bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᚏ"): self.meta
        }
    def bstack1ll1l1l11ll_opy_(self):
        return {
            bstack1ll1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᚐ"): {
                bstack1ll1ll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᚑ"): self.bstack1ll1l11lll1_opy_
            }
        }
    def bstack1ll1l1l1ll1_opy_(self, bstack1ll1l1l1l11_opy_, details):
        step = next(filter(lambda st: st[bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࠭ᚒ")] == bstack1ll1l1l1l11_opy_, self.meta[bstack1ll1ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚓ")]), None)
        step.update(details)
    def bstack111ll11l1_opy_(self, bstack1ll1l1l1l11_opy_):
        step = next(filter(lambda st: st[bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨᚔ")] == bstack1ll1l1l1l11_opy_, self.meta[bstack1ll1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚕ")]), None)
        step.update({
            bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚖ"): bstack1l1l11l11l_opy_()
        })
    def bstack11ll1lll11_opy_(self, bstack1ll1l1l1l11_opy_, result, duration=None):
        bstack1ll1l1l1l1l_opy_ = bstack1l1l11l11l_opy_()
        if bstack1ll1l1l1l11_opy_ is not None and self.meta.get(bstack1ll1ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚗ")):
            step = next(filter(lambda st: st[bstack1ll1ll_opy_ (u"ࠩ࡬ࡨࠬᚘ")] == bstack1ll1l1l1l11_opy_, self.meta[bstack1ll1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᚙ")]), None)
            step.update({
                bstack1ll1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᚚ"): bstack1ll1l1l1l1l_opy_,
                bstack1ll1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ᚛"): duration if duration else bstack111111l111_opy_(step[bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᚜")], bstack1ll1l1l1l1l_opy_),
                bstack1ll1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᚝"): result.result,
                bstack1ll1ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᚞"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1l1l111l_opy_):
        if self.meta.get(bstack1ll1ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᚟")):
            self.meta[bstack1ll1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᚠ")].append(bstack1ll1l1l111l_opy_)
        else:
            self.meta[bstack1ll1ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚡ")] = [ bstack1ll1l1l111l_opy_ ]
    def bstack1ll1l111lll_opy_(self):
        return {
            bstack1ll1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᚢ"): self.bstack11l11ll1ll_opy_(),
            **self.bstack1ll1l11l1ll_opy_(),
            **self.bstack1ll1l11llll_opy_(),
            **self.bstack1ll1l11ll1l_opy_()
        }
    def bstack1ll1l1ll111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚣ"): self.bstack1ll1l1l1l1l_opy_,
            bstack1ll1ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᚤ"): self.duration,
            bstack1ll1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᚥ"): self.result.result
        }
        if data[bstack1ll1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᚦ")] == bstack1ll1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᚧ"):
            data[bstack1ll1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᚨ")] = self.result.bstack111llllll1_opy_()
            data[bstack1ll1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᚩ")] = [{bstack1ll1ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᚪ"): self.result.bstack1111ll1lll_opy_()}]
        return data
    def bstack1ll1l11l1l1_opy_(self):
        return {
            bstack1ll1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚫ"): self.bstack11l11ll1ll_opy_(),
            **self.bstack1ll1l11l1ll_opy_(),
            **self.bstack1ll1l11llll_opy_(),
            **self.bstack1ll1l1ll111_opy_(),
            **self.bstack1ll1l11ll1l_opy_()
        }
    def bstack11l1lll1ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1ll_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᚬ") in event:
            return self.bstack1ll1l111lll_opy_()
        elif bstack1ll1ll_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚭ") in event:
            return self.bstack1ll1l11l1l1_opy_()
    def bstack11l1l1l1ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1l1l1l1l_opy_ = time if time else bstack1l1l11l11l_opy_()
        self.duration = duration if duration else bstack111111l111_opy_(self.bstack11ll11lll1_opy_, self.bstack1ll1l1l1l1l_opy_)
        if result:
            self.result = result
class bstack11ll1ll1ll_opy_(bstack11l11lll1l_opy_):
    def __init__(self, hooks=[], bstack11ll1111ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll1111ll_opy_ = bstack11ll1111ll_opy_
        super().__init__(*args, **kwargs, bstack1111l11l1_opy_=bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࠨᚮ"))
    @classmethod
    def bstack1ll1l11l111_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧᚯ"): id(step),
                bstack1ll1ll_opy_ (u"ࠬࡺࡥࡹࡶࠪᚰ"): step.name,
                bstack1ll1ll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᚱ"): step.keyword,
            })
        return bstack11ll1ll1ll_opy_(
            **kwargs,
            meta={
                bstack1ll1ll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᚲ"): {
                    bstack1ll1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚳ"): feature.name,
                    bstack1ll1ll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᚴ"): feature.filename,
                    bstack1ll1ll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᚵ"): feature.description
                },
                bstack1ll1ll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᚶ"): {
                    bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᚷ"): scenario.name
                },
                bstack1ll1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚸ"): steps,
                bstack1ll1ll_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᚹ"): bstack1ll1lll1l11_opy_(test)
            }
        )
    def bstack1ll1l1l11l1_opy_(self):
        return {
            bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚺ"): self.hooks
        }
    def bstack1ll1l11ll11_opy_(self):
        if self.bstack11ll1111ll_opy_:
            return {
                bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᚻ"): self.bstack11ll1111ll_opy_
            }
        return {}
    def bstack1ll1l11l1l1_opy_(self):
        return {
            **super().bstack1ll1l11l1l1_opy_(),
            **self.bstack1ll1l1l11l1_opy_()
        }
    def bstack1ll1l111lll_opy_(self):
        return {
            **super().bstack1ll1l111lll_opy_(),
            **self.bstack1ll1l11ll11_opy_()
        }
    def bstack11l1l1l1ll_opy_(self):
        return bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᚼ")
class bstack11ll11ll1l_opy_(bstack11l11lll1l_opy_):
    def __init__(self, hook_type, *args,bstack11ll1111ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1l1ll11l_opy_ = None
        self.bstack11ll1111ll_opy_ = bstack11ll1111ll_opy_
        super().__init__(*args, **kwargs, bstack1111l11l1_opy_=bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᚽ"))
    def bstack11l1l1ll1l_opy_(self):
        return self.hook_type
    def bstack1ll1l11l11l_opy_(self):
        return {
            bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᚾ"): self.hook_type
        }
    def bstack1ll1l11l1l1_opy_(self):
        return {
            **super().bstack1ll1l11l1l1_opy_(),
            **self.bstack1ll1l11l11l_opy_()
        }
    def bstack1ll1l111lll_opy_(self):
        return {
            **super().bstack1ll1l111lll_opy_(),
            bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᚿ"): self.bstack1ll1l1ll11l_opy_,
            **self.bstack1ll1l11l11l_opy_()
        }
    def bstack11l1l1l1ll_opy_(self):
        return bstack1ll1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᛀ")
    def bstack11ll11ll11_opy_(self, bstack1ll1l1ll11l_opy_):
        self.bstack1ll1l1ll11l_opy_ = bstack1ll1l1ll11l_opy_