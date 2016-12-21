const Lokka = require('lokka').Lokka;
const Transport = require('lokka-transport-http').Transport;
const graphQLClient = new Lokka({
    transport: new Transport('http://the-matrix:5000/graphql')
});

class GraphQLStore {
    constructor() {
        this.query = null;
        this.variables = {};
    }

    setQuery(query) {
        this.query = query;
    }

    setVariable(name, value) {
        this.variables[name] = value;
    }

    getVariable(name) {
        return this.variables[name];
    }

    setData(data) {
        this.data = data;
    }

    getData() {
        return this.data;
    }

    resetData() {
        console.log('Call to resetData');
        this.setData({});
    }

    sendQuery() {
        const query = this.query;
        const vars = this.variables;

        this.setData({loading: true});
        graphQLClient.query(query, vars).then(
            (resp) => {
                this.setData(resp);
            },
            (err) => {
                this.setData({error: err.message})
            }
        );
    }
}

module.exports = GraphQLStore;
