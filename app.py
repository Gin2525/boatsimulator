from flask import Flask, render_template, request

app = Flask(__name__)

w = [1,1,1,1,30]#重みの宣言

@app.route('/')
def simulator():
    
    return render_template('simulator.html',w=w)

@app.route('/results/',methods=['POST'])
def reusults():
    scores = list() #選手のスコアの格納用
    points = list() #各選手のポイントの格納用
    sorted_points = list() #rank付け用の別途ソートした数列を用意

    for i in range(6):
        scores.append(list()) #二次元配列を宣言

    for i in range(6): #player i のデータを2次元配列:scoresに順次格納
        scores[i].append(7-int(request.form[f"player{i+1}_rOw"]))
        scores[i].append(7-int(request.form[f"player{i+1}_moter"]))
        scores[i].append(7-int(request.form[f"player{i+1}_starttime"]))
        scores[i].append(7-int(request.form[f"player{i+1}_tOe"]))
        scores[i].append(int(request.form[f"player{i+1}_cOf"])) # フライングは最後に格納。

    #重みを格納
    w[0]=int(request.form["w_rOw"])
    w[1]=int(request.form["w_moter"])
    w[2]=int(request.form["w_starttime"])
    w[3]=int(request.form["w_tOe"])
    w[4]=int(request.form["w_cOf"])

    # 格納終わり。ポイントの計算を行う。

    for i in range(6):
        points.append(list())
        point = 0
        points[i].append(f"player{i+1}")
        if scores[i][4] == 2: #cOfが2なら失格にする。
            points[i].append(0) #0を格納
            continue #0のまま次の選手に。
        else:
            for j in range(4):
                point += scores[i][j] * w[j] #各cOf以外のスコアを重みを掛けて加算する。
            point -= scores[i][4] * w[4]#フライングの減点を行う。
            points[i].append(point)

    #points[i][2]に順番づけを行う為にソート済みのpointsを用意。
    for i in range(6):
        points[i].append(0)#ついでにpoints[2]に初期値を代入
        sorted_points.append(points[i][1])#ソート用の配列に格納
    sorted_points = sorted(sorted_points,reverse=True) #降順でソートを行う。

    #points[i][2]に順番に対応している数字を格納する。
    for i in range(6):
        for j in range(6):
            if points[j][2]==0 and points[j][1]==sorted_points[i]: #sortedからpoints[i][1]と同じものを探す
                points[j][2]=i+1
                break

    #最終的に[player, point, rank]をhtmlに渡す。
    return render_template('results.html',points=points)

if __name__ == "__main__":
    app.run()