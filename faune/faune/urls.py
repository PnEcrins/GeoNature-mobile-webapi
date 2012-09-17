from django.conf.urls import patterns, include, url

from faune.views import import_data, export_taxon, export_family, export_unity, export_taxon_unity, export_criterion, export_user

urlpatterns = patterns('',    
    (r'^import/$', import_data),
    (r'^export/taxon/$', export_taxon),
    (r'^export/family/$', export_family),
    (r'^export/unity/$', export_unity),
    (r'^export/taxon_unity/$', export_taxon_unity),
    (r'^export/criterion/$', export_criterion),
    (r'^export/user/$', export_user),
)
