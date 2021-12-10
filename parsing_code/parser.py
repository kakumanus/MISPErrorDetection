import json
import csv

# NOTE: ORDERING OF INPUT AND OUTPUT FILE LISTS MUST BE EQUIVALENT i.e 1:1 mapping!!!
input_files = ['raw_json/records_test_DATAdev_OP3_EDprob=0.995_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=1.0_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=0.75_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=0.5_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=0.25_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=0.65_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=0.9_USERsim_SETTINGonline_pretrain_10p.json',\
        'raw_json/records_test_DATAdev_OP3_EDprob=0.95_USERsim_SETTINGonline_pretrain_10p.json']

prob_thresholds = [0.995, 1.0, 0.75, 0.5, 0.25, 0.65, 0.9, 0.95]

# JSON Output Files
# output_files = ['output_json/prob=0.995_10p_out.json',\
#         'output_json/prob=1.0_10p_out.json',\
#         'output_json/prob=0.75_10p_out.json',\
#         'output_json/prob=0.50_10p_out.json',\
#         'output_json/prob=0.25_10p_out.json']

# CSV - 1 file with 5 columns (tag name, tag prob, tag resp, # of semantic unit, prob threshold)
output_file = 'output_csv/10p_out.csv'
header = ['tag_name', 'tag_prob', 'tag_resp', '#_in_feedback', 'prob_threshold']
# This is why...
#for input_file, output_file in zip(input_files, output_files):
count = 0
output_list = []
for input_file in input_files:
    with open(input_file) as infile:
        data = infile.read()

    obj = json.loads(data)

    #output_list = [] # Append out tag entries to this list, which will then be appended as a whole to a json file
    for i in range(len(obj)):
        feedback_str = obj[i].get("feedback_records")

        # Check to make sure it's a string (avoiding an error) and also a lack of empty feedback list
        if feedback_str != "[]" and type(feedback_str) == str:
            feedback_list = eval(feedback_str)
            for j in range(len(feedback_list)):
                tag_tuple = feedback_list[j]
                # tag_entry = {
                #     'tag_name': tag_tuple[0][0],
                #     'tag_prob': tag_tuple[0][-2],
                #     'tag_resp': 0 if tag_tuple[1] == 'no' else 1
                # }
                tag_entry = [tag_tuple[0][0],\
                        tag_tuple[0][-2], 0 if tag_tuple[1] == 'no' else 1, \
                        j+1, prob_thresholds[count]]
                output_list.append(tag_entry)
    count = count + 1
    # with open(output_file, mode='w',encoding='utf-8') as outfile:
    #     json.dump(output_list, outfile, indent=2)
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(output_list)