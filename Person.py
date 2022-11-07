class Person:
    """
    This class is used to represent a person
    :ivar _name: The name of the person
    :ivar _weight: The Weight of the person (in pounds)
    :ivar _savings: The person's savings
    :ivar _pay_rate: The rate the person is paid per hour
    """

    def __init__(self, person_name: str):
        """
        This function constructs the person with default values
        :param person_name: The name of the person
        :type person_name: str
        """
        self._name = person_name
        self._weight: float = 8
        self._savings: float = 100
        self._pay_rate: float = 9.25

    def eat(self, pounds: float) -> None:
        """
        This function makes a person eat the specified amount of pounds of food
        :param pounds: The pounds the person is eating
        :type pounds: float
        """
        self._weight += pounds

    def calculate_paycheck(self, hours: int) -> float:
        """
        Calculates the person's paycheck given the amount of hours they've worked
        :param hours: The hours the person has worked
        :type hours: int
        :returns: The paycheck of the person
        :rtype: float
        """
        pay = self._pay_rate * hours
        self._savings += pay
        return pay

    def exercise(self, time_spent: int) -> None:
        """
        Makes the person exercise for a specific amount of time
        :param time_spent: the time spent in minutes exercising
        :type time_spent: int
        """
        self._weight -= time_spent // 20

    def promotion(self, increase_amount: float) -> None:
        """
        Raises the pay rate of the user by the specified amount
        :param increase_amount: The amount to increase the pay rate by
        :type increase_amount: float
        """
        self._pay_rate += increase_amount

    def get_weight(self) -> float:
        """
        Gets the weight of the person
        :returns: The weight of the person
        :rtype: float
        """
        return self._weight

    def get_savings(self) -> float:
        """
        Gets the saving of the person
        :returns: The savings of the person
        :rtype: float
        """
        return self._savings

    def get_pay_rate(self) -> float:
        """
        Gets the pay rate of the person
        :returns: The pay rate of the person
        :rtype: float
        """
        return self._pay_rate

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        """
        Returns an string representation of this object
        :returns: A str used to reproduce the object
        :rtype: str
        """
        return f"Person(Name={self._name}, Weight={self._weight}, Savings={self._savings}, PayRate={self._pay_rate})"


class InsuredPerson(Person):
    """
    This class represents an insured person
    :cvar InsuranceRates: Stores the rates for each insurance type
    :type InsuranceRates: dict[str, float]
    :ivar _insurance_status: Stores whether the person is opted in to each insurance
    :type _insurance_status: dict[str, bool]
    """
    InsuranceRates = {
        'vision': 2.43,
        'dental': 3.50,
        'medical': 43.00
    }

    def __init__(self, person_name: str):
        """
        Constructs a new InsuredPerson instance
        By default, the person is opted out of all insurance types
        :param person_name: The name of the person
        :type person_name: str
        """
        super(InsuredPerson, self).__init__(person_name)
        self._insurance_status = {key: False for key in self.InsuranceRates.keys()}

    def __repr__(self):
        """
        Returns a string representation of this object
        :returns: A str used to reproduce the object
        :rtype: str
        """
        base_string = super(InsuredPerson, self).__repr__()
        new_string = base_string[:-1] + f", Insurances={self._insurance_status})"
        new_string = new_string.replace("Person", "InsuredPerson", 1)
        return new_string

    def edit_insurance_status(self, insurance_name: str, is_opted_in: bool) -> None:
        """
        Opts a person in or out of the specified insurance
        :param insurance_name: The name of the insurance to edit
        :type insurance_name: str
        :param is_opted_in: Whether the person is opted in
        :type is_opted_in: bool
        """
        self._insurance_status[insurance_name] = is_opted_in

    def get_total_deducted_from_paycheck(self) -> float:
        """
        Gets the total amount of money to deduct from the paycheck
        :returns: Total amount of money to deduct from the paycheck
        :rtype: float
        """
        return sum(
            [self.InsuranceRates[key] for key in self._insurance_status.keys() if
             self._insurance_status[key] is True])

    def calculate_paycheck(self, hours: int) -> float:
        """
        Calculates the person's paycheck
        :param hours: The hours worked
        :type hours: int
        :returns: The person's paycheck for the number of hours entered
        :rtype: float
        """
        return super(InsuredPerson, self).calculate_paycheck(hours) - self.get_total_deducted_from_paycheck()
