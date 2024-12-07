from typing import Optional
import torch


# page attention ops
def paged_attention_v1(
    out: torch.Tensor,
    query: torch.Tensor,
    key_cache: torch.Tensor,
    value_cache: torch.Tensor,
    head_mapping: torch.Tensor,
    scale: float,
    block_tables: torch.Tensor,
    seq_lens: torch.Tensor,
    block_size: int,
    max_seq_len: int,
    alibi_slopes: Optional[torch.Tensor],
    kv_cache_dtype: str,
    kv_scale: float,
) -> None:
    torch.ops._attention_kernels.paged_attention_v1(
        out,
        query,
        key_cache,
        value_cache,
        head_mapping,
        scale,
        block_tables,
        seq_lens,
        block_size,
        max_seq_len,
        alibi_slopes,
        kv_cache_dtype,
        kv_scale,
    )


def paged_attention_v2(
    out: torch.Tensor,
    exp_sum: torch.Tensor,
    max_logits: torch.Tensor,
    tmp_out: torch.Tensor,
    query: torch.Tensor,
    key_cache: torch.Tensor,
    value_cache: torch.Tensor,
    head_mapping: torch.Tensor,
    scale: float,
    block_tables: torch.Tensor,
    seq_lens: torch.Tensor,
    block_size: int,
    max_seq_len: int,
    alibi_slopes: Optional[torch.Tensor],
    kv_cache_dtype: str,
    kv_scale: float,
) -> None:
    torch.ops._attention_kernels.paged_attention_v2(
        out,
        exp_sum,
        max_logits,
        tmp_out,
        query,
        key_cache,
        value_cache,
        head_mapping,
        scale,
        block_tables,
        seq_lens,
        block_size,
        max_seq_len,
        alibi_slopes,
        kv_cache_dtype,
        kv_scale,
    )


def reshape_and_cache(
    key: torch.Tensor,
    value: torch.Tensor,
    key_cache: torch.Tensor,
    value_cache: torch.Tensor,
    slot_mapping: torch.Tensor,
    kv_cache_dtype: str,
    kv_scale: float,
) -> None:
    torch.ops._attention_kernels.reshape_and_cache(
        key,
        value,
        key_cache,
        value_cache,
        slot_mapping,
        kv_cache_dtype,
        kv_scale,
    )


__all__ = ["paged_attention_v1", "paged_attention_v2", "reshape_and_cache"]
