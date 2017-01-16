import os
from bs4 import BeautifulSoup
os.chdir('C:/wamp/www/nemo/application/views/ingredients')
with open('add.php', 'r+') as file:
    html = file.read()

html = '''
    <div>
       <h1>title</h1>
        <div><a href="google.com">inside</a>outside</div>
        <div><a href="yahoo.com"></a></div>
    </div>
    '''

soup = BeautifulSoup(html, 'lxml')
divlist = []
for divs in soup.html.findAll('a'):
    print(divs)
    print('\nnext:\n')


# for item in divlist:
#     print(item)
#     print('\nnext:\n')

# print(soup.select('div > a'))