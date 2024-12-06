import numpy as np
import random,sys,os

def array_round(array):
    new_array = np.zeros(len(array))
    for i,j in enumerate(array):
        new_array[i] = round(j,2)
    return new_array

def chi_calculation(y,e,y_th):
    chi_square = sum((y-y_th)**2/(e**2))/len(y)
    return chi_square

def residuals(y,y_th):
    return abs(y-y_th)

def SimAnn_fit(x, y, e, func, params, __min, __max, temp, alpha, n, chi_or_y_th, args):

    if chi_or_y_th == 'chi':
        chi_initial = func(params,*args)
    else:
        chi_initial = chi_calculation(y,e,func(params,*args))
        
    result_comp = [chi_initial]
    temp_comp   = [temp]
    values_comp = np.zeros([int(n),len(params)])
    count_of_accepted = 0
    acc_params = np.zeros(len(params))
    values_comp[0] = params[:]
    for i in range(int(n)):
        for par in range(len(params)):
            params[par] = random.uniform(__min[par],__max[par])

        if chi_or_y_th == 'chi':
            result = func(params,*args)
        else:
            result = chi_calculation(y,e,func(params,*args))
            
        temp = temp * alpha
        DE = abs(result_comp[-1]-result)
        p  = np.exp(-DE/temp)

        #random r
        r = random.uniform(0,1)

        if result_comp[-1]<result:
            if r < p :
                accept = True
            else:
                accept = False

        else:
            accept = True


        if accept == True:
            count_of_accepted = count_of_accepted+1
            result_comp       = np.append(result_comp,result)
            temp_comp         = np.append(temp_comp,temp)
            values_comp[count_of_accepted] = params[:]
            acc_params = values_comp[count_of_accepted]
        pr = 'Iteration step: '+str(i)+' Parameters: '+str(array_round(acc_params))+' chi: '+str(round(result_comp[-1],2))

        sys.stdout.write(f'\r{pr}')
        sys.stdout.flush()

        percentage_process = i/n
        
    np.savetxt('Minimization_SA.txt', np.c_[range(count_of_accepted+1),result_comp,temp_comp])
    fitted_params = values_comp[count_of_accepted,:]
    np.savetxt('Fitted_SA_Params.txt', np.c_[result_comp[1:],values_comp[:count_of_accepted]])
    print('\nFitted params ',fitted_params)
    return fitted_params

