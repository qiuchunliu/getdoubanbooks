# f15() 注释版
# 获取豆瓣读书 港台类的书籍
# 包括 书名，作者，价格
import requests
from bs4 import BeautifulSoup

def get_soup(url):
	# 根据获取的 url 来返回一个 soup
	# 用于后续查找标签
	ht = requests.get(url)
	ht.encoding = ht.apparent_encoding
	htsoup = BeautifulSoup(ht.text, 'html.parser')
	return htsoup

def get_urllist():
	# 根据网页源码，找出 url 的规律
	# 创建一个 url 的列表
	# 用于后续的网页访问
	urllist = []
	url0 = 'https://book.douban.com'
	for i in range(0, 43):
		urllist.append(url0 + '/tag/港台?start={0}&type=T'.format(i * 20))
		# 网址开头 + 代表每页网址的代码
		# 返回一个 url 的列表
	return urllist

def get_book_item(soup):
	# 根据每个 soup 查找 li 的标签
	# 并且放在一个收集 li 标签的列表里
	bookitem = []
	for item in soup.find_all('li', class_='subject-item'):
		bookitem.append(item)  # !!!! 注意循环
	return bookitem

def get_contents(tag_list):
	# 根据获取的 li 标签来获取相关的内容
	bo_name = []
	bo_author = []
	bo_price = []
	for tag in tag_list:
		if tag.find('h2').a.find('span'):
			# 如果书名由两部分组成，则用这个 if
			name1 = tag.find('h2').a.get('title').strip().replace('\\n', '')
			# 去除换行、空格等
			name2 = tag.find('h2').a.span.text.strip().replace('\\n', '')
			bo_name.append(name1 + name2)
		else:
			bo_name.append(tag.find('h2').a.text.strip().replace('\\n', ''))
		bo_price.append(tag.find('div', class_='pub').string.split('/')[-1].replace("\n", "").replace(" ", ""))
		# 有的书没有显示价格
		bo_author.append(tag.find('div', class_='pub').string.split('/')[0].replace("\n", "").replace(" ", ""))
	contents = [bo_name, bo_author, bo_price]
	# 把书名列表，作者列表，价格列表放在一个总列表里，便于后续使用
	return contents

def main():
	url = get_urllist()
	all_item = []
	for link in url:
		soupp = get_soup(link)
		for li in get_book_item(soupp):
			# 这个 for 循环主要是把所有的 li 标签放在一起
			all_item.append(li)
	content = get_contents(all_item)
	return content

if __name__ == '__main__':
	conten = main()
	for n in range(len(conten[0])):
		# 长度由书名里列表的长度确定
		with open('tttt.csv', 'a', encoding='utf-8') as ff:
			# 如果没有 encoding='utf-8' 则会出现编码错误
			ff.write('{}, {}, {} \n'.format(conten[0][n], conten[1][n], conten[2][n]))
			# 这样可以写到 csv 文件里，用 excel 打开即可

