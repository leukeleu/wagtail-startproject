# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    contenttype = apps.get_model('contenttypes.ContentType')
    page = apps.get_model('wagtailcore.Page')
    site = apps.get_model('wagtailcore.Site')
    homepage = apps.get_model('pages.HomePage')

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    page.objects.filter(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, __ = contenttype.objects.get_or_create(
        model='homepage', app_label='pages')

    # Create a new homepage
    new_homepage = homepage.objects.create(
        title="Home",
        slug='home',
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )

    # Create a site with the new homepage set as the root
    site.objects.create(
        hostname='localhost', root_page=new_homepage, is_default_site=True)


def remove_homepage(apps, schema_editor):
    # Get models
    contenttype = apps.get_model('contenttypes.ContentType')
    homepage = apps.get_model('pages.HomePage')

    # Delete the default homepage
    # Page and Site objects CASCADE
    homepage.objects.filter(slug='home', depth=2).delete()

    # Delete content type for homepage model
    contenttype.objects.filter(model='homepage', app_label='pages').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
