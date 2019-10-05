# paper_crawler
this crawler is to collect papers from arxiv and conference.

for different conference, keyword and time range, please modify following variable
## this is an example
    conferences = ['www']                                 # conference shortcut on dblp
    context_key = set(['change'])                         # keyword in title
    arthur_key = set(['Kuo Yu Huang'])                    # arthur's full name
    months = ['{:0>2d}'.format(i+1) for i in range(12)]   # month for arxiv
    years = ['{:0>2d}'.format(i) for i in range(17, 20)]  # year for conference and arxiv
    fields = ['CL']                                       # category shortcut on arxiv
