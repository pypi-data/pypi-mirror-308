#pragma once

#include <torch/library.h>

void paged_attention_v1(
  torch::Tensor& out,
  torch::Tensor& query,
  torch::Tensor& key_cache,
  torch::Tensor& value_cache,
  torch::Tensor& head_mapping,
  double scale,
  torch::Tensor& block_tables,
  torch::Tensor& context_lens,
  int64_t block_size,
  int64_t max_context_len,
  const c10::optional<torch::Tensor>& alibi_slopes,
  const std::string& kv_cache_dtype,
  double kv_scale);

void paged_attention_v2(
  torch::Tensor& out,
  torch::Tensor& exp_sums,
  torch::Tensor& max_logits,
  torch::Tensor& tmp_out,
  torch::Tensor& query,
  torch::Tensor& key_cache,
  torch::Tensor& value_cache,
  torch::Tensor& head_mapping,
  double scale,
  torch::Tensor& block_tables,
  torch::Tensor& context_lens,
  int64_t block_size,
  int64_t max_context_len,
  const c10::optional<torch::Tensor>& alibi_slopes,
  const std::string& kv_cache_dtype,
  double kv_scale);

void reshape_and_cache(
  torch::Tensor& key,
  torch::Tensor& value,
  torch::Tensor& key_cache,
  torch::Tensor& value_cache,
  torch::Tensor& slot_mapping,
  const std::string& kv_cache_dtype,
  const double kv_scale);

