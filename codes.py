from bs4 import BeautifulSoup
import urllib.request
import re

resp = urllib.request.urlopen("http://pylint-messages.wikidot.com/all-messages")
soup = BeautifulSoup(resp, 'lxml')

link_test = []
for link in soup.find_all('a', href=True):
    if link.text:
        link_test.append(link['href'])

r = re.compile("^/messages:*")
newlist = list(filter(r.match, link_test))

codes = []
prefix = '/messages'
for i in newlist:
    i = i.strip(prefix)
    codes.append(i.upper()[1:])

print(codes)
# codes.append("code")
# codes.append("code_token")
#print(codes)
print(len(codes))