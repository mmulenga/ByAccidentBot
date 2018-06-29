import plotly.offline as py
import plotly.graph_objs as go
import datetime
from firebase import Firebase

fb = Firebase()
commentDictionary = dict()
timeList = list()
occurenceDictionary = dict()

def countOccurrences():
  for item in fb.pullAll('comments'):
    response = item.to_dict()
    commentDictionary[response['id']] = response['timestamp']

  for key, value in commentDictionary.items():
    timeList.append(value.date())

  for item in timeList:
    if item in occurenceDictionary:
      occurenceDictionary[item] += 1
    else:
      occurenceDictionary[item] = 1

def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

countOccurrences()

data = [go.Scatter(
            x=list(occurenceDictionary.keys()), # keys go here
            y=list(occurenceDictionary.values()))] # values go here

layout = go.Layout(xaxis = dict(
                   range = [to_unix_time(min(commentDictionary.values()).replace(tzinfo=None)),
                            to_unix_time(max(commentDictionary.values()).replace(tzinfo=None))]
    ))

fig = go.Figure(data = data, layout = layout)
py.plot(fig)