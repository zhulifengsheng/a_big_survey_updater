import xlrd
import os
import shutil

file = xlrd.open_workbook('survey.xlsx')
bib_path = os.path.join(os.getcwd(), 'bib')
extra_bib_path = os.path.join(os.getcwd(), 'extra-bib')	# 多余的md文件存在的这里

dirs = ['Natural-Language-Processing', 'Machine-Learning']

def success(flag, i):
	if flag == False:
		if i == 0:
			print("NLP无报错，通过\n")
		else:
			print("ML无报错，通过\n")
	else:
		if i == 0:
			print("NLP有报错，不通过\n")
		else:
			print("ML有报错，不通过\n")

def empty(path):
	#print(path)
	r = ''
	with open(path, 'r', encoding='utf-8-sig') as f:
		for l in f:
			r += l
	if r == '':
		return True
	return False

if __name__ == "__main__":
	for p in range(2):
		if p == 1:
			continue
		flag = False
		
		total = set()	# 记录当前'Natural-Language-Processing' 或 'Machine-Learning'中所有的md文件
		
		filelist = os.listdir(os.path.join(bib_path, dirs[p]))
		# 记录当前'Natural-Language-Processing' 或 'Machine-Learning'中所有的md文件 到 total中
		for i in filelist:
			x = os.listdir(os.path.join(bib_path, dirs[p], i))
			for k in x:
				total.add(os.path.join(bib_path, dirs[p], i, k))

		sheet = file.sheet_by_index(p)
		nrows = sheet.nrows

		# NLP or ML 的bib文件夹地址
		bib_dir = os.path.join(bib_path, dirs[p])

		for i in range(1, nrows):	# 以excel中的每行来遍历
			row = sheet.row_values(i)

			bib_category = row[6].strip().split('/')[-2].replace(' ', '-')
			bib_name = row[6].strip().split('/')[-1]
			
			# 当前excel中这行md文件所在路径
			filepath = os.path.join(bib_dir, bib_category, bib_name)
			
			# md文件路径不存在
			if not os.path.exists(filepath):	# os.path.exists()对大小写不敏感
				flag = True
				print('第%d行的md文件路径不存在, 请在类别%s中创建%s' % (i+1, bib_category, bib_name))
			
			# md文件路径存在
			else:
				try:	
					total.remove(filepath)
				except:		# 出现大小写不一致的情况时，同不存在该md文件
					flag = True
					print('第%d行的md文件路径不存在, 请在类别%s中创建%s' % (i+1, bib_category, bib_name))
			
		# print('有%d个文件是多余的' % len(total))
		for i in total:
			if not os.path.exists(extra_bib_path):
				os.mkdir(extra_bib_path)
			shutil.move(i, os.path.join(extra_bib_path, i.strip().split('\\')[-1]))
			
		success(flag, p)