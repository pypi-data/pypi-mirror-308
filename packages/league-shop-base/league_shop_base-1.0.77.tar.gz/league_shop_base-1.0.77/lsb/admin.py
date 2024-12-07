from typing import Any

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django_advanced_search import AdvancedSearchMixin  # type: ignore
from django_form_button import FormButtonMixin

from lsb import list_filters
from lsb.actions import check_password
from lsb.actions import clear_disabled_with_status
from lsb.actions import clear_handleveled
from lsb.actions import mark_as_disabled_with_status
from lsb.actions import mark_as_handleveled
from lsb.actions import update_banned_accounts
from lsb.actions import update_skins

from .models import Champion
from .models import Product
from .models import Skin
from .utils.product import get_products_query_set


def custom_titled_filter(title: str):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args: Any, **kwargs: Any):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin[Champion]):
    list_display = (
        "id",
        "name",
        "roles",
        "lanes",
        "date_created",
        "date_modified",
    )

    search_fields = (
        "id",
        "name",
    )


@admin.register(Skin)
class SkinAdmin(FormButtonMixin, admin.ModelAdmin[Skin]):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "tier",
                    "name",
                    "champion",
                    "value",
                    "date_created",
                    "date_modified",
                )
            },
        ),
        (
            "Additinal Info",
            {
                "fields": ("stock", "sold"),
            },
        ),
    )

    list_display = (
        "id",
        "name",
        "champion",
        "tier",
        "value",
        "date_created",
        "date_modified",
    )

    readonly_fields = (
        "tier",
        "name",
        "champion",
        "value",
        "date_created",
        "date_modified",
        "stock",
        "sold",
    )

    search_fields = (
        "id",
        "name",
        "champion__name",
    )

    list_filter = ("tier",)

    form_buttons = (update_skins,)

    def stock(self, obj: Skin) -> int:
        return obj.all_skins_products.filter(is_purchased=False).count()  # type: ignore

    def sold(self, obj: Skin) -> int:
        return obj.all_skins_products.filter(is_purchased=True).count()  # type: ignore


@admin.register(Product)
class ProductAdmin(
    AdvancedSearchMixin, FormButtonMixin, admin.ModelAdmin[Product]
):
    """ProductAdmin class"""

    fields = (
        "username",
        "password",
        "level",
        "region",
        "blue_essence",
        "orange_essence",
        "mythic_essence",
        "country",
        "flash_key",
        "is_safe",
        "is_handleveled",
        "is_bare_metal",
        "is_proxmox",
        "is_aram_only",
        "rank",
        "division",
        "is_current_season_rank",
        "solo_wins",
        "solo_losses",
        "quickplay_wins",
        "quickplay_losses",
        "disabled_until",
        "status",
        "remarks",
        "uploaded_by",
        "is_auth_error",
        "is_banned",
        "date_banned",
        "ban_reason",
        "all_skins",
        "skins",
        "owned_skins",
        "permanent_skins",
        "email",
        "date_sign_up",
        "dob",
        "ip_address",
        "city",
        "date_checked",
        "date_last_played",
        "is_recovery_requested",
    )
    readonly_fields = ("all_skins",)
    list_display = (
        "id",
        "username",
        "region",
        "summoner_name",
        "discrete_level",
        "discrete_blue_essence",
        "orange_essence",
        "mythic_essence",
        "skin_count",
        "skin_score",
        "is_purchased",
        "country",
        "flash_key",
        "is_safe",
        "is_handleveled",
        "is_premium",
        "is_proxmox",
        "rank",
        "division",
        "is_current_season_rank",
        "solo_wins",
        "solo_losses",
        "quickplay_wins",
        "quickplay_losses",
        "is_disabled",
        "status",
        "remarks",
        "uploaded_by",
        "is_auth_error",
        "is_banned",
        "date_banned",
        "ban_reason",
        "email",
        "date_sign_up",
        "dob",
        "ip_address",
        "city",
        "date_last_played",
        "date_checked",
        "date_created",
        "date_modified",
    )
    list_filter = (
        "date_created",
        "date_modified",
        list_filters.AccountTypeListFilter,
        list_filters.ValidAcccountFilter,
        list_filters.OldStockFilter,
        "discrete_level",
        "discrete_blue_essence",
        "region",
        list_filters.IsDisabledFilter,
        "status",
        "uploaded_by",
        "is_purchased",
        "is_banned",
        "is_auth_error",
        "is_safe",
        "is_aram_only",
        "is_handleveled",
        ("is_bare_metal", custom_titled_filter("is premium")),
        "is_proxmox",
        "rank",
        "division",
        "is_current_season_rank",
        "date_checked",
        "date_last_played",
        "is_recovery_requested",
    )
    search_fields = [
        "id",
        "username",
        "summoner_name",
    ]
    advanced_search_fields = [
        "id",
        "username",
        "summoner_name",
    ]
    actions = (
        mark_as_handleveled,
        clear_handleveled,
        mark_as_disabled_with_status,
        clear_disabled_with_status,
        check_password,
    )
    form_buttons = (update_banned_accounts,)
    filter_horizontal = ("skins", "permanent_skins", "owned_skins")

    def get_queryset(self, request: HttpRequest):
        qs: QuerySet[Any] = super().get_queryset(request)
        return get_products_query_set(qs)

    @admin.display(ordering="skin_count")
    def skin_count(self, obj: Product) -> int:
        return obj.skin_count  # type: ignore

    @admin.display(ordering="skin_score")
    def skin_score(self, obj: Product) -> int:
        return obj.skin_score  # type: ignore

    @admin.display(ordering="disabled_until", boolean=True)
    def is_disabled(self, obj: Product) -> bool:
        return obj.disabled_until >= timezone.now()

    @admin.display(ordering="is_bare_metal", boolean=True)
    def is_premium(self, obj: Product) -> bool:
        return obj.is_bare_metal
