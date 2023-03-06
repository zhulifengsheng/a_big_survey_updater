import xlrd

file = xlrd.open_workbook('survey.xlsx')

# 同名论文，不同作者
Special = {
	'NLP': [
		'word sense disambiguation: a survey', 
		'machine translation approaches and survey for indian languages',
	],
	'ML':
	[
		
	]
}

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

if __name__ == "__main__":
	for p, item in enumerate(['NLP', 'ML']):
		flag = False
		sheet = file.sheet_by_index(p)
		nrows = sheet.nrows

		total = set()

		for i in range(1, nrows):
			row = sheet.row_values(i)
			i = i + 1
			papername = ' '.join(row[0].strip().upper().lower().split())
			category = row[1].strip()
			
			# 将tuple(论文名字, 类别)加入集合total中
			if (papername, category) not in total:
				total.add((papername, category))
			else:
				if papername not in Special[item]:
					flag = True
					print('行数', i, papername)	# 输出有问题的论文
		
		success(flag, p)