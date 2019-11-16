import random
from datetime import datetime
import argparse
import time
from flask import Flask, render_template, request, redirect, url_for, send_file
import os

app = Flask(__name__)

'''providers dictionary: Name:[Days Working] 1=Monday,2=Tuesday,3=Wednesday,4=Thursday,5=Friday'''
rfm_providers = {"Brenda Lenhart": [2,3,4], "Corrie Piper": [1, 2, 3, 4, 5], "Gregor Gray": [1, 2, 3, 4, 5], "Leanna Robinson": [1, 2, 4, 5],
             "Margaret Stearns": [1, 2, 3, 4, 5], "Meredith Thompson": [1, 2, 3, 4, 5], "Stefanie Davis": [1, 2, 3, 4, 5], "Sean Obrien": [1, 3, 4]}
fac_providers = {"Brenda": [1, 3, 4, 5], "Jody": [2, 3, 4, 5], "Jarim": [1, 2, 3, 4, 5], "Katrina": [1, 2, 4], "Mike": [1, 2, 3, 4],
             "Susan": [2, 3, 4, 5], "Margaret": [1, 2, 3, 4], "Dael": [1, 2, 3, 4], "Lynette": [1, 2, 3, 4, 5]}
location_list = ['fac','rfm']

def get_parse_args():
    """
    Used to parse arguments and provide error/entry checking returns 2 parsed arguments
    options.location is the 3 digit location code and will throw an error if no valid input is added
    this function will also check to make sure that the 3 digit location code is in the location_list
    options.number is the number of days out that will be built, the default is 200
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--location", dest="location", help="3 digit location code")
    parser.add_argument("-n","--number", dest="number", help="Number of days that will be given in the output csv file", default=200)
    options = parser.parse_args()
    if not options.location:
        parser.error('[-] please provide a 3 digit location code')
    if options.location.lower() not in location_list:
        parser.error('[-] please provider a valid locations code options are: ' + location_list)
    return options.location, options.number

def check_day(name_choice, day, providers):
    """
    checks the day to make sure that the provider is working and can be assigned a hold that day
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


def prov_lst_dict(prov_list):
    """
        takes nothing but iterates through the provider list and creates a dictionary with key=name and value=0
        used for checking equitibility later on
    """
    rtrn_dict = {}
    for name in prov_list:
        rtrn_dict.update({name:0})
    return rtrn_dict

def run_list_randomizer(number,prov_list,providers):
    """
        main function which will call other functions to complete the task
        will create a list of length run_number, checking the reverse length with is based on 1/2 of the number of providers
        will shuffle a list of names and pop these off randomly to determine the name
            will then check the name to see if they work that day/can have a bha hold, if yes will reach out to check_list function
            if the check_list function returns True, it will append the name selected to the list, will add 1 to the num_assigned dictonary for that name
        if the list empties = no one is appropriate for that spot, will break out of function and try again from scratch
            breaks out of function by returning a list of dictionaries, the difference being 4 which will be rejected in the while max line
        if everything goes through, at the end it will return a list of dictionaries, item[0] is the list while item[1] is the num_assigned
    """
    bhaurgentlist = []
    num_assigned = prov_lst_dict(prov_list) #this will help to keep track of how many times people have been assigned for equitability check later
    day = 1
    count = 1
    rev_len = int(len(providers)*(.5)+1) #reverse length, the amount of days before a provider can be selected again. Based on 1/2 the number of providers, 6 providers = 3 days
    rand = 0
    run_number = number
    brk = False
    while count < run_number:
        exp_list = list(providers.keys())
        random.shuffle(exp_list)
        while exp_list != []:
            name_choice = exp_list.pop(random.randint(0,len(exp_list)-1))
            if check_day(name_choice,day,providers):
                if check_list(name_choice, count, rev_len, prov_list, bhaurgentlist):
                    count +=1
                    bhaurgentlist.append(name_choice)
                    num_assigned[name_choice] += 1
                    day +=1
                    if day > 5:
                        day = 1
                    break
        if exp_list == []:
            #only run if options have been run out
            #returns a list with None and a dictionary with bad1 and bad2 as keys and 1 and 5 as values
            #this will break the loop and trigger the randomizer to run again from scratch
            return [None, {'bad':1,"bad2":5}]
    return [bhaurgentlist, num_assigned]

def main(location, number_out):
    """
    providers the main function to call that will reach out to other functions
    is responsible for sorting through the parser as well as testing the output of the randomizer
    once an equitiable rotation has been achieved it will create a csv file and write to it
    """
    # location, number_out = get_parse_args()
    number_out = int(number_out)
    if location.lower() == "fac":
        providers = fac_providers
    elif location.lower() == "rfm":
        providers = rfm_providers
    prov_list = list(providers.keys())
    start = time.time()
    num_runs = 1
    test_list = run_list_randomizer(number_out, prov_list, providers)
    while max(test_list[1].values()) - min(test_list[1].values()) > 2: #equitability check, looks at max and min and keeps calling list randomizer until everyone is within '2'
        num_runs += 1
        test_list = run_list_randomizer(number_out,prov_list, providers)
    opt_file = location.lower() +"_bha_holds_" + datetime.now().strftime("%m-%d-%Y") + '_' + str(number_out) + '.csv'
    with open(opt_file, "w") as of:
        day = 1
        for nm in test_list[0]:
            of.write(f"{nm},")
            day+=1
            if day == 6:
                of.write(",,")
                day = 1
    end = time.time()
    return send_file(opt_file,
                    mimetype='text/csv',
                    attachment_filename=opt_file,
                    as_attachment=True
    )
    # print(f"[+] Finished! {opt_file} created\n[+] Time taken: {end-start} seconds\n[+] # of runs required {num_runs}")


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        try:
            location = request.form['location']
            if location.lower() not in ['fac', 'rfm']:
                raise NameError
            num_days_out = request.form['num_days_out']
            main(location,num_days_out)
        except:
            return render_template("incomplete.jinja2")
    return render_template('all.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)