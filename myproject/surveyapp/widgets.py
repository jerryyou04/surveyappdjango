from django_svelte_jsoneditor.widgets import SvelteJSONEditorWidget

class CustomSvelteJSONEditorWidget(SvelteJSONEditorWidget):
    def __init__(self, attrs=None):
        # Remove 'style' and add other valid props if necessary
        super().__init__(attrs)
