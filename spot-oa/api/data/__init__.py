from netflow import Resolver as NetflowResolver

class DataApi(object):
    def resolve_netflow(self, *_):
        print 'Resolving Netflow'

SpotDataApi = DataApi()
