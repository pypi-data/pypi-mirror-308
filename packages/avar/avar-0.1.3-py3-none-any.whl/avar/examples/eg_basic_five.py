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
p = avar.params(vc=np.array([0.5, 1.0, 5, 0.5, 0.1]) * 1e-9)

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
va_fit, p_fit = avar.fit(tau, va_ideal, tol=0.001)

print("vc true:", p.vc)
print("vc fit: ", p_fit.vc)

# Show the results.
itrm.iplot(tau, [va_ideal, va_fit, va_real], lg="xy", rows=0.8,
        label=["Allan variances", "Ideal", "Fit to ideal", "Averaged real"])
