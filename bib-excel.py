import xlrd

file = xlrd.open_workbook('survey.xlsx')

# 作者的姓特殊或带中文 或者 论文名字有特殊字符或带中文
Special_papername = {
	'NLP': [
		'领域知识图谱研究综述',
		'新一代知识图谱关键技术综述',
		'知识表示学习研究进展',
		# '网络表示学习算法综述',
		# '神经机器翻译前沿综述',
		# 'Data-Driven Sentence Simplification: Survey and Benchmark',
		# 'Survey on the Use of Typological Information in Natural Language Processing',
		# 'From Word to Sense Embeddings: A Survey on Vector Representations of Meaning',
		# 'Recommender systems survey',
		# 'A reproducible survey on word embeddings and ontology-based methods for word similarity: Linear combinations outperform the state of the art',
		# 'Sentiment Analysis of Twitter Data: A Survey of Techniques',
		# 'Sentiment/Subjectivity Analysis Survey for Languages other than English',
	],
	'ML':[
		'Image/Video Deep Anomaly Detection: A Survey',
		# '网络表示学习算法综述',
		# 'Fusion of Federated Learning and Industrial Internet of Things: A Survey',
		# '机器学习的五大类别及其主要算法综述',
		# 'An Overview of Neural Network Compression',
		# '机器学习模型安全与隐私研究综述',
	]
}

dirs = ['Natural Language Processing', 'Machine Learning']

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

# 存放excel表格中所有的bib信息
exist_bib = {}

if __name__ == "__main__":
	for p, item in enumerate(['NLP', 'ML']):
		flag = False

		sheet = file.sheet_by_index(p)
		nrows = sheet.nrows
		ncols = sheet.ncols

		for i in range(1, nrows):
			row = sheet.row_values(i)
			
			paper_name = row[0].strip()
			paper_first_word = paper_name.replace(',', '').replace(':', '').split()[0]
			year = str(int(row[4]))
			author = row[2].strip().split(',')[0]
			first_name = author.strip().split()[-1]

			# 得到正确的bib名字
			name = first_name + year + paper_first_word
			category = row[1].strip()
			bib = '/bib/'+dirs[p]+'/'+category+'/'+name
			
			if bib in exist_bib.keys():
				exist_bib[bib] += 1
				bib += str(exist_bib[bib])
			else:
				exist_bib[bib] = 0
			# 得到最终的bib信息
			bib += '.md'
			
			# 目前表格中填的
			if len(row) == 7:
				bib_excel = row[6].strip()
				if bib != bib_excel or paper_name in Special_papername[item]:
					flag = True
					print('%d行引用列错误，请修改为%s' % (i+1, bib))
			else:
				flag = True
				print('%d行引用列为空，请输入%s' % (i+1, bib))

		success(flag, p)