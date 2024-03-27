import argparse

parser = argparse.ArgumentParser(description='parser')
arg = parser.add_argument
arg('--user', type=str, default='', help='유사도 계산이 필요한 user의 ip/endpoint를 넣습니다. 현재는 hashed_ip를 넣습니다.')
arg('--save_path', type=str, default='../asset/', help='User vector를 저장할 path를 설정할 수 있습니다.')
arg('--new_item', type=str, default='', help='새로운 상품의 title을 받습니다.')
args = parser.parse_args()