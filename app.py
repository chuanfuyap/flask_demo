from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import io
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.io import show
app = Flask(__name__)
app.vars={}
feat = ['open','close','high', 'low']


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['ticker'] = request.form['ticker'].upper()
        app.vars['select'] = [feat[q] for q in range(4) if feat[q] in request.form.values()]
        return redirect('/graph')

@app.route('/graph',methods=['GET','POST'])
def graph():
    urlData = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?start_date=2017-11-01&end_date=2018-01-01'
                          %app.vars['ticker']).content
    df = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    df.set_index('Date', inplace=True)
    df.set_index(pd.to_datetime(df.index), inplace=True)
    df.sort_index(inplace=True)
    source = ColumnDataSource(df)
                           
    p = figure(title='%s PLOT' %app.vars['ticker'], x_axis_type="datetime",plot_width=800, plot_height=200)

    if 'open' in app.vars['select']:
        p.line('Date', 'Open', line_width=2,line_color='#3288bd',legend='Opening price',source = ColumnDataSource(df))
    if 'close' in app.vars['select']:
        p.line('Date', 'Close', line_width=2, line_color="#FB8072",legend='Closing price',source = ColumnDataSource(df))
    if 'high' in app.vars['select']:
        p.line('Date', 'High', line_width=2,line_color='#99d594',legend='Highest of the Day',source = ColumnDataSource(df))
    if 'low' in app.vars['select']:
        p.line('Date','Low', line_width=2, line_color="#d53e4f",legend='Lowest of the Day',source = ColumnDataSource(df))
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)

