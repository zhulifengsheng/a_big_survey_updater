import xlrd

file = xlrd.open_workbook('survey.xlsx')

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
	for p in range(2):
		# if p == 0:
		# 	continue
		flag = False
		sheet = file.sheet_by_index(p)
		nrows = sheet.nrows
		ncols = sheet.ncols
		dic = {}
		for i in range(1, nrows):
			row = sheet.row_values(i)
			
			bib_category = row[6].strip().split('/')[-2]
			bib_name = row[6].strip().split('/')[-1].split('.')[0]
			
			if bib_category not in dic.keys():
				dic[bib_category] = [bib_name]
			elif bib_name in dic[bib_category]:
				flag = True
				print('%d行错误，%s类下面有同名的bib信息%s' % (i+1, bib_category, bib_name))
				
			else:
				dic[bib_category].append(bib_name)

		success(flag, p)
