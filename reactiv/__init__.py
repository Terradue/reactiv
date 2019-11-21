import numpy as np

from scipy.special import gamma
from skimage import color

def reactiv(inputs, date_vector):

    N = inputs.shape[0]
    
    nx = inputs.shape[1]
    ny = inputs.shape[2]
    
    im = inputs[0,:,:]
    threshold = 5 * im.mean()
    
    m1 = im
    m2 = im**2
    Imax = im
    
    ds = float(max(date_vector) - min(date_vector))
    
    M1 = np.zeros([nx, ny])
    M2 = np.zeros([nx, ny]) 
    Kmax = np.zeros([nx, ny]) 
    Imax = np.zeros([nx, ny])
    
    k=0
    for i in range(0, N):
        im = inputs[i,:,:]
        M1 = M1 + im
        M2 = M2 + im**2
        Matrix_indicek = (date_vector[k] - min(date_vector)) / ds * np.ones([nx, ny])
        k = k + 1
        Kmax = (im > Imax) * Matrix_indicek + (im < Imax) * Kmax 
        Imax = np.maximum(Imax, im)

    M1 = M1 / N
    M2 = M2 / N
    R = np.sqrt(M2 - M1**2) / M1

    gam = R.mean()
    L = ((0.991936 + 0.067646 * gam - 0.098888 * gam**2 - 0.048320 * gam**3) / (0.001224 - 0.034323 * gam + 4.305577 * gam**2 - 1.163498 * gam**3))

    CV = np.sqrt((L * gamma(L)**2 / (gamma(L + 0.5)**2)) - 1) # theretical mean value
    num = (L * gamma(L)**4. * (4 * (L**2) * gamma(L)**2 - 4 * L * gamma(L + 1 / 2)**2 - gamma(L + 1 / 2)**2))
    den = (gamma(L + 1 / 2)**4.*(L * gamma(L)**2 - gamma(L + 1 / 2)**2))
    alpha = 1 / 4 * num / den # theretical standard deviation value

    R = (R - CV) / (alpha / np.sqrt(N)) / 10.0 + 0.25;
    R = (R > 1) * np.ones([nx, ny]) + (R < 1) * R;   # Cast Coefficient of Varation R max to 1.
    R = (R > 0) * R;

    I = (Imax / threshold) # Cast Intensity to threshold. 
    I = (I < 1) * I + (I > 1) * np.ones([nx, ny])

    hsv = np.zeros([nx, ny, 3])
    hsv[:, :, 0] = Kmax
    hsv[:, :, 1] = R 
    hsv[:, :, 2] = I 

    C = color.hsv2rgb(hsv)
    
    return C