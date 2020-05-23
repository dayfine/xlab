from absl.testing import absltest

from xlab.data.calc.producers import factories
from xlab.data.proto import data_type_pb2
from xlab.data.calc import registry
from xlab.util.status import errors


class CalcProducerRegistryTest(absltest.TestCase):

    def test_raise_for_unsupported_calc_type(self):
        with self.assertRaisesRegex(errors.NotFoundError,
                                    'No available calc factory'):
            registry.get_calc_producer(
                data_type_pb2.DataType.DATA_TYPE_UNSPECIFIED)

    def test_factories_are_for_the_right_type(self):
        for calc_type in factories._FACTORIES.keys():
            calc_producer = registry.get_calc_producer(calc_type)
            self.assertEqual(calc_type, calc_producer.calc_type)


if __name__ == '__main__':
    absltest.main()
