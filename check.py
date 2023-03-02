import xlrd
import requests
import time
import re
import html as HTML

file = xlrd.open_workbook('survey.xlsx')

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
}

# 这里记录通过代码没有在HTML页面中找到论文名字，但是人工访问链接后确认HTML页面里面有论文名字的特例
Special_url = {
	'NLP': [
		'https://www.mitpressjournals.org/doi/pdf/10.1162/COLI_a_00370',
		'https://www.sciencedirect.com/science/article/abs/pii/S0167923616300173',
		'http://ceur-ws.org/Vol-1988/LPKM2017_paper_15.pdf',
		'http://ceur-ws.org/Vol-779/derive2011_submission_1.pdf',
		'https://www.sciencedirect.com/science/article/pii/S266665102100005X/pdfft?md5=3983861e9ae91ce7b45f0c5533071077&pid=1-s2.0-S266665102100005X-main.pdf',
		'https://www.sciencedirect.com/science/article/abs/pii/S1574013719301297',
		'https://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00519/2060745/tacl_a_00519.pdf',
		'https://onlinelibrary.wiley.com/doi/epdf/10.1002/widm.1389',
		'http://www.semantic-web-journal.net/system/files/swj1167.pdf',
		'https://www.sciencedirect.com/science/article/pii/S2666651021000061/pdfft?md5=41dae412c5802b063f8ff0615ba12622&pid=1-s2.0-S2666651021000061-main.pdf',
		'http://www.c-s-a.org.cn/html/2020/6/7431.html#top',
		'https://www.sciencedirect.com/science/article/abs/pii/S0031320316303399',
		'https://arxiv.org/abs/1903.12394',
		'https://arxiv.org/abs/2105.14875',
		'http://www.aclclp.org.tw/clclp/v18n1/v18n1a3.pdf',
		'https://www.sciencedirect.com/science/article/pii/S2666651020300024',
		'https://nlp.cs.nyu.edu/sekine/papers/li07.pdf',
		'https://www.sciencedirect.com/science/article/pii/S0885230801901743',
		'http://krchowdhary.com/ai/ai14/lects/nlp-research-com-intlg-ieee.pdf',
		'https://www.sciencedirect.com/science/article/pii/S2095809919304928',
		'https://dspace.mit.edu/bitstream/handle/1721.1/116314/10462_2017_9588_ReferencePDF.pdf?sequence=2&isAllowed=y',
		'https://www.sciencedirect.com/science/article/pii/S1532046419302436',
		'https://aclanthology.org/2022.acl-demo.10.pdf',
		'https://www.sciencedirect.com/science/article/pii/S0020025511003860',
		'https://www.sciencedirect.com/science/article/pii/S1877050915034663',
		'https://www.mdpi.com/2076-3417/10/21/7640/html',
		'https://www.sciencedirect.com/science/article/abs/pii/S0140366413001722',
		'https://downloads.hindawi.com/archive/2009/421425.pdf',
		'https://link.springer.com/article/10.1007/s10844-018-0542-3',
		'http://staff.ustc.edu.cn/~hexn/papers/www18-tutorial-deep-matching-paper.pdf',
		'https://www.sciencedirect.com/science/article/abs/pii/S0950705117300680',
		'https://www.sciencedirect.com/science/article/abs/pii/S0950705113001044',
		'https://doi.org/10.1016/j.elerap.2019.100879',
		'https://watermark.silverchair.com/coli_a_00371.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAAqUwggKhBgkqhkiG9w0BBwagggKSMIICjgIBADCCAocGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMwFfpYsXe-j1WZLOYAgEQgIICWK8_os-_3bOw2Egxl-QP8k6_eaUBXbfLcdwSiN1AKd2RyuDFyjIlDYSZ5NTAAsDgDlMCD3TrhPG0ikKF7P7kuegNT5PvSubob_GmEmkrscxcBW6EJJepel-bEup-_A22uwRLCznueNRO_TIF1YCNc5jsTEopV_PzSEeI-vqG3BTbc_EtWxty9udu1sZYsHmXO2i8h7_m5MGt3nCX8aXXNkRPhrmNZ4IHU2moi76_JOuBQb6U6n6SItsdwObWewSPB3eGmx4DmUboNcB-Dv7OJAS9jmWHgsNzsSiRw9lRBcsf1O_0Nkv5YkFSkVNTiCldQ3B1fWgjDN0GWSOTsMS-6Je6keFnovcc8nQnxw-ubXQ57UZYQjZHa8jg6Ea1kOUHJem8uRdc4IMJuKCunIKRJLT1SSLFGYDgehwxQfOQk-H6LOIsbWOaiXwP9aDDqG4a6Pxl_bwnpi8JUp5dQYvqLNteQ-rjGS8FbRvlaV34wL49UAEBwa2DFlkTVhebzCkrzuzN-H3obLkhqnR-LDXbjSQhYOzROGh74Gq-beWVM7boVegN49iq-El7CzRqnoTIzVjtBrp3b-tnaevilOo05l0s2rhFLr-46GRyXgD11UTbz0tCy892aJACw6XYCsRvx2veM2tzBxg5D6a65ev1F3ViYbOlyz99M11QLllIMdoRT1R5fkdEyFrDQh-Q6VCJT3tJAOdlhWCc6kpie4jME3xACsVXSKXIW4q7OCXDHtdvmQnUWWJURJAYZ2Rwfvc9JwQ20jY37wr5ZyyQ8VuiRXwkiiOK4EScHg',
		'https://doi.org/10.1504/IJSNM.2015.069773',
		'https://www.sciengine.com/SSI/doi/10.1360/SSI-2021-0329',
		'https://www.sciencedirect.com/science/article/pii/S0952197619301745',
		'http://ceur-ws.org/Vol-1883/invited6.pdf',
		'http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.153.8457&rep=rep1&type=pdf',
		'http://cse.iitkgp.ac.in/~saptarshi/courses/socomp2020a/sentiment-analysis-survey-yue2019.pdf',
		'https://www.sciencedirect.com/science/article/pii/S2090447914000550',
		'https://aclanthology.org/2021.acl-long.107.pdf',
		'https://openreview.net/pdf?id=N0n_QyQ5lBF',
		'https://aclanthology.org/2022.acl-long.524.pdf',
		'https://www.sciencedirect.com/science/article/pii/S1319157820303554',
		'https://aclanthology.org/2021.eacl-main.160.pdf',
		'https://aclanthology.org/2020.emnlp-main.33.pdf',
		'https://wires.onlinelibrary.wiley.com/doi/epdf/10.1002/wics.195',
		'https://link.springer.com/article/10.1007/BF00058766',
		'https://www.sciencedirect.com/science/article/abs/pii/S0306457317305757',
		'https://arxiv.org/abs/2004.03705',
	],
	'ML': [

	],
}

# ML
# 	'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9363463',
# 	'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7352306',
# 	'http://doras.dcu.ie/25121/1/ACCESS3031549.pdf',
# 	'https://link.springer.com/content/pdf/10.1007/s10458-019-09433-x.pdf',
# 	'http://www.macs.hw.ac.uk/~ic14/IoannisChalkiadakis_RRR.pdf',
# 	'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9233366',
# 	'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8466590',
# 	'https://cs.nju.edu.cn/_upload/tpl/01/0b/267/template267/zhouzh.files/publication/nsr18.pdf',
# 	'https://www.aclweb.org/anthology/P19-4007.pdf',
# 	'https://arxiv.org/abs/1808.03591',	# arXiv网页上是?，没有:
# 	'https://arxiv.org/abs/1901.11303',	# arXiv网页上是Hyperbox based，没有- 
# 	'https://arxiv.org/abs/1804.11191', # arXiv网页上是network see，excel上是networks see
# 	'https://arxiv.org/abs/2006.00632',	# arXiv网页上是---，excel上是 - 
# 	'https://arxiv.org/abs/1012.4051',	# 标题中有&，html代码显示不出&
# 	'http://www.rjdk.org/thesisDetails#10.11907/rjdk.182932&lang=zh',	# 该网页html没有论文信息
# 	'https://wires.onlinelibrary.wiley.com/doi/abs/10.1002/widm.1139',	# 该网页html没有论文信息

# 这里记录dblp检索不到的论文的信息
Special_papername = {
	'NLP': {
		'Neural Approaches to Conversational AI: Question Answering, Task-oriented Dialogues and Social Chatbots': ('Now Foundations and Trends', '2019', 'Jianfeng Gao, Michel Galley, Lihong Li'),
		'A Survey on Deep Learning Event Extraction: Approaches and Applications': ('arXiv', '2021', 'Qian Li, Jianxin Li, Jiawei Sheng, Shiyao Cui, Jia Wu, Yiming Hei, Hao Peng, Shu Guo, Lihong Wang, Amin Beheshti, Philip S. Yu'),
		'A survey of embedding models of entities and relationships for knowledge graph completion': ('arXiv', '2017', 'Dat Quoc Nguyen'),
		'A Survey of Techniques for Constructing Chinese Knowledge Graphs and Their Applications': ('Sustainability', '2018', 'Tianxing Wu, Guilin Qi, Cheng Li, Meng Wang'),
		'Knowledge Graphs': ('ACM Comput. Surv.', '2021', "Aidan Hogan, Eva Blomqvist, Michael Cochez, Claudia d'Amato, Gerard de Melo, Claudio Gutiérrez, Sabrina Kirrane, José Emilio Labra Gayo, Roberto Navigli, Sebastian Neumaier, Axel-Cyrille Ngonga Ngomo, Axel Polleres, Sabbir M. Rashid, Anisa Rula, Lukas Schmelzeisen, Juan Sequeda, Steffen Staab, Antoine Zimmermann"),
		'领域知识图谱研究综述': ('计算机系统应用', '2020', '刘烨宸, 李华昱'),
		'新一代知识图谱关键技术综述': ('计算机研究与发展', '2022', '王萌, 王昊奋, 李博涵, 赵翔, 王鑫'),
		'知识表示学习研究进展': ('计算机研究与发展', '2016', '刘知远, 孙茂松, 林衍凯, 谢若冰'),
		'Towards a Robust Deep Neural Network in Texts: A Survey': ('arXiv', '2019', 'Wenqi Wang, Lina Wang, Run Wang, Zhibo Wang, Aoshuang Ye'),
		'网络表示学习算法综述': ('计算机科学', '2020', '丁钰, 魏浩, 潘志松, 刘鑫'),
		'Machine Translation Evaluation Resources and Methods: A Survey': ('Ireland Postgraduate Research Conference', '2018', 'Lifeng Han'),
		'神经机器翻译前沿综述': ('中文信息学报', '2020', '冯洋, 邵晨泽'),
		'A survey of named entity recognition and classification': ('Lingvisticae Investigationes', '2007', 'David Nadeau, Satoshi Sekine'),
		'Recent Advances in Natural Language Inference: A Survey of Benchmarks, Resources, and Approaches': ('arXiv', '2019', 'Shane Storks, Qiaozi Gao, Joyce Y Chai'),
		'Chinese Word Segmentation: A Decade Review': ('Journal of Chinese Information Processing', '2007', 'Changning Huang, Hai Zhao'),
		'Natural Language Processing - A Survey': ('arXiv', '2012', 'Kevin Mote'),
		'Progress in Neural NLP: Modeling, Learning, and Reasoning': ('Engineering', '2020', 'Ming Zhou, Nan Duan, Shujie Liu, Heung-Yeung Shum'),
		'文档智能: 数据集、模型和应用': ('中文信息学报', '2022', '崔磊, 徐毅恒, 吕腾超, 韦福如'),
		'Question Answering Systems: Survey and Trends': ('Procedia Computer Science', '2015', 'Abdelghani Bouziane, Djelloul Bouchiha, Noureddine Doumi, Mimoun Malki'),
		'基于隐私保护的联邦推荐算法综述': ('自动化学报', '2022', '张洪磊, 李浥东, 邬俊, 陈乃月, 董海荣'),
		'Adversarial Machine Learning in Recommender Systems-State of the art and Challenges': ('arXiv', '2020', 'Yashar Deldjoo, Tommaso Di Noia, Felice Antonio Merra'),
		'Recommender systems survey': ('Knowl. Based Syst.', '2013', 'Bobadilla J., Ortega F., Hernando A., Gutiérrez A.'),
		'Survey for Trust-aware Recommender Systems: A Deep Learning Perspective': ('arXiv', '2020', 'Manqing Dong, Feng Yuan, Lina Yao, Xianzhi Wang, Xiwei Xu, Liming Zhu'),
		'基于联邦学习的推荐系统综述': ('中国科学:信息科学', '2022', '梁锋, 羊恩跃, 潘微科, 杨强, 明仲'),
		'Survey of Computational Approaches to Lexical Semantic Change': ('arXiv', '2018', 'Nina Tahmasebi, Lars Borin, Adam Jatowt'),
		'Sentiment analysis algorithms and applications: A survey': ('Ain Shams Engineering Journal', '2014', 'Walaa Medhat, Ahmed Hassan, Hoda Korashy'),
		'Sentiment Analysis of Twitter Data: A Survey of Techniques': ('IJCAI', '2016', 'Vishal.A.Kharde, Prof. Sheetal.Sonawane'),
		'Deep Emotion Recognition in Dynamic Data using Facial, Speech and Textual Cues: A Survey': ('TechRxiv', '2021', 'Tao ZhangTao Zhang, Zhenhua Tan'),
		'Speech and Language Processing': ('Stanford', '2019', 'Dan Jurafsky, James H. Martin'),
		'多模态信息处理前沿综述:应用、融合和预训练': ('中文信息学报', '2022', '吴友政, 李浩'),
		'Deep Learning Based Abstractive Text Summarization: Approaches, Datasets, Evaluation Measures, and Challenges': ('Mathematical Problems in Engineering', '2020', 'Dima Suleiman, Arafat Awajan'),
		'Part‐of‐speech tagging': ('Wiley Interdisciplinary Reviews: Computational Statistics', '2011', 'Angel R. Martinez'),
		'Syntactic Parsing: A Survey': ('Computers and the Humanities', '1989', 'Alton F. Sanders and Ruth H. Sanders'),
		'A Survey on In-context Learning': ('arXiv', '2023', 'Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Zhiyong Wu, Baobao Chang, Xu Sun, Jingjing Xu, Lei Li, Zhifang Sui'),
		'A Survey on Model Compression and Acceleration for Pretrained Language Models': ('arXiv', '2022', 'Canwen Xu, Julian J. McAuley'),
		'A Survey on Accuracy-oriented Neural Recommendation: From Collaborative Filtering to Information-rich Recommendation': ('arXiv', '2021', 'Le Wu, Xiangnan He, Xiang Wang, Kun Zhang, Meng Wang'),
		'Automatic Speech Recognition And Limited Vocabulary: A Survey': ('arXiv', '2021', 'Jean Louis K. E. Fendji, Diane C. M. Tala, Blaise O. Yenke, Marcellin Atemkeng')
	},
	'ML': {

	}
}

# 	# 通过excel链接找到的
# 	'Network representation learning: A macro and micro view': ('AI Open', '2021', 'Xueyi Liu, Jie Tang'),	
# 	# 通过arXiv网页信息找到的
# 	'Survey of Expressivity in Deep Neural Networks': ('NIPS', '2016', 'Maithra Raghu, Ben Poole, Jon Kleinberg, Surya Ganguli, Jascha Sohl-Dickstein'),		
# 	# 通过excel链接找到的
# 	'Comprehensive Review of Deep Reinforcement Learning Methods and Applications in Economics': ('Mathematics', '2020', 'Amirhosein Mosavi, Yaser Faghan, Pedram Ghamisi, Puhong Duan, Sina Faizollahzadeh Ardabili, Ely Salwana, Shahab S. Band'),	
# 	# 通过excel链接找到的
# 	'A Survey on Surrogate Approaches to Non-negative Matrix Factorization': ('Vietnam journal of mathematics', '2018', 'Pascal Fernsel, Peter Maass'),	
# 	# 通过arXiv网页信息找到的
# 	'Graph Representation Learning: A Survey': ('APSIPA Transactions on Signal and Information Processing', '2020', 'Fenxiao Chen, Yuncheng Wang, Bin Wang, C.-C. Jay Kuo'),
# 	# 通过google学术找到的
# 	'Meta-Learning in Neural Networks: A Survey': ('TPAMI', '2021', 'Timothy Hospedales, Antreas Antoniou, Paul Micaelli, Amos Storkey'),
# 	# 通过google学术找到的
# 	'A Survey on Multi-Task Learning': ('IEEE Trans. Knowl. Data Eng.', '2021', 'Yu Zhang, Qiang Yang'),
# 	# 通过arXiv网页信息找到的
# 	'A Survey on Semi-Supervised Learning Techniques': ('IJCTT', '2014', 'V. Jothi Prakash, Dr. L.M. Nithya'),
# 	# dblp上的作者信息不对，pdf中有两个，dblp只检索出一个
# 	'Transfer Adaptation Learning: A Decade Survey': ('arXiv', '2019', 'Lei Zhang, Xinbo Gao'),
# 	},
# 	# dblp检索不到的论文, 检查期刊会议 年份 作者
# 	{
# 	# 通过excel链接找到的
# 	'A Review of Binarized Neural Networks': ('Electronics', '2019', 'Taylor Simons, Dah-Jye Lee'),	
# 	# 通过excel链接找到的
# 	'A State-of-the-Art Survey on Deep Learning Theory and Architectures': ('Electronics', '2019', 'Md Zahangir Alom, Tarek M. Taha, Chris Yakopcic, Stefan Westberg, Paheding Sidike, Mst Shamima Nasrin, Mahmudul Hasan, Brian C. Van Essen, Abdul A. S. Awwal and Vijayan K. Asari'),	
# 	'A Survey on Vision Transformer': ('arXiv', '2020', 'Kai Han, Yunhe Wang, Hanting Chen, Xinghao Chen, Jianyuan Guo, Zhenhua Liu, Yehui Tang, An Xiao, Chunjing Xu, Yixing Xu, Zhaohui Yang, Yiman Zhang, Dacheng Tao'),
# 	# 通过arXiv网页信息找到的
# 	'A continual learning survey: Defying forgetting in classification tasks': ('TPAMI', '2021', 'Matthias De Lange, Rahaf Aljundi, Marc Masana, Sarah Parisot, Xu Jia, Ales Leonardis, Gregory Slabaugh, Tinne Tuytelaars'),	
# 	'A Survey of Black-Box Adversarial Attacks on Computer Vision Models': ('arXiv', '2019', 'Siddhant Bhambri, Sumanyu Muku, Avinash Tulasi, Arun Balaji Buduru'),
# 	'Deep Learning for Instance Retrieval: A Survey': ('arXiv', '2021', 'Wei Chen, Yu Liu, Weiping Wang, Erwin Bakker, Theodoros Georgiou, Paul Fieguth, Li Liu, Michael S. Lew'),
# 	'MmWave Radar and Vision Fusion for Object Detection in Autonomous Driving: A Review': ('arXiv', '2021', 'Zhiqing Wei, Fengkai Zhang, Shuo Chang, Yangyang Liu, Huici Wu, Zhiyong Feng'),
# 	# 通过arXiv网页信息找到的
# 	'A Survey on Curriculum Learning': ('TPAMI', '2021', 'Xin Wang, Yudong Chen, Wenwu Zhu'),	
# 	'A Survey on Active Deep Learning: From Model-driven to Data-driven': ('arXiv', '2021', 'Peng Liu, Lizhe Wang, Guojin He, Lei Zhao'),	
# 	'A Survey on Assessing the Generalization Envelope of Deep Neural Networks: Predictive Uncertainty, Out-of-distribution and Adversarial Samples': ('arXiv', '2020', 'Julia Lust, Alexandru Paul Condurache'),
# 	# dblp能检索到，不过代码里request访问的方式检索不到，名字太短搜出来的东西太多
# 	'Deep learning': ('Nat.', '2015', 'Yann LeCun, Yoshua Bengio, Geoffrey Hinton'),	
# 	# 通过excel链接找到的
# 	'Embracing Change: Continual Learning in Deep Neural Networks': ('Trends in Cognitive Sciences', '2020', 'Raia Hadsell, Dushyant Rao, Andrei A. Rusu, Razvan Pascanu'),
# 	# 通过excel链接找到的
# 	'Network representation learning: an overview': ('SCIENTIA SINICA Informationis', '2017', 'Cunchao TU, Cheng YANG, Zhiyuan LIU, Maosong SUN'),	
# 	# 通过excel链接找到的
# 	'Time-series forecasting with deep learning: a survey': ('Philosophical Transactions of the Royal Society A', '2021', 'Bryan Lim, Stefan Zohren'),
# 	# 通过excel链接找到的
# 	'网络表示学习算法综述': ('计算机科学', '2020', '丁钰, 魏浩, 潘志松, 刘鑫'),	
# 	# 没找到出处，paper上面写个某个大学
# 	'A Survey of Exploration Strategies in Reinforcement Learning': ('McGill University', '2003', 'R. McFarlane'),	
# 	'Deep Model-Based Reinforcement Learning for High-Dimensional Problems, a Survey': ('arXiv', '2020', 'Aske Plaat, Walter Kosters, Mike Preuss'),	
# 	'Towards Utilizing Unlabeled Data in Federated Learning: A Survey and Prospective': ('arXiv', '2020', 'Yilun Jin, Xiguang Wei, Yang Liu, Qiang Yang'),	
# 	'Survey & Experiment: Towards the Learning Accuracy': ('arXiv', '2010', 'Zeyuan Allen Zhu'),
# 	# 通过知网找到的
# 	'机器学习的五大类别及其主要算法综述': ('软件导刊', '2019', '李旭然, 丁晓红'),
# 	'Stabilizing Generative Adversarial Networks: A Survey': ('arXiv', '2019', 'Maciej Wiatrak, Stefano V. Albrecht, Andrew Nystrom'),
# 	# 通过excel链接找到的
# 	'Robustness of deep learning models on graphs: A survey': ('AI Open', '2021', 'Jiarong Xu, Junru Chen, Siqi You, Zhiqing Xiao, Yang Yang, Jiangang Lu'),
# 	# 通过google学术找到的
# 	'A brief survey of visualization methods for deep learning models from the perspective of Explainable AI': ('macs.hw.ac.uk', '2018', 'Ioannis Chalkiadakis'),
# 	# 通过excel链接找到的
# 	'Machine Learning Interpretability: A Survey on Methods and Metrics': ('Electronics', '2019', 'Diogo V. Carvalho, Eduardo M. Pereira, Jaime S. Cardoso'),
# 	# 通过google学术找到的
# 	'On Interpretability of Artificial Neural Networks: A Survey': ('IEEE Transactions on Radiation and Plasma Medical Sciences', '2021', 'Feng-Lei Fan, Jinjun Xiong, Mengzhou Li, Ge Wang'),
# 	# 通过excel链接找到的
# 	'A guide to deep learning in healthcare': ('Nature Medicine', '2019', 'Andre Esteva, Alexandre Robicquet, Bharath Ramsundar, Volodymyr Kuleshov, Mark DePristo, Katherine Chou, Claire Cui, Greg Corrado, Sebastian Thrun, Jeff Dean'),
# 	# 通过arXiv网页信息找到的
# 	'A Survey on Deep Learning-based Non-Invasive Brain Signals:Recent Advances and New Frontiers': ('Journal of Neural Engineering', '2021', 'Xiang Zhang, Lina Yao, Xianzhi Wang, Jessica Monaghan, David McAlpine, Yu Zhang'),
# 	'Graph Representation Learning in Biomedicine': ('arXiv', '2021', 'Michelle M. Li, Kexin Huang, Marinka Zitnik'),
# 	# 通过excel链接找到的
# 	'An overview of multi-task learning': ('National Science Review', '2017', 'Yu Zhang, Qiang Yang'),
# 	# 通过arXiv网页信息找到的
# 	'Multi-Task Learning for Dense Prediction Tasks: A Survey': ('TPAMI', '2021', 'Simon Vandenhende, Stamatios Georgoulis, Wouter Van Gansbeke, Marc Proesmans, Dengxin Dai, Luc Van Gool'),
# 	# 没找到出处，citeseerx是个和arXiv类似的网站
# 	'Convex Optimization Overview': ('citeseerx', '2008', 'Zico Kolter, Honglak Lee'),
# 	# 通过google学术找到的
# 	'A brief introduction to weakly supervised learning': ('National Science Review', '2017', 'Zhi-Hua Zhou'),
# 	'A survey on domain adaptation theory: learning bounds and theoretical guarantees': ('arXiv', '2020', 'Ievgen Redko, Emilie Morvant, Amaury Habrard, Marc Sebban, Younès Bennani'),
# 	'A Survey on Negative Transfer': ('arXiv', '2020', 'Wen Zhang, Lingfei Deng, Lei Zhang, Dongrui Wu'),
# 	# 通过excel链接找到的 
# 	'机器学习模型安全与隐私研究综述': ('软件学报', '2021', '纪守领, 杜天宇, 李进锋, 沈超, 李博'),
# 	'A Survey on Graph Structure Learning: Progress and Opportunities': ('arXiv', '2021', 'Yanqiao Zhu, Weizhi Xu, Jinghao Zhang, Yuanqi Du, Jieyu Zhang, Qiang Liu, Carl Yang, Shu Wu'),

def _change_arxiv(url):
	'''
	把网址 https://arxiv.org/pdf/2105.04387.pdf 转换为 https://arxiv.org/abs/2105.04387
	把网址 https://arxiv.org/pdf/2105.04387 转换为 https://arxiv.org/abs/2105.04387
	'''
	res = url
	if 'arxiv' in url:
		res = url.split('/')
		res[-2] = 'abs'
		if url[-3:] == 'pdf':
			res[-1] = res[-1][:-4]
		return '/'.join(res)
	else:
		return res

def _uncased_same(str1, str2):
	'''
	判断两个字符串是否一样
	'''
	if str1.upper().lower() == str2.upper().lower():
		return True
	return False

def check_paper_url(row, which, i):
	url = row[-2].strip()
	
	url = _change_arxiv(url)
	try:
		response = requests.get(url, headers=headers, timeout=10)
	except:
		print('第{}行的url链接访问失败，URL链接为{}'.format(i+1, row[-2].strip()))
		return
	
	html = response.text 
	#print(html)
	if row[0].strip() not in html and row[0].strip().replace(' - ', ' -- ') not in html:
		# HTML页面中无论文名字
		if row[-2].strip() in Special_url[which]:
			return

		print('第{}行的论文{}，其HTML页面中不存在论文名字，URL链接为{}'.format(i+1, row[0].strip(), row[-2].strip()))
		return

	# HTML页面中有论文名字
	
def check_arxiv(url: str, i: int):
	pattern = re.compile(r'v\d')	# v+数字的模式
	if 'arxiv' in url and pattern.findall(url):
		print(i+1, url)

def get_info_bydblp(row, i: int):
	'''
	return一个二维列表，该列表中的每个元素都是一个论文信息列表（依次包含有：作者、 年份、 期刊会议）
	返回多个论文信息列表的原因是：有多个同名论文的存在可能
	'''

	# 匹配HTML中论文信息部分的正则表达式
	rule = re.compile(r'<ul class="publ-list">(.*?)</ul><p id="completesearch-info-skipping"')

	# 检索地址
	url = 'https://dblp.org/search?q='+row[0].strip()
	try:
		response = requests.get(url, headers=headers, timeout=10)
	except:
		print('第{}行paper的dblp检索访问超时'.format(str(i)))
		# 返回空信息
		return []

	html = response.text
	# 取页面中写着论文信息的HTML代码，findall会返回一个列表，如果页面正常其应该是一个长度为1的列表
	l = rule.findall(html)	
	if len(l) != 1:
		print('第{}行paper的dblp检索访问出错，大概率是dblp检索服务响应太慢'.format(str(i)))
		# 返回空信息
		return []

	# 再从l[0]中取出论文信息，如果dblp检索出了几个结果，contents就是长度为几的列表
	contents = re.findall(r'<li class="entry (.*?)<meta property="genre" content="computer science"></li>', l[0])	# paper信息内容
	
	# contents为空，说明dblp没有对应的paper检索信息
	if len(contents) == 0:
		# 返回空信息
		return []

	# 根据检索到的HTML页面信息，找到该论文的作者、 年份、 期刊会议
	res = []	# 初始化返回的二维列表
	for content in contents:
		# 再从HTML代码中取出论文信息
		paper_info = re.findall(r'<cite class="data tts-content"(.*?)</cite>', content)
		paper_info = paper_info[0]
		
		# 取出论文名字
		papername = re.findall(r'<span class="title" itemprop="name">(.*?)</span>', paper_info)
		papername[0] = HTML.unescape(papername[0])	# 例如：*符号从转义字符形式转换为真正的*
		if papername[0][-1] == '.':	# 去掉结尾的.
			papername[0] = papername[0][:-1]

		excel_papername = row[0].strip()
		# dblp检索出来的论文名字和excel中的论文名字在不区分大小的情况下是否一致
		if _uncased_same(papername[0], excel_papername):	
			# 如果检索到的论文名是我们要寻找的论文，则继续找出它的其他信息
			author_list = re.findall(r'<span itemprop="author" itemscope itemtype="http://schema.org/Person">(.*?)/span>', paper_info)	# 取出作者信息
			paper_authors = []
			for author in author_list:
				tmp = re.findall(r'<span itemprop="name" title="(.*?)<', author)	# 得到中间结果
				paper_authors.append(HTML.unescape(tmp[0].split('>')[-1]))	# HTML转义字符转换，将德文转义出来
			
			# paper_partOf是论文来源 
			paper_partOf = [] 
			_from = re.findall(r'<span itemprop="isPartOf" itemscope itemtype="http://schema.org/(.*?)</span>', paper_info)	# HTML代码中的论文来源 
			for item in _from: 
				if 'PublicationVolume' not in item and 'PublicationIssue' not in item: 
					tmp = item.split('>')[-1] 
					if tmp == 'CoRR': 
						tmp = 'arXiv' 
					elif 'ACL/IJCNLP' in tmp:	# 去掉/IJCNLP，只取前面ACL EACL NACL AACL等的部分 
						tmp = tmp.split('/')[0] 
					elif ' (' in tmp:			# 去掉括号中的数字，只取前面的部分 
						tmp = tmp.split(' (')[0] 
					paper_partOf.append(tmp)

			year = re.findall(r'<span itemprop="datePublished">(.*?)</span>', paper_info)

			# 作者有先后顺序之分，所以应将作者信息以字符串看待
			res.append([', '.join(paper_authors), year[0], paper_partOf[0]])

	'''
	以下处理res中有多个结果的情况
	因为dblp返回多个结果：存在同名论文不同作者 或 同名论文相同作者不同论文来源的情况
	'''
	dic_temp = {}	# 以作者为键，[(论文归属,res索引), (论文归属,res索引), ...]为值，构建一个临时字典
	for idx, item in enumerate(res):
		author = item[0]
		paper_partOf = item[-1]
		if author not in dic_temp.keys():
			dic_temp[author] = [(paper_partOf, idx)]
		else:
			dic_temp[author].append((paper_partOf, idx))

	author_list_temp = []	# 一个临时列表，存放非arXiv来源的论文的作者名字
	for author, tuple_partOf_idx_list in dic_temp.items():
		for tuple_partOf_idx in tuple_partOf_idx_list:
			if 'arXiv' != tuple_partOf_idx[0]:
				author_list_temp.append(author)

	# 如果该论文该作者有不是arXiv的论文信息，则返回那些来源不是arXiv的论文信息
	if len(author_list_temp) > 0:	
		no_need_index = []
		for author in author_list_temp:
			for tuple_partof_idx in dic_temp[author]:
				if 'arXiv' == tuple_partof_idx[0]:
					no_need_index.append(tuple_partof_idx[1])	# 将不需要的索引取出来
		
		new_res = []
		for idx, item in enumerate(res):	# 返回需要的论文信息
			if idx not in no_need_index:
				new_res.append(item)
		return new_res
	
	else:	
		# 如果仅有arxiv的论文信息，则返回这些arxiv的论文信息	
		return res

def is_info_same(infos, row, j: int, which: int):
	papername = row[0].strip()
	outtext = ""
	for idx, info in enumerate(infos):
		flag = True			# 标识dblp检索到的信息和excel信息是否完全匹配
		if idx != 0:		# 让输出好看
			outtext += '\n'	# 让输出好看

		dblp_authors = info[0]
		excel_authors = row[2].strip()

		if dblp_authors != excel_authors:
			if flag == False:
				outtext += '作者应为: ' + dblp_authors + ', '
			else:
				outtext += '第'+str(j)+'行的信息错误：  作者应为：' + dblp_authors + ', '
			flag = False

		dblp_partOf = info[2]
		excel_partOf = row[-4].strip()
		
		if dblp_partOf != excel_partOf:
			if flag == False:
				outtext += '期刊会议应为: ' + dblp_partOf + ', '
			else:
				outtext += '第'+str(j)+'行的信息错误：  期刊会议应为：' + dblp_partOf + ', '
			flag = False

		dblp_year = info[1]
		excel_year = str(int(row[-3])).strip()
		
		if dblp_year != excel_year:
			if flag == False:
				outtext += '年份应为: ' + dblp_year + ', '
			else:
				outtext += '第'+str(j)+'行的信息错误：  年份应为：' + dblp_year + ', '
			flag = False

		# 只要有一个info是完全符合Excel记录的信息，直接返回True
		if flag:	
			return True

	# 如果有不符合的，输出修正信息
	print(outtext[:-2].replace(', \n', '\n'))
	return False

def check_info_bydblp(row, i: int, which: str):
	'''
		row：excel中的行信息
		i：该信息的在excel中的行号
		which：NLP or ML
	'''
	infos = get_info_bydblp(row, i+1)

	# dblp检索到了论文
	if len(infos) > 0:
		flag = is_info_same(infos, row, i+1, which)
		if flag == False:
			# dblp检索到的信息和excel上面的信息不一致	
			print('请给论文{}更新正确数据。'.format(row[0].strip()))
		elif row[0].strip() in Special_papername[which].keys():
			# 这篇论文被找到了，我们应该在Special_papername里面删除掉它
			del Special_papername[which][row[0].strip()]

	# dblp没检索到
	else:
		if row[0].strip() not in Special_papername[which].keys():
			print('第{}行paper的信息在dblp和脚本记录中都检索不到，其名为{}'.format(i+1, row[0].strip()))	
		else:	
			# 判断记录在脚本中的信息和excel中的信息是否一致
			partOf, year, authors = Special_papername[which][row[0].strip()] 
			excel_partOf, excel_year, excel_authors = row[3].strip(), str(int(row[4])).strip(), row[2].strip()
			outtext = ''
			if authors != excel_authors:
				outtext += '作者应为: ' + authors + ', '
			if partOf != excel_partOf:
				outtext += '期刊会议应为: ' + partOf + ', '
			if year != excel_year:
				outtext += '年份应为: ' + year + ', '
			if outtext != '':
				print('第'+str(i+1)+'行的信息错误：  '+outtext[:-2])
				print('请给论文{}更新正确数据。'.format(row[0].strip()))

dirs = ['NLP', 'ML']
if __name__ == "__main__":
	for p, k in enumerate(dirs):
		sheet = file.sheet_by_index(p)	# 获取excel中的sheet表单（p=0对应NLP，p=1对应ML）
		nrows = sheet.nrows	# 该表单一共有多少行

		start = 1 # 因为第一行是标题，所以i从1开始
		
		for i in range(start, nrows):
			row = sheet.row_values(i)	# 获取第i行的信息，返回一个列表
			assert len(row) == 7	# excel中每行都必须是7列

			# 检查1 检查网址为arXiv的链接是否带 v几
			check_arxiv(row[-2].strip(), i)

			# 检查2 根据dblp的检索结果检查excel中的年份，作者，期刊会议是否正确
			'''
			特例论文：Word sense disambiguation: a survey —— dblp检索到的不对
			'''
			check_info_bydblp(row, i, k)

			# 检查3 检查excel里链接的HTML页面中是否有论文名字，防止链接错误。
			# 如果输出“Except: url链接访问失败”，则说明 链接失效 或 链接访问不上去 -> 多次访问确认链接是否可以访问
			check_paper_url(row, k, i)


	# 输出不被dblp检索出来的论文信息
	# print('NLP')
	# for papername, info in Special_papername['NLP'].items():
	# 	print("'"+papername+"'", end=': ')
	# 	print(info)
	# print()

	# print('ML')
	# for papername, info in Special_papername['ML'].items():
	# 	print("'"+papername+"'", end=': ')
	# 	print(info)
		