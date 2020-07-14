alpha_beta_lines = list(open("Question 2 (AlphaBeta).log"))
minimax_lines = list(open("Question 2 (Minimax).log"))
savings = []
for i in range (len(alpha_beta_lines)):
    if(i % 2 == 1):
        savings.append((float(minimax_lines[i][15:-1]) - float(alpha_beta_lines[i][15:-1])) / float(minimax_lines[i][15:-1]))

average = 0

for i in savings:
    average += i

average /= len(savings)
print("The total number of savings are ",average * 100)