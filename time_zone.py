import json
from pylab import *
from collections import Counter
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_counts(content):
	count = {}
	for i in content:
		if i in count:
			count[i] += 1
		else:
			count[i] = 1
	return count

def top_counts(count_dict, n=10):
	value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
	value_key_pairs = value_key_pairs.sort()
	return value_key_pairs[-n:]

path = 'usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
# time_zones = [rec['tz'] for rec in records if 'tz' in rec]
# counts = get_counts(time_zones)
# counts = Counter(time_zones) # much faster way is to use collections.Counter
frame = DataFrame(records)

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()

tz_counts[:10].plot(kind='barh', rot=0)
plt.show()