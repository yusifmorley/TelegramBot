#加密文件 使散列算法
import hashlib


def gen_name(str_):

    # 创建一个SHA-1哈希对象
    sha1 = hashlib.sha1()

    # 更新哈希对象的内容
    sha1.update(str(str_).encode('utf-8'))

    # 获取计算后的SHA-1哈希值
    return  sha1.hexdigest()