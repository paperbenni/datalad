from unittest.mock import patch

from datalad.runner.protocol import GeneratorMixIn
from datalad.runner.coreprotocols import (
    StdOutErrCapture,
)
from datalad.tests.utils import assert_equal

from ..gitrunner import GitWitlessRunner


class TestGeneratorProtocol(GeneratorMixIn, StdOutErrCapture):
    pass


def test_gitrunner_generator():
    # Expect GitRunner._get_chunked_results() to return generators,
    # if the protocol is a subclass of GeneratorMixIn, and expect
    # run_on_filelist_chunks_items_ to yield elements from
    # all generators returned by GitRunner._get_chunked_results().
    git_runner = GitWitlessRunner(["a", "b", "c"])
    generator = git_runner.run_on_filelist_chunks_items_(
        ["a", "b", "c"],
        ["f1.txt", "f2.txt"],
        TestGeneratorProtocol)
    with patch.object(git_runner, "_get_chunked_results") as get_mock:
        get_mock.return_value = (range(2), range(3))
        assert_equal(tuple(generator), (0, 1, 0, 1, 2))
