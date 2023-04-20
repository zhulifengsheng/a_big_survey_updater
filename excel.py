import xlrd
import codecs

file = xlrd.open_workbook('survey.xlsx')
out = codecs.open('out.txt', 'w', encoding="utf-8")

def sum(dic):
    res = 0
    for k,v in dic.items():
        res += v
    return res

if __name__ == "__main__":
    for p in range(2):
        sheet1 = file.sheet_by_index(p)
        nrows = sheet1.nrows
        ncols = sheet1.ncols
        line1 = sheet1.row_values(0)
        categorization = ''
        dict = {}
        nums = 0
        dict_year = {}
        temp = 1

        for i in range(1, nrows):
            row = sheet1.row_values(i)
            year = str(row[4])[:4].strip()
            if year in dict_year.keys():    # 每个年份有多少个论文
                dict_year[year] += 1
            else:
                dict_year[year] = 1
            if row[1].strip() != categorization:
                dict[categorization] = nums
                nums = 0
                categorization = row[1].strip()
                out.write('#### [' + categorization + '](#content)\n\n')
                temp = 1

            out.write(str(temp) + '. **' + row[0].strip().strip('.') + '.** ' + row[3].strip() + ' ' + str(row[4])[
                                                                                                       :4].strip() + ' [paper](' +
                      row[5] + ')' + ' [bib](' + row[6].replace(" ", "-") + ')\n\n')
            out.write('    *' + row[2].strip() + '*\n\n')
            nums += 1
            temp += 1

        dict[categorization] = nums
        del dict[""]
        assert sum(dict) == nrows-1, "行数不对"
        
        # 按每个类别的个数来排序
        d_order = sorted(dict.items(), key=lambda x: x[1], reverse=True)

        for i in d_order:
            print("{}\t{}".format(i[0], i[1]))
        print()