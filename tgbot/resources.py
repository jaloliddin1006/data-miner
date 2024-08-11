from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from tgbot.models import Text, Voice, User


class TextResource(resources.ModelResource):

    class Meta:
        model = Text
        fields = ('id', 'text_id', 'text', 'created_at')
        import_order = ('text_id', 'text',)
        export_order = ('id', 'text_id', 'text', 'created_at')
        

class VoiceResource(resources.ModelResource):
    user_username = fields.Field(
        column_name='user_username',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    text_text = fields.Field(
        column_name='text_text',
        attribute='text',
        widget=ForeignKeyWidget(Text, 'text')
    )

    class Meta:
        model = Voice
        fields = ('id','user', 'user_username', 'text','text_text', 'voice', 'voice_id', 'length', 'size', 'created_at', 'like', 'dislike')
        export_order = ('id','user', 'user_username', 'text', 'user_username', 'text_text', 'voice', 'voice_id', 'length', 'size', 'created_at', 'like', 'dislike')

