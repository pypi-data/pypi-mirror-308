# coding=utf-8
# Copyright 2024 Jaxpruner Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the Sparsity updater classes in base_updater.py."""

import functools
from unittest import mock

import chex
import jax.numpy as jnp
from absl.testing import absltest, parameterized

from fjformer.jaxpruner import (
	base_updater,
	sparsity_distributions,
	sparsity_schedules,
	sparsity_types,
)


class BaseUpdaterTest(parameterized.TestCase, absltest.TestCase):
	def setUp(self):
		super(BaseUpdaterTest, self).setUp()
		self.updater = base_updater.BaseUpdater(
			scheduler=sparsity_schedules.PolynomialSchedule(
				update_freq=2, update_start_step=4, update_end_step=9
			),
			sparsity_distribution_fn=functools.partial(
				sparsity_distributions.uniform, sparsity=0.8
			),
		)

	def testUpdaterInitialized(self):
		self.assertIsInstance(self.updater.sparsity_type, sparsity_types.Unstructured)
		self.assertTrue(callable(self.updater.topk_fn))

	def testOptaxWrapper(self):
		distribution_fn = mock.MagicMock()
		sparse_updater = base_updater.BaseUpdater(
			scheduler=sparsity_schedules.PolynomialSchedule(
				update_freq=1, update_start_step=0, update_end_step=1
			),
			sparsity_distribution_fn=distribution_fn,
		)
		sparse_updater.get_initial_masks = mock.MagicMock()
		sparse_updater.maybe_update_mask = mock.MagicMock()
		sparse_updater.maybe_update_mask.return_value = ({}, {})

		inner = mock.MagicMock()
		inner.update.return_value = ({}, None)

		tx = sparse_updater.wrap_optax(inner)

		_ = tx.init({})
		distribution_fn.assert_called_once()
		sparse_updater.get_initial_masks.assert_called_once()

		sparse_updater.calculate_scores = mock.MagicMock()
		sparse_updater.calculate_scores.return_value = None

		_ = tx.update({}, base_updater.SparseState(masks=None, count=0), {})
		inner.update.assert_called_once()
		sparse_updater.calculate_scores.assert_called_once()

		# Test passing an extra argument to update().
		inner = mock.MagicMock()
		inner.update.return_value = ({}, None)
		sparse_updater.calculate_scores.reset_mock()
		inner.update.assert_not_called()

		tx = sparse_updater.wrap_optax(inner)
		extra_arg = object()
		_ = tx.update({}, base_updater.SparseState(masks=None, count=0), {}, foo=extra_arg)
		inner.update.assert_called_once()
		_, kwargs = inner.update.call_args
		self.assertEmpty(kwargs, "Should not pass extra args to inner")
		sparse_updater.calculate_scores.assert_called_once()
		_, kwargs = sparse_updater.calculate_scores.call_args
		self.assertDictContainsSubset({"foo": extra_arg}, kwargs)

	def testInstantSparsify(self):
		distribution_fn = mock.MagicMock()
		distribution_fn.return_value = {}
		sparse_updater = base_updater.BaseUpdater(
			scheduler=sparsity_schedules.PolynomialSchedule(
				update_freq=1, update_start_step=0, update_end_step=1
			),
			sparsity_distribution_fn=distribution_fn,
		)
		sparse_updater.calculate_scores = mock.MagicMock()
		sparse_updater.calculate_scores.return_value = {}
		sparse_updater.create_masks = mock.MagicMock()
		masks_returned = {"a": jnp.array([1, 0])}
		sparse_updater.create_masks.return_value = masks_returned
		masked_vars, masks = sparse_updater.instant_sparsify({"a": jnp.array([2.0, -3.0])})
		chex.assert_trees_all_close(masks, masks_returned)
		chex.assert_trees_all_close(masked_vars, {"a": jnp.array([2.0, 0.0])})
		distribution_fn.assert_called_once()
		sparse_updater.calculate_scores.assert_called_once()

		# Test passing an extra argument to instant_sparsify().
		sparse_updater.calculate_scores.reset_mock()
		extra_arg = object()
		_ = sparse_updater.instant_sparsify({"a": jnp.array([2.0, -3.0])}, foo=extra_arg)
		sparse_updater.calculate_scores.assert_called_once()
		_, kwargs = sparse_updater.calculate_scores.call_args
		self.assertDictContainsSubset({"foo": extra_arg}, kwargs)

	def testNoPruning(self):
		updater = base_updater.NoPruning()
		param_tree = {"a": 0, "b": {"c": 0, "d": 0}}
		expected = {"a": None, "b": {"c": None, "d": None}}
		self.assertEqual(
			updater.get_initial_masks(param_tree, target_sparsities=None), expected
		)
		chex.assert_trees_all_close(updater.instant_sparsify(param_tree)[0], param_tree)

	def testCustomTopkFn(self):
		def _mock_topk_fn(t, _):
			return jnp.ones_like(t)

		sparse_updater = base_updater.BaseUpdater(
			topk_fn=_mock_topk_fn,
		)
		# Test if custom topk_fn is not overrided.
		self.assertEqual(sparse_updater.topk_fn, _mock_topk_fn)


if __name__ == "__main__":
	absltest.main()
