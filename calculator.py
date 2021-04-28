import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as stat
class Calculator:
    def calc(mylst):
        ANS = 0,0,0,0,0,0,0,0,0 # return ans once exception occur
        try:
            # measurelst = [np.asscalar(i) for i in mylst]
            # measurelst = pd.DataFrame(measurelst)
            goodlst = mylst['goodlst']
            defectlst = mylst['defectlst']
            uslspec = mylst['lslspec']
            lslspec = mylst['lslspec']
            parselst = mylst['valuelst']
            

            arr = np.array(parselst)
            arr = arr.ravel()
            num_good = len(goodlst)
            num_defect = len(defectlst)
            total_num = num_good + num_defect
            good_rate = num_good / total_num
            defect_rate = num_defect / total_num
            ngroup = 10 #input() #給使用者指定每組大小
            ppkarr = np.array_split(arr,ngroup)# 將資料分組計算
            ppkarrSig = [np.mean(i) for i in ppkarr]
            sigmaPpk = np.std(ppkarrSig)
            sigmaCpk = np.std(arr)
            median = np.mean(arr)
            Cp = float(uslspec - lslspec) / (6*sigmaCpk)
            Cpu = float(uslspec - median) / (3*sigmaCpk)
            Cpl = float(median - lslspec) / (3*sigmaCpk)
            Cpk = np.min([Cpu, Cpl])
            ppu = float(uslspec - median) / (3*sigmaPpk)
            ppl = float(median - lslspec) / (3*sigmaPpk)
            Ppk = np.min([ppu,ppl])
            ANS = Cp, Cpu, Cpk, Ppk, uslspec, lslspec, good_rate, defect_rate, total_num
            keys = ["Cp","Cpu","Cpk","Ppk","usl","lsl","good_rate","defect_rate","total_num"]
            resultCapablity = dict(zip(keys, ANS))
            return resultCapablity
        except  ZeroDivisionError() as e:
            print('sigma zero result from variance: '+ str(e))
            print("fix infinity", ANS)



# df = pd.read_csv('workbook_name.csv', sep=',',header=0); nmp = df.to_numpy()  #nmp[:,11]
# b = '2020-09-02T07:41:03Z'
# e = '2021-01-15T10:47:32Z'
# wuuid = 'd5473fb7-42ac-4794-bf4d-358f4ddccd1c'
# suuid = '69636a46-48cb-4a99-976e-5ecc024c1332'
# df= spcTable.queryfunc(begin_time=b, expiry_time=e, wooh_uuid=wuuid, smpc_uuid=suuid)
# ptV = nmp[:,11]
# trendObj = {'all_vals': ptV,'format_1': np.zeros(len(ptV)),'format_2': np.zeros(len(ptV)),'format_3': np.zeros(len(ptV)),'format_4': np.zeros(len(ptV))}

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


    alphabets = [chr(i) for i in range(ord('A'),ord('Z')+1)]

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

# if __name__ == "__main__":
#     print("open")
#     calc({"valuelst":100,"goodlst":100 ,"defectlst":88 ,"lslspec": 60,"uslspec": 10})