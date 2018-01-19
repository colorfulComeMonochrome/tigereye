from flask_classy import FlaskView, route


class MiscView(FlaskView):
    route_base = '/'

    def index(self):
        return self.check()

    def check(self):
        return 'I am OK'



