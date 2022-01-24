from numpy import str0
import pygsheets
gc = pygsheets.authorize(service_account_file='service_acc_sheets.json')
sh = gc.open(title='test sheet')
sh.share('', role='reader', type='anyone')
print(sh.url)
# wk1 = sh.add_worksheet('sheet 1 test')
wk1 = sh.worksheets()[1]

# sh.worksheet('title',)

# # print(wk1)

# wk1.update_value('A0','test')

# for i in range(1,10):
#     l = 'A' + str(i)
#     wk1.update_value(l,i)
your_result_link = sh.url + '/edit#gid=' + str(wk1.id)
print(your_result_link)


