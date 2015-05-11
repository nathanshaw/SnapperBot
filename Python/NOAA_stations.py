from os import system

#system('curl ' + 'http://w1.weather.gov/xml/current_obs/seek.php?state=ny&Find=Find')

data =  system('curl ' + 'http://w1.weather.gov/xml/current_obs/seek.php?state=ny&Find=Find')
print("----------------------------------------------")
print(data)
print("----------------------------------------------")

def find_between(s, first, last):
    try:
        start = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

print find_between(data, 'href="', '.rss')
