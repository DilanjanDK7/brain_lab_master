import numpy as np

from projects.qm_brain.utils.utils import *

num_subjects = 13
main_path = '/home/user/Desktop/QMBrain/RestData/Try2/'

filepathX = main_path + 'x_chanloc.csv'
filepathY = main_path + 'y_chanloc.csv'


x = load_matrix(filepathX)
y = load_matrix(filepathY)

for i in range(num_subjects):

    subject_path = main_path + str(i + 1) + '/'

    if not file_exists(subject_path + 'DeltaX.csv'):

        print('Running for subject ', i + 1)

        filepathData = subject_path + 'data.csv'

        data = load_matrix(filepathData)

        phase, normAmp, probability = process_eeg_data(data)

        psi = normAmp * np.exp(1j * phase)

        xAvg = probability @ x
        yAvg = probability @ y

        xSqrAvg = probability @ (x * x)
        ySqrAvg = probability @ (y * y)

        dx = np.sqrt(xSqrAvg - (xAvg * xAvg))
        dy = np.sqrt(ySqrAvg - (yAvg * yAvg))

        # probability_conservation_plot(len(x),probability)

        momentum_wavefunction = momentum_wavefunc(psi)

        momenta_phase, momenta_norm_amp, momentum_prob = momenta_prob(momentum_wavefunction)

        prob_deriv = prob_derivative(probability)

        first_term_x, first_term_y = [], []

        second_term_x, second_term_y = [], []
        st_x, st_y = [], []

        for i in range(data.shape[1]):

            a1 = np.square(x) * np.square(prob_deriv[i, :]) * ((1 / momentum_prob[i, :]) - 1)
            a2 = np.square(y) * np.square(prob_deriv[i, :]) * ((1 / momentum_prob[i, :]) - 1)

            b1 = np.sum(a1)
            b2 = np.sum(a2)

            first_term_x.append(b1)
            first_term_y.append(b2)

            for k in range(len(x)):
                for l in range(len(x)):
                    if k > l:
                        st_x.append(prob_deriv[i, k] * prob_deriv[i, l] * x[k] * x[l])
                        st_y.append(prob_deriv[i, k] * prob_deriv[i, l] * y[k] * y[l])
            second_term_x.append(sum(st_x))
            second_term_y.append(sum(st_y))
            st_x = []
            st_y = []

        m = 1

        dpx = m * np.sqrt(np.array(first_term_x) - 2 * np.array(second_term_x))
        dpy = m * np.sqrt(np.array(first_term_y) - 2 * np.array(second_term_y))

        uncertainty_x = dpx * dx
        uncertainty_y = dpy * dy

        # Save the values for future analysis
        save_file(dx, subject_path, 'DeltaX')
        save_file(dy, subject_path, 'DeltaY')
        save_file(dpx, subject_path, 'DeltaPX')
        save_file(dpy, subject_path, 'DeltaPY')
        save_file(uncertainty_x, subject_path, 'DeltaXDeltaPX')
        save_file(uncertainty_y, subject_path, 'DeltaYDeltaPY')

    else:
        print('The file ', subject_path + 'DeltaX.csv', ' already exists!')
