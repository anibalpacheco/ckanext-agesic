# -*- coding: utf-8 -*-
import logging
import csv

from ckan import model
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


def create_country_codes():
    '''Create country_codes vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible dataset country code values) using the API.

    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'country_codes'}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info("Creating vocab 'country_codes'")
        data = {'name': 'country_codes'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'uk', u'ie', u'de', u'fr', u'es'):
            logging.info(
                    "Adding tag {0} to vocab 'country_codes'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def country_codes():
    '''Return the list of country codes from the country codes vocabulary.'''
    create_country_codes()
    try:
        country_codes = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'country_codes'})
        return country_codes
    except tk.ObjectNotFound:
        return None


class AgesicIDatasetFormPlugin(plugins.SingletonPlugin,
        tk.DefaultDatasetForm):
    '''Implements IDatasetForm CKAN plugin to add some extra fields.

    Uses a tag vocabulary to add a custom metadata field to datasets.

    '''
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)

    # These record how many times methods that this plugin's methods are
    # called, for testing purposes.
    num_times_new_template_called = 0
    num_times_read_template_called = 0
    num_times_edit_template_called = 0
    num_times_comments_template_called = 0
    num_times_search_template_called = 0
    num_times_history_template_called = 0
    num_times_package_form_called = 0
    num_times_check_data_dict_called = 0
    num_times_setup_template_variables_called = 0

    def after_map(self, map):
        """
        Example to use if we want to define a route either to a new controller
        inside our plugin or one that already defined in CKAN.
        """
        map.connect('apps', '/apps',
            #controller='apps.controller:AppsController', action='index')
            controller='controllers.related:RelatedController',
                action='dashboard')
        #intentando remapear register para deshabilitarlo (no funciono)
        #map.connect('register', '/user/register',
        #    controller='controllers.home:HomeController', action='index')
        return map

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_public_directory(config, 'public')
        tk.add_template_directory(config, 'templates')
        self.most_viewed_path = config['agesic.most_viewed_path']

    def most_viewed(self):
        """
        Most viewed datasets.
        Return HTML that can be rendered in the templates calling
        {{ h.most_viewed() }}
        """
        packages = []
        for row in csv.reader(open(self.most_viewed_path), delimiter='\t'):
            pq = model.Session.query(model.Package).filter(
                model.Package.name == row[0].replace('/dataset/', ''))
            if pq:
                packages.append(pq.first().as_dict())
        data = {'packages': packages, 'list_class': "unstyled dataset-list",
            'item_class': "dataset-item module-content", 'truncate': 120,
            'hide_resources': True}
        return plugins.toolkit.render_snippet('snippets/package_list.html', data)

    def get_helpers(self):
        return {'country_codes': country_codes, 'most_viewed': self.most_viewed}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        # Add our custom country_code metadata field to the schema.
        schema.update({
                'country_code': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('country_codes')]
                })
        # Add our custom fields metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
        schema.update({
                'update_frequency': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')],
                'spatial_ref_system': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')],
                'spatial_coverage': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')],
                'temporal_coverage': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')]
                })
        return schema

    def create_package_schema(self):
        schema = super(AgesicIDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(AgesicIDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(AgesicIDatasetFormPlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Add our custom country_code metadata field to the schema.
        schema.update({
            'country_code': [
                tk.get_converter('convert_from_tags')('country_codes'),
                tk.get_validator('ignore_missing')]
            })

        # Add our custom fields to the dataset schema.
        schema.update({
            'update_frequency': [tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')],
            'spatial_ref_system': [tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')],
            'spatial_coverage': [tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')],
            'temporal_coverage': [tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')]
            })

        return schema

    # These methods just record how many times they're called, for testing
    # purposes.
    # TODO: It might be better to test that custom templates returned by
    # these methods are actually used, not just that the methods get
    # called.

    def setup_template_variables(self, context, data_dict):
        AgesicIDatasetFormPlugin.num_times_setup_template_variables_called += 1
        return super(AgesicIDatasetFormPlugin, self).setup_template_variables(
                context, data_dict)

    def new_template(self):
        AgesicIDatasetFormPlugin.num_times_new_template_called += 1
        return super(AgesicIDatasetFormPlugin, self).new_template()

    def read_template(self):
        AgesicIDatasetFormPlugin.num_times_read_template_called += 1
        return super(AgesicIDatasetFormPlugin, self).read_template()

    def edit_template(self):
        AgesicIDatasetFormPlugin.num_times_edit_template_called += 1
        return super(AgesicIDatasetFormPlugin, self).edit_template()

    def comments_template(self):
        AgesicIDatasetFormPlugin.num_times_comments_template_called += 1
        return super(AgesicIDatasetFormPlugin, self).comments_template()

    def search_template(self):
        AgesicIDatasetFormPlugin.num_times_search_template_called += 1
        return super(AgesicIDatasetFormPlugin, self).search_template()

    def history_template(self):
        AgesicIDatasetFormPlugin.num_times_history_template_called += 1
        return super(AgesicIDatasetFormPlugin, self).history_template()

    def package_form(self):
        AgesicIDatasetFormPlugin.num_times_package_form_called += 1
        return super(AgesicIDatasetFormPlugin, self).package_form()

    # check_data_dict() is deprecated, this method is only here to test that
    # legacy support for the deprecated method works.
    def check_data_dict(self, data_dict, schema=None):
        AgesicIDatasetFormPlugin.num_times_check_data_dict_called += 1
