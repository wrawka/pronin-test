from django.contrib import admin


from .models import Collection, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "date")
    search_fields = ("user__username",)
    list_filter = ("user",)
    ordering = ("-date",)
    readonly_fields = ("is_hidden",)
    list_per_page = 20


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author")
    search_fields = ("name", "author__username")
    list_filter = ("author",)
    ordering = ("-id",)
    fields = ("name", "author", "description", "participant_count")
    readonly_fields = ("participant_count",)
    list_per_page = 20
