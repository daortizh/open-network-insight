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
                    raw(startDate: $startDate,endDate: $endDate) {
                        unix_tstamp
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

        data.netflow.raw
            .forEach(record => {
                record.date = new Date(record.unix_tstamp*1000);

                let month = `${record.date.getFullYear()}-${record.date.getMonth()}`;
                let minute = `${month}-${record.date.getDate()} ${record.date.getHours()}:${record.date.getMinutes()}`;

                if (!(month in dataByMonth)) dataByMonth[month] = {};
                if (!(minute in dataByMonth[month])) dataByMonth[month][minute] = {date:record.date,flows:0};

                dataByMonth[month][minute].flows++;
            });

        // Sort dates
        return Object.keys(dataByMonth).map(month => {
            let monthData = dataByMonth[month];

            return Object.keys(monthData).map(minute => monthData[minute]).sort((a, b) => a.date - b.date)
        });
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
