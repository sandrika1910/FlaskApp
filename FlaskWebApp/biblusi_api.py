import requests,csv
from bs4 import BeautifulSoup as bs
from time import sleep
from fake_useragent import UserAgent
import re,random
	
class MainClass:
	def __init__(self):
		# super().__init__(soup,url,r,header)
		pass
	def get_book_titles(self):
		self.page_increment = 1
		''' titles, prices,authors lists '''
		self.book_titles_lst = []
		self.book_prices_lst = []
		self.book_authors_lst = []
		self.book_img_urls = []

		f = open('anotherbiblusi.csv','w',encoding="utf-8_sig",newline='\n')
		f_obj = csv.writer(f)
		f_obj.writerow(['წიგნის სათაური','წიგნის ავტორი','წიგნის ფასი','წიგნის ფოტოს მისამართი'])


		while True:
			self.url = 'https://biblusi.ge/products?page={}&category=291&category_id=293'.format(self.page_increment)
			self.ua = UserAgent()
			self.header = {'User-Agent':str(self.ua.chrome)}
			self.r = requests.get(self.url,headers=self.header)
			self.soup = bs(self.r.text,'html.parser')
			self.sub_soup = self.soup.find_all('div',class_='mb-1_875rem col-sm-4 col-md-3 col-xl-2 col-6')
			self.book_title = self.soup.find_all('acronym') 
			self.book_prices = self.soup.find_all('div',class_='text-primary font-weight-700')	

			''' append book's prices in the list '''
			for self.book_price in self.book_prices:
				self.book_prices_lst.append(self.book_price.text.strip())

			''' add titles of books in the self.book_title_lst '''
			for self.title in self.book_title:
				# if self.title['title'] not in self.book_titles_lst:
				self.book_titles_lst.append(self.title['title'])

			''' prettify items of the book_prices_lst  '''
			for self.x in range(len(self.book_prices_lst)):
				self.book_prices_lst[self.x] = self.book_prices_lst[self.x][0:5].strip()
				# print(self.book_prices_lst[self.x])

			self.author_names_link = self.soup.find_all('a',class_='d-block')
			for self.author in self.author_names_link:
				''' აქ ახალ რიქვესთს ვგზავნი სხვა ფეიჯზე, რადგანაც იგივე
				 ფეიჯიდან არ მოაქვს ავტორის სახელები. მიწევს ანქორ თეგის
				 "href" ატრიბუტი წამოვიღო და მთავარ url –ს დავუმატო, რითაც
				 გადავდივარ უკვე სხვა ფეიჯზე და იქედან მომაქვ ავტორების
				 სახელები. ამიტომაც სერვერზე ორმაგი რაოდენობით მიწევს მოთხოვნის გაგზავნა'''
				
				self.new_url = 'https://biblusi.ge' + str(self.author['href'])
				sleep(random.randint(8,15))
				self.new_r = requests.get(self.new_url,headers=self.header).text
				self.new_soup = bs(self.new_r,'html.parser')

				self.author_name = self.new_soup.find('div',class_='author-name')
				self.img_div = self.new_soup.find('div',class_='book-img-bg')
				self.img_url = self.img_div.contents[2]['src']
				self.book_img_urls.append(self.img_url)
				''' ზოგჯერ ავტორები არაა მითითებული საიტზე და ცარიელი 
				სტრინგის ნაცვლად ვაბრუნებ Null –ს ავტორის მნიშვნელობად.
				'''

				if len(self.author_name.text.strip())>0:
					self.book_authors_lst.append(self.author_name.text.strip())
				else:
					self.book_authors_lst.append('Null')
			
			if self.page_increment == 2:
				for self.x in range(len(self.book_prices_lst)):
					f_obj.writerow([self.book_titles_lst[self.x],self.book_authors_lst[self.x],self.book_prices_lst[self.x],self.book_img_urls[self.x]])
				
					# print('წიგნის დასახელება - "{}". | წიგნის ავტორი – "{}". | წიგნის ფასი - {}₾'.format(self.book_titles_lst[self.x],self.book_authors_lst[self.x],self.book_prices_lst[self.x]),end='\n')
				print('ოპერაცია დასრულებულია. ყველა მონაცემი შენახულია ფაილში. ')
				break
			else:
				print('მიმდინარეობს მე–{} გვერდიდან ინფორმაციის წამოღება...'.format(self.page_increment))
				sleep(random.randint(12,20))

			self.page_increment += 1
