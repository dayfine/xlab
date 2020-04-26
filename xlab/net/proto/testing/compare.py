from google.protobuf import text_format


def assertProtoEqual(self, a, b, msg=None):
    """Fails with a useful error if a and b aren't equal.
    Comparison of repeated fields matches the semantics of
    unittest.TestCase.assertEqual(), ie order and extra duplicates fields matter.
    Either A or B can be a text proto.
    Args:
        self: absl.TestCase
        a: proto2 PB instance, or text string representing one
        b: proto2 PB instance, or text string representing one
        msg: if specified, is used as the error message on failure
    """
    if isinstance(a, str):
        a = text_format.Merge(a, b.__class__())

    if isinstance(b, str):
        b = text_format.Merge(b, a.__class__())

    self.assertMultiLineEqual(text_format.MessageToString(a),
                              text_format.MessageToString(b),
                              msg=msg)
