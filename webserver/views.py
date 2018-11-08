from django.shortcuts import render_to_response
from sklearn.externals import joblib
from sklearn.multioutput import RegressorChain
import numpy as np
import os


def stateHelper(state_code):
    states = ['AK','AL','AR','AS','AZ','CA','CO','CT','DC','DE','FL','FM','GA','GU','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MH','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','PR','PW','RI','SC','SD','TN','TX','UT','VA','VI','VT','WA','WI','WV','WY']
    result = [0] * len(states)
    result[states.index(str(state_code))] = 1
    print(result)
    return result

def index (request):
    if request.method == 'GET':
        return render_to_response('index.html', {'earning6': 0, 'earning8': 0, 'earning10': 0,'rates1': 0,
            'rates3': 0, 'rates5': 0, 'rates7': 0})
    else:
        inputFeatures = np.asarray([int(request.POST.get('PREDDEG')), int(request.POST.get('CONTROL')), int(request.POST.get('DEBT_MDN')), 
            float(request.POST.get('MEDIAN_HH_INC').strip(' "')), float(request.POST.get('POVERTY_RATE').strip(' "')), 
            float(request.POST.get('UNEMP_RATE').strip(' "')), int(request.POST.get('LOCALE')), 1, int(request.POST.get('NPT4_PUB'))] + 
            stateHelper(request.POST.get('STABBR'))).reshape(1, -1)
        print(inputFeatures)
        earningsModel = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RegressorChainGradientBoostingRegressorEarnings.pkl'))
        ratesModel = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RegressorChainGradientBoostingRegressorRepayment.pkl'))
        earnings = earningsModel.predict(inputFeatures)
        rates = ratesModel.predict(inputFeatures)
        print(type(earnings))
        print(earnings[0])
        print(earnings[0][0])
        print(int(earnings[0][0]))
        print(earnings)
        print(rates)
        return render_to_response('index.html', {'earning6': int(earnings[0][0]), 'earning8': int(earnings[0][1]), 'earning10': int(earnings[0][2]), 
            'rates1': rates[0][0], 'rates3': rates[0][1], 'rates5': rates[0][2], 'rates7': rates[0][3]})
