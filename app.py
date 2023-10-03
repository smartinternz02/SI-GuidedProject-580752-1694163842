from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    case_study = {'CERTIFIED' : 0, 'CERTIFIED-WITHDRAWN' : 1, 'DENIED' : 2, 'WITHDRAWN' : 3, 
                                           'PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED' : 4, 'REJECTED' : 5, 'INVALIDATED' : 6}
    socs = ['Computer Systems Analysts', 'Computer Programmers',
       'SOFTWARE DEVELOPERS, APPLICATIONS', 'COMPUTER SYSTEMS ANALYSTS',
       'Software Developers, Applications']
    full_time_position = request.form.get('FULL_TIME_POSITION')
    full_time_position = 1 if full_time_position== 'Yes' else 0
    year = request.form.get('YEAR')
    prevailing_wave = request.form.get('Balance')
    soc_name = request.form.get('SOC_N')
    soc_name = socs.index(soc_name) + 1
    data = {
        'FULL_TIME_POSITION' : [full_time_position],
        'PREVAILING_WAGE':[prevailing_wave],
        'YEAR':[year],
        'SOC_N':[soc_name]
    }
    df = pd.DataFrame(data)
    model = pickle.load(open('finalized_model.sav', 'rb'))
    prediction = model.predict(df)
    cstudy = [k for k,v in case_study.items() if v == int(prediction)][0]
    return f"The Case Study : {cstudy}"

if __name__ == '__main__':
    app.run(debug=True)
