from django.conf.urls import patterns, include, url

from faune.views import import_data, export_sqlite, export_taxon, export_unity, export_taxon_unity, export_criterion, export_user, export_classes, export_unity_geojson, export_unity_polygons, check_status, soft_version, soft_download, data_download

urlpatterns = patterns('',
    (r'^status/$', check_status),
    (r'^soft_version/$', soft_version),
    (r'^soft_download/(?P<apk_name>[A-Za-z0-9\-\.]+)/$', soft_download),
    (r'^data_download/(?P<file_name>[A-Za-z0-9\-\.\_]+)/$', data_download),
    (r'^data_download/(?P<organisme_name>[A-Za-z0-9\-\.\_]+)/(?P<file_name>[A-Za-z0-9\-\.\_]+)/$', data_download),
    (r'^import/$', import_data),
    (r'^export/sqlite/$', export_sqlite),
    (r'^export/taxon/$', export_taxon),
    (r'^export/unity/$', export_unity),
    (r'^export/taxon_unity/$', export_taxon_unity),
    (r'^export/criterion/$', export_criterion),
    (r'^export/user/$', export_user),
    (r'^export/classes/$', export_classes),
    (r'^export/unity_geojson/$', export_unity_geojson),
    (r'^export/unity_polygons/$', export_unity_polygons),
)

