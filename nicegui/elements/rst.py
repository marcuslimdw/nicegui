import os
from functools import lru_cache

from docutils.core import publish_parts

from .markdown import remove_indentation
from .mixins.content_element import ContentElement


class ReStructuredText(ContentElement, component='rst.js'):

    def __init__(self, content: str = '') -> None:
        """ReStructuredText

        Renders ReStructuredText onto the page.

        :param content: the ReStructuredText content to be displayed
        """
        super().__init__(content=content)
        self._classes.append('nicegui-markdown')

    def _handle_content_change(self, content: str) -> None:
        html = prepare_content(content)
        if self._props.get('innerHTML') != html:
            self._props['innerHTML'] = html
            self.run_method('update', html)


@lru_cache(maxsize=int(os.environ.get('RST_CONTENT_CACHE_SIZE', '1000')))
def prepare_content(content: str) -> str:
    """Render ReStructuredText content to HTML."""
    html = publish_parts(
        remove_indentation(content),
        writer_name='html5'
    )
    return html["html_body"]
