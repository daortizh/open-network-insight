const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');

const ObservableWithHeadersGraphQLStore = require('../../../js/stores/ObservableWithHeadersGraphQLStore');

const DATE_VAR = 'date';
const SRC_IP_VAR = 'srcIp';
const DST_IP_VAR = 'dstIp';
const TIME_VAR = 'time';

class DetailStore extends ObservableWithHeadersGraphQLStore {
    constructor() {
        super();

        this.headers = {
            tstart: 'Time',
            srcip: 'Source IP',
            dstip: 'Destination IP',
            sport: 'Source Port',
            dport: 'Destination Port',
            proto: 'Protocol',
            flags: 'Flags',
            tos: 'Type Of Service',
            ibytes: 'Input Bytes',
            ipkts: 'Input Packets',
            obytes:  'Output Bytes',
            opkts: 'Output Packets',
            rip: 'Router IP',
            input: 'Input iface',
            output: 'Output iface'
        };

        this.ITERATOR = ['tstart', 'srcip', 'dstip', 'sport', 'dport', 'proto', 'flags', 'tos', 'ibytes', 'ipkts', 'obytes', 'opkts', 'rip', 'input', 'output'];
    }

    getQuery() {
        return `
            query($date: String!, $srcIp: String!, $dstIp: String!, $time: String!) {
                netflow {
                    details(date: $date, srcIp: $srcIp, dstIp: $dstIp, time: $time) {
                        tstart
                        srcip: srcIp
                        sport: srcPort
                        dstip: dstIp
                        dport: dstPort
                        proto: protocol
                        flags
                        tos
                        ipkts: inPkts
                        ibytes: inBytes
                        opkts: outPkts
                        obytes: outBytes
                        rip: routerIp
                        input: inIface
                        output: outIface
                    }
                }
            }
        `;
    }

    unboxData(data) {
        return data.netflow.details;
    }

    setDate(date) {
      this.setVariable(DATE_VAR, date);
    }

    setSrcIp(ip) {
      this.setVariable(SRC_IP_VAR, ip);
    }

    setDstIp(ip) {
      this.setVariable(DST_IP_VAR, ip);
    }

    setTime(time) {
      var timeParts = time.split(' ')[1].split(':');
      this.setVariable(TIME_VAR, `${timeParts[0]}:${timeParts[1]}`);
    }
}

const ds = new DetailStore();

SpotDispatcher.register(function (action) {
  switch (action.actionType) {
    case SpotConstants.UPDATE_DATE:
      ds.setDate(action.date);
      break;
    case SpotConstants.SELECT_THREAT:
      ds.setSrcIp(action.threat.srcIP);
      ds.setDstIp(action.threat.dstIP);
      ds.setTime(action.threat.tstart);
      break;
    case SpotConstants.RELOAD_SUSPICIOUS:
      ds.resetData();
      break;
    case SpotConstants.RELOAD_DETAILS:
      ds.sendQuery();
      break;
  }
});

module.exports = ds;
