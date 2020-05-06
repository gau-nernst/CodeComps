Google Hash Code 2020
==================

https://hashcode.withgoogle.com/overview.html

My team, LdR, ranked 2723rd place in the Online Qualification round. Problem statement can be found [here](hashcode_2020_online_qualification_round.pdf)

File structure

|File name|Description|
|---------|-------|
|b_read_on.txt|Datasets|
|b_read_on_output.txt|Results (Output) of my code|
|b_read_on_output2.txt|Results (Output) of my code for the script 2|
|b_read_on_extended_output.txt|Results of my code, after the competition (Extended round)|
|script2.py|Python script version 2|

My code has extended use of List comprehension to speed up the runtime. I came up with a ranking criteria to choose which library will be chosen next for registration. After a library is registered, I removed the duplicated books in all other libraries.

Initially, my ranking criteria is based on the potential points that a library can make if it is chosen. However, the final points is not very optimistic. My teammate included other variables in the ranking criteria, such as duration of registration process, number of books can be sent in a day and others. The idea greatly improved the final points, and it can be reflected in my extended version of the code (done after the competition ends)

```Python
total_score = sum([S[bookId] for bookId in books[libraryIndex][:endIndex]])
weights = [1/math.log(1+Nuniques[i])/T[i] * M[i]**0.8 for i in range(L)]
library_score = total_score**1.2 * weights[libraryIndex]
```