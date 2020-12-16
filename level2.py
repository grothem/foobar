"""
Ion Flux Relabeling

Oh no! Commander Lambda's latest experiment to improve the efficiency of
her LAMBCHOP doomday device has backfired spectacularly. She had ben
improving the strucutre of the ion flux converter tree, but somthing went
terribly wrong and the flux chains exploded. Some of the ion flux converters
survived the explosion intact, but others had their position labels blased
off. She's having her henchmen rebuild the ion flux converter tree by
hand, buy you think you can do it much more quickly - quickly enough, perhaps
to ear a promotion!

Flux chaines require perfect binary trees, so Lambda's design arranged the ion flux
converts to form one. To label them, sher perfomred post-order traversal of the tree
of converters and labeld each overter with the order of that coverter in the
traversal., starting at 1.

Write a function solution(h, q) - where h is the height of the perfect tree
of coverters and q is a list of positive integers representing different
flux converters - which returns a list of integers p where each element in p
is the label of the converter that sits on top of the respective coverter in
q, or -1 if there is no such coverter. For example, solution(3, [1, 4, 7]) would return
the coverters above the coverters at indexes 1, 4, and 7 in a perfect binary tree
height of 3, which is [3, 6, -1].
"""

def solution(h, q):
    rootNodeValue = 2**h - 1
    answers = []
    for i in q:
        answers.append(search(rootNodeValue, i, h))

    return answers

def search(rootNodeValue: int, targetValue: int, level: int) -> int:
    leftValue = leftNodeValue(rootNodeValue, level)
    rightValue = rootNodeValue - 1

    if leftValue == targetValue or rightValue == targetValue:
        return rootNodeValue

    if targetValue <= leftValue:
        return search(leftValue, targetValue, level - 1)
    elif targetValue <= rightValue:
        return search(rightValue, targetValue, level - 1)
    else:
        return - 1

def leftNodeValue(parentNodeValue: int, level: int) -> int:
    return parentNodeValue - 2**(level - 1)

print(solution(5, [19,14,28]))