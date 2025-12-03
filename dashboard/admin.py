from django.contrib import admin
from .models import ChiaDataset

@admin.register(ChiaDataset)
class ChiaDatasetAdmin(admin.ModelAdmin):
    _all_fields = [f.name for f in ChiaDataset._meta.fields]
    list_display = tuple(_all_fields[:12] + ["pueblo_ccdgo"]) or ('id',)

    _text_fields = [
        f.name for f in ChiaDataset._meta.fields
        if f.get_internal_type() in ('CharField', 'TextField')
    ]
    search_fields = tuple(_text_fields[:6])

    _filter_fields = [
        f.name for f in ChiaDataset._meta.fields
        if f.get_internal_type() in ('BooleanField', 'CharField', 'IntegerField', 'DateField', 'DateTimeField')
    ]
    list_filter = tuple(_filter_fields[:6])

    readonly_fields = tuple(f.name for f in ChiaDataset._meta.fields if f.auto_created or f.editable is False) or ('id',)

    list_per_page = 50
    ordering = (_all_fields[0],)
    save_on_top = True
    list_select_related = False

    fieldsets = (
        (None, {
            'fields': tuple(_all_fields[:8])
        }),
        ('Datos adicionales', {
            'classes': ('collapse',),
            'fields': tuple(_all_fields[8:24])
        }),
        ('Más campos', {
            'classes': ('collapse',),
            'fields': tuple(_all_fields[24:])
        }),
    )

    # Improve display: shorten long text in list_display using a helper
    def _shorten(self, obj, field_name, max_len=50):
        val = getattr(obj, field_name, '')
        s = str(val) if val is not None else ''
        return (s[:max_len - 3] + '...') if len(s) > max_len else s

    def get_list_display(self, request):
        display = list(self.list_display)
        for i, fname in enumerate(display):
            if hasattr(self, f"_col_{fname}"):
                continue
            field_obj = next((f for f in ChiaDataset._meta.fields if f.name == fname), None)
            if field_obj and field_obj.get_internal_type() in ('TextField', 'CharField'):
                def make_short(fname):
                    def _fn(obj):
                        return self._shorten(obj, fname, max_len=60)

                    _fn.short_description = fname
                    _fn.admin_order_field = fname
                    return _fn

                setattr(self, f"_col_{fname}", make_short(fname))
                display[i] = f"_col_{fname}"
        return tuple(display)
