
from src.util_rc.main import util_rc
import numpy as np
from matplotlib import pyplot as plt

import time
import scipy
x = scipy.version.version
alphas = np.random.uniform(0.5, 1, size=9)
indiff_alphas = np.arange(0.02, 2.02, .02)
amount1 = np.ones(100)*20
prob1 = np.ones(100)
amount2 = np.round(np.random.uniform(21, 100, size=100))
prob2 = np.round((np.exp(indiff_alphas * (np.log(amount1) - np.log(amount2))))*100)/100
inv_temp = np.random.uniform(0, 2, size=9)
# expected utility
start_time = time.time()
estimates_e = {}
for i in np.arange(0, 9):
    util_diff = (prob2*amount2**alphas[i] - prob1*amount1**alphas[i])
    for j in np.arange(0, 9):
        util_diff1 = util_diff/inv_temp[j]
        logit = 1/(1+np.exp(-util_diff1))
        estimates_e[alphas[i], inv_temp[j]] = []
        for k in np.arange(0, 100):
             choice_prob = np.random.uniform(0, 1, 100)
             choices = logit < choice_prob
             estk = util_rc("E", choices, amount1, prob1, amount2, prob2).params[:2]
             estimates_e[alphas[i], inv_temp[j]].append(estk)
time1 = time.time() - start_time
mean_est = []
for i in np.arange(0,81):
    mean_i = np.mean([x[0] for x in list(estimates_e.values())[i]])
    mean_est.append(mean_i)

x = [x[0] for x in list(estimates_e.keys())]
plt.scatter(x,mean_est)
plt.xlabel('true alphas')
plt.ylabel('mean estimates')
plt.show()

# risk return
def ev_var(am, prob):
    ev = am * prob
    var = prob * (am - ev) ** 2 + (1 - prob) * (-ev) ** 2
    return [ev, var]

r = np.random.uniform(-0.05, 0.03, size=9)
#
estimates_r = {}
start_time = time.time()
for i in np.arange(0, 9):
    ev1 = ev_var(amount1, prob1)
    ev2 = ev_var(amount2, prob2)
    util_diff = ((ev2[0] - r[i]*ev2[1]) - (ev1[0] - r[i]*ev1[1]))
    for j in np.arange(0, 9):
        utildiff1 = util_diff/inv_temp[j]
        logit = 1/(1+np.exp(-utildiff1))
        estimates_r[r[i], inv_temp[j]] = []
        for k in np.arange(0, 100):
            choice_prob = np.random.uniform(0, 1, 100)
            choices = logit < choice_prob
            estk = util_rc("R", choices, amount1, prob1, amount2, prob2).params[:2]
            estimates_r[r[i], inv_temp[j]].append(estk)
time1 = time.time() - start_time
mean_est = []
for i in np.arange(0,81):
    mean_i = np.mean([x[0] for x in list(estimates_r.values())[i]])
    mean_est.append(mean_i)

x = [x[0] for x in list(estimates_r.keys())]
plt.scatter(x,mean_est)
plt.xlabel('true r')
plt.ylabel('mean estimates')
plt.show()

# coefficient of variation

estimates_w = {}
cv = np.random.uniform(-5.43, 61.42, size=9)

for i in np.arange(0, 9):
    for j in np.arange(0, 9):
        ev1 = ev_var(amount1, prob1)
        ev2 = ev_var(amount2, prob2)
        util_diff = (ev2[0] - cv[i] * np.sqrt(ev2[1]) / ev2[0] - (ev1[0] - cv[i] * np.sqrt(ev1[1]) / ev1[0]))/inv_temp[j]
        logit = 1/(1+np.exp(-util_diff))
        estimates_w[cv[i], inv_temp[j]] = []
        for k in np.arange(0, 100):
            choice_prob = np.random.uniform(0, 1, 100)
            choices = logit < choice_prob
            estk = util_rc("W", choices, amount1, prob1, amount2, prob2).params[:2]
            estimates_w[cv[i], inv_temp[j]].append(estk)

mean_est = []
for i in np.arange(0,81):
    mean_i = np.mean([x[0] for x in list(estimates_w.values())[i]])
    mean_est.append(mean_i)
#
x = [x[0] for x in list(estimates_w.keys())]
plt.scatter(x,mean_est)
plt.xlabel('true w')
plt.ylabel('mean estimates')
plt.show()

# hyperbolic
estimates_h = {}
h = np.random.uniform(0.306, 3.37, size=9)
for i in np.arange(0, 9):
    theta1 = (1 - prob1) / prob1
    theta2 = (1 - prob2) / prob2
    util_diff4 = ((amount2 / (1 + h[i] * theta2)) - (amount1 / (1 + h[i] * theta1)))/inv_temp[i]

for i in np.arange(0, 9):
    for j in np.arange(0, 9):
        theta1 = (1 - prob1) / prob1
        theta2 = (1 - prob2) / prob2
        util_diff = ((amount2 / (1 + h[i] * theta2)) - (amount1 / (1 + h[i] * theta1)))/inv_temp[j]
        logit = 1/(1+np.exp(-util_diff))
        estimates_h[h[i], inv_temp[j]] = []
        for k in np.arange(0, 100):
            choice_prob = np.random.uniform(0, 1, 100)
            choices = logit < choice_prob
            estk = util_rc("H", choices, amount1, prob1, amount2, prob2).params[:2]
            estimates_h[h[i], inv_temp[j]].append(estk)

mean_est = []
for i in np.arange(0,81):
    mean_i = np.mean([x[0] for x in list(estimates_h.values())[i]])
    mean_est.append(mean_i)

x = [x[0] for x in list(estimates_h.keys())]
plt.scatter(x,mean_est)
plt.show()

x = 1
