import itertools
import math
import json

class HMM:
    def __init__(self, states, alphabet, pi, a, e):
        self.states = states
        self.alphabet = alphabet
        a_keys = [list(a[x].keys()) for x in a.keys()]
        a_key_bool = True if (a_keys[0] == x for x in a_keys) else False

        e_keys = [list(e[x].keys()) for x in e.keys()]
        e_key_bool = True if (e_keys[0] == x for x in e_keys) else False
        if list(pi.keys()) == list(a.keys()) and list(a.keys()) == list(e.keys()) and list(e.keys()) == states and a_key_bool and states == list(a_keys[0]):
            pass
        else:
            raise ValueError("Incorrect format")
        if list(e_keys[0]) == alphabet and e_key_bool:
            pass
        else:
            raise ValueError("Incorrect format")
        self.pi = pi
        self.a = a
        self.e = e
        self.log_pi = {key:log2(self.pi[key]) for key in self.pi.keys()}
        self.log_e = {}
        for key in self.e.keys():
            self.log_e[key] = {key_s:log2(self.e[key][key_s]) for key_s in self.e[key].keys()}
        self.log_a = {}
        for key in self.a.keys():
            self.log_a[key] = {key_s:log2(self.a[key][key_s]) for key_s in self.a[key].keys()}
        print(self.log_a)

    def joint_probability(self, x, z):
        mult = 1
        fist_iter = True
        for i in range(len(x)):
            if fist_iter:
                fist_iter = False
                mult = mult * self.pi[z[i]]

            else:
                mult = mult * self.a[z[i-1]][z[i]]
            mult = mult * self.e[z[i]][x[i]]
        return mult

    def log_joint(self, x, z):
        sum = 0
        fist_iter = True
        for i in range(len(x)):
            if fist_iter:
                fist_iter = False
                sum += self.log_pi[z[i]]

            else:
                sum += self.log_a[z[i-1]][z[i]]
            sum += self.log_e[z[i]][x[i]]
        return sum

    def brute_force(self, x):
        max_p = 0
        best_c = ""
        sum = 0
        comb = ["".join(x) for x in list(itertools.product(self.states, repeat=len(x)))]
        for c in comb:
            if self.joint_probability(x, c) > max_p:
                best_c = c
                max_p = self.joint_probability(x, c)
            sum += self.joint_probability(x, c)
        return (best_c, max_p, sum)


    def viterbi(self, x):
        v = [{} for _ in range(len(x))]
        back = [{} for _ in range(len(x))]
        first = True
        for i in range(len(x)):
            if first:
                first = False
                for key in self.states:
                    v[i][key] = self.log_pi[key] + self.log_e[x[i]]
            else:




def log2(p):
    if p == 0:
        return -math.inf
    else:
        return math.log2(p)

def read_model(path):
    with open(path, "r") as file:
        data = json.load(file)
    print(data)
    hmm = HMM(data["states"], data["alphabet"], data["pi"], data["a"], data["e"])
    return hmm



hmm = read_model("weather_model.json")
print(hmm.brute_force("ssrssrrrss"))

