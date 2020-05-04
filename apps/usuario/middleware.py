class RolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configuracion e inicializacion

    def __call__(self, request):
        # ** Codigo a ser ejecutado para cada request antes que los views y los demas middlewares en settings.py **

        response = self.get_response(request)
        # ** Codigo a ser ejecutado por cada request/response luego de que los views son llamados **
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # ** Llamado exactamente antes de que Django llame a la vista, retorna un None o un HttpResponse **
        if request.user.is_authenticated:
            request.roles = None
            groups = request.user.groups.all()
            if groups:
                request.roles = groups[0].name

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>