import math

# 状态的样本空间
states = ('FF', 'L1_0.4', 'L1_0.7', 'L2_0.4', 'L2_0.7')
# 观测的样本空间
observations = ('0.6m', '1.05m', 'a1.05m')
# 起始个状态概率
start_probability = {'FF': 0.2, 'L1_0.4': 0.2, 'L1_0.7': 0.2, 'L2_0.4': 0.2, 'L2_0.7': 0.2}
# 状态转移概率
transition_probability = {
    'FF': {'FF': 0.75, 'L1_0.4': 0.10, 'L1_0.7': 0.05, 'L2_0.4': 0.05, 'L2_0.7': 0.05},
    'L1_0.4': {'FF': 0.10, 'L1_0.4': 0.70, 'L1_0.7': 0.10, 'L2_0.4': 0.05, 'L2_0.7': 0.05},
    'L1_0.7': {'FF': 0.05, 'L1_0.4': 0.10, 'L1_0.7': 0.70, 'L2_0.4': 0.15, 'L2_0.7': 0.05},
    'L2_0.4': {'FF': 0.05, 'L1_0.4': 0.10, 'L1_0.7': 0.10, 'L2_0.4': 0.60, 'L2_0.7': 0.15},
    'L2_0.7': {'FF': 0.05, 'L1_0.4': 0.05, 'L1_0.7': 0.05, 'L2_0.4': 0.15, 'L2_0.7': 0.70},
}
# 状态->观测的发散概率
emission_probability = {
    'FF': {'0.6m': 0.10, '1.05m': 0.30, 'a1.05m': 0.60},
    'L1_0.4': {'0.6m': 0.70, '1.05m': 0.20, 'a1.05m': 0.10},
    'L1_0.7': {'0.6m': 0.30, '1.05m': 0.50, 'a1.05m': 0.20},
    'L2_0.4': {'0.6m': 0.70, '1.05m': 0.20, 'a1.05m': 0.10},
    'L2_0.7': {'0.6m': 0.30, '1.05m': 0.50, 'a1.05m': 0.20},
}


def E(x):
    # return math.pow(math.e,x)
    return x


def get_state_sequence(result_m):
    infered_states = []
    final = len(result_m) - 1
    (p, pre_state), final_state = max(zip(result_m[final].values(), result_m[final].keys()))
    infered_states.insert(0, final_state)
    infered_states.insert(0, pre_state)
    for t in range(final - 1, 0, -1):
        _, pre_state = result_m[t][pre_state]
        infered_states.insert(0, pre_state)
    return infered_states


def viterbi(obs, states, start_p, trans_p, emit_p):
    result_m = [{}]  # 存放结果,每一个元素是一个字典，每一个字典的形式是 state:(p,pre_state)
    # 其中state,p分别是当前状态下的概率值，pre_state表示该值由上一次的那个状态计算得到
    for s in states:  # 对于每一个状态
        result_m[0][s] = (E(start_p[s] * emit_p[s][obs[0]]), None)  # 把第一个观测节点对应的各状态值计算出来

    for t in range(1, len(obs)):
        result_m.append({})  # 准备t时刻的结果存放字典，形式同上

        for s in states:  # 对于每一个t时刻状态s,获取t-1时刻每个状态s0的p,结合由s0转化为s的转移概率和s状态至obs的发散概率
            # 计算t时刻s状态的最大概率，并记录该概率的来源状态s0
            # max()内部比较的是一个tuple:(p,s0),max比较tuple内的第一个元素值
            result_m[t][s] = max(
                [(E(result_m[t - 1][s0][0] * trans_p[s0][s] * emit_p[s][obs[t]]), s0) for s0 in states])
    return result_m  # 所有结果（包括最佳路径）都在这里，但直观的最佳路径还需要依此结果单独生成，在显示的时候生成


def cal_state_sequence(distance_sequence):
    obs = []
    for i in distance_sequence:
        if i < 0.6:
            obs.append("0.6m")
        elif i < 1.05:
            obs.append("1.05m")
        elif i > 1.05:
            obs.append("a1.05m")
        else:
            pass
    result_m = viterbi(obs, states, start_probability, transition_probability, emission_probability)
    return get_state_sequence(result_m)
