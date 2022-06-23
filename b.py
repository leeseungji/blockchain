from hashlib import sha256

blockchain = []


def make_genesis_block():
    """첫 블록을 만듭니다"""
    data = 'Genesis'
    prev_hash = b''
    current_hash = make_hash(data, prev_hash)
    blockchain.append((data, prev_hash, current_hash))


def make_hash(data: str, prev_hash: bytes) -> bytes:
    """해시를 만듭니다."""
    # 코드 한 줄이지만, 여기 저기 쓰이니 함수로 분리하는 게 좋습니다.
    # bytes형은 str형이랑 왔다 갔다 헷갈리는 경우가 있어서.
    # 파라미터 뒤에 타입을 기록해 두면 편하더군요.
    return sha256(data.encode() + prev_hash).digest()


def add_block(data: str):
    """블록을 블록 체인에 추가합니다."""
    _, _, prev_hash = blockchain[-1]
    current_hash = make_hash(data, prev_hash)
    blockchain.append((data, prev_hash, current_hash))


def show_blockchain():
    """블록 체인을 보여줍니다."""
    # 해시값을 bytes형으로 저장했기 때문에
    # hex()로 16진수 str로 변환해야 print 시 읽기 좋습니다.
    for i, (data, prev_hash, current_hash) in enumerate(blockchain):
        print(f'블록 {i}\n{data}\n{prev_hash.hex()}\n{current_hash.hex()}')


def verify_blockchain():
    """블록 체인을 검증합니다."""
    for i in range(1, len(blockchain)):
        data, prev_hash, current_hash = blockchain[i]
        last_data, last_prev_hash, last_current_hash = blockchain[i - 1]
        # 변수명이 뭐 같습니다. 코딩보다 작명이 더 어려운 것 같습니다.
        if prev_hash != last_current_hash:
            # 1. 현 블록의 이전 해시 값과
            # 이전 블록의 현재 해시 값이 일치하는 지 확인합니다.
            print(f"블록 {i} 이전 해시 != 블록 {i - 1} 현 해시. \n"
                  f"{prev_hash.hex()} != \n{last_current_hash.hex()}")
            return False
        if last_current_hash != (temp := make_hash(last_data, last_prev_hash)):
            # 2. 이전 블록을 해시 함수로 검증합니다.
            # 이 부분이 없으면 genesis 블록의 검증이 안됩니다.
            print(f"블록 {i - 1} 검증 실패. \n"
                  f"{last_current_hash.hex()} != \n{temp.hex()}")
            return False
        if current_hash != (temp := make_hash(data, prev_hash)):
            # 3. 현 블록을 해시 함수로 검증합니다.
            print(f"블록 {i}, 검증 실패. \n"
                  f"{current_hash.hex()} != \n{temp.hex()}")
            return False
        # print(f'[Block {i}: {blockchain[i][0]}] has been verified.')
    return True


make_genesis_block()
add_block('박혜수')
add_block('박현수')
add_block('이승지')
show_blockchain()
print()
print(verify_blockchain())

blockchain[1] = ('abcd', blockchain[0][2], make_hash('abcd',blockchain[0][2]))
show_blockchain()
print()
print(verify_blockchain())
