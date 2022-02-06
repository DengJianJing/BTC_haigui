#import svmMLiA
from numpy import *
import matplotlib.pyplot as plt
from datetime import datetime 
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib as mpl
mpl.rcParams['path.simplify'] = True
register_matplotlib_converters();
#FILE_PATH = './data/daily_price_btc_cny.csv'
FILE_PATH = './data/20190108.csv' #美元兑BTC

#加载数据
#0		1		2		3		4	5		6
#no		date	open	high	low	close	volume
def loadDataSet(fileName):
    dataMat = []; labelMat = []
    fr = open(fileName)
	#第一行的标签不读
    next(fr)
    for line in fr.readlines():
        lineArr = line.strip('\n').split(',')
        dataMat.append(lineArr)
        #labelMat.append(float(lineArr[2]))
    return dataMat

#matplotlib绘图
def paintAnlysis(dataMat):
    list_time = [x[1] for x in dataMat]
    xs = [datetime.strptime(d, "%Y-%m-%d") for d in list_time]
    yOpen = [y[2] for y in dataMat]
    yHigh = [y[3] for y in dataMat]
    yLow = [y[4] for y in dataMat]
    yClose = [y[5] for y in dataMat]
    yVolumn = [y[6] for y in dataMat]	
    yHighN = rolling_max(dataMat,20)
    yLowN = rolling_min(dataMat,10) 
	
    plt.figure(figsize=(15, 6))#返回图像实例
    plt.subplot(1, 2, 1)#1代表行，2代表列，所以一共有2个图，1代表此时绘制第二个图。
    plt.title('BTC/CNY')
    ##########################
    #https://blog.csdn.net/cjcrxzz/article/details/79627483
    plt.plot(xs, yOpen, ',-r')
    plt.plot(xs, yClose, ',-b')
    plt.plot(xs, yHighN, ',k:')
    plt.plot(xs, yLowN, ',k:')
    plt.xlabel('Time')
    plt.ylabel('Value')
    #绘制第二个图
    plt.subplot(1, 2, 2)
    plt.title('BTC/CNY Volumn')
    plt.xlabel('Time')
    plt.ylabel('Volumn')
    plt.plot(xs, yVolumn, ',-b')
    plt.gcf().autofmt_xdate()
    plt.show()

#####################策略1，利用概率事件，三连涨和三连跌的情况
def strategy_1(dataMat):
	yClose = [y[5] for y in dataMat]
	#增长率
	yIncrease = [(float(yClose[i+1]) - float(yClose[i]))*100/float(yClose[i]) for i in range(len(yClose)-1)]
	flag_increase_tri = 0
	flag_increase_tri_up = 0
	flag_increase_tri_down = 0
	flag_discrease_tri = 0
	flag_discrease_tri_up = 0
	flag_discrease_tri_down = 0
	#计算连升3个，和连降3个的概率
	for i in range(len(yIncrease)-3):
		if(yIncrease[i]>0 and yIncrease[i+1] >0 and yIncrease[i+2]>0):
			#连升3个的概率
			flag_increase_tri += 1
			if(yIncrease[i+3] > 0):
				flag_increase_tri_up +=1
			elif(yIncrease[i+3] < 0):
				flag_increase_tri_down += 1
		if(yIncrease[i]<0 and yIncrease[i+1] <0 and yIncrease[i+2]<0):
			flag_discrease_tri+= 1
			if(yIncrease[i+3] > 0):
				flag_discrease_tri_up +=1
			elif(yIncrease[i+3] < 0):
				flag_discrease_tri_down += 1
	print('flag_increase_tri:\n',flag_increase_tri)
	print('flag_discrease_tri:\n',flag_discrease_tri)
	print('probability flag_increase_tri_up:',flag_increase_tri_up*100/flag_increase_tri,'%')
	print('probability flag_increase_tri_down:',flag_increase_tri_down*100/flag_increase_tri,'%')	
	print('probability flag_discrease_tri_up:',flag_discrease_tri_up*100/flag_discrease_tri,'%')
	print('probability flag_discrease_tri_down:',flag_discrease_tri_down*100/flag_discrease_tri,'%')
	flag_increase_dou = 0
	flag_discrease_dou = 0
	#计算连升2个，和连降2个的概率
	for i in range(len(yIncrease)-1):
		if(yIncrease[i]>0 and yIncrease[i+1] >0 ):
			#连升2个的概率
			flag_increase_dou += 1
		if(yIncrease[i]<0 and yIncrease[i+1] <0 ):
			flag_discrease_dou+= 1
	print('flag_increase_dou:\n',flag_increase_dou)
	print('flag_discrease_dou:\n',flag_discrease_dou)

#####################################################3
###################策略2，海龟策略##################
#matplotlib绘图
def paintAnlysis_turtle(dataMat,buy_list,sell_list,yPrincipal_list):
	list_time = [x[1] for x in dataMat]
	xs = [datetime.strptime(d, "%Y-%m-%d") for d in list_time]
	yOpen = [float(y[2]) for y in dataMat]
	yHigh = [float(y[3]) for y in dataMat]
	yLow = [float(y[4]) for y in dataMat]
	yClose = [float(y[5]) for y in dataMat]
	yVolumn = [y[6] for y in dataMat]	
	yHighN = rolling_max(dataMat,20)
	yLowN = rolling_min(dataMat,10) 
	xBuy = [xs[buy_list[i]] for i in range(len(buy_list))]
	yBuy = [yClose[buy_list[i]] for i in range(len(buy_list))]
	xSell = [xs[sell_list[i]] for i in range(len(sell_list))]
	ySell = [yClose[sell_list[i]] for i in range(len(sell_list))]
	
	#plt.ylim(ymin = 0);#设置下限
	plt.figure(figsize=(15, 6))#返回图像实例
	plt.subplot(1, 1, 1)#1代表行，2代表列，所以一共有2个图，1代表此时绘制第二个图。
	plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
	plt.title('BTC/CNY')
	##########################
	#https://blog.csdn.net/cjcrxzz/article/details/79627483
	#plt.plot(xs, yOpen, ',-r');

	#print(yClose);
	#print(xs);
	plt.plot(xs, yClose, ',-b')
	plt.plot(xs, yHighN, ',r:')
	plt.plot(xs, yLowN, ',g:')
	#画出buy点
	for i in range(len(xBuy)):
		plt.annotate('buy',xy = (xBuy[i], yBuy[i]),xytext=(xBuy[i], float(yBuy[i])+3))
	plt.plot(xBuy, yBuy, '+r')
	##画出sell点
	for i in range(len(xSell)):
		plt.annotate('sell',xy = (xSell[i], ySell[i]),xytext=(xSell[i], float(ySell[i])+3))
	plt.plot(xSell, ySell, '+g')
	plt.xlabel('Time')
	plt.ylabel('Value')
	plt.gcf().autofmt_xdate()#使Xlabel显示斜着
	plt.show()

def rolling_max(dataMat,N):
	#计算出N日内的最高值
	yHighN = [30000]*N
	yHigh = [float(y[3]) for y in dataMat]
	for i in range(len(yHigh)-N):
		yHighN.append(max(yHigh[i:i+N]))
	return yHighN
	#print(yHighN)
	#print(len(yHighN))
	#print(len(yHigh))

def rolling_min(dataMat,N):
	#计算出N日内的最低值
	yLowN = [0]*N
	yLow = [float(y[4]) for y in dataMat]
	for i in range(len(yLow)-N):
		yLowN.append(min(yLow[i:i+N]))
	return yLowN
	#print(yLowN)
	#print(len(yLowN))
	
#海龟策略
def strategy_turtle(dataMat,N1):
	yHigh = [float(y[3]) for y in dataMat]
	yLow = [float(y[4]) for y in dataMat]
	yClose = [float(y[5]) for y in dataMat]
	yHighN = rolling_max(dataMat,20)
	yLowN = rolling_min(dataMat,10) 
	buy_list = []
	sell_list = [];
	flag_buy_sell = 1
	for i in range(N1,len(yClose)):
		if(yHigh[i] > yHighN[i] and flag_buy_sell ==1):
			buy_list.append(i)
			flag_buy_sell = 0
		elif(yLow[i] < yLowN[i] and flag_buy_sell ==0):
			sell_list.append(i)
			flag_buy_sell = 1
	print('buy_list\n',buy_list)
	print('sell_list\n',sell_list)
	
	#计算增益曲线
	yPrincipal = 1
	yPrincipal_list = []
	yIncome = [(float(yClose[sell_list[i]]) - float(yClose[buy_list[i]]))/float(yClose[buy_list[i]]) for i in range(len(buy_list))]
	for i in range(len(yIncome)):
		yPrincipal = yPrincipal*(1+yIncome[i])
		yPrincipal_list.append(yPrincipal)
	print('yIncome\n',yIncome)
	print('yPrincipal_list\n',yPrincipal_list)
	return buy_list,sell_list,yPrincipal_list
	
dataMat = loadDataSet(FILE_PATH)
#print(dataMat)
buy_list,sell_list,yPrincipal_list = strategy_turtle(dataMat,20)
paintAnlysis_turtle(dataMat,buy_list,sell_list,yPrincipal_list)
#paintAnlysis(dataMat)
#strategy_1(dataMat)