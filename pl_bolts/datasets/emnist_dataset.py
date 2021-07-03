from pl_bolts.utils import _PIL_AVAILABLE, _TORCHVISION_AVAILABLE, _TORCHVISION_LESS_THAN_0_9_1
from pl_bolts.utils.warnings import warn_missing_pkg

if _TORCHVISION_AVAILABLE:
    from torchvision.datasets import EMNIST
else:  # pragma: no cover
    warn_missing_pkg('torchvision')
    EMNIST = object

if _PIL_AVAILABLE:
    from PIL import Image
else:  # pragma: no cover
    warn_missing_pkg('PIL', pypi_name='Pillow')

_TABLE = """

| Name     | Classes | No. Training | No. Testing | Validation | Total   |
|----------|---------|--------------|-------------|------------|---------|
| By_Class | 62      | 697,932      | 116,323     | No         | 814,255 |
| By_Merge | 47      | 697,932      | 116,323     | No         | 814,255 |
| Balanced | 47      | 112,800      | 18,800      | Yes        | 131,600 |
| Digits   | 10      | 240,000      | 40,000      | Yes        | 280,000 |
| Letters  | 37      | 88,800       | 14,800      | Yes        | 103,600 |
| MNIST    | 10      | 60,000       | 10,000      | Yes        | 70,000  |

"""

EMNIST_METADATA = {
    'table': _TABLE,
    'source': 'Table-II in paper: https://arxiv.org/pdf/1702.05373.pdf',
    'splits': {
        'byclass': {
            'name': 'byclass',
            'num_classes': 62,
            'num_train': 697_932,
            'num_test': 116_323,
            'validation': False,
            'num_total': 814_255,
        },
        'bymerge': {
            'name': 'bymerge',
            'num_classes': 47,
            'num_train': 697_932,
            'num_test': 116_323,
            'validation': False,
            'num_total': 814_255,
        },
        'balanced': {
            'name': 'balanced',
            'num_classes': 47,
            'num_train': 112_800,
            'num_test': 18_800,
            'validation': True,
            'num_total': 131_600,
        },
        'digits': {
            'name': 'digits',
            'num_classes': 10,
            'num_train': 240_000,
            'num_test': 40_000,
            'validation': True,
            'num_total': 280_000,
        },
        'letters': {
            'name': 'letters',
            'num_classes': 37,
            'num_train': 88_800,
            'num_test': 14_800,
            'validation': True,
            'num_total': 103_000,
        },
        'mnist': {
            'name': 'mnist',
            'num_classes': 10,
            'num_train': 60_000,
            'num_test': 10_000,
            'validation': True,
            'num_total': 70_000,
        },
    },
}


# TODO(sugatoray): This is needed to avoid 503 error when downloading MNIST dataset
# from http://yann.lecun.com/exdb/mnist/ and can be removed after `torchvision==0.9.1`.
# See https://github.com/pytorch/vision/issues/3549 for details.
if _TORCHVISION_AVAILABLE and _TORCHVISION_LESS_THAN_0_9_1:
    EMNIST.resources = [
        (
            "https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz",
            "f68b3c2dcbeaaa9fbdd348bbdeb94873"
        ),  # noqa: E501
        (
            "https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz",
            "d53e105ee54ea40749a09fcbcd1e9432"
        ),  # noqa: E501
        (
            "https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz",
            "9fb629c4189551a2d022fa330f9573f3"
        ),  # noqa: E501
        (
            "https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz",
            "ec29112dd5afa0611ce80d1b7f02629c"
        )   # noqa: E501
    ]

EMNIST._metadata = EMNIST_METADATA


class BinaryEMNIST(EMNIST):

    def __getitem__(self, idx):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        if not _TORCHVISION_AVAILABLE:  # pragma: no cover
            raise ModuleNotFoundError('You want to use `torchvision` which is not installed yet.')

        img, target = self.data[idx], int(self.targets[idx])

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(img.numpy(), mode='L')

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        # binary
        img[img < 0.5] = 0.0
        img[img >= 0.5] = 1.0

        return img, target
