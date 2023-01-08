from argrelay.interp_plugin.AbstractInterp import AbstractInterp
from argrelay.misc_helper.AbstractPlugin import AbstractPlugin
from argrelay.runtime_context.InterpContext import InterpContext


class AbstractInterpFactory(AbstractPlugin):

    def create_interp(self, interp_ctx: InterpContext) -> AbstractInterp:
        pass
