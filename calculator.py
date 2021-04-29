import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as stat
class Calculator:
    def __init__(self,mean,variance,sojourn):
        self.mean = mean
        self.variance = variance
        self.sojourn = sojourn
    def calc(datatables):
        try:
            # measurelst = [np.asscalar(i) for i in 
            # measurelst = pd.DataFrame(measurelst)
            print('/Dataframe:/',datatables.head(),sep=' ')
            goodNum = len(datatables['goodlst']) 
            defectNum = len(datatables['defectlst'])
            rangespec = max(datatables['valuelst']) - min(datatables['valuelst'])
            totalNum = goodNum + defectNum
            goodRate = goodNum / totalNum 
            defectRate = defectNum / totalNum
            llim = datatables.iloc[1,3]
            ulim = datatables.iloc[1,4]
            Target = (llim+ulim)/2
            UCL = (ulim+Target)/2
            LCL = (Target+llim)/2
            
            
            arr = datatables['valuelst']
            ngroup = 10 #input() #給使用者指定每組大小
            # ngroups = datatables.groupby(['stratification']).sum('valuelst')
            # print('nnnnn',ngroups,sep='\n')
            ppkarr = np.array_split(arr,ngroup)# 將資料分組計算
            sampleStd = [np.mean(i) for i in ppkarr]
            sigmaPpk = np.std(sampleStd)
           
            cp_mean = np.mean(datatables['valuelst'])
            sigmaCpk = np.std(datatables['valuelst'])
            Cp = float(rangespec) / (sigmaCpk*6) 
            Ck = float(cp_mean - UCL)/ Target / 2
            Cpu = float(ulim - cp_mean) / (sigmaCpk*3)
            Cpl = float(cp_mean - llim) / (sigmaCpk*3)
            Cpk = np.min([Cpu,Cpl])
            Ppu = float(ulim - cp_mean) / (sigmaPpk*3)
            Ppl = float(cp_mean - llim) / (sigmaPpk*3)
            Ppk = np.min([Ppu,Ppl])

            CPR = goodNum,totalNum,goodRate,ulim,llim,UCL,LCL,cp_mean, Target,rangespec, Cpu, Cpl, Cp, Ck, Cpk, Ppk, # capability ratio
            keys = ["good","totalNum","goodRate","USL","LSL","UCL","LCL","overallmean","target","range","Cpu","Cpl","Cp","Ck","Cpk","Ppk"]
            capability = dict(zip(keys, CPR))
            ### Reference :https://en.wikipedia.org/wiki/Process_performance_index
            # print(capability)
            return capability # total 17
        except ZeroDivisionError() as e:
            print('sigma zero result from variance: '+ str(e))
            print("fix infinity", None)


# ptV = nmp[:,11]
# trendObj = {'all_vals': ptV,'format_1': np.zeros(len(ptV)),'format_2': np.zeros(len(ptV)),'format_3': np.zeros(len(ptV)),'format_4': np.zeros(len(ptV))}

# alphabets = [chr(i) for i in range(ord('A'),ord('Z')+1)]

# pd_trendObj = pd.DataFrame(trendObj) #, columns = [alphabets[name] for name in range(len(trendObj))], index = [i for i  in range(len(ptV)+1)] )


# print([index for index,val in enumerate(trendObj['format_1']) if val])
# print(pd_trendObj)
# plt.plot(trendObj['all_vals'])
# assign_datum(obj = trendObj, datum = 10)
# mark = 3.5
# plt.figure(figsize=(60,30))
# plt.plot(trendObj['all_vals'], color='red',markevery=format_arr(1), ls="", marker='s',mfc = 'none', mec='red', label="Rule1", markersize=mark*1.5)
# plt.plot(trendObj['all_vals'], color='blue',markevery=format_arr(2), ls="", marker='o', mfc='none',mec='blue',label="Rule2", markersize=mark*1)
# plt.plot(trendObj['all_vals'], color='brown',markevery=format_arr(3), ls="", marker='o', mfc='none',mec='brown',label="Rule3", markersize=mark*1.5)
# plt.plot(trendObj['all_vals'], color='blue',markevery=format_arr(4), ls="", marker='s', mfc='none',mec='green',label="Rule4", markersize=mark*1.0)
# plt.plot(trendObj['all_vals'], color='#81B5CB', ls="", marker=".", markersize=mark)
# plotAxlines(trendObj['all_vals'])

# plt.legend()
# plt.ylim(0,25)
# # # plt.plot(ptV)
# # # # plt.savefig('static/control-chart.png')
# # # g = sns.relplot(x = 'all_vals', y = 'format_1', data = trendObj, kind="line")
# # # g.fig.autofmt_xdate()
# # # # # plotQuery()
# plt.show()

class western(Calculator):

    def rando():
        theNum = np.random.randint(low = 7.5, high = 15 , size = 195)
        return theNum

    def testRule1(obj,newNum, mean, sd):

        sigUp = mean + sd*3
        sigDown = mean - sd*3
        code = (newNum > sigUp) or (newNum < sigDown)
        obj['format_1'] = np.append(obj['format_1'],code)
        return 

    def testRule2(obj, newNum, mean, sd):
        twoSigUp = mean + sd*2
        twoSigDown = mean - sd*2
        temp_clipped = obj['all_vals'][-2:]
        temp_clipped = np.append(temp_clipped,newNum)
        above2 = temp_clipped > twoSigUp
        below2 = temp_clipped < twoSigDown
        code = (above2.sum(axis=0) >= 2) or (below2.sum(axis=0) >= 2)
        obj['format_2'] = np.append(obj['format_2'],code)
        return

    def testRule3(obj, newNum, mean, sd):
        oneSigUp = mean + sd
        oneSigDown = mean - sd
        temp_clipped = obj['all_vals'][-5:]
        temp_clipped = np.append(temp_clipped,newNum)
        above1 = temp_clipped > oneSigUp
        below1 = temp_clipped < oneSigDown
        code = (above1.sum(axis=0) >= 4) or (below1.sum(axis=0) >= 4)
        obj['format_3'] = np.append(obj['format_3'],code)
        return

    def testRule4(obj, newNum, mean):
        temp_clipped = obj['all_vals'][-8:]
        temp_clipped = np.append(temp_clipped,newNum)
        above = temp_clipped > mean
        below = temp_clipped < mean
        code = (above.sum(axis=0) >= 9) or (below.sum(axis=0) >= 9)
        obj['format_4'] = np.append(obj['format_4'],code)
        return

    def violations(obj,datum):
        theMean = np.mean(obj['all_vals'])
        sd = np.std(obj['all_vals'])
        testRule1(obj,datum, theMean, sd)
        testRule2(obj,datum, theMean, sd)
        testRule3(obj,datum, theMean, sd)
        testRule4(obj,datum, theMean)
        return
        
    def assign_datum(obj,datum):  # datum = None
        # if(datum is None):
        #     datum = rando()
        # datum = obj['all_vals'][1:100]
        violations(obj,datum)
        obj['all_vals'] = np.append(obj['all_vals'],datum)
        return

    #Return the value's index if rule has been violated.  This is used for formatting.

    def format_arr(rule):
        rule_arr = 'format_' + str(rule)
        # aa=[index for index,val in enumerate(trendObj[rule_arr]) if val]
        # print(aa)
        return [index for index,val in enumerate(trendObj[rule_arr]) if val]

    def plotAxlines(array):
        theMean = np.mean(array)
        sd = np.std(array)
        colors = ['black','green','violet','red']
        for level,color in enumerate(colors):
            upper = theMean + sd*level
            lower = theMean - sd*level
            plt.axhline(y=upper, linewidth=0.5, color=color)
            plt.axhline(y=lower, linewidth=0.5, color=color)
        return


# if __name__ == "__main__":
#     print("open")
#     calc({"valuelst":100,"goodlst":100 ,"defectlst":88 ,"lslspec": 60,"uslspec": 10})