from django.contrib import admin
from models import *

class DokumenAdmin(admin.ModelAdmin):
	list_display = ('nama_dokumen', 'prinsip', 'indikator', 'created_at', 'updated_at', )
	list_display_links = ('nama_dokumen', 'prinsip', 'indikator', )

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('nama', 'email', 'status', 'phone_number', 'created_at', 'updated_at', )
	list_display_links = ('nama', 'email', 'status', 'phone_number',)

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('no_transaksi', 'bukti_foto', 'status', 'created_at', 'updated_at', )
	list_display_links = ('no_transaksi', 'bukti_foto',)

class IndikatorAdmin(admin.ModelAdmin):
	list_display = ('nama_indikator', 'created_at', 'updated_at', )

class PrinsipAdmin(admin.ModelAdmin):
	list_display = ('nama_prinsip', 'created_at', 'updated_at', )

# Register your models here.
admin.site.register(Dokumen, DokumenAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Indikator, IndikatorAdmin)
admin.site.register(Prinsip, PrinsipAdmin)
admin.site.register(Payment, PaymentAdmin)
