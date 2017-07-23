from pyecharts import WordCloud

word = [
'magnet', 'superconduct', 'current', 'HTS', 'field', 'coil', 'critic', 'film', 'YBCO', 'tape', 
'high-temperatur', 'power', 'conduct', 'effect', 'studi', 'cabl', 'method', 'bulk', 'measur', 'coat',
'densiti', 'model', 'oper', 'properti', 'DC',
]

num = [
'309', '371', '180', '168', '147', '100', '82', '80', '77', '72', '194', '70', '69',
 '61', '60', '60', '58', '57', '55', '52', '50', '49', '47', '46', '45']

wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("", word, num, word_size_range=[40,100])
wordcloud.show_config()
wordcloud.render()