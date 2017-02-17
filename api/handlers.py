from piston.handler import BaseHandler
from django.contrib.auth.models import User
from accounts.models import *
from django.core.exceptions import ObjectDoesNotExist
from piston.utils import rc, validate
from django.contrib import auth
from django.http import HttpResponse
from django.utils import simplejson
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import re
import json
import random
import string
import uuid

class GenerateTokenHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request):
		return str(uuid.uuid4()).replace('-', '')

class LoginHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request):

		username = request.GET.get('username')
		password = request.GET.get('password')

		if username is not None or password is not None:
			try:
				user = auth.authenticate(username=username, password=password)

				if user.is_active:

					user.profile.token = str(uuid.uuid4()).replace('-', '')
					user.profile.save()

					return { 'status': True, 'message': 'login success', 'token': user.profile.token }
				else:
					return { 'status': False, 'message': 'your account is not active' }

			except Exception, e:
				return { 'status': False, 'message': 'login failed' }
		else:
			return { 'status': False, 'message': 'login failed' }

class UserHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request, user_id=None):

		if user_id:
			try:
				return User.objects.get(pk=user_id)
			except ObjectDoesNotExist:
				return None
		else:
			return User.objects.all()

class ProfileHandler(BaseHandler):
	allowed_methods = ('GET','POST', 'PUT', 'DELETE',)

	def read(self, request):
		token = request.GET.get('token')

		if token:
			try:
				i = Profile.objects.get(token=token)

				p = {
					'status': True,
					'data': {
						'id': i.id,
						'first_name': i.user.first_name,
						'last_name': i.user.last_name,
						'email': i.user.email,
						'phone_number': i.phone_number,
						'status': i.status,
						'payment': i.payment
					},
					'message': 'success'
				}

				return p
			except ObjectDoesNotExist:
				return { 'status': False, 'message': 'User not found' }
		else:
			return { 'status': False, 'message': 'token not found' }

	def create(self, request):
		if request.content_type:
			data = request.data

			try:
				u = User.objects.create_user(username=data['username'], password=data['password'])
				u.first_name = data['first_name']
				u.last_name = data['last_name']
				u.email = data['email']
				u.save()

				prof = Profile()
				prof.user_id = u.id
				prof.status = data['status']
				prof.phone_number = data['phone_number']
				prof.payment = data['payment']
				prof.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success created user'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed created user'}
			return resp

	def update(self, request, token=None):
		if request.content_type:
			data = request.data

			try:
				prof = Profile.objects.get(token=token)
				prof.user.first_name = data['first_name']
				prof.user.last_name = data['last_name']
				prof.user.email = data['email']
				prof.status = data['status']
				prof.phone_number = data['phone_number']
				prof.payment = data['payment']

				prof.user.save()
				prof.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success updated user'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed updated user'}
			return resp

	def delete(self, request, token=None):
		if token:

			try:
				prof = Profile.objects.get(token=token)
				prof.user.delete()
				prof.delete()

			except Exception, e:
				return {'status': False, 'message': unicode(e)}
			else:
				return { 'status': True, 'message': 'success' }
			
		else:
			return {'status': False, 'message': 'failed'}

class DokumenHandler(BaseHandler):
	allowed_methods = ('GET','POST', 'PUT', 'DELETE',)

	def read(self, request, dok_id=None):

		if dok_id:
			try:
				i = Dokumen.objects.get(pk=dok_id)

				p = {
					'status': True,
					'data': {
						'id': i.id,
						'prinsip_id': i.prinsip.id,
						'indikator_id': i.indikator.id,
						'nama_dokumen': i.nama_dokumen
					},
					'message': 'success'
				}

				return p
			except ObjectDoesNotExist:
				return []
		else:
			dokumens = Dokumen.objects.all()

			data = []

			for i in dokumens:
				p = {
					'id': i.id,
					'prinsip_id': i.prinsip.id,
					'indikator_id': i.indikator.id,
					'nama_dokumen': i.nama_dokumen
				}

				data.append(p)

			return data

	def create(self, request):
		if request.content_type:
			data = request.data
			nama_dokumen = request.FILES['nama_dokumen']

			try:
				d = Dokumen()
				d.prinsip_id = data['prinsip_id']
				d.indikator_id = data['indikator_id']
				d.nama_dokumen = nama_dokumen
				d.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success created dokumen'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed created dokumen'}
			return resp

	def update(self, request, dok_id=None):
		if request.content_type:
			data = request.data
			nama_dokumen = request.FILES['nama_dokumen']

			try:
				d = Dokumen.objects.get(pk=dok_id)
				d.prinsip_id = data['prinsip_id']
				d.indikator_id = data['indikator_id']
				d.nama_dokumen = nama_dokumen
				d.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success updated dokumen'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed updated dokumen'}
			return resp

	def delete(self, request, dok_id=None):
		if dok_id:

			try:
				d = Dokumen.objects.get(pk=dok_id)
				d.delete()

			except Exception, e:
				return {'status': False, 'message': unicode(e)}
			else:
				return { 'status': True, 'message': 'success deleted dokumen' }
			
		else:
			return {'status': False, 'message': 'failed deleted dokumen'}

class PrinsipHandler(BaseHandler):
	allowed_methods = ('GET','POST', 'PUT', 'DELETE',)

	def read(self, request, prinsip_id=None):

		if prinsip_id:
			try:
				i = Prinsip.objects.get(pk=prinsip_id)

				p = {
					'status': True,
					'data': {
						'id': i.id,
						'nama_prinsip': i.nama_prinsip
					},
					'message': 'success'
				}

				return p
			except ObjectDoesNotExist:
				return []
		else:
			prinsips = Prinsip.objects.all()

			data = []

			for i in prinsips:
				p = {
					'id': i.id,
					'nama_prinsip': i.nama_prinsip
				}

				data.append(p)

			return data

	def create(self, request):
		if request.content_type:
			data = request.data

			try:
				p = Prinsip()
				p.nama_prinsip = data['nama_prinsip']
				p.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success created prinsip'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed created prinsip'}
			return resp

	def update(self, request, prinsip_id=None):
		if request.content_type:
			data = request.data

			try:
				p = Prinsip.objects.get(pk=prinsip_id)
				p.nama_prinsip = data['nama_prinsip']
				p.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success updated prinsip'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed updated prinsip'}
			return resp

	def delete(self, request, prinsip_id=None):
		if prinsip_id:

			try:
				p = Prinsip.objects.get(pk=prinsip_id)

			except Exception, e:
				return {'status': False, 'message': unicode(e)}
			else:
				dok = Dokumen.objects.filter(prinsip=p)

				if dok.count() == 0:
					p.delete()

					return { 'status': True, 'message': 'success deleted prinsip' }					
				else:
					return { 'status': True, 'message': 'failed delete, because any data related' }
			
		else:
			return {'status': False, 'message': 'failed'}

class IndikatorHandler(BaseHandler):
	allowed_methods = ('GET','POST', 'PUT', 'DELETE',)

	def read(self, request, indikator_id=None):

		if indikator_id:
			try:
				i = Indikator.objects.get(pk=indikator_id)

				p = {
					'status': True,
					'data': {
						'id': i.id,
						'nama_indikator': i.nama_indikator
					},
					'message': 'success'
				}

				return p
			except ObjectDoesNotExist:
				return []
		else:
			indikators = Indikator.objects.all()

			data = []

			for i in indikators:
				p = {
					'id': i.id,
					'nama_indikator': i.nama_indikator
				}

				data.append(p)

			return data

	def create(self, request):
		if request.content_type:
			data = request.data

			try:
				p = Indikator()
				p.nama_indikator = data['nama_indikator']
				p.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success created indikator'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed created indikator'}
			return resp

	def update(self, request, indikator_id=None):
		if request.content_type:
			data = request.data

			try:
				p = Indikator.objects.get(pk=indikator_id)
				p.nama_indikator = data['nama_indikator']
				p.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success updated indikator'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed updated indikator'}
			return resp

	def delete(self, request, indikator_id=None):
		if indikator_id:

			try:
				p = Indikator.objects.get(pk=indikator_id)

			except Exception, e:
				return {'status': False, 'message': unicode(e)}
			else:
				dok = Dokumen.objects.filter(indikator=p)

				if dok.count() == 0:
					p.delete()

					return { 'status': True, 'message': 'success deleted indikator' }					
				else:
					return { 'status': True, 'message': 'failed delete, because any data related' }
			
		else:
			return {'status': False, 'message': 'failed'}

class PaymentHandler(BaseHandler):
	allowed_methods = ('GET','POST', 'PUT', 'DELETE',)

	def read(self, request, token=None):

		if token:
			try:
				i = Payment.objects.get(profile__token=token)

				p = {
					'status': True,
					'data': {
						'id': i.id,
						'profile_id': i.profile.id,
						'no_transaksi': i.no_transaksi,
						'bukti_foto': i.bukti_foto
					},
					'message': 'success'
				}

				return p
			except ObjectDoesNotExist:
				return []
		else:
			payments = Payment.objects.all()

			data = []

			for i in payments:
				p = {
					'id': i.id,
					'profile_id': i.profile.id,
					'no_transaksi': i.no_transaksi,
					'bukti_foto': i.bukti_foto
				}

				data.append(p)

			return data

	def create(self, request):
		token = request.GET.get('token')

		if token:
			if request.content_type:
				data = request.data
				bukti_foto = request.FILES['bukti_foto']

				try:
					profile = Profile.objects.get(token=token)

				except Exception, e:
					resp = {'status': False, 'message': unicode(e)}
					return resp
				else:
					try:
						p = Payment()
						p.profile_id = profile.id
						p.no_transaksi = data['no_transaksi']
						p.bukti_foto = bukti_foto
						p.save()

					except Exception, e:
						resp = {'status': False, 'message': unicode(e)}
						return resp
					else:
						resp = {'status': True, 'message': 'success created payment'}
						return resp
		else:
			return { 'status': False, 'message': 'Token not found' }

	def update(self, request, token=None):
		if request.content_type:
			data = request.data
			bukti_foto = request.FILES['bukti_foto']

			try:
				p = Payment.objects.get(profile__token=token)
				p.profile_id = data['profile_id']
				p.no_transaksi = data['no_transaksi']
				p.bukti_foto = bukti_foto
				p.save()

			except Exception, e:
				resp = {'status': False, 'message': unicode(e)}
				return resp
			else:
				resp = {'status': True, 'message': 'success updated payment'}
				return resp
		else:
			resp = {'status': False, 'message': 'failed updated payment'}
			return resp

	def delete(self, request, token=None):
		if token:

			try:
				p = Payment.objects.get(profile__token=token)

			except Exception, e:
				return {'status': False, 'message': unicode(e)}
			else:
				p.delete()

				return { 'status': True, 'message': 'success deleted payment' }
			
		else:
			return { 'status': False, 'message': 'failed' }

class DownloadHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request):
		token = request.GET.get('token')
		dok_id = request.GET.get('id')

		url_web = 'http://%s' % request.META['HTTP_HOST']

		if token:
			try:
				prof = Profile.objects.get(token=token)
			except Exception, e:
				return {'status': False, 'message': unicode(e)}
			else:
				if dok_id:
					try:
						dokumen = Dokumen.objects.get(pk=dok_id)
					except Exception, e:
						return { 'status': False, 'message': unicode(e) }
					else:
						full_path_url = url_web + dokumen.nama_dokumen.url
						return { 'status': True, 'file': full_path_url, 'message': 'success' }
				else:
					return { 'status': False, 'message': 'id not found' }
		else:
			return { 'status': False, 'message': 'token not found' }
