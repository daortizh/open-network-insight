# Create a flask application
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/graphql": {"origins": "*", "supports_credentials": True}})

from flask_graphql import GraphQLView

from schema import schema

# Add a flask route for graphql
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, context={'test':True},  graphiql=True))

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
