from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class VariableNameChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'variable-names'
    priority = -1
    msgs = {
        'E6101': (
            'Has an invalid variable name: non-temporary variable should not contain "temp"',
            'bad-variable-name',
            'Non-temporary variable should not contain "temp"'
        ),
    }
    options = ()

    def visit_assignname(self, node):
        if "temp" in node.name.lower():
            self.add_message("bad-variable-name", node=node)

def register(linter):
    linter.register_checker(VariableNameChecker(linter))
