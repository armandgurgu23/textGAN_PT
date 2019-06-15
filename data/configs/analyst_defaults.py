from yacs.config import CfgNode as CN

_C = CN()
_C.dataset = CN()
_C.dataset.path = ''


def get_analyst_defaults():
    return _C.clone()
