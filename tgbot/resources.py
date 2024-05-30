from import_export import resources
from tgbot.models import Text

class TextResource(resources.ModelResource):

    class Meta:
        model = Text
        fields = ('id', 'text_id', 'text', 'created_at')
        import_order = ('text_id', 'text',)
        export_order = ('id', 'text_id', 'text', 'created_at')