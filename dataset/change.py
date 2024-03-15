import pandas as pd
import io

# Input dataset
input_data = """
train_ID,origin,arrival,departure_time,arrival_time,delay,train_type,detection_date
13,Mumbai_CST,Kolkata_Howrah_Junction,399,503.0,5,,2023-08-13
20,Kolkata_Howrah_Junction,Mumbai_CST,398,489.0,5,,2023-08-13
25,Mumbai_CST,Kolkata_Howrah_Junction,532,623.0,5,,2023-08-13
26,Kolkata_Howrah_Junction,Mumbai_CST,458,549.0,5,,2023-08-13
29,Mumbai_CST,Kolkata_Howrah_Junction,579,683.0,5,,2023-08-13
31,Mumbai_CST,Kolkata_Howrah_Junction,639,743.0,5,,2023-08-13
32,Mumbai_Central,Delhi_Junction,517,600.0,6,,2023-08-13
34,Mumbai_Central,Delhi_Junction,788,886.0,6,,2023-08-13
35,Delhi_Junction,Chennai_Central,499,764.0,6,,2023-08-13
36,Kolkata_Howrah_Junction,Mumbai_CST,578,669.0,5,,2023-08-13
39,Delhi_Junction,Mumbai_Central,980,1063.0,6,,2023-08-13
40,Kolkata_Howrah_Junction,Mumbai_CST,638,742.0,5,,2023-08-13
41,Delhi_Junction,Mumbai_Central,1277,1360.0,5,,2023-08-13
44,Chennai_Central,Delhi_Junction,984,1249.0,6,,2023-08-13
46,Mumbai_Central,Delhi_Junction,1052,1135.0,6,,2023-08-13
47,Delhi_Junction,Mumbai_Central,621,704.0,6,,2023-08-13
49,Mumbai_CST,Kolkata_Howrah_Junction,879,983.0,5,,2023-08-13
50,Mumbai_Central,Delhi_Junction,460,543.0,6,,2023-08-13
51,Delhi_Junction,Mumbai_Central,568,651.0,6,,2023-08-13
52,Mumbai_Central,Delhi_Junction,696,779.0,6,,2023-08-13
53,Delhi_Junction,Mumbai_Central,812,895.0,6,,2023-08-13
54,Mumbai_Central,Delhi_Junction,934,1017.0,6,,2023-08-13
55,Mumbai_CST,Kolkata_Howrah_Junction,939,1043.0,5,,2023-08-13
56,Mumbai_Central,Delhi_Junction,1100,,6,,2023-08-13
57,Delhi_Junction,Mumbai_Central,923,1006.0,6,,2023-08-13
59,Delhi_Junction,Mumbai_Central,1217,1300.0,5,,2023-08-13
61,Mumbai_CST,Kolkata_Howrah_Junction,1012,1103.0,5,,2023-08-13
66,Kolkata_Howrah_Junction,Mumbai_CST,998,1102.0,5,,2023-08-13
67,Mumbai_CST,Kolkata_Howrah_Junction,1072,1163.0,5,,2023-08-13
75,Mumbai_CST,Kolkata_Howrah_Junction,1132,1223.0,5,,2023-08-13
78,Kolkata_Howrah_Junction,Mumbai_CST,1118,1222.0,5,,2023-08-13
82,Chennai_Central,Delhi_Junction,815,,5,,2023-08-13
83,Mumbai_CST,Kolkata_Howrah_Junction,1239,1343.0,5,,2023-08-13
84,Delhi_Junction,Bengaluru,636,950.0,6,,2023-08-13
86,Delhi_Junction,Bengaluru,661,,6,,2023-08-13
88,Delhi_Junction,Bengaluru,464,708.0,5,,2023-08-13
114,Chennai_Central,Mumbai_CST,376,438.0,5,,2023-08-13
117,Mumbai_CST,Chennai_Central,463,524.0,5,,2023-08-13
122,Chennai_Central,Mumbai_CST,436,498.0,5,,2023-08-13
123,Mumbai_CST,Chennai_Central,523,584.0,5,,2023-08-13
126,Chennai_Central,Mumbai_CST,496,558.0,5,,2023-08-13
129,Mumbai_CST,Chennai_Central,583,644.0,5,,2023-08-13
131,Mumbai_CST,Chennai_Central,643,704.0,5,,2023-08-13
132,Chennai_Central,Mumbai_CST,556,618.0,5,,2023-08-13
135,Mumbai_CST,Chennai_Central,703,764.0,5,,2023-08-13
136,Chennai_Central,Mumbai_CST,616,678.0,5,,2023-08-13
140,Chennai_Central,Mumbai_CST,676,738.0,5,,2023-08-13
141,Mumbai_CST,Chennai_Central,763,824.0,5,,2023-08-13
144,Chennai_Central,Mumbai_CST,736,798.0,5,,2023-08-13
145,Mumbai_CST,Chennai_Central,823,884.0,5,,2023-08-13
146,Chennai_Central,Mumbai_CST,796,858.0,5,,2023-08-13
149,Mumbai_CST,Chennai_Central,883,944.0,5,,2023-08-13
150,Chennai_Central,Mumbai_CST,856,918.0,5,,2023-08-13
151,Chennai_Central,Mumbai_Central,902,950.0,5,,2023-08-13
153,Chennai_Central,Mumbai_Central,1135,1190.0,5,,2023-08-13
154,Mumbai_CST,Chennai_Central,916,978.0,5,,2023-08-13
155,Chennai_Central,Mumbai_CST,943,1004.0,5,,2023-08-13
156,Mumbai_Central,Chennai_Central,490,550.0,5,,2023-08-13
158,Mumbai_Central,Chennai_Central,610,670.0,5,,2023-08-13
159,Mumbai_CST,Chennai_Central,1003,1064.0,5,,2023-08-13
160,Chennai_Central,Mumbai_CST,976,1038.0,5,,2023-08-13
165,Mumbai_CST,Chennai_Central,1063,1124.0,5,,2023-08-13
166,Chennai_Central,Mumbai_CST,1036,1098.0,5,,2023-08-13
170,Chennai_Central,Mumbai_CST,1096,1158.0,5,,2023-08-13
173,Mumbai_CST,Chennai_Central,1123,1184.0,5,,2023-08-13
176,Chennai_Central,Mumbai_CST,1156,1218.0,5,,2023-08-13
179,Mumbai_CST,Chennai_Central,1183,1244.0,5,,2023-08-13
180,Chennai_Central,Mumbai_CST,1216,1278.0,5,,2023-08-13
183,Mumbai_CST,Chennai_Central,1243,1304.0,5,,2023-08-13
184,Chennai_Central,Mumbai_CST,1276,1338.0,5,,2023-08-13
187,Mumbai_CST,Chennai_Central,1303,1364.0,5,,2023-08-13
188,Chennai_Central,Mumbai_CST,1336,1398.0,5,,2023-08-13
191,Mumbai_CST,Chennai_Central,1363,1424.0,5,,2023-08-13
233,Vadodara,Mumbai_Central,326,692.0,6,,2023-08-13
235,Mumbai_Central,Vadodara,1038,1429.0,6,,2023-08-13
240,Mumbai_Central,Vadodara,1038,1429.0,6,,2023-08-13
241,Vadodara,Mumbai_Central,326,692.0,6,,2023-08-13
242,Vadodara,Mumbai_Central,326,692.0,6,,2023-08-13
243,Vadodara,Mumbai_Central,326,692.0,6,,2023-08-13
244,Mumbai_Central,Vadodara,1038,1429.0,6,,2023-08-13
245,Mumbai_Central,Vadodara,1038,1429.0,6,,2023-08-13
287,Bengaluru,Chennai_Central,365,540.0,5,,2023-08-13
288,Bengaluru,Chennai_Central,365,540.0,5,,2023-08-13
289,Bengaluru,Chennai_Central,365,540.0,5,,2023-08-13
296,Chennai_Central,Bengaluru,1275,1415.0,5,,2023-08-13
"""

# Convert the input data to a DataFrame
data = pd.read_csv(pd.compat.String.io(input_data))

# Function to map train_ID values to numbers in the range 10001 to 15000
def map_train_ID(train_ID):
    return train_ID + 10000

# Apply the mapping function to the train_ID column
data['train_ID'] = data['train_ID'].apply(map_train_ID)

# Output the updated dataset in the same format as input
output_data = data.to_csv(index=False)
print(output_data)
