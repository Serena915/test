#无序的数字经过两两比较，每一次比较之后把较大的往后排列，循环多次。
nums=[30,12,56,9,8,68,2]
def bubble(nums):
    for i in range(0,len(nums)-1):         #外层循环多次调用内层循环
        for j in range(0,len(nums)-1-i):   #内层循环  当每次比较结束之后，会确定好最大的数字放在最后，减少了最后的数字比较次数  
           if nums[j]>nums[j+1]:
             nums[j],nums[j+1]=nums[j+1],nums[j]   #两数交换
        print(nums)
bubble(nums)