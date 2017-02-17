from django.db import models
from django.contrib.auth.models import User
from datetime import *

import uuid

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User)
	status = models.CharField(max_length=255)
	phone_number = models.IntegerField(max_length=20)
	payment = models.CharField(max_length=255)
	token = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

	def save(self, *args, **kwargs):
		if self.created_at == None:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		super(Profile, self).save(*args, **kwargs)

	def nama(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

	def email(self):
		return '%s' % (self.user.email)

class Payment(models.Model):
	profile = models.ForeignKey(Profile, related_name='profile')
	no_transaksi = models.CharField(max_length=255)
	bukti_foto = models.FileField(upload_to='attachment')
	status = models.CharField(max_length=255, null=True, default="Pending")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.no_transaksi)

	def save(self, *args, **kwargs):
		if self.created_at == None:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		super(Payment, self).save(*args, **kwargs)

class Indikator(models.Model):
	nama_indikator = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.nama_indikator)

	def save(self, *args, **kwargs):
		if self.created_at == None:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		super(Indikator, self).save(*args, **kwargs)

class Prinsip(models.Model):
	nama_prinsip = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.nama_prinsip)

	def save(self, *args, **kwargs):
		if self.created_at == None:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		super(Prinsip, self).save(*args, **kwargs)

class Dokumen(models.Model):
	prinsip = models.ForeignKey(Prinsip)
	indikator = models.ForeignKey(Indikator)
	nama_dokumen = models.FileField(upload_to='dokumen')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.nama_dokumen)

	def save(self, *args, **kwargs):
		if self.created_at == None:
			self.created_at = datetime.now()
		self.updated_at = datetime.now()
		super(Dokumen, self).save(*args, **kwargs)

