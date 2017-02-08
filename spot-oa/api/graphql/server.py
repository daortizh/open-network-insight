import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Create a flask application
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/graphql": {"origins": "*", "supports_credentials": True}})

from flask_graphql import GraphQLView

from schema import schema
from api.data import SpotDataApi

# Add a flask route for graphql
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema,  graphiql=True))

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
