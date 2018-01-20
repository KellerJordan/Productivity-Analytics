import json
import pandas


def main():
    df = pandas.read_json('./dataset/history.json')
    i = 0
    for a in df:
        print(a)
        i += 1
        if i > 5:
            return
    # print(df['visitCount'])
    print(df.iloc[29])


    # with open('./dataset/history.json') as f:
    #     browser_history = json.loads(f.read())
    #     print(browser_history[:3])


if __name__ == '__main__':
    main()


# browser_history = json.loads()
