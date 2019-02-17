
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug,request, static_file
from random import randint
from csv import reader
usernovel = ""
with open("text.txt") as input_file:
    for x in input_file:
        usernovel += x
open("text.txt").close()

def htmlfy(text, title):
    page = """
<!DOCTYPE html>
  <html lang="en">
    <head>
    
      <meta charset="UTF-8">
      <title>%(title)s</title>
      <style>
      body{
      background-color:gray;}
      table{
      border-collapse:collapse;}
      
      th{
       border:1px solid black;
       font-size:20px;
       width:200px;
      }
      td{
      color:black;
      font-size:15px;
      border:1px solid black;
      }
      p{
      color:white;}
      form{
      color:black;
      font-size:19px;}
      
      .searchtable td{
      font-size:25px;
      }

      </style>
    </head>
    <body>
     %(text)s
    </body>
  </html>
""" %{'text':text,'title':title}
    return page





f = open("a2_processing.csv")
thead = True
sor_lst = []
with f as in_file:
    for i in in_file:
        sor_lst.append(i.split(","))
    lst1 = sor_lst[1:]
f.close()
tableh = "<thead><tr>\n"
for s in sor_lst[0]:
    tableh += "<th>{}</th>\n".format(s)
tableh += "</tr></thead>\n<tbody>\n"

# when search with author name give him a table
def search():
    author = request.POST.getall("authors")
    tab ='''<table class="searchtable"><thead>
<tr>
<th>Name</th>
<th>Chapter</th>
<th>Website</th>
<th>Chapter For A Day</th>
<th>Numbers of Words in A Chapter</th>
<th>The number of total words</th>
<th>Author</th>
</tr></thead><tbody>'''
    with open("a2_processing.csv") as infile:
        for s in reader(infile):
            for i in s:
                if i in author:
                    tab += "<tr>"
                    for info in s:
                        tab += "<td>{}</td>\n".format(info)
                    tab += "</tr>"
        tab += '</tbody></table><br><a href="/"">Home</a>'
        open("a2_processing.csv").close()
    return htmlfy(tab,"Title")


def homepage():
    global lst1, tableh, usernovel

    index = """
          <p>Learn if your number is a prime or not!</p>
            <form action="/second" method="get">
                <input type="text" name="search" maxlength="16" />
                <input type="submit" value="Search" />
            </form>
        <p>Are You Bored?Let's Find a Random Prime</p>
        <form action="/random" method="POST">
          <input type="radio" name="rprime" value="small" checked>Random prime<br>
          <input type="radio" name="rprime" value="big">Find a Bigger One!<br>
          <input type="submit" value="Find!">
        </form>
        <p>----------------------------------------------------</p>
        <form action="/novelpage" method="post">
          <p>Search from author</p>
          <select name="authors" multiple>
            <option value="Er-gen">Er-gen</option>
            <option value="Tian-Can-Tu-Dou">Tian-Can-Tu-Dou</option>
            <option value="Cocooned-Cow">Cocooned-Cow</option>
            <option value="Su Yue Xi">Su Yue Xi</option>
            <option value="Jing Wu Hen">Jing Wu Hen</option>
            <option value="Shan Liang de Mi Feng">Shan Liang de Mi Feng</option>
          </select>
        <input type="submit" value="Search!"/>
        </form>
        <form action="/" method="get">
            Sort by Chapter Word: <input type="radio" name="srta" value="chapterword">
            Sort by Total Word:   <input type="radio" name="srta" value="totalword">
            <input type="submit" value="Sort!">
        </form>        
    """
    usertext = """        <p>If you Want another novel to present here please enter its name</p>
            <form action="/" method="GET">
           <input type="text" name="novelname" maxlength="50" >
           <input type="submit" value="Go!">
        </form>"""
    if 'novelname' in request.GET:
        fle = open("text.txt", "w")
        usernovel += request.GET["novelname"] + "\n"
        fle.write(str(usernovel))
        fle.close()
    if "srta" in request.GET:
        srt = request.GET["srta"]
    else:
        srt = ""
    if srt == "chapterword":
        lst1 = sorted(lst1, key=lambda x: int(x[4]))
    elif srt == "totalword":
        lst1 = sorted(lst1, key=lambda x: int(x[5]))
    tab = '<table class="table">\n' + tableh
    for s in lst1:
        tab += "<tr>"
        for i in s:
            tab += "<td>{}</td>\n".format(i)
        tab += "</tr>\n"
    tab += "</tbody></table>"
    index += "<p></p><br>\n" + tab + usertext
    return htmlfy(index, "HomePrime")

# They for my prime part
#prime func
def prime(num):
    if num == 2:
        return True
    if num == 1:
        return False
    i = 2
    num1 = num**0.5 +1
    while i <= num1:
        if num%i == 0:
            return False
        i += 1
    return True

# One big and One small prime to a non-prime number
def near_primes(num):
    if num == 1:
        return "bigger prime: 2"
    i = 1
    num1 = num
    while True:
        if prime(num1):
            break
        num1 = num - i
        i += 1
    i = 1
    num2 = num
    while True:
        if prime(num2):
            break
        num2 = num + i
        i += 1
    ind = """smaller prime:{}<br>
    bigger prime:{}
    """.format(str(num1),str(num2))
    return ind

# For make a random prime first I will take a normal number then I will convert it to one small prime.
def sprime(num):
        i = 1
        num1 = num
        while True:
            if prime(num1):
                break
            num1 = num - i
            i += 1
        return num1


def randgen():
    boyut = request.POST["rprime"]
    if boyut == "small":
        randnm = randint(1, 10 ** 6)
    elif boyut == "big":
        randnm = randint(10**6, 10 ** 9)
    index = """<p>Your Random Prime Number is {}.</p><br>
    <a href="/">Home</a>""".format(sprime(randnm))
    return htmlfy(index,"RandomPrime")

#Take the Request and with the functions above make a html code then return it.
def reqtry():
    try:
        try1 = request.GET["search"]
        try2 = int(try1)
        try3 = near_primes(try2)
        if try2 == 47:
            index = '<p>You Inputted my favorite Prime!</p><br>\n<a href="/">Input yer</a>'
        elif prime(try2):
            index = '<p>You Inputted a Prime Number</p><br>\n<a href="/">Input yer</a>'
        else:
            index = '<p>{} is not a Prime Number.</p>\n<p>{}</p><br>\n<a href="/">Input yer</a>'.format(try1, try3)
    except:
        index = '<p>Please Enter a Valid Value!</p><br>\n<a href="/"">Input yer</a>'
    return htmlfy(index, "Is Prime?")






route('/novelpage','POST',search)
route('/','GET',homepage)
route('/random','POST',randgen)
route('/second', 'GET', reqtry)

#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(True)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
  run()
