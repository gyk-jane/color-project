#%%
import csv
import numpy as np
import pandas as pd 
import webcolors
import itertools
import matplotlib.pyplot as plt 
from scipy.optimize import minimize
from numpy.polynomial.polynomial import polyfit 
from sklearn import linear_model, datasets 

# .csv to list (color chart which contains all the HEX-note relationship)
colors_by_notes = []
with open('etc/color_chart.csv') as file:
    reader = csv.reader(file, lineterminator = '\n')
    colors_by_notes = list(reader)
df_colors = pd.DataFrame(colors_by_notes[1:], columns=colors_by_notes[0])    
flatten = itertools.chain.from_iterable(colors_by_notes[1:])
to_rgb = []
for i in flatten:
    to_rgb.append(webcolors.hex_to_rgb(i))

# get unique lists of red,green,blue
red_only = []
green_only = []
blue_only = []
for i in to_rgb:
    red_only.append(i[0])
    green_only.append(i[1])
    blue_only.append(i[2])
unique_red = set(red_only)
unique_green = set(green_only)
unique_blue = set(blue_only)

# get trend lines for each RGB. each RGB should have two lines. total of 6
# @param unique_RGB is a list of all red, green, or blue codes
# returns best fit lines from unique_RGB list
def get_trend_line(unique_RGB):
    x = np.arange(len(unique_RGB))
    y = np.array(list(unique_RGB))

    MIN_SAMPLES = 2

    colors = 'rgkby'
    idx = 0

    final_out = []

    while len(x) > MIN_SAMPLES:
        X = np.ones((len(x), 2))
        X[:,1] = x

        ransac = linear_model.RANSACRegressor(residual_threshold=50, min_samples=MIN_SAMPLES)
        res = ransac.fit(X, y)

        inlier_mask = ransac.inlier_mask_

        xinlier = x[inlier_mask]
        yinlier = y[inlier_mask]

        color = colors[idx % len(colors)]
        idx += 1

        x = x[~inlier_mask]
        y = y[~inlier_mask]
        plt.plot(xinlier, yinlier, color + "*")
        
        final_out.append([xinlier, yinlier])


    x1 = np.array(list(final_out[0][0]))
    y1 = np.array(list(final_out[0][1]))

    b1, m1 = polyfit(x1, y1, 1)

    x2 = np.array(list(final_out[1][0]))
    y2 = np.array(list(final_out[1][1]))

    b2, m2 = polyfit(x2, y2, 1)

    plt.plot(x1, y1, '.')
    plt.plot(x1, b1+m1*x1, '-')

    plt.plot(x2, y2, '.')
    plt.plot(x2, b2+m2*x2, '-')
    plt.show()

    return [final_out, [b1,m1], [b2,m2]]

# get_trend_line(unique_blue)


#%%

# returns the final HEX codes (for 2 notes) but RED only
# @param x - list of two RED codes AND the RED code from the original chord HEX
# @param b,m - from y=b+mx
# @param c original HEX code
# @param length upper bound of "x-axis"
# @param bound interval of the list
def optimize_two_notes(b, m, c, bound_x, bound_y):
    def f(param):
        x1, x2 = param
        return abs(0.5*(x1+x2)-c)

    x0 = [0,0]

    if len(bound_y)==2:
        xlb, xup = bound_x
        cons = ({'type': 'ineq', 'fun': lambda x: (xup-xlb) - (x[0]-b)/m},
        {'type': 'ineq', 'fun': lambda x: (xup-xlb) - (x[1]-b)/m})
        
        lb, up = bound_y
        res = minimize(f, x0, constraints=cons, bounds=[(lb,up), (lb,up)])
    elif len(bound_y)==4:
        b1, b2 = b
        m1, m2 = m
        xlb1, xup1, xlb2, xup2 = bound_x
        cons = ({'type': 'ineq', 'fun': lambda x: (xup1-xlb1) - (x[0]-b1)/m1},
        {'type': 'ineq', 'fun': lambda x: (xup2-xlb2) - (x[1]-b2)/m2})
        
        lb1, up1, lb2, up2 = bound_y   
        res = minimize(f, x0, constraints=cons, bounds=[(lb1,up1), (lb2,up2)])
        
    return res['x']

def optimize_three_notes(b, m, c, bound_x, bound_y):
    def f(param):
        x1, x2, x3 = param
        return abs((1/3)*(x1+x2+x3)-c)

    x0 = [0,0,0]


    if len(bound_y)==2:
        xlb, xup = bound_x
        cons = ({'type': 'ineq', 'fun': lambda x: (xup-xlb) - (x[0]-b)/m},
        {'type': 'ineq', 'fun': lambda x: (xup-xlb) - (x[1]-b)/m},  
        {'type': 'ineq', 'fun': lambda x: (xup-xlb) - (x[2]-b)/m})

        lb, up = bound_y
        res = minimize(f, x0, constraints=cons, bounds=[(lb,up), (lb,up), (lb,up)])
    elif len(bound_y)==4:
        b1, b2 = b
        m1, m2 = m
        xlb1, xup1, xlb2, xup2 = bound_x
        cons = ({'type': 'ineq', 'fun': lambda x: (xup1-xlb1) - (x[0]-b1)/m1},
        {'type': 'ineq', 'fun': lambda x: (xup2-xlb2) - (x[1]-b2)/m2}, 
        {'type': 'ineq', 'fun': lambda x: (xup2-xlb2) - (x[2]-b2)/m2})
        
        ylb1, yup1, ylb2, yup2 = bound_y   
        res = minimize(f, x0, constraints=cons, bounds=[(ylb1,yup1), (ylb2,yup2), (ylb2,yup2)])
        
    return res['x']

red_hex = 150
set_1_1 = optimize_two_notes(135.1488,2.2282,red_hex,[3,57],[134,254])
set_1_2 = optimize_two_notes([135.1488,3.8613],[2.2282,2.3277],red_hex,[3,57,0,53],[134,254,0,120])
set_2_2 = optimize_two_notes(3.8613,2.3277,red_hex,[0,53],[0,120])

calc_1_1 = abs(0.5*(set_1_1[0]+set_1_1[1])-red_hex)
calc_1_2 = abs(0.5*(set_1_2[0]+set_1_2[1])-red_hex)
calc_2_2= abs(0.5*(set_2_2[0]+set_2_2[1])-red_hex)

set_keys = {'calc_1_1':set_1_1, 'calc_1_2':set_1_2, 'calc_2_2':set_2_2}
# which optimization produces the minimizer? 
var = {calc_1_1:'calc_1_1',calc_1_2:'calc_1_2',calc_2_2:'calc_2_2'}
min_val = var.get(min(var)) # this one
print(calc_1_1, calc_1_2, calc_2_2)
print(set_keys['calc_1_2'])

# set_1_1_1 = optimize_three_notes(-1.8,2.4,red_hex,25,[0,53])
# set_1_1_2 = optimize_three_notes([-1.8,-.5292],[2.4,5.2308],red_hex,25,[0,53,0,120])
# set_1_2_2 = optimize_three_notes([-.5292,-1.8],[5.2308,2.4],red_hex,25,[0,120,0,53])
# set_2_2_2 = optimize_three_notes(-.5292,5.2308,red_hex,25,[0,120])

# print('SEPARATE')

# calc_1_1_1 = abs((1/3)*(set_1_1_1[0]+set_1_1_1[1]+set_1_1_1[2])-red_hex)
# calc_1_1_2 = abs((1/3)*(set_1_1_2[0]+set_1_1_2[1]+set_1_1_2[2])-red_hex)
# calc_1_2_2 = abs((1/3)*(set_1_2_2[0]+set_1_2_2[1]+set_1_2_2[2])-red_hex)
# calc_2_2_2 = abs((1/3)*(set_2_2_2[0]+set_2_2_2[1]+set_2_2_2[2])-red_hex)

# print(calc_1_1_1, calc_1_1_2, calc_1_2_2, calc_2_2_2)

# def get_red(red_hex, num):
#     res_red = 255
#     if num==2:
#         set_1_1 = optimize_two_notes(-1.8,2.4,red_hex,25,[0,53])
#         set_1_2 = optimize_two_notes([-1.8,-.5292],[2.4,5.2308],red_hex,25,[0,53,0,120])
#         set_2_2 = optimize_two_notes(-.5292,5.2308,red_hex,25,[0,120])

#         calc_1_1 = abs(0.5*(set_1_1[0]+set_1_1[1])-red_hex))
#         calc_1_2 = abs(0.5*(set_1_2[0]+set_1_2[1])-red_hex))
#         calc_2_2= abs(0.5*(set_2_2[0]+set_2_2[1])-red_hex))

#         set_keys = {'calc_1_1':set_1_1, 'calc_1_2':set_1_2, 'calc_2_2':set_2_2}
#         # which optimization produces the minimizer? 
#         var = {calc_1_1:'calc_1_1',calc_1_2:'calc_1_2',calc_2_2:'calc_2_2'}
#         min_val = var.get(min(var)) # this one

#         res_red = set_keys[min_val]
#     elif num==3:
#         set_1_1_1 = optimize_three_notes(-1.8,2.4,red_hex,25,[0,53])
#         set_1_1_2 = optimize_three_notes([-1.8,-.5292],[2.4,5.2308],red_hex,25,[0,53,0,120])
#         set_1_2_2 = optimize_three_notes([-.5292,-1.8],[5.2308,2.4],red_hex,25,[0,120,0,53])
#         set_2_2_2 = optimize_three_notes(-.5292,5.2308,red_hex,25,[0,120])

#         calc_1_1_1 = abs((1/3)*(set_1_1_1[0]+set_1_1_1[1]+set_1_1_1[2])-red_hex))
#         calc_1_1_2 = abs((1/3)*(set_1_1_2[0]+set_1_1_2[1]+set_1_1_2[2])-red_hex))
#         calc_1_2_2 = abs((1/3)*(set_1_2_2[0]+set_1_2_2[1]+set_1_2_2[2])-red_hex))
#         calc_2_2_2 = abs((1/3)*(set_2_2_2[0]+set_2_2_2[1]+set_2_2_2[2])-red_hex))

#         # calcs should be scalar so whichever is the min, return the set{'x'} of corresponding
#         set_keys = {'calc_1_1':set_1_1, 'calc_1_2':set_1_2, 'calc_2_2':set_2_2}
#         # which optimization produces the minimizer? 
#         var = {calc_1_1:'calc_1_1',calc_1_2:'calc_1_2',calc_2_2:'calc_2_2'}
#         min_val = var.get(min(var)) # this one

        # res_single_hex = #some set{'x'}
    # elif num==3:
        # similar to above
    # else:
    #     res_single_hex = "num must be 2 or 3"

    # return res_single_hex 


# # @param hex is a list of all the RGB notes (is of length 2 or 3 always)
# def chord_to_HEX(hex, num):
#     red = get_red(hex[0], num)
#     green = get_single_hex(hex[1], num)
#     blue = get_single_hex(hex[2], num)
    
#     HEX_codes = list(red,green,blue)
#     return HEX_codes


# %%
a=1
b=2

min(1,1)

# %%
