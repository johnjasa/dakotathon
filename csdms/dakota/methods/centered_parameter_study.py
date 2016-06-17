#! /usr/bin/env python
"""Implementation of a Dakota centered parameter study."""

from .base import MethodsBase


classname = 'CenteredParameterStudy'


class CenteredParameterStudy(MethodsBase):

    """Define parameters for a Dakota centered parameter study."""

    def __init__(self,
                 variables=('x1', 'x2'),
                 initial_point=(0.0, 0.0),
                 steps_per_variable=(5, 4),
                 step_vector=(0.4, 0.5),
                 responses=('y1',),
                 **kwargs):
        """Create a new Dakota centered parameter study.

        Parameters
        ----------
        variables, responses : array_like of str
          Names used for input and output variables.
        initial_point : array_like of float
          Start point (the center) for the parameter study.
        steps_per_variable : array_like of int
          Number of steps to take in each direction.
        steps_vector : array_like of float
          Size of steps in each direction.

        Examples
        --------
        Create a default centered parameter study experiment:

        >>> c = CenteredParameterStudy()

        """
        MethodsBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self.variables = variables
        self._initial_point = initial_point
        self._steps_per_variable = steps_per_variable
        self._step_vector = step_vector
        self.responses = responses

    @property
    def initial_point(self):
        """Start points used by study variables."""
        return self._initial_point

    @initial_point.setter
    def initial_point(self, value):
        """Set start points used by study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The new initial points.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Initial points must be a tuple or a list")
        self._initial_point = value

    @property
    def steps_per_variable(self):
        """Number of steps to take in each direction."""
        return self._steps_per_variable

    @steps_per_variable.setter
    def steps_per_variable(self, value):
        """Set number of steps to take in each direction.

        Parameters
        ----------
        value : list or tuple of int
          The new number of steps.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Steps must be a tuple or a list")
        self._steps_per_variable = value

    @property
    def step_vector(self):
        """Step size in each direction."""
        return self._step_vector

    @step_vector.setter
    def step_vector(self, value):
        """Set step size in each direction.

        Parameters
        ----------
        value : list or tuple of int
          The new step size.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Step size must be a tuple or a list")
        self._step_vector = value

    def method_block(self):
        """Define a centered parameter study method block.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.method_block

        """
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    steps_per_variable ='
        for step in self.steps_per_variable:
            s += ' {}'.format(step)
        s += '\n' \
            + '    step_vector ='
        for step in self.step_vector:
            s += ' {}'.format(step)
        s += '\n\n'
        return(s)

    def variables_block(self):
        """Define a centered parameter study variables block.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.variables_block

        """
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type,
                                     len(self.variables)) \
            + '    initial_point ='
        for pt in self.initial_point:
            s += ' {}'.format(pt)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variables:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
