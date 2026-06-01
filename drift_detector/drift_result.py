class DriftResult:

    def __init__(
        self,
        resource,
        attribute,
        expected,
        actual,
        risk,
        status
    ):
        self.resource = resource
        self.attribute = attribute
        self.expected = expected
        self.actual = actual
        self.risk = risk
        self.status = status

    def to_dict(self):
        return {
            "resource": self.resource,
            "attribute": self.attribute,
            "expected": self.expected,
            "actual": self.actual,
            "risk": self.risk,
            "status": self.status
        }
