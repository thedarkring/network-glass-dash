def debug_post(f):
    def wrap(self, *args, **kwargs):
        for key in self.request.POST:
            value = request.POST[key]
            print("KEY: %s VALUE: %s" % (key, value))
            return f(self, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap