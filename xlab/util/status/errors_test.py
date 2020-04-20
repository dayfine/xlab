from absl.testing import absltest

from xlab.util.status import errors, error_codes_pb2


class ErrorsTest(absltest.TestCase):
    def test_cancelled_error(self):
        with self.assertRaisesWithPredicateMatch(
                errors.GenericError,
                lambda e: e.code == error_codes_pb2.CANCELLED):
            raise errors.CancelledError('The call is cancelled')


if __name__ == '__main__':
    absltest.main()
