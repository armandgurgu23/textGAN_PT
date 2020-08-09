from yacs.config import CfgNode as CN

_C = CN()
_C.dataset = CN()
_C.dataset.path = ''
_C.dataset.dataset_name = ''
_C.dataset.cache_tokens = ''
_C.dataset.compute_tokens = True
_C.dataset.processed_dataset = CN()
_C.dataset.processed_dataset.token_threshold = 1
_C.dataset.processed_dataset.generate_processed_dataset = False


def get_analyst_defaults():
    return _C.clone()
