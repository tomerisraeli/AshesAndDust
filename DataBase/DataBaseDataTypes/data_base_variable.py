class DBVariable:
    """
    the data in a NetCDF file is stored in variables. this class represents those
    """

    def __init__(self, name, var_type, dimensions, units, full_name, default=None):
        """
        create a new database var
        :param name: (str) the name of the var
        :param var_type: (np.type) the type of the variable
        :param dimensions: (tuple of str) the dimensions of the variable.
            if there is an unlimited dim it should be first
        :param units: (str) the units of the var
        :param full_name: (str) the full name of the var
        """

        self.name = name
        self.var_type = var_type
        self.dimensions = dimensions
        self.units = units
        self.full_name = full_name
        self.default = default

    @property
    def is_spatial_only(self):
        """
        check if the var is changing over time
        :return:
        """
        return len(self.dimensions) == 2
