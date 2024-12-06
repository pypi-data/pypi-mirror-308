import numpy as np
import avar
import itrm

# Build time.
T = 0.01
t_dur = 200.0
t = np.arange(0, t_dur, T)
K = len(t)

# Constants
J = 100
p = avar.params(
        vfogm=np.array([1e-8, 1e-7]),
        tfogm=np.array([0.1, 10]))

# Get mean Allan variance from Monte-Carlo noise.
M = avar.windows(K)
tau = M*T
va_real = np.zeros(len(M))
bar = itrm.Progress(J)
for j in range(J):
    y = avar.noise(K, T, p)
    va_real += avar.variance(y, M)/J
    bar.update(j)

# Get the ideal and fitted Allan variances.
va_ideal, _ = avar.ideal(tau, p)
va_fit, p_fit = avar.fit(tau, va_ideal, fogms=2)

print("var FOGM true:", p.vfogm)
print("tau FOGM true:", p.tfogm)
print("var FOGM fit: ", p_fit.vfogm)
print("tau FOGM fit: ", p_fit.tfogm)

# Show the results.
y = np.array([va_ideal, va_fit, va_real])
itrm.iplot(tau, y, lg="xy",
        label=["Allan variance", "Ideal", "Fit to ideal", "Averaged real"])
