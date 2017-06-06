import mysql.connector

age = input('Enter Age: ')
initial = input('Enter Initial Investment: ')
time = input('Enter time frame in years: ')
expected = input('ENTER Return Investment: ')
risk = input('Risk Facotr: ')
print


lowest = {
    1 : "50%" ,
    2 : "20%" ,
    3 : "20%" ,
    4 : "10%"
}

def findpercent(x , y , ans , total) :
    # print x , y , ans , total

    if x== y :
        return 0.5 * total , 0.5 * total

    sol1  = ((1.0) * (ans - y)) / (x - y)
    sol2 = 1 - sol1
    return sol1 * total , sol2 * total



def print_percent(li , expected):
    # print expected
    if len(li) == 1 :
        print li[0][1] , 100
    elif len(li) == 2 :
        sol1  , sol2 = findpercent(li[0][0] , li[1][0] , expected , 1)
        print li[0][0] , sol1
        print li[1][0] , sol2
    elif len(li) == 3 :
        rate1 = (li[1][0] + li[2][0]) / 2.0
        rate2 = (li[0][0])
        sol1, sol2 = findpercent(rate1, rate2 ,  expected, 1)
        print li[0][1] , sol2

        sol3 , sol4 = findpercent( li[1][0] , li[2][0]  , rate1 , sol1 )
        print li[1][1], sol3
        print li[2][1], sol4
    elif len(li) == 4 :
        rate1 = (li[0][0]  +  li[2][0]) / 2.0
        rate2 = (li[1][0] + li[3][0] ) / 2.0
        if rate1 == rate2 :
            rate1 = (li[0][0] + li[1][0]) / 2.0
            rate2 = (li[2][0] + li[3][0]) / 2.0
            sol1, sol2 = findpercent(rate1, rate2, expected, 1)

            sol3, sol4 = findpercent(li[0][0], li[1][0], rate1, sol1)
            print li[0][1], sol3
            print li[1][1], sol4

            sol5, sol6 = findpercent(li[2][0], li[3][0], rate2, sol2)
            print li[2][1], sol5
            print li[3][1], sol6
        else :

            sol1, sol2 = findpercent(rate1, rate2 ,  expected, 1)

            sol3 , sol4 = findpercent( li[0][0] , li[2][0]  , rate1 , sol1 )
            print li[0][1], sol3
            print li[2][1], sol4

            sol5, sol6 = findpercent(li[1][0], li[3][0], rate2, sol2)
            print li[1][1], sol5
            print li[3][1], sol6


def investor(age , initial , time,expected  , risk):
    conn = mysql.connector.Connect(host='localhost', user='root',password='root',database='new')
    cur = conn.cursor()

    print

    if risk < 2 :
        risk = 'LOW'
    elif risk < 4 :
        risk = 'MEDIUM'
    else :
        risk = 'HIGH'


    expectedRate = (((expected * 1.0) / initial) ** (1.0 / time) - 1 ) * 100
    # print expectedRate


    def findRates(age , risk , time) :
        query = "SELECT * FROM funds WHERE AgeLower <= %s AND AgeUpper >= %s AND Risk = '%s' AND TimeLower <= %s" % (str(age) , str(age) , risk , str(time))
        # print query
        results = []
        cur.execute(query)
        for row in cur :
            results.append([row[0] , row[6]])

        return results



    results = findRates(age ,  risk , time )
    mean = 0
    ans = []
    for i in results :
        # print i
        temp = i[1]
        if '+' in temp :
            ll = int(temp[:-1])
            rate = int(ll)
            ul = 1000
        elif '--' in temp :
            ll , ul = map(int , temp.split('--') )
            rate = (int(ll) + int(ul)) / 2.0
        else :
            print "Rate not Recognized " , temp
            exit(1)
        mean += rate
        # print ll , ul
        if expectedRate >=  ll  and expectedRate <= ul :
            ans.append([ rate , i[0]])
        elif ll > expectedRate :
            ans.append([int(ll), i[0]])

    mean = mean * 1.0 / len(results)

    # print mean


    if ans == [] :
        if mean < expectedRate :
            if risk == 'LOW' :
                investor(age, initial , time  , expected , 3)
            elif risk == 'MEDIUM' :
                investor(age, initial, time, expected, 5)
            else :
                print "No Products Found"
                exit(1)
        else :
            if risk == 'HIGH':
                investor(age, initial, time, expected, 3)
            elif risk == 'MEDIUM':
                investor(age, initial, time, expected, 1)
            else:
                print "No Products Found"
                exit(1)

    ans.sort()
    # print ans

    low = True
    high = True # IF expected return is greater than all

    # ans = 15,16,17

    for i in ans :
        # print i[0] , expectedRate
        # print i[0] > expectedRate
        # print i[0] <= expectedRate
        if i[0] > expectedRate :
            high = False
        if i[0] < expectedRate :
            low = False

    # print low , high


    if low or high :
        if high :
            if risk == 'MEDIUM' :
                investor(age , initial , time , expected , 1)
            elif risk == 'HIGH' :
                investor(age, initial, time, expected, 3)
            else :
                for i in range(1 , min(5 , len(ans) + 1)) :
                    print ans[-i][1] , lowest[i]
        if low :
            h = min(4 , len(ans))
            for i in range(h) :
                print ans[i][1] , 100.0 / h

    else:

        ans = ans[max(-5 , -len(ans)) : ]
        print_percent(ans , expectedRate)

    conn.close()

investor(age , initial  , time, expected , risk)