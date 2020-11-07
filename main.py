import os
import re
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import time
import datetime
import webbrowser
import winsound
import csv
from tkinter import messagebox


# main window
window = Tk()
window.title("Job Finder")
window.geometry("1000x700")

def get_saved_string(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            string = f.read()
            f.close()
            return string
    else:
        with open(filename, 'w+') as f:
            file = f.read()
            string = ""
            f.close()
            return string



# Create Job Title label and entry widget
Label(window, text="Enter a comma-separated list of job titles you are interested in").pack()
job_title_input = StringVar()
job_title_entry = Entry(window, width=120, textvariable=job_title_input)
job_title_saved = get_saved_string(('job_titles.txt'))
job_title_entry.insert(0, job_title_saved)
job_title_entry.pack()

# States List Entry Widget
Label(window, text="Enter a comma-separated list of states you would like to apply to").pack()
states_list_input = StringVar()
states_list_entry = Entry(window, width=120, textvariable=states_list_input)
states_list_saved = get_saved_string('states.txt')
states_list_entry.insert(0, states_list_saved)
states_list_entry.pack()

# Filter_Phrases List Entry Widget
Label(window, text=
    "Enter a Comma-separated list of words/phrases to filter out job listings (Example: MBA Required)").pack()
filter_list_input = StringVar()
filter_list_entry = Entry(window, width=120, textvariable=filter_list_input)
filter_list_saved = get_saved_string('filters.txt')
filter_list_entry.insert(0, filter_list_saved)
filter_list_entry.pack()

# Match_Phrases List Entry Widget
Label(window, text=
    "Enter a Comma-separated list of words/phrases that indicate a good match (Example: Tableau)").pack()
match_list_input = StringVar()
match_list_entry = Entry(window, width=120, textvariable=match_list_input)
match_list_saved = get_saved_string('matches.txt')
match_list_entry.insert(0, match_list_saved)
match_list_entry.pack()

# Match_Phrases List Entry Widget
Label(window, text=
    "Enter the # of jobs you want to search in numeric format").pack()
jobs_list_input = StringVar()
jobs_list_entry = Entry(window, width=10, textvariable=jobs_list_input)
jobs_list_saved = get_saved_string('jobs_count.txt')
jobs_list_entry.insert(0, jobs_list_saved)
jobs_list_entry.pack()



def search_clicked():
    # When button is clicked, make sure mandatory fields are not blank
    blank_counter = 0
    total_input = [jobs_list_input.get(), job_title_input.get()]
    for input in total_input:
        if input == "":
            blank_counter += 1

    if blank_counter > 0:
        messagebox._show(title="Required Fields Missing!", message="Job Title and # of Jobs must not be blank")


    else:
        # Starting Timer
        start_time = time.time()
        now = datetime.datetime.now()
        print("")
        print("Time started: " + str(now.strftime("%m-%d-%Y %H:%M:%S")))

        # Saving Input to Files
        with open('job_titles.txt', 'w') as output:
            output.write(str(job_title_input.get()))
            output.close()

        with open('states.txt', 'w') as output:
            output.write(str(states_list_input.get()))
            output.close()

        with open('filters.txt', 'w') as output:
            output.write(str(filter_list_input.get()))
            output.close()

        with open('matches.txt', 'w') as output:
            output.write(str(match_list_input.get()))
            output.close()

        with open('jobs_count.txt', 'w') as output:
            output.write(str(jobs_list_input.get()))
            output.close()

        # Getting Eligible Job Titles
        job_titles = []
        job_titles_string = job_title_input.get()
        job_titles_raw = job_titles_string.split(",")
        for title in job_titles_raw:
            if title[0] == " ":
                title = title[1:]
            if title[-1] == " ":
                title = title[0:-1]
            job_titles.append(title)
        titles = []
        for title in job_titles:
            title = title.replace(" ", "+")
            titles.append(title)



        # Getting Eligible States
        states_list = []
        states_list_string = states_list_input.get()
        states_list_raw = states_list_string.split(",")

        if len(states_list_raw) > 1:
            for state in states_list_raw:
                if state[0] == " ":
                    state = state[1:]
                if state[-1] == " ":
                    state = state[0:-1]
                states_list.append(state)

        # Getting phrases to remove job descriptions
        filter_list = []
        filter_single_word = ""
        filter_list_string = filter_list_input.get()
        filter_list_raw = filter_list_string.split(",")

        # formatting filter name
        if len(filter_list_raw) > 1:
            for filter in filter_list_raw:
                if filter[0] == " ":
                    filter = filter[1:]
                if filter[-1] == " ":
                    filter = filter[0:-1]

                # Parsing words vs phrases
                single_test = filter.split()
                if len(single_test) > 1:
                    filter_list.append(filter)
                if len(single_test) == 1:
                    filter_single_word = filter_single_word + filter + "%2C+"
            if len(filter_single_word) > 2:
                filter_single_word = filter_single_word[:-4]

        # Getting good matching phrases
        match_list = []
        match_list_string = match_list_input.get()
        match_list_raw = match_list_string.split(",")
        if len(match_list_raw) > 1:
            for match in match_list_raw:
                if match[0] == " ":
                    match = match[1:]
                if match[-1] == " ":
                    match = match[0:-1]
                match_list.append(match)

        # Getting job count entry value
        jobs_count = jobs_list_input.get()

        # Indeed Parameters Setup
        indeed_base = 'https://indeed.com/jobs?q=title%3A('
        separator = '&'
        location = "l"
        assignor = "="
        single_word_filter = "as_not"

        # Indeed setup for results not in the first page
        page_appendor = '&start='
        start = '50'

        opportunity_count = int(jobs_list_input.get())

        search_urls = []
        if len(filter_single_word) > 1:
            if len(states_list) > 0:
                for title in titles:
                    for state in states_list:
                        search_urls.append(indeed_base + title + ")" + separator + location + assignor + state +
                                    separator + single_word_filter + assignor + filter_single_word +
                                    "&sr=directhire&fromage=7&jt=fulltime")
            else:
                for title in titles:
                    search_urls.append(indeed_base + title + ")" +
                                       separator + single_word_filter + assignor + filter_single_word +
                                       "&sr=directhire&fromage=7&jt=fulltime")
        else:
            if len(states_list) > 1:
                search_urls.append(indeed_base + title + ")" + separator + location + assignor + state +
                                   "&sr=directhire&fromage=7&jt=fulltime")
            else:
                search_urls.append(indeed_base + title + ")" + "&sr=directhire&fromage=7&jt=fulltime")

        # Getting urls for pages beyond page 1
        page_urls_numbers = []
        page_count = round((opportunity_count - 50)/50, 0)
        i = 0
        prev_page = 0
        while i < page_count:
            prev_page = prev_page + 50
            page_urls_numbers.append(prev_page)
            i += 1

        secondary_urls = []
        # Adding in non-page-1 urls to url list
        for url in search_urls:
            for number in page_urls_numbers:
                secondary_url = url + page_appendor + str(number)
                secondary_urls.append(secondary_url)
        for url in secondary_urls:
            search_urls.append(url)



        print("Urls:")
        job_keys_list = []
        for url in search_urls:

            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            html_text = soup.prettify()
            list(soup.children)

            # Get Job IDs from url
            job_ids = ','.join(re.findall(r"jobKeysWithInfo\['(.+?)'\]", html_text))
            job_keys = job_ids.split(",")
            for job in job_keys:
                if job not in job_keys_list:
                    job_keys_list.append(job)
            time.sleep(30)

        # Fetch Job Descriptions
        descriptions = {}
        base_url = 'https://www.indeed.com/viewjob?jk='

        for job in job_keys_list:
            temp_url = base_url + job
            job_description = requests.get(temp_url)
            soup = BeautifulSoup(job_description.content, 'html.parser')
            html_text = soup.prettify()
            list(soup.children)

            job_descr = soup.find_all("div", {'class': 'jobsearch-jobDescriptionText'})
            descriptions.update({str(job): str(job_descr)})

        # Removing Descriptions that have filter phrases
        descriptions_filtered = {}
        filter_time_start = time.time()
        print("")
        print("Beginning Filtering Phrases...")
        print("There are " + str(len(filter_list)) + " filter phrases:")
        if len(filter_list) > 0:
            for filter in filter_list:
                print(filter)
            for key, value in descriptions.items():
                pass_count = 0
                fail_count = 0
                for filter in filter_list:
                    if filter.lower() not in value.lower():
                        pass_count += 1
                    else:
                        fail_count += 1
                if fail_count == 0:
                    descriptions_filtered.update({key: value})
        else:
            for key, value in descriptions.items():
                descriptions_filtered.update({key: value})

        filtered_description_counter = 0
        for key, value in descriptions_filtered.items():
            filtered_description_counter += 1
        print("There are " + str(filtered_description_counter) + " job descriptions")
        print(str(len(descriptions) - filtered_description_counter) + " opportunities have been removed by filter phrases")
        print("Finished Filtering Phrases")
        filter_time_end = time.time()
        print("Time to Filter Phrases: " + str(round(filter_time_end - filter_time_start, 6)) + " seconds")

        filtered_matched_descriptions = {}
        if len(match_list) > 0:
            for key, value in descriptions_filtered.items():
                match_counter = 0
                for matching in match_list:
                    count = value.lower().count(matching.lower())
                    match_counter = match_counter + count
#                    print("Occurrences of " + matching + " in " + key + ": " + str(count))
#                print(key + "- Total Matching: " + str(match_counter))
#                print("")

                filtered_matched_descriptions.update({key: match_counter})
            finished_descriptions = filtered_matched_descriptions
        else:
            finished_descriptions = descriptions_filtered

        pre_final_dict = {}
        for key, value in finished_descriptions.items():
            key = "https://www.indeed.com/viewjob?jk=" + key
            pre_final_dict.update({key: value})


        final_dict = sorted(pre_final_dict.items(), key=lambda kv:kv[1], reverse=True)

        #print(final_dict)

        # Insert Data into Treeview from dictionary
        #results_tree.insert("", 'end', final_dict['Link'], final_dict['Points?'])
        for item in final_dict:
            results_tree.insert("", 'end', values=item)

        with open('results.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(final_dict)

        # Time to Complete
        end_time = time.time()
        run_time = str(round(end_time - start_time, 4))
        print("Time to Complete: " + run_time)

        os.startfile('results.csv')


        # for key, value in descriptions_filtered.items():
        #     print("")
        #     print(key)
        #     print(value)
        #     print("")



# Button Action Assignment
search_click = Button(window, text="Search!", command=search_clicked)
search_click.pack()

# Results Table
results_tree = ttk.Treeview(window, columns=("Link", "Points", "Saved?"), show=["headings"])
# Headings
results_tree.heading("#1", text="Link")
results_tree.heading("#2", text="Points")
results_tree.heading("#3", text="Saved?")

# Pack Treeview
results_tree.pack(pady=20)
# Results Table scroll bar
verscrlbar = ttk.Scrollbar(window,
                           orient ="vertical",
                           command = results_tree.yview)
verscrlbar.pack(side ='right', fill ='x')
results_tree.configure(xscrollcommand = verscrlbar.set)


# run the main loop
window.mainloop()



# # First Page URL
# url = ('https://www.indeed.com/jobs?q=title%3A(Product%20Manager)%20-fargo%2C%20-MBA%2C%20-biotech%2C%20-thermo%2C%20-ebay%2C%20-vmware%2C%20-bilingual%2C&sort=date')

