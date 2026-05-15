"""
Defines custom rst based sphinx domain to create
a custom PyProperty that instead uses QML based
information like signals and slots
"""

from sphinx.application import Sphinx
from sphinx.domains.python import PyProperty
from sphinx.addnodes import desc_annotation
from docutils import nodes
from sphinx import addnodes

class PySignal(PyProperty):
    """
    Directive that looks like a py:property but labeled with 'signal' instead.
    """
    def handle_signature(self, sig, signode):
        result = super().handle_signature(sig, signode)
        for node in signode.traverse(desc_annotation):
            for child in node.children:
                if child.astext().strip() == 'property':
                    child.replace_self(addnodes.desc_sig_keyword('signal', 'signal'))
        return result

def setup(app: Sphinx):
    app.add_directive_to_domain('py', 'signal', PySignal)
    return {'version': '0.1', 'parallel_read_safe': True}
