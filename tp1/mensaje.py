class Mensaje(object):
    def __init__(self, cuerpo, asunto):  # TODO: agregar todo lo que viene en el JSON
        self._cuerpo = cuerpo
        self._asunto = asunto

    def cuerpo(self):
        return self._cuerpo

    def asunto(self):
        return self._asunto
