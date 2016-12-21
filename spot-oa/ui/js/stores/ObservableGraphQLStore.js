const EventEmitter = require('events').EventEmitter;

const GraphQLStore = require('./GraphQLStore');

const DATA_CHANGE_EVENT = 'data-change';

class ObervableGraphQLStore extends GraphQLStore {
    constructor() {
        super();
        this.eventEmitter = new EventEmitter();
    }

    addChangeDataListener(callback) {
        this.eventEmitter.on(DATA_CHANGE_EVENT, callback);
    }

    removeChangeDataListener(callback) {
        this.eventEmitter.removeListener(callback);
    }

    setData(data) {
        super.setData(data);
        this.eventEmitter.emit(DATA_CHANGE_EVENT);
    }
}

module.exports = ObervableGraphQLStore;
