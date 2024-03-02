import pymysql


def get_product_list_from_db():
    datas = []
    # 获取数据库链接
    connection = pymysql.connect(host="localhost", user="root", passwd="123456", db="jd", port=3306,
                                 charset="utf8")
    try:
        # 获取会话指针
        with connection.cursor() as cursor:
            # 创建sql语句
            sql = "select * from jd_product"

            # 执行sql语句
            cursor.execute(sql)

            datas = cursor.fetchall()

            # 提交数据库
            connection.commit()
    finally:
        connection.close()

    return datas


if __name__ == '__main__':
    product_list = get_product_list_from_db()
    # print(data)
    i = 0
    for product in product_list:
        # print(product[1])
        i += 1
    print(i)
