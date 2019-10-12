import random
'''providers dictionary: Name:[Days Working] 1=Monday,2=Tuesday,3=Wednesday,4=Thursday,5=Friday'''
providers = {"Brenda": [1, 3, 4, 5], "Jody": [2, 3, 4, 5], "Jarim": [1, 2, 3, 4, 5], "Katrina": [1, 2, 4], "Mike": [1, 2, 3, 4],
             "Susan": [2, 3, 4, 5], "Margaret": [1, 2, 3, 4], "Dael": [1, 2, 3, 4], "Lynette": [1, 2, 3, 4, 5]}
prov_list = list(providers.keys())

def check_day(name_choice, day):
    """
    checks the day to make sure that the provider can be assigned as MLT that day
    """
    if day in providers[name_choice]:
        return True
    else:
        return False


def check_list(name_choice, count, rev, prov_list, bhaurgentlist):
    """
    this takes 5 arguments and checks to see if the person can be assigned by looking to see if they have been assigned in the past
    based on the count (number of people currently in the list) it makes a decision whether or not to go back by a max of 4 for count in current list or by the reverse num if >4
    if a person shows up, move forward check
    """
    mv_fwrd_chk = 0
    if count == 1:
        return True
    elif count < 4:
        for num in range(count):
            if name_choice == bhaurgentlist[(len(bhaurgentlist)-1)-num]:
                return False
    else:
        for num in range(rev):
            if name_choice == bhaurgentlist[(len(bhaurgentlist)-1)-num]:
                return False
    return True


def prov_lst_dict():
    rtrn_dict = {}
    for name in prov_list:
        rtrn_dict.update({name:0})
    return rtrn_dict

def run_list_randomizer():
    global prov_list
    bhaurgentlist = []
    num_assigned = prov_lst_dict()
    day = 1
    count = 1
    rev_len = int(len(providers)*(.5)+1) #reverse length, the amount of days before a provider can be selected again. Based on 1/2 the number of providers, 6 providers = 3 days
    rand = 0
    run_number = 200
    brk = False
    while count < run_number:
        exp_list = list(providers.keys())
        random.shuffle(exp_list)
        while exp_list != []:
            name_choice = exp_list.pop(random.randint(0,len(exp_list)-1))
            if check_day(name_choice,day):
                if check_list(name_choice, count, rev_len, prov_list, bhaurgentlist):
                    count +=1
                    bhaurgentlist.append(name_choice)
                    num_assigned[name_choice] += 1
                    day +=1
                    if day > 5:
                        day = 1
                    break
        if exp_list == []:
            return [None, {'bad':1,"bad2":5}]
    return [bhaurgentlist, num_assigned]


test_list = run_list_randomizer()
while max(test_list[1].values()) - min(test_list[1].values()) > 2: #equitability check, looks at max and min and keeps calling list randomizer until everyone is within '2'
    test_list = run_list_randomizer()
with open("bhamltlist.csv", "w") as of:
    day = 1
    for nm in test_list[0]:
        of.write(f"{nm},")
        day+=1
        if day == 6:
            of.write(",,")
            day = 1
 