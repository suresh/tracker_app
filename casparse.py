import casparser
# data = casparser.read_cas_pdf("/path/to/cas/file.pdf", "password")

# Get data in json format
json_str = casparser.read_cas_pdf("data/march2021-portfolio.pdf", "3454p3", output="json")
print(json_str) 

# # Get transactions data in csv string format
# csv_str = casparser.read_cas_pdf("/path/to/cas/file.pdf", "password", output="csv")
