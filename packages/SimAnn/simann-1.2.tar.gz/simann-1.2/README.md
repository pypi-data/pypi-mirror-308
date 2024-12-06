# Simple Simulated Annealing curve fit algorithm

## Introduction
Simulated Annealing algorithm has been extensively used for many applications from computer science to biology. This algorithm is a random-search method in which the new solutions, generated according to a sequence of probability distributions (in this case the Boltzmann distribution), may be accepted even if theydo not lead to an improvement in the objective function. This algorithm can also be used to fit experimental data with complex theoretical models, where the need to escape from relative minima is a cricial part of the fitting process.

### Usage
The principal function of this package is the following:

SimAnn_fit(x, y, e, func, params, min, max, temp, alpha, n, chi_or_y_th, args)

Where:
- x:           is the x values of your experimental data (numpy array);
- y:           is the y values of your experimental data (numpy array);
- e:           is the error values of your experimental data (numpy array);
- func:        is your theoretical model;
- params:      are the parameters for your theoretical model that you want to optimise;
- min and max: are two different numpy arrays with the min and the max of your params array;
- temp:        is the temperature of the simulated annealing (for the Boltzmann distribution);
- alpha:       is a number between 0 and 1 expressing the decreasing of the temperature in each interation cycle;
- n:           is the number of iteration cycles;
- chi_or_y_th: if your function returns a single value of chi square, you need to put 'chi' in this fiels, otherwise put 'not_chi';
- args:        numpy array tipe of anything else you need to pass to your theoretical function a part from the x, y, e, and params.

The function returns the optimised parameters!

#### Considerations
Not always it gives a good fit. Indeed, since it is a random based algorithm, higher iterations allow to explore more the parameters space.
- If you have a very large range (min end max range) of many parameters, the algorithm might struggle to find the absolute minima. A suggestion would be to fit your function many times and reduce the range of your parameters to have a final better fit, changing also the temperature, alpha and iteration number.

- A good thing would be to use other minimisation algorithms after the SimAnn in order to cool down a bit more the fit (using for instance a steepest descent method) to find a more minimised parameters.

##### Other functions in the library
- residuals(y,y_th)
It is a small function returning the difference between the the experimental and theoretical y

- chi_calculation(y,e,y_th)
It is a function calculating the chi square.

- array_round(array)
If it is useful, is a function rounding each element within an array to the second digit after the decimal point.

All these functions can be imported and called within your python script.

FOR ANY ISSUE OF DOUBTS, YOU CAN VISIT THE GITHUB PAGE AT: https://github.com/gcorucci/Simple_Simulated_Annealing_curve_fit
OR DROP AN EMAIL AT: giacomocorucci@virgilio.it