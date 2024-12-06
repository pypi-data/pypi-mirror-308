from flask import Flask, redirect, url_for

class RouteManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.site_map = {}

    def create_route(self, route_name, route_link):
        # Adiciona o nome da rota e o link ao dicionário
        self.site_map[route_name] = route_link

        # Função que redireciona para o site configurado no dicionário
        def route_function():
            url = self.site_map.get(route_name)
            if url:
                return redirect(url)  # Redireciona para o site configurado
            else:
                return "URL não configurada para esta rota", 404

        # Adiciona a rota dinamicamente usando o nome especificado
        self.app.add_url_rule(f"/{route_name}", route_name, route_function)

    def use_route(self, route_name):
        if route_name in self.site_map:
            # Redireciona para a rota especificada
            return redirect(url_for(route_name))
        else:
            return "Rota não encontrada", 404

    def add_use_route(self):
        @self.app.route("/use/<route_name>")
        def use(route_name):
            return self.use_route(route_name)

    def run(self, host="0.0.0.0", debug=True):
        self.app.run(host=host, debug=debug)
