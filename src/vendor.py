# coding:utf-8
import os, json
PRICE_CASH = 130  # 現金で購入した時の切符の金額
PRICE_EMONEY = 124 # 電子マネーで購入した時の切符の金額
PATH_CASH = "../data/have_money.json" # 所持金情報を格納するファイル
PATH_EMONEY = "../data/electric_money_balance.txt" # 電子マネー残高情報を格納するファイル

def electric_money(before_balance):
    '''
    電子マネー処理
    :param before_balance:電子マネーの購入前残高
    :return:success:引去成功・失敗(成功の場合：1、失敗の場合：2)
    　　　　　　after_balance: 電子マネーの購入後残高
    　　　　　　PRICE_EMONEY：引去金額(切符代金)
    '''
    if before_balance < PRICE_EMONEY:
        success = 2
        after_balance = before_balance
    else:
        after_balance = before_balance - PRICE_EMONEY
        success = 1
    return success, after_balance, PRICE_EMONEY

def main():
    insert_money = {"10000": 0, "5000": 0, "1000": 0, "500": 0, "100": 0, "50": 0, "10": 0}
    change_money = {"10000": 0, "5000": 0, "1000": 0, "500": 0, "100": 0, "50": 0, "10": 0}
    if not os.path.exists(PATH_CASH):
        os.makedirs("../data", exist_ok=True)
        have_money = {"10000": 1, "5000": 1, "1000": 1, "500": 1, "100": 2, "50": 3, "10": 15}
    else:
        with open(PATH_CASH, 'r') as f:
            have_money = json.load(f)

    flag = 1
    print("現金または電子マネーを投入してください")
    money = 0
    while money < PRICE_CASH:
        insert = input()
        if insert == 'e-money': # 金種の代わりに「e-money」と打ち込めば電子マネーを使用して購入できる
            flag = 2
            break
        else:
            have_money[insert] -= 1
            insert_money[insert] += 1
            money += int(insert)

    if flag == 1:
        change = money - PRICE_CASH
        for k in change_money.keys():
            while change >= int(k):
                change -= int(k)
                change_money[k] += 1
                have_money[k] += 1
        print("投入金額")
        for k, v in insert_money.items():
            print(" {}円：{}枚".format(k, v))
        print("釣り銭")
        for k, v in change_money.items():
            print(" {}円：{}枚".format(k, v))
        print("所持金")
        for k, v in have_money.items():
            print(" {}円：{}枚".format(k, v))
        with open(PATH_CASH, 'w') as f:
            json.dump(have_money, f)
    else:
        if not os.path.exists(PATH_EMONEY):
            os.makedirs("../data", exist_ok=True)
            before_balance = 1000
        else:
            with open(PATH_EMONEY, 'r') as f:
                before_balance = int(f.read())
        success, after_balance, used = electric_money(before_balance)
        with open(PATH_EMONEY, 'w') as f:
            f.write(str(after_balance))
        print('購入前の電子マネー残高：{}円'.format(before_balance))
        if success == 2:
            print("残高が不足しています。(引去失敗)")
        else:
            print("購入後の電子マネー残高：{}円".format(after_balance))
            print("引去額：{}円".format(used))

if __name__ == '__main__':
    main()
