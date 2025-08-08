import os
import random
import hashlib
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# SQLAlchemy base
class Base(DeclarativeBase):
    pass

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "portugal-ab-test-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Use env DB or fallback to SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///site.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Init DB
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create tables on startup
with app.app_context():
    import models  # noqa: F401
    db.create_all()

def get_visitor_id():
    """Generate a unique visitor ID based on IP and user agent."""
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')
    return hashlib.md5(f"{ip}_{user_agent}".encode()).hexdigest()

def assign_variant(visitor_id):
    """Assign A/B test variant to visitor."""
    from models import Visitor

    # Check if visitor already has a variant
    visitor = Visitor.query.filter_by(visitor_id=visitor_id).first()
    if visitor:
        return visitor.variant

    # Assign new variant (50/50 split)
    variant = 'A' if random.random() < 0.5 else 'B'

    # Store visitor
    new_visitor = Visitor(
        visitor_id=visitor_id,
        variant=variant,
        ip_address=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
        user_agent=request.headers.get('User-Agent', '')
    )
    db.session.add(new_visitor)
    db.session.commit()

    return variant

@app.route('/')
def index():
    """Render the main page with A/B testing."""
    visitor_id = get_visitor_id()
    variant = assign_variant(visitor_id)

    video_configs = {
        'A': {
            'media_id': 'jz42mm3kzf',
            'script_src': 'https://fast.wistia.com/embed/jz42mm3kzf.js'
        },
        'B': {
            'media_id': 'ncb9bu8s4y',
            'script_src': 'https://fast.wistia.com/embed/ncb9bu8s4y.js'
        }
    }

    return render_template('index.html',
                           variant=variant,
                           video_config=video_configs[variant],
                           visitor_id=visitor_id)

@app.route('/track-conversion', methods=['POST'])
def track_conversion():
    """Track when a visitor clicks on Typeform (conversion)."""
    from models import Conversion

    data = request.get_json()
    visitor_id = data.get('visitor_id')
    variant = data.get('variant')

    if visitor_id and variant:
        conversion = Conversion(
            visitor_id=visitor_id,
            variant=variant,
            conversion_type='typeform_click',
            ip_address=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        )
        db.session.add(conversion)
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False})

@app.route('/ab-test-results')
def ab_test_results():
    """View A/B test results (admin dashboard)."""
    from models import Visitor, Conversion
    from sqlalchemy import func

    visitor_stats = db.session.query(
        Visitor.variant,
        func.count(Visitor.id).label('visitors')
    ).group_by(Visitor.variant).all()

    conversion_stats = db.session.query(
        Conversion.variant,
        func.count(Conversion.id).label('conversions')
    ).group_by(Conversion.variant).all()

    results = {}
    for stat in visitor_stats:
        variant = stat.variant
        visitors = stat.visitors
        conversions = next((c.conversions for c in conversion_stats if c.variant == variant), 0)
        conversion_rate = (conversions / visitors * 100) if visitors > 0 else 0

        results[variant] = {
            'visitors': visitors,
            'conversions': conversions,
            'conversion_rate': round(conversion_rate, 2)
        }

    return render_template('ab_results.html', results=results)
