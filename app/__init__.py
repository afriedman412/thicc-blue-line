from flask import Flask, render_template, request, Response
import requests
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config['BUDGET_DATA'] = requests.get(app.config['BUDGET_PATH']).json()

    @app.route('/')
    def index():
        return render_template('index.html', pct=30)
    
    @app.route('/<state>/<city>')
    def localized(state, city):
        local_data = app.config['BUDGET_DATA'].get('_'.join([state, city]), None)
        location = local_data['name']
        police_budget = locale.currency(float(local_data['policeBudget']), grouping=True)
        total_budget = locale.currency(float(local_data['totalBudget']), grouping=True)
        pct = float(local_data['policeBudget'])/float(local_data['totalBudget'])*100
        return render_template(
            'index.html',
            location = location,
            police_budget = police_budget,
            total_budget = total_budget,
            pct = int(pct)
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