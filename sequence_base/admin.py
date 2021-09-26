from django.contrib import admin
from sequence_base.models import Sequence


class SequenceAdmin(admin.ModelAdmin):

    list_filter = ['is_valid']
    list_display = ['letters_hash', 'is_valid', 'creation_date']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Sequence, SequenceAdmin)
