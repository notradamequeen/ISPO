from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *

user_handler = Resource(UserHandler)
profile_handler = Resource(ProfileHandler)
login_handler = Resource(LoginHandler)
dokumen_handler = Resource(DokumenHandler)
prinsip_handler = Resource(PrinsipHandler)
indikator_handler = Resource(IndikatorHandler)
payment_handler = Resource(PaymentHandler)
generate_token_handler = Resource(GenerateTokenHandler)
download_handler = Resource(DownloadHandler)

urlpatterns = patterns('api.views',
	# generate token
	url(r'^token/$', generate_token_handler),

	# users saja
	url(r'^users/$', user_handler),
    url(r'^users/(?P<user_id>[^/]+)/$', user_handler), 	

    # profile
	url(r'^user/profiles/$', profile_handler),
    # url(r'^user/profiles/(?P<token>[^/]+)/$', profile_handler),

	# login
	url(r'^login/$', login_handler),

	# create dokumen
	url(r'^dokumen/$', dokumen_handler),
    url(r'^dokumen/(?P<dok_id>[^/]+)/$', dokumen_handler),

    # create indikator
	url(r'^indikator/$', indikator_handler),
    url(r'^indikator/(?P<indikator_id>[^/]+)/$', indikator_handler),

    # create prinsip
	url(r'^prinsip/$', prinsip_handler),
    url(r'^prinsip/(?P<prinsip_id>[^/]+)/$', prinsip_handler),

    # create payment
	url(r'^payment/$', payment_handler),
    url(r'^payment/(?P<token>[^/]+)/$', payment_handler),

    # download dokumen
    url(r'^download/dokumen/$', download_handler),
)