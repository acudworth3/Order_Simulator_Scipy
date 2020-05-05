from scipy.stats import norm
from scipy.stats import skewnorm
from scipy.stats import uniform
from scipy.stats import gamma
import matplotlib.pyplot as plt
import random

import pandas as pd
import numpy as np

class network_data:
    def __init__(self,default=False):
        self.routes = {}
        self.whse = {}
        self.region = {}
        self.route_whse = {}
        self.whse_route = {}
        self.region_route = {}
        self.route_region = {}

        if default:
            self.add_routes(),self.add_whse(),self.add_regions(),self.build_network_naive(),self.gen_orders()

    def add_whse(self,whse_df=None):
        if not whse_df:
            whse_dist = skewnorm(a=100,loc=20,scale=3)
            self.whse = {key:whse_dist  for key in ['whse_'+str(num) for num in range(3)]}

    def add_routes(self,route_df=None):
        if not route_df:
            #generate 5 route with value below
            route_dist = skewnorm(a=100,loc=20,scale=3)
            self.routes = {key:route_dist  for key in ['route_'+str(num) for num in range(6)]}
            #TODO build from csv

    def add_regions(self,region_df=None):
        if not region_df:
            #add or subtract 3 hours randomly
            region_dist = uniform(loc=-3, scale=6)
            self.region = {key:region_dist  for key in ['region_'+str(num) for num in range(6)]}
            # plt.scatter(np.arange(1000), uniform(loc=-3, scale=6).rvs(1000)); #visualize

    def build_network_naive(self,network_df = None):
        if not network_df:
            #3 warehouse; 2 routes per warehouse; 2 regions per route
            self.region_route = {0: [0, 1], 1: [0, 1], 2: [2, 3], 3: [2, 3], 4: [4, 5], 5: [4, 5]}
            self.route_region = {0: [0, 1], 1: [0, 1], 2: [2, 3], 3: [2, 3], 4: [4, 5], 5: [4, 5]}
            self.route_whse = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}
            self.whse_route = {0:[0,1],1:[2,3],2:[4,5]}
            self.whse_region = {0:[0,1],1:[2,3],2:[4,5]}

    def gen_orders(self,N=10000,order_df=None,fh='sample_data.csv'):

        order_arr = np.ones((N,5))
        df = pd.DataFrame(order_arr, columns=['route','whse','region','total_time','on_time'])
        # df['region'].to_numpy()[0]
        #random regions
        order_arr[:,]
        #generate regions randomly
        if order_df is not None:
            df['region'] = order_df
        else:
            df['region'] = np.random.randint(0, len(self.region), N)
        # from region choose route randomly
        df['route'] = [np.random.choice(self.region_route[df['region'][idx]], p=[0.5, 0.5]) for idx in range(N)]
        # from route choose warehouse
        df['whse'] = [self.route_whse[df['route'][idx]] for idx in range(N)]

        #generate order time
        times = np.ones((N,3))
        times[:,0] = [list(self.whse.values())[idx].rvs(1)[0] for idx in df['whse']]
        times[:, 1] = [list(self.routes.values())[idx].rvs(1)[0] for idx in df['route']]
        times[:, 2] = [list(self.region.values())[idx].rvs(1)[0] for idx in df['region']]
        df['total_time'] = np.sum(times, axis=1)
        #ontime
        ot_vec = df.to_numpy()[:,3] > 48
        df['on_time'][df.to_numpy()[:, 3] > 48] = 0
        ot_perc = df['on_time'].sum() / len(df['on_time'])
        df.to_csv(fh,index=False)
        return  df








            #TODO build from csv

    #TODO finish in evening
    def network_visual(self):
        whse_skew_obj = self.whse['whse_1']
        route_skew_obj = self.routes['route_1']
        region_skew_obj = self.region['region_1']
        time_range = np.arange(0.6, 72, 0.001)
        sample_10000 = whse_skew_obj.rvs(10000) + route_skew_obj.rvs(10000) + region_skew_obj.rvs(10000)

        fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(9, 6),
                                subplot_kw={'xticks': [], 'yticks': []})


        for row in range (3):

            # warehouses
            ax1 = axs[row, 0]
            whse_skew_obj = self.whse['whse_' + str(row)]
            ax1.set_title(list(self.whse.keys())[row])
            ax1.set_xlabel('Hours')
            ax1.plot(time_range, whse_skew_obj.pdf(time_range), label=None, linestyle=':')
            ax1.axvline(x=24, ymin=0, ymax=1, label='24hr')
            ax1.set_ylabel('P(H)')
            ax1.legend()

            # routes
            ax2 = axs[row, 1]
            # ax2.set_title('Routes P(H) Left Tail 90%  CS: ['+str(int(route_skew_obj.ppf(0.01)))+','+str(int(route_skew_obj.ppf(0.9)))+']')
            ax2.set_title('Routes P(H)')
            # TODO update with route-warehouse assgnment
            [ax2.plot(time_range,list(self.routes.values())[idx].pdf(time_range), label=idx, linestyle=':') for idx in
             self.whse_route[row]]
            ax2.set_xlabel('Hours')
            # ax2.set_ylabel('P(H)')

            ax2.axvline(x=24, ymin=0, ymax=1, label='24hr')
            ax2.legend()
            # ax2.set_xticks([24])

            #regions
            ax3 = axs[row,2]
            ax3.set_title('Regions P(H)')
            #TODO update with route-warehouse assgnment
            #TODO generalize xrange
            [ax3.plot(np.linspace(-4,4,1000),list(self.region.values())[idx].pdf(np.linspace(-4,4,1000)), label=idx, linestyle=':') for idx in
             self.whse_region[row]]
            ax3.set_xlabel('Hours')
            ax3.set_xticks([-3,0,3])
            # ax2.set_ylabel('P(H)')
            ax3.legend()


            #Total
            ax4 = axs[row,3]

            N = 10000
            # regions = np.random.randint(0, len(self.region), N)
            order_df = np.random.randint(self.whse_region[row][0], self.whse_region[row][1] + 1, N)
            rslt = self.gen_orders(N=N, fh='junk.csv', order_df=order_df)
            ax4.hist(rslt['total_time'],bins=100)
            ax4.axvline(x=48, ymin=0, ymax=1, label='48hr', color='red')
            # ot_perc =
            ax4.legend()
            ax4.set_title('Delivery Time OT: '+str(rslt['on_time'].sum() / len(rslt['on_time']))+'%')
            # ax4.set_xlabel('Hours')
            # df = self.gen_orders(N=N, fh='junk.csv', order_df=order_df)
            #TODO update with route-warehouse assgnment
            #TODO generalize xrange

            # [ax3.plot(np.linspace(-4,4,1000),self.region[key].pdf(np.linspace(-4,4,1000)),label=key,linestyle=':') for key in random.sample(list(self.region.keys()),2)]
            # ax2.set_xlabel('Hours')
            # ax2.set_ylabel('P(H)')
            # ax3.legend()


        plt.savefig('sample.png')
        plt.close()



network_1 = network_data(default=True)
#route_dist = skewnorm(a=100,loc=20,scale=3) DEFAULT
network_1.routes['route_0'] = skewnorm(a=100,scale=12,loc=20) #bad route
network_1.routes['route_3'] = skewnorm(a=100,scale=3,loc=18) #good route
network_1.gen_orders(fh='test_sample.csv', N=500)
network_1.network_visual()
marker = 1
