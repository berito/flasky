import os
import sys
import click
from random import randint
from sqlite3 import IntegrityError
from app import create_app, db
from app.models import User, Role, Permission,Post
from flask_migrate import Migrate
from faker import Faker
from flask_migrate import upgrade


COV=None
if os.environ.get('FLASK_COVERAGE'):
  import coverage
  COV=coverage.coverage(branch=True,include='app/*')
  COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests"""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
@click.option('--coverage/--no-coverage',default=False,help='Run tests under code coverage')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE']=str(1)
        os.execvp(sys.executable,[sys.executable]+sys.argv)
    import unittest
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('COverage Summary')
        COV.report()
        basedir=os.path.abspath(os.path.dirname(__file__))
        covdir=os.path.join(basedir,'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version:file://%s/index.html'%covdir)
        COV.erase()

@app.cli.command()
@click.option('--length', default=25,help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],profile_dir=profile_dir)
    if __name__=="__main__":
     app.run(debug=False)
@app.cli.command()
def deploy():
    upgrade()
    Role.insert_roles()
    User.add_self_follows()