from flask import (
	Flask,
	render_template,
	redirect,
	url_for,
	request,
	session,
	flash
)
from config import User,db #create tables
from flask_bcrypt import Bcrypt #to has passwords
from time import sleep #sleeping
from sqlalchemy import and_
from config import Books #create Book table
import sqlalchemy as sa 
from biblusi_api import MainClass # use API , which i made
import csv, urllib.request


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = ''.join(a for a in 'ofiefirefj34343434cidcjdcd')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite'
db.init_app(app)
	

''' თუ ფაილს გადმოიწერთ ქვემო ორ ხაზზე მოცემული კოდს
ერთხელ გაუკეთეთ ანკომენტირება, რომ შეიქმნას ტეიბლები ცხრილში,
შექმნის შემდეგ კი ისევ დააკომენტარეთ '''	

# with app.app_context():
# 	db.create_all()


rows = []
with open('biblusi.csv','r',encoding='utf-8_sig') as file:
	csvreader = csv.reader(file)
	header = next(csvreader)
	for row in csvreader:
		rows.append(row)
	file.close()


''' ამ მონაკვეთში .csv ფაილიდან მოგვაქვს შენახული ლინკები	
	და urllib.request.retrieve() –ის გამოყენებით ვინახავთ
	'images' საქაღალდეში '''

def save_imgs():
	img_urls = []
	img_title = []
	with open('biblusi.csv','r',encoding='utf-8_sig') as f:
		csvreader = csv.reader(f)
		header = next(csvreader)
		for url in csvreader:
			img_urls.append(url[3])

	for x in range(len(img_urls)):
		url = img_urls[x]	
		filename = f"C:/Users/sann/Desktop/python_homework/lastquizz/static/images/filename0{x}.jpg"
		urllib.request.urlretrieve(str(url),filename)

# save_imgs()

@app.route('/home')
@app.route('/',methods=['POST','GET'])
def home():
	lst = []
	titles, authors, prices = [],[],[]
	for x in range(len(rows)):
		titles.append(rows[x][0])
		authors.append(rows[x][1])
		prices.append(rows[x][2])
	# print(img_urls)
	ammount_of_books = len(titles)
	return render_template('home.html',book_ammount=ammount_of_books,titles=titles,authors=authors,prices=prices)


@app.route('/logout')
def logout():
	if 'username' in session:
		flash('თქვენ გახვედით სისტემიდან. ','success')
		session.pop('username',None)

	return redirect(url_for('home'))


@app.route('/register',methods=['POST','GET'])
def register():
	if request.method == "POST":
		password = request.form['password']
		username = request.form['username']
		filtered_user = User.query.filter_by(username=username).first()
		if username=='' or password=='':
			flash('ყველა ველი სავალდებულოა!','error')

		elif filtered_user:
			flash(f'მომხარებელი {username}-თ უვკე არსებობს.')

		elif not filtered_user:
			hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
			u1 = User(username=username,password=hashed_password)
			db.session.add(u1)
			db.session.commit()
			flash('თქვენ წარმატებით გაიარეთ რეგისტრაცია :) ','success')
			return redirect(url_for('login')) 

	return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
	if request.method == "POST":
		input_username = request.form['username']
		input_password = request.form['password']

		if input_username != '' and input_password != '':
			check_username = User.query.filter_by(username=input_username).first()
			if check_username:
				check_password = bcrypt.check_password_hash(check_username.password,input_password)
				if check_password:	
					session['username'] = input_username
					return redirect(url_for('home'))

			else:
				flash('მომხმარებლის სახელი ან პაროლი არასწორია.','error')
		
		else:
			flash('ყველა ველი სავალდებულოა!','error')

	return render_template('login.html')


@app.route('/user',methods=['POST','GET'])
def user():
	return render_template('user.html')


@app.route('/books/<img_src_inc>/<title>/<price>',methods=['POST','GET'])
def books(img_src_inc,title,price):
	return render_template('books.html',img_src_inc=img_src_inc,title=title,price=price)


if __name__=="__main__":
	app.run(debug=True)