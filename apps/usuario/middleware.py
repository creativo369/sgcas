class RolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configuracion e inicializacion

    def __call__(self, request):
        """
        Codigo a ser ejecutado para cada request antes que los views y los demas middlewares en settings.py
        """
        response = self.get_response(request)
        """
        Codigo a ser ejecutado por cada request/response luego de que los views son llamados
        """
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """
        Llamado exactamente antes de que Django llame a la vista, retorna un None o un HttpResponse
        """
        if request.user.is_authenticated:
            request.roles = None
            groups = request.user.groups.all()
            if groups:
                request.roles = groups[0].name
    #
    # def process_exception(self, request, exception):
    #     """
    #     Es llamado por el response si alguna excepcion es lanzada por el view
    #     :return:None o HttpResponse
    #     """
    #     pass
