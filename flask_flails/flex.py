class Flex(object):
    """
    Flask extension registration
    """
    def __init__(self):
        self.extensions = None


    def configure_extensions(self, app, extensions):
        self.extensions = extensions
        for extension in extensions:
            try:
                extension.initiate(app)
            except Exception as e:
               raise e


class ExtensionConfig(object):
    """
    A wrapper for extension registry

    defaults to to registering an extension to the app provided by:

        by_class: ExtensionObject(app, *options, **options)

    alternately

        by_init: ExtensionObject.init_app(app, *options, **options)

    Other extension registration methods should subclass and customize this class.
    """
    def __init__(self, extension_class, *args, **kwargs):
        self.extension_class = extension_class
        self.init_type = kwargs.pop('init_type', 'by_class')
        self.args = args
        self.kwargs = kwargs


    def initiate(self, app):
        try:
            return getattr(self, self.init_type, None)(app)
        except Exception, e:
            raise


    def by_class(self, app):
        return self.extension_class(app, *self.args, **self.kwargs)


    def by_init(self, app):
        return self.extension_class.init_app(app, *self.args, **self.kwargs)


    def __repr__(self):
        return "<ExtensionConfig for: ({}, args: {}, kwargs: {})>".format \
                (self.extension_class,
                 self.args,
                 self.kwargs)