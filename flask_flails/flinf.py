import pprint


class Flinf(object):
    """Information about a generated flask application. By default, provides
    the url map and configuration variables of the generated application. To
    return additional information pass a list to requested.

    :param requested: a list of information items to extract from the
                      provided app, default includes a url map and listing of
                      configuaration variables
    """
    def __init__(self, flail, app=None, requested=None):
        self.flail = flail
        self.app = app
        self.provide_information = ['url_map', 'config_vars']
        if requested:
            self.provide_information.extend(requested)
        self.printer = pprint.PrettyPrinter(indent=4)

    @property
    def config_vars(self):
        return {k: v for k, v in self.app.config.iteritems()}

    @property
    def url_map(self):
        return [r for r in self.app.url_map.iter_rules()]

    @property
    def jinja_env(self):
        return self.app.jinja_env.__dict__

    @property
    def list_templates(self):
        return self.app.jinja_env.list_templates()

    @property
    def asset_env(self):
        return self.jinja_env.get('assets_environment').__dict__

    @property
    def asset_bundles(self):
        return self.asset_env['_named_bundles']

    def return_basic(self, item):
        return getattr(self.app, item, None)

    @property
    def app_information(self):
        """Returns a dict containing parameters in cls.provide_information
        list attribute. This will first attempt to resolve the parameter in the
        list as an attribute/property on this class, then as an attribute on
        the current associated application."""
        to_return = {}
        for item in self.provide_information:
            to_return[item] = getattr(self, item, self.return_basic(item))
        return to_return

    @property
    def info_applog(self):
        self.app.logger.info(self.app_information)

    @property
    def info_out(self):
        self.printer.pprint(self.app_information)
