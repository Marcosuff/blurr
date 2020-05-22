# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01e_data-summarization.ipynb (unless otherwise specified).

__all__ = ['HF_SummaryInput']

# Cell
import ast
from functools import reduce

import torch
from transformers import *
from fastai2.text.all import *

from ..utils import *
from .core import *

# Cell
class HF_SummaryInput(list): pass

# Cell
@typedispatch
def build_hf_input(task:ForConditionalGenerationTask, tokenizer, a_tok_ids, b_tok_ids=None, targets=None,
                   max_length=512, pad_to_max_length=True, truncation_strategy='longest_first',
                   trg_tok_kwargs={}):

    base_res = build_hf_input(None, tokenizer, a_tok_ids, b_tok_ids, targets,
                              max_length, pad_to_max_length, truncation_strategy, {})

    max_length = trg_tok_kwargs['max_length'] if ('max_length' in trg_tok_kwargs) else max_length
    ts = trg_tok_kwargs['truncation_strategy'] if ('truncation_strategy' in trg_tok_kwargs) else truncation_strategy

    dec_res = tokenizer.prepare_for_model(base_res[1][0].tolist(), None,
                                      max_length=max_length,
                                      pad_to_max_length=pad_to_max_length,
                                      truncation_strategy=ts,
                                      return_tensors='pt')

    return HF_SummaryInput(base_res[0]), tuplify(dec_res['input_ids'][0])

# Cell
@typedispatch
def show_batch(x:HF_SummaryInput, y, samples, hf_tokenizer, skip_special_tokens=True, ctxs=None, max_n=6, **kwargs):
    res = L()
    for inp, trg in zip(x[0], y):
        txt = hf_tokenizer.decode(inp, skip_special_tokens=skip_special_tokens).replace(hf_tokenizer.pad_token, '')
        s = hf_tokenizer.decode(trg, skip_special_tokens=skip_special_tokens).replace(hf_tokenizer.pad_token, '')
        res.append((txt, s))

    display_df(pd.DataFrame(res, columns=['text', 'summary'])[:max_n])
    return ctxs