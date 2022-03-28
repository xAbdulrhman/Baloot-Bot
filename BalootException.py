class BalootException(Exception):
    pass

    def _CheckParameterType(Parameter=None, Type=None, ParameterName=None):
        if not isinstance(Parameter, int):
            raise BalootException('{} parameter is expected to be of type int. {} = {}, type({}) = {}'.format(
                ParameterName, ParameterName, Parameter, ParameterName, type(Parameter)))

