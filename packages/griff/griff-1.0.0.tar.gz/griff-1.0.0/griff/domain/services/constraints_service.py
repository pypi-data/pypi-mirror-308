from abc import ABC

from griff.domain.auto_vo.constraints.abstract_constraint import AbstractConstraint
from griff.domain.auto_vo.constraints.required import Required


class ConstraintsService(ABC):
    @classmethod
    @staticmethod
    def sanitize(
        constraints_list: list[AbstractConstraint],
    ) -> list[AbstractConstraint]:
        # for each constraint, remove duplicates
        if constraints_list is None or len(constraints_list) == 0:
            return list()
        santitized = [constraints_list[0]]
        for constraint in constraints_list:
            if type(constraint) in [type(elem) for elem in santitized]:
                continue
            santitized.append(constraint)
        return santitized

    @classmethod
    @staticmethod
    def prioritize(
        constraints_list: list[AbstractConstraint],
    ) -> list[AbstractConstraint]:
        opt_inserted = False
        ordered_constraint_list = list()
        sanitized_constraint_list = ConstraintsService.sanitize(constraints_list)

        # in the case of no constraint, add an Required(False) constraint
        if len(sanitized_constraint_list) == 0:
            ordered_constraint_list.insert(0, Required(False))
            return ordered_constraint_list

        # check if constraints contains required clause,
        # and place it in first pos if found
        if Required in [type(elem) for elem in sanitized_constraint_list]:
            # assert required clause will be checked in first, and keep only the first
            for constraint in sanitized_constraint_list:
                if type(constraint) is Required:
                    ordered_constraint_list.insert(0, constraint)
                    opt_inserted = True
                else:
                    ordered_constraint_list.append(constraint)

        # if required constraint is not found,
        # insert a required(False) constraint, in first pos
        if not opt_inserted or Required not in [
            type(elem) for elem in sanitized_constraint_list
        ]:
            ordered_constraint_list = sanitized_constraint_list
            ordered_constraint_list.insert(0, Required(False))

        return ordered_constraint_list
