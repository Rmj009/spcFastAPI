import numpy as np
import matplotlib.pyplot as plt

"""
References: 
Douglas C. Montgomery-Introduction to statistical quality control 7th edtition-Wiley (2009)
Part III chapter 8.3, p362.-p372
"""
class Calculator(object):
    # def __init__(self,tbls,sojourn):
    #     self.tbls = tbls
    #     self.sojourn = sojourn
    # def __del__(self,object):  #1>>> cleanup the seq, 2>>> return the seq after drop point(s)
    #     print('drop points...')
    #     dropindex = np.argwhere(max(object) or min(object))
    #     sequences = np.delete(object,object[1]) #specific points
    #     return sequences

    # def __repr__(self) -> str:
    #     return super().__repr__()

    def calc(datatables):
        try:
            datatables = datatables[datatables.valuelst != -88888888]
            # print('###Dataframe###',datatables.head(),sep='\n')
            goodNum = len(datatables['goodlst']) 
            defectNum = len(datatables[datatables.defectlst > 0])
            totalNum = goodNum + defectNum
            goodRate = goodNum / totalNum
            Target = datatables.stdValue[0]
            USL = Target + datatables['usllst'][0]
            LSL = Target - datatables['lsllst'][0]
            LCL = (LSL + Target)/2
            UCL = (USL + Target)/2
            rangespec = USL - LSL
            ngroup = int(datatables.shape[0])/int(datatables.amount[1])
            if (ngroup.is_integer() == False):
                cpkarr = datatables['valuelst'].sort_index(axis = 0,ascending = False) #coz the array_split method 
                cpkarr = np.array_split(cpkarr,datatables.shape[0]//datatables.amount[1])
                cpkarrMEAN = [np.mean(i) for i in cpkarr]
                sigmaCpk = np.std(cpkarrMEAN,ddof=1) #pd.std() >>> //(n)
            else:
                cpkarr = np.array_split(datatables['valuelst'],ngroup)
                cpkarrMEAN = [np.mean(i) for i in cpkarr]
                sigmaCpk = np.std(cpkarrMEAN,ddof=1) # numpy standard deviation >>> //(n-1)
            cp_mean = np.mean(datatables['valuelst'])
            sigmaPpk = np.std(datatables['valuelst'],ddof=1)
            if (sigmaCpk == 0) or (sigmaPpk == 0):
                raise Exception('unreasonable anomaly') 
            assert sigmaPpk != 0
            assert sigmaCpk != 0
            Cp = (rangespec) / (sigmaCpk*6) 
            Ck = abs((Target - cp_mean)/ (rangespec / 2))
            Cpu = (USL - cp_mean) / (sigmaCpk*3)
            Cpl = (cp_mean - LSL) / (sigmaCpk*3)
            Cpk = np.min([Cpu,Cpl]) 
            # Cpk = abs((1-Ck)*Cp) // calculation requires to be discussed
            Ppu = (UCL - cp_mean) / (sigmaPpk*3)
            Ppl = (cp_mean - LCL) / (sigmaPpk*3)
            Ppk = np.min([Ppu,Ppl]) 
            # capability ratio
            CPR = goodNum,totalNum,goodRate ,USL,LSL,UCL,LCL,cp_mean,Target ,rangespec, Cpu, Cpl, Cp, Ck, Cpk, Ppk
            keys = ["good","totalNum","goodRate","USL","LSL","UCL","LCL","overallMean","target","range","Cpu","Cpl","Cp","Ck","Cpk","Ppk"]
            capability = dict(zip(keys, CPR))
            ### Reference :https://en.wikipedia.org/wiki/Process_performance_index
            return capability # total 17
        except ZeroDivisionError as e:
            print('sigma zero result from variance: '+ str(e))
            print("fix infinity", None)
        except Exception as error:
            print('CALC_ERROR',error)
            return error

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
