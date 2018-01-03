import urllib2, urllib, json

def main():
	base_url = "https://query.yahooapis.com/v1/public/yql?"
	yql_query = "select wind from weather.forecast where woeid=2460286"
	yql_url = base_url + urllib.urlencode({'q':yql_query}) + "&format=json"
	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)

	print data['query']['results']

if __name__ == "__main__":
	main()