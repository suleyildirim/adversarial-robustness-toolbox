# MIT License
#
# Copyright (C) The Adversarial Robustness Toolbox (ART) Authors 2020
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging

import numpy as np
import pytest

from art.attacks.evasion import BrendelBethgeAttack
from art.estimators.estimator import BaseEstimator, LossGradientsMixin
from art.estimators.classification.classifier import ClassifierMixin

from tests.attacks.utils import backend_test_classifier_type_check_fail
from tests.utils import ARTTestException

logger = logging.getLogger(__name__)


@pytest.mark.skipMlFramework("keras", "mxnet", "non_dl_frameworks")
@pytest.mark.parametrize("targeted", [True, False])
@pytest.mark.parametrize("norm", [1, 2, np.inf, "inf"])
def test_generate(
    art_warning, get_default_mnist_subset, image_dl_estimator_for_attack, is_tf_version_2, targeted, norm
):
    try:

        if not is_tf_version_2:
            logging.warning("Couldn't perform this test because it only supports TensorFlow v2.")
            return

        (x_train_mnist, y_train_mnist), (x_test_mnist, y_test_mnist) = get_default_mnist_subset
        classifier = image_dl_estimator_for_attack(BrendelBethgeAttack, defended=False, from_logits=True)

        attack = BrendelBethgeAttack(
            estimator=classifier,
            norm=norm,
            targeted=targeted,
            overshoot=1.1,
            steps=1,
            lr=1e-3,
            lr_decay=0.5,
            lr_num_decay=20,
            momentum=0.8,
            binary_search_steps=1,
            init_size=5,
            batch_size=32,
        )

        attack.generate(x=x_test_mnist[0:1].astype(np.float32), y=y_test_mnist[0:1].astype(np.int32))

    except ARTTestException as e:
        art_warning(e)


def test_classifier_type_check_fail():
    backend_test_classifier_type_check_fail(BrendelBethgeAttack, [BaseEstimator, LossGradientsMixin, ClassifierMixin])
