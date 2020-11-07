# job_finder
Allows U.S. job-seekers to specify multiple job titles, multiple states, filter words/phrases, and skills. Scrapes indeed.com for matching results, sorts by job descriptions that have the highest matching skills/phrases. 

The "Job Titles" field and "# of jobs" fields are required before the application will commence the search. 

The program will create urls to query indeed.com based on the user entry. To prevent indeed.com blocking the program with a reCaptcha, a 30 second timer will start after each indeed.com query. Use this information to determine how long the program will take to run. Each job title + each state is a query. For each job + title, for each "# of jobs" increment of 50, a new url will be queried. For example, a query set for "Product Manager" in "California, Washington" with "# of job = 100" will require searching:
job title + california
job title + california (page 2) 
job title + washington
job title + washington (page 2) 

If each query uses the 30 second delay timer, the minimum time for the above queries to complete would be 2 minutes. With 5 job titles and 5 states searching for 200 jobs on each query, 100 queries would be necessary. 100 * 30 seconds = 3000 seconds, which is 50 minutes. In future versions, I will implement a reCaptcha bypass and the delay timer will be removed, allowing the program to run the same number of queries in 10% of the time. 

When the process is finished, the program will open a CSV file with links to each job, as well as how many matching words/phrases/skills entered were in the job description. 

Note that the settings are currently hardcoded to only search for jobs that are "Full-Time" and were posted in the last 7 days. 

Happy hunting!