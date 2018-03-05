data_in = "4d420000000000130000000000000000000000000000000000000000000000a2"
new_list = []
for x in data_in:
    new_list.append(x)

for x in range(0, len(data_in), 4):
    print(new_list[x:x+4])
    ans = int(new_list[x] + new_list[x + 1] + new_list[x + 2] + new_list[x + 3], 16)
    print(ans)
