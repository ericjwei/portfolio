from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')

    with app.app_context():
        from portfolio import routes

        from portfolio.climate_risk_dash.dashboard import create_dashboard
        app = create_dashboard(app)

        # from portfolio.assets import compile_assets
        # compile_assets(app)

        return app