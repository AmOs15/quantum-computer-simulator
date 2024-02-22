import numpy as np
import matplotlib.pyplot as plt

#アダマールゲート
H = np.matrix([[1/np.sqrt(2), 1/np.sqrt(2)], 
                [1/np.sqrt(2), -1/np.sqrt(2)]])
#Xゲート　パウリ行列
X = np.matrix([[0, 1], 
               [1, 0]])
#Yゲート　パウリ行列
Y = np.matrix([[0, -1j],
               [1j, 0]])
#Zゲート　パウリ行列
Z = np.matrix([[1, 0],
               [0, -1]])
#単位行列
I = np.matrix([[1, 0],
               [0, 1]])               
#Sゲート　位相ゲート
S = np.matrix([[1, 0],
               [0, 1j]])
#S_t(ダガー)ゲート 
S_dagger = np.matrix([[1,0],
                      [0, -1j]])
#Tゲート　π/8ゲート
T = np.matrix([[1, 0],
               [0, (1 / np.sqrt(2)) + (1 / np.sqrt(2))*1j]])
#T_t(ダガー)ゲート
T_dagger = np.matrix([[1, 0],
                      [0, (1 / np.sqrt(2)) - (1 / np.sqrt(2))*1j]])
#|0><0|
E =  np.matrix([[1, 0],
                [0, 0]])
#|1><1|
F = np.matrix([[0, 0],
               [0, 1]])

#量子計算を行う
def simulateQComputer(vector: np.ndarray, CList, num):
    for i in range(len(CList[0])):
        gate = ''.join([CList[j][i] for j in range(num-1, -1, -1)])
        print(f"{i}:{gate}")
        chk = -1
        for i in range(len(gate)):
            if gate[i].isdigit():
                chk = i
        if(chk != -1):
            vector = ctrZ(gate, chk, vector)
            print(vector)
            continue
        vector = np.ravel(getMatrix(gate) @ vector)
        print(getMatrix(gate))
        print(vector)

    return vector

#コントロールZ
def ctrZ(gate, index, vector):
    gateA:str = []
    gateB:str = []
    for i in range(len(gate)):
        if(i == (len(gate)-int(gate[index])-1)):
            print("E F")
            gateA.append('E')
            gateB.append('F')
        elif(i == index):
            gateA.append('I')
            gateB.append('X')
            print("I X")
        else:
            gateA.append('I')
            gateB.append('I')
            print("I I")
    result = np.ravel((getMatrix(gateA)+getMatrix(gateB)) @ vector)
    print(getMatrix(gateA))
    print(getMatrix(gateB))
    print(getMatrix(gateA)+getMatrix(gateB))
    return result
    

#ゲートの行列の作成
def getMatrix(gate):
    gateA = setMatrix(gate[0])
    for i in range(1, len(gate)):
        gateB = setMatrix(gate[i])
        gateA = np.kron(gateA, gateB)
    return gateA
    

#文字から量子ゲート
def setMatrix(QGate):
    switcher = {
        'I': I, 'H': H, 'X': X, 'Y': Y, 'Z': Z,
        'S': S, 's': S_dagger, 'T': T, 't': T_dagger,
        'E': E, 'F': F
    }
    return switcher.get(QGate, I)

n: int = int(input("量子ビット数の入力："))  # ビット数の入力
init = input("量子ビットの初期状態の入力：")
qbitVector: np.ndarray = np.zeros(2**n, dtype=np.complex128) #量子ビットのベクトル
qbitVector[int(init, 2)] += 1

circuitList :str = []  # 回路を表す文字列を格納するリスト
for i in range(n):
    gate = input()
    circuitList.append(gate)

# 量子計算の実行
qsimResult = simulateQComputer(qbitVector, circuitList, n)

# 結果の出力
print("result:")
for num in qsimResult:
    print(f'{num:.3f}')

# 確率の出力
print("probability:")
for i in range(len(qsimResult)):
    print(f"{i:08b}: {np.abs(qsimResult[i])**2:.3f}")

# 二進数表記
binary_labels = [format(i, '06b') for i in range(len(qsimResult))]
# 実部の取得
real_parts = [num.real for num in qsimResult]
# 棒グラフの色を設定
colors = ['blue' if num >= 0 else 'red' for num in real_parts]
# 棒グラフの描画
plt.bar(binary_labels, real_parts, color=colors)
# 軸ラベルの設定
plt.xlabel('量子ビット')
plt.ylabel('確率振幅')
# グリッドの表示
plt.grid(True)
# グラフの表示
plt.show()