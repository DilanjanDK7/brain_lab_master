import numpy as np

from projects.qm_brain.utils.utils import *


def get_probability(wavefun):

    amplitude = np.abs(wavefun).T

    ampMag = np.sqrt(np.sum((amplitude * amplitude).T, axis=0))

    normAmp = (np.asarray(amplitude.T) / np.asarray(ampMag)).T

    return normAmp * normAmp

def get_n_largest(array,n=92):
    ind = np.argpartition(np.abs(array), -n)[-n:]
    return array[ind]



main_path = '/home/user/Desktop/QMBrain/nyc_data/'

filepathX = main_path + 'x_chanloc.csv'
filepathY = main_path + 'y_chanloc.csv'

x = load_matrix(filepathX)
y = load_matrix(filepathY)

coord_stack = zip_x_y(x,y)

condition_list = ['Cond10/','Cond12/']

for condition in condition_list:

    for i in range(13):

        data_path = main_path + condition + str(i + 1) + '/'

        subject_path = main_path + condition + str(i + 1) + '/results/norm/'

        print('Running for subject ', i + 1, 'in folder ', condition)

        if not file_exists(subject_path+'DeltaXDeltaPY.csv'):

            #filepathPos = subject_path + 'position_wavefunction_1d.npy'
            filepathMom = subject_path + 'momentum_prob_short2.csv'

            data = np.squeeze(load_matrix(data_path+'data.csv'))
            probability, wavefun = process_eeg_data2(data)

            momentum_prob = np.squeeze(load_matrix(filepathMom))

            xAvg = probability @ x
            yAvg = probability @ y

            xSqrAvg = probability @ (x * x)
            ySqrAvg = probability @ (y * y)

            dx = np.sqrt(xSqrAvg - (xAvg * xAvg))
            dy = np.sqrt(ySqrAvg - (yAvg * yAvg))

            # Determine the 92 best points
            #
            # psi_p_small = np.zeros(shape=(psi_p.shape[0],psi_p.shape[1]),dtype=np.complex64)
            #
            # for t in range(psi_p.shape[0]):
            #
            #     psi_p_small[t,:] = get_n_largest(psi_p[t,...].flatten())

            #momentum_prob = get_probability(psi_p_small.T)

            prob_deriv = prob_derivative(probability)

            m = 1

            pxAvg = np.sum(prob_deriv[...] * x[:], axis=1)
            pyAvg = np.sum(prob_deriv[...] * y[:], axis=1)

            pxAvgSqr = np.sum(np.square(prob_deriv[:, :]) * ((1 / momentum_prob[:, :])) * np.square(x[:]), axis=1)
            pyAvgSqr = np.sum(np.square(prob_deriv[:, :]) * ((1 / momentum_prob[:, :])) * np.square(y[:]), axis=1)

            dpx = m * np.sqrt(pxAvgSqr - (pxAvg * pxAvg))
            dpy = m * np.sqrt(pyAvgSqr - (pyAvg * pyAvg))

            uncertainty_x = dpx * dx
            uncertainty_y = dpy * dy

            save_file(uncertainty_x, subject_path, 'DeltaXDeltaPX')
            save_file(dx, subject_path, 'DeltaX')
            save_file(dpx, subject_path, 'DeltaPX')

            save_file(uncertainty_y, subject_path, 'DeltaXDeltaPY')
            save_file(dy, subject_path, 'DeltaY')
            save_file(dpy, subject_path, 'DeltaPY')

        else:
            print('The file already exists!')
