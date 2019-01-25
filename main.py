#!/usr/bin/env python
import os
from jinja2 import FileSystemLoader, Environment
from webapp2 import RequestHandler, WSGIApplication, Route
import time
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("FakeBook v3.html")


class TimeHandler(BaseHandler):
    def get(self):
        now = time.strftime("%H:%M:%S")

        params = {"time": now}

        return self.render_template("Ura.html", params=params)


class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("Blog.html")


class KalkulatorHandler(BaseHandler):
    def get(self):
        return self.render_template("Kalkulator.html")

    def post(self):
        prva_stevilka = self.request.get("prva_stevilka")
        druga_stevilka = self.request.get("druga_stevilka")

        vsota = int(prva_stevilka) + int(druga_stevilka)

        params = {
            "vsota": vsota
        }

        return self.render_template("Kalkulator.html", params)


class Loto_generatorHandler(BaseHandler):
    def get(self):

        return self.render_template("Loto_generator.html")

class Loto_numbersHandler(BaseHandler):
    def get(self):

        numbers = []

        for x in range(8):
            numbers.append(random.randint(1, 39))
            params = {
                "numbers": str(numbers)
            }

        return self.render_template("Loto_numbers.html", params=params)


app = WSGIApplication([
    Route('/', MainHandler),
    Route('/time', TimeHandler),
    Route("/blog", BlogHandler),
    Route("/kalkulator", KalkulatorHandler),
    Route("/loto_generator", Loto_generatorHandler),
    Route("/loto_numbers", Loto_numbersHandler),
], debug=True)
