from flask import Flask, render_template, request, Response
import requests
from .helpers import get_muni_data, generate_plot_points

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config['BUDGET_DATA'] = requests.get(app.config['BUDGET_PATH']).json()
    app.config['PLOT_POINTS'] = generate_plot_points(app.config['BUDGET_DATA'])
    app.config['SCATTER'] = False

    @app.template_filter('currency')
    def currency_format(value):
        if value == 0: 
            return "n/a"
        if isinstance(value, str):
            value = float(value)
        return "${:,.2f}".format(value)
    
    @app.template_filter('pct')
    def police_pct(police, total):
        pct = "n/a"
        police = float(police)
        total = float(total)
        try:
            pct = str(int(police/total*100)) + "%"
        except ZeroDivisionError:
            pass
        return pct

    @app.context_processor
    def inject_plot_points():
        return {
            'BUDGET_DATA': app.config['BUDGET_DATA'],
            'PLOT_POINTS': app.config['PLOT_POINTS'],
            'SCATTER': app.config['SCATTER']
            }
    
    @app.route('/clean/')
    @app.route('/clean/<state>/<city>')
    def zzz(state=None, city=None):
        # location, police_budget, total_budget, pct = get_muni_data(state, city)
        return render_template(
            'index.html',
            city=city,
            state=state
        )

    @app.route('/')
    @app.route('/<state>/<city>')
    def main_page(state=None, city=None):
        app.config['SCATTER'] = request.args.get('scatter', "False")
        return render_template(
            'index.html',
            city=city,
            state=state
        )
    
    @app.route('/plot/')
    @app.route('/plot/<state>/<city>')
    def plot_test(state=None, city=None):
        return render_template(
            'index.html',
            IMAGE_PAGE='scatter.html'
            )
    
    @app.route('/tbl.css')
    def tbl_css():
        line_height = request.args.get('line_height')
        css = f"""
            :root {{
                --blue-line-height: {line_height}%;
            }}
        """
        return Response(css, mimetype='text/css')
    



        

    @app.route('/test')
    def testo():
        return "test"
    
    

    # # Register blueprints or routes here
    # from .routes import main
    # app.register_blueprint(main)

    return app