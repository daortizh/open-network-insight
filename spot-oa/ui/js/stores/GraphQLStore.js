const $ = require('jquery');
const SpotConstants = require('../constants/SpotConstants');

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
        const variables = this.variables;

        this.setData({loading: true});
        $.post({
            accept: 'application/json',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                query,
                variables
            }),
            url: SpotConstants.GRAPHQL_ENDPOINT
        })
        .done((response) => {
            this.setData(response.data);
        })
        .fail((jqxhr, textStatus, error) => {
            console.error('Unexpected GraphQL error', jqxhr.responseJSON)
            this.setData({error: `${textStatus}: ${error}`})
        });
    }
}

module.exports = GraphQLStore;
