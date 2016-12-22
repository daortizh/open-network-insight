const d3 = require('d3');

const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');
const NetflowConstants = require('../constants/NetflowConstants');
const DateUtils = require('../../../js/utils/DateUtils');

const ObervableGraphQLStore = require('../../../js/stores/ObservableGraphQLStore');

class IngestSummaryStore extends ObervableGraphQLStore {
    getQuery() {
        return `
            query($startDate:String!, $endDate:String!) {
                netflow {
                    ingestSummary(startDate: $startDate,endDate: $endDate) {
                        date
                        flows: total
                    }
                }
            }
        `;
    }

    setStartDate(date) {
        this.setVariable('startDate', date);
    }

    getStartDate() {
        return this.getVariable('startDate');
    }

    setEndDate(date) {
        this.setVariable('endDate', date);
    }

    getEndDate() {
        return this.getVariable('endDate');
    }

    requestSummary() {
        this.sendQuery();
    }

    unboxData(data) {
        const dataByMonth = {};
        const parse = d3.time.format("%Y-%m-%d %H:%M").parse;

        const startDate = DateUtils.parseDate(`${this.getStartDate()} 00:00`);
        const endDate = DateUtils.parseDate(`${this.getEndDate()} 23:59`);

        data.netflow.ingestSummary
            .forEach(record => {
                record.date = parse(record.date);

                // Filter out dates outside range
                if (record.date<startDate || endDate<record.date) return;

                let month = `${record.date.getYear()}-${record.date.getMonth()}`;

                if (!(month in dataByMonth)) dataByMonth[month] = [];

                dataByMonth[month].push(record);
            });

        // Sort dates
        return Object.keys(dataByMonth).map(month => dataByMonth[month].sort((a, b) => a.date - b.date));
    }
}

const iss = new IngestSummaryStore();

SpotDispatcher.register(function (action) {
    switch (action.actionType) {
        case SpotConstants.UPDATE_DATE:
            switch (action.name) {
                case NetflowConstants.START_DATE:
                    iss.setStartDate(action.date);
                    break;
                case NetflowConstants.END_DATE:
                    iss.setEndDate(action.date);
                    break;
            }
            break;
        case NetflowConstants.RELOAD_INGEST_SUMMARY:
            iss.requestSummary();
            break;
    }
});

module.exports = iss;
