from absl.testing import absltest

from xlab.data.proto import data_type_pb2
from xlab.data.calc import registry
from xlab.data.store import in_memory
from xlab.util.status import errors


class CalcProducerRegistryTest(absltest.TestCase):

    def test_raise_for_unsupported_calc_type(self):
        with self.assertRaisesRegex(errors.NotFoundError,
                                    'No available calc factory'):
            registry.get_producer_factory(
                data_type_pb2.DataType.DATA_TYPE_UNSPECIFIED)

    def test_factories_are_for_the_right_type(self):
        for calc_type in registry.available_calc_types():
            calc_producer = registry.get_producer_factory(calc_type)(
                in_memory.InMemoryDataStore())
            self.assertEqual(calc_type, calc_producer.calc_type)


if __name__ == '__main__':
    absltest.main()
