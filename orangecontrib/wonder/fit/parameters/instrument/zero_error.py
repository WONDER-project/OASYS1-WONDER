from wonder.fit.parameters.fit_parameter import ParametersList


class ZeroError(ParametersList):
    shift = None

    @classmethod
    def get_parameters_prefix(cls):
        return "zero_error_"

    def __init__(self, shift):
        super(ZeroError, self).__init__()

        self.shift = shift
