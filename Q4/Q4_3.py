import matplotlib.pyplot as plt
import numpy as np

tau = 1
d_c = 15
v_0 = 20
v_a = 10

# independent variable is d_alpha
d_alpha = np.linspace(0,40,1000)

# ovm spec 1
v_e_1 = (v_0/2)*(np.tanh(d_alpha-d_c) + np.tanh(d_c))
print(v_e_1)
a_1 = (v_e_1-v_a)/tau

# ovm spec 2
f_2 = np.tanh((d_alpha/(v_a+1e-10)-1)) + np.tanh(1)
# for d_alpha < 10 m f_2 = 0
idx = np.where(d_alpha<10)[0]
f_2[idx] = 0
v_e_2 = (v_0/2)*f_2
a_2 = (v_e_2-v_a)/tau

plt.figure()
plt.plot(d_alpha,a_1, label = "Model Spec 1")
plt.plot(d_alpha,a_2, label = "Model Spec 2")
# Set the aspect ratio to 'equal' to ensure consistent scaling
plt.xlabel(r'$d_\alpha (m)$', fontsize=14)
plt.ylabel(r'$\frac{\mathrm{d}v_\alpha}{\mathrm{d}t} (m/s^2)$', fontsize=14)
plt.legend()
plt.show()

# model 1 acceleration limiting d_alpha is higher
# but jerk of model 1 is much higher (therefore breaking/accelerating force is higher)
# more appropriate for cars (more space in between) 
