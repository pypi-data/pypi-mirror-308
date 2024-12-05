import inquirer.themes as themes
from inquirer.render.console import ConsoleRender


def prompt(questions, render=None, answers=None, theme=themes.Default(), raise_keyboard_interrupt=False):
    render = render or ConsoleRender(theme=theme)
    answers = answers or {}

    try:
        for question in questions:
            # support the hidden field
            # the answer is getting from callback, not by users input directly
            if hasattr(question, 'callback') and getattr(question, 'callback') is not None:
                answers[question.name] = question.callback(answers)
            else:
                answers[question.name] = render.render(question, answers)
        return answers
    except KeyboardInterrupt:
        if raise_keyboard_interrupt:
            raise
        print("")
        print("Cancelled by user")
        print("")
