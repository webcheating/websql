import string

nums = [str(i) for i in range(501)]
print(f"nums: {nums}")
left, right = 0, len(nums) - 1
print(f"left, right = {left}, {right}")
#while left <= right:
#    mid = (left + right) // 2
#    print(f"mid = {nums[mid]}")


chars = sorted(string.ascii_letters + string.digits)
chars2 = sorted(string.ascii_lowercase + string.digits)
print(f"chars: {chars}")
print(f"chars2: {chars2}")
left2, right2 = 0, len(chars2) - 1
left3, right3 = 0, len(chars) - 1
mid2 = (left2 + right2) // 2
mid = (left3 + right3) // 2
print(f"left2, right2 = {left2}, {right2} || mid == {mid} || chars2[mid2] == {chars2[mid2]} || chars[mid] = {chars[mid]}")
#while left2 <= right2:
#    mid2 = (left2 + right2) // 2
#    print(f"mid2 = {chars[mid2]}")
