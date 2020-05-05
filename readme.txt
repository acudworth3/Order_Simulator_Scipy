Simulate simple orders via scipy objects

invoke with the following:

network_1 = network_data(default=True)

#adust routes as desired
network_1.routes['route_0'] = skewnorm(a=100,scale=12,loc=20) #bad route
network_1.routes['route_3'] = skewnorm(a=100,scale=3,loc=18) #good route

#generate sample orders
network_1.gen_orders(fh='test_sample.csv', N=500)
#create plots
network_1.network_visual()
