from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import *

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('zone_name', 'workstation_number', 'description')
    search_fields = ('zone_name', 'workstation_number')
    list_filter = ('zone_name',)

class EquipmentTypeInline(admin.TabularInline):
    model = EquipmentType
    extra = 1
    fields = ('type_name', 'category', 'description')

class EquipmentStatusInline(admin.TabularInline):
    model = EquipmentStatus
    extra = 1
    fields = ('status_name', 'description')
    readonly_fields = ('status_name', 'description')

class EquipmentSpecificationInline(admin.TabularInline):
    model = EquipmentSpecification
    extra = 1

class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0
    readonly_fields = ('movement_date', 'reason', 'responsible_user')
    fields = ('from_location', 'to_location', 'movement_date', 'reason')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('inventory_number', 'name', 'manufacturer', 
                    'model', 'current_location', 'created_at')
    list_filter = ('current_location', 
                   ('created_at', DateFieldListFilter))
    search_fields = ('inventory_number', 'name', 'manufacturer', 
                     'model', 'serial_number')
    inlines = [EquipmentTypeInline, EquipmentStatusInline, 
               EquipmentSpecificationInline, MovementInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('inventory_number', 'name', 'manufacturer', 
                      'model', 'serial_number')
        }),
        ('Местоположение', {
            'fields': ('current_location',)
        }),
        ('Гарантия и заметки', {
            'fields': ('warranty_expiry_date', 'notes'),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'type_name', 'category')
    list_filter = ('category',)
    search_fields = ('type_name', 'category', 'equipment__name')

@admin.register(EquipmentStatus)
class EquipmentStatusAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'status_name', 'description')
    list_filter = ('status_name',)
    search_fields = ('equipment__name', 'description')

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('spec_name', 'spec_value', 'unit')
    search_fields = ('spec_name', 'spec_value')
    list_filter = ('spec_name',)

@admin.register(EquipmentSpecification)
class EquipmentSpecificationAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'specification')
    list_filter = ('equipment__current_location',)
    search_fields = ('equipment__name', 'specification__spec_name')

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'from_location', 'to_location', 
                    'movement_date', 'responsible_user')
    list_filter = ('movement_date', 'from_location', 'to_location')
    search_fields = ('equipment__name', 'reason')
    date_hierarchy = 'movement_date'

@admin.register(WriteOff)
class WriteOffAdmin(admin.ModelAdmin):
    list_display = ('act_number', 'equipment', 'write_off_date', 
                    'approved_by')
    list_filter = ('write_off_date',)
    search_fields = ('act_number', 'equipment__name', 'reason')
    date_hierarchy = 'write_off_date'
