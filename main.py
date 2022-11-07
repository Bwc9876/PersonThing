from json import dumps, loads
from pathlib import Path

from Person import Person, InsuredPerson
from console.inputs import SelectionInput, SelectionInputOptions, StringInput, NumericInput, NumericInputOptions, \
    BooleanInput, BooleanInputOptions, StringInputOptions, InputResult
from console.menus import Menu, MenuOptions
from console.output import color_text, ConsoleTextStyle, FourBitConsoleColors

name_input = StringInput(StringInputOptions(recurring=True))
float_input = NumericInput(NumericInputOptions(minimum=0, recurring=True))
yes_no = BooleanInput(BooleanInputOptions(recurring=True))
select_input = SelectionInput(SelectionInputOptions())

_context = {
    "people": [],
    "selected_person": -1,
    "selected_person_name": ""
}

success_style = ConsoleTextStyle(fg_color=FourBitConsoleColors.GREEN)


def print_success(in_str: str):
    print(color_text(in_str, success_style))


def get_selected(context) -> Person:
    return context['people'][context['selected_person']]


def person_eat(context):
    _, amount = float_input("How much did they eat")
    context['people'][context['selected_person']].eat(amount)
    print_success(f"{get_selected(context)} Is Now {get_selected(context).get_weight()} pounds!")


def person_exercise(context):
    _, time_spent = float_input("How much time did they spend")
    context['people'][context['selected_person']].exercise(time_spent)
    print_success(f"{get_selected(context)} Is Now {get_selected(context).get_weight()} pounds!")


def promote_person(context):
    _, amount = float_input("How much would you like to promote them by")
    context['people'][context['selected_person']].promotion(amount)
    print_success(f"{get_selected(context)}'s Wage Is Now ${get_selected(context).get_pay_rate():.2f}/hour")


def person_paycheck(context):
    _, hours = float_input("How many hours did they work")
    person = get_selected(context)
    print_success(f"{person} Got Paid ${person.calculate_paycheck(hours):.2f}!")
    print_success(f"{person} Now Has ${person.get_savings():.2f} In Savings!")


def kill_person(context):
    _, sure = yes_no("Are you sure you want to delete this person")
    if sure:
        context["people"].pop(context["selected_person"])
        print_success("Deleted")
    else:
        print_success("Cancelled")


menu = Menu(MenuOptions())

person_edit_actions = {
    "Eat": person_eat,
    "Exercise": person_exercise,
    "Promote": promote_person,
    "Calculate Paycheck": person_paycheck,
    "Delete": kill_person
}


def add_person(context):
    _, name = name_input("What is the person's name?")

    _, insurance = yes_no(f"Does {name} have insurance?")

    new_person = (InsuredPerson if insurance else Person)(name)

    if insurance:
        for insurance_type in InsuredPerson.InsuranceRates.keys():
            _, has_type = yes_no(f"Does {name} have {insurance_type}")
            if has_type:
                new_person.edit_insurance_status(insurance_type, True)

    context['people'].append(new_person)
    print(color_text(f"Added Person: {name}", success_style))


def select_person(context):
    while True:
        status, index = select_input("Who do you want to edit?", context['people'])
        if status == InputResult.SUCCESS:
            context["selected_person"] = index
            person = context["people"][context["selected_person"]]
            context["selected_person_name"] = str(person)
            print(repr(person))
            menu("What would you like to do?", person_edit_actions, context=context)
            context["selected_person"] = -1
        else:
            break


main_actions = {
    "Add Person": add_person,
    "View People": select_person
}


def main():
    result = None
    while result is None or result == InputResult.SUCCESS:
        result = menu("What would you like to do?", main_actions, _context)


if __name__ == "__main__":
    main()
