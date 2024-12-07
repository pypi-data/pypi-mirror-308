############################################################################

# Created by: Marcio Pereira Basilio, Valdecy Pereira, Fatih Yigit
# email:      valdecy.pereira@gmail.com
# GitHub:     <https://github.com/Valdecy>

# The EC-TOPSIS Method - A Committee Approach for Outranking Problems Using Randoms Weights

############################################################################

# Required Libraries
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import seaborn as sns

from collections import Counter
from matplotlib import colormaps
from matplotlib.ticker import MaxNLocator

###############################################################################

# EC TOPSIS Class
class ec_topsis():
    def __init__(self, dataset, criterion_type, custom_sets = [], iterations = 10000):
      self.data  = np.copy(dataset).astype(float)
      self.ctype = criterion_type
      self.cset  = custom_sets
      self.iter  = iterations
      self.f     = -1
      self.run()
      
    ###############################################################################
    
    # Function: CRITIC (CRiteria Importance Through Intercriteria Correlation). From https://github.com/Valdecy/pyDecision
    def critic_method(self):
        X     = np.copy(self.data).astype(float)
        best  = np.zeros(X.shape[1])
        worst = np.zeros(X.shape[1])
        for i in range(0, X.shape[1]):
            if (self.ctype[i] == 'max'):
                best[i]  = np.max(X[:, i])
                worst[i] = np.min(X[:, i])
            else:
                best[i]  = np.min(X[:, i])
                worst[i] = np.max(X[:, i])
            if (best[i] == worst[i]):
                best[i]  = best[i]  + 1e-9
                worst[i] = worst[i] - 1e-9
        for j in range(0, X.shape[1]):
            X[:,j] = ( X[:,j] - worst[j] ) / ( best[j] - worst[j] )
        std      = (np.sum((X - X.mean())**2, axis = 0)/(X.shape[0] - 1))**(1/2)
        sim_mat  = np.corrcoef(X.T)
        conflict = np.sum(1 - sim_mat, axis = 1)
        infor    = std*conflict
        weights  = infor/np.sum(infor)
        return weights

    ###############################################################################
    
    # Function: Entropy. From https://github.com/Valdecy/pyDecision
    def entropy_method(self):
        X = np.copy(self.data).astype(float)
        for j in range(0, X.shape[1]):
            if (self.ctype[j] == 'max'):
                X[:,j] =  X[:,j] / np.sum(X[:,j])
            else:
                X[:,j] = (1 / X[:,j]) / np.sum((1 / X[:,j]))
        X = np.abs(X)
        H = np.zeros((X.shape))
        for j, i in itertools.product(range(H.shape[1]), range(H.shape[0])):
            if (X[i, j]):
                H[i, j] = X[i, j] * np.log(X[i, j] + 1e-9)
        h = np.sum(H, axis = 0) * (-1 * ((np.log(H.shape[0] + 1e-9)) ** (-1)))
        d = 1 - h
        d = d + 1e-9
        w = d / (np.sum(d))
        return w

    ###############################################################################
    
    # Function: Rank. From https://github.com/Valdecy/pyDecision
    def ranking(self):    
        rank_xy = np.zeros((self.f.shape[0], 2))
        for i in range(0, rank_xy.shape[0]):
            rank_xy[i, 0] = 0
            rank_xy[i, 1] = self.f.shape[0]-i           
        for i in range(0, rank_xy.shape[0]):
            plt.text(rank_xy[i, 0],  rank_xy[i, 1], 'a' + str(int(self.f[i,0])), size = 12, ha = 'center', va = 'center', bbox = dict(boxstyle = 'round', ec = (0.0, 0.0, 0.0), fc = (0.8, 1.0, 0.8),))
        for i in range(0, rank_xy.shape[0]-1):
            plt.arrow(rank_xy[i, 0], rank_xy[i, 1], rank_xy[i+1, 0] - rank_xy[i, 0], rank_xy[i+1, 1] - rank_xy[i, 1], head_width = 0.01, head_length = 0.2, overhang = 0.0, color = 'black', linewidth = 0.9, length_includes_head = True)
        axes = plt.gca()
        axes.set_xlim([-1, +1])
        ymin = np.amin(rank_xy[:,1])
        ymax = np.amax(rank_xy[:,1])
        if (ymin < ymax):
            axes.set_ylim([ymin, ymax])
        else:
            axes.set_ylim([ymin-1, ymax+1])
        plt.axis('off')
        plt.tight_layout()
        plt.show() 
        return
    
    # Function: TOPSIS. From https://github.com/Valdecy/pyDecision
    def topsis_method(self, weights, graph = False, verbose = False):
        X         = np.copy(self.data)
        w         = np.copy(weights)
        sum_cols  = np.sum(X*X, axis = 0)
        sum_cols  = sum_cols**(1/2)
        r_ij      = X/sum_cols
        v_ij      = r_ij*w
        p_ideal_A = np.zeros(X.shape[1])
        n_ideal_A = np.zeros(X.shape[1])
        for i in range(0, X.shape[1]):
            if (self.ctype[i] == 'max'):
                p_ideal_A[i] = np.max(v_ij[:, i])
                n_ideal_A[i] = np.min(v_ij[:, i])
            else:
                p_ideal_A[i] = np.min(v_ij[:, i])
                n_ideal_A[i] = np.max(v_ij[:, i]) 
        p_s_ij = (v_ij - p_ideal_A)**2
        p_s_ij = np.sum(p_s_ij, axis = 1)**(1/2)
        n_s_ij = (v_ij - n_ideal_A)**2
        n_s_ij = np.sum(n_s_ij, axis = 1)**(1/2)
        c_i    = n_s_ij / ( p_s_ij  + n_s_ij )
        self.f = np.copy(c_i)
        self.f = np.reshape(self.f , (c_i.shape[0], 1))
        self.f = np.insert(self.f , 0, list(range(1, c_i.shape[0]+1)), axis = 1)
        self.f = self.f [np.argsort(self.f[:, 1])]
        self.f = self.f [::-1]
        if (verbose == True):
            for i in range(0, c_i.shape[0]):
                print('a' + str(i+1) + ': ' + str(round(c_i[i], 2)))
        if ( graph == True):
            self.ranking()
        return c_i
    
    ###############################################################################

    # Function: Generate Ranks. From https://github.com/Valdecy/pyDecision
    def generate_rank_array(self, arr, sorted_indices):
        rank_array = np.zeros(len(arr), dtype = int)
        for rank, index in enumerate(sorted_indices, start = 1):
            rank_array[index] = rank
        return rank_array
    
    # Function: Find Mode
    def find_column_modes(self, matrix):
        transposed_matrix = np.transpose(matrix)
        mode_list         = []
        for column in transposed_matrix:
            counter   = Counter(column)
            max_count = max(counter.values())
            modes     = [x for x, count in counter.items() if count == max_count]
            mode_list.append(modes)
        return mode_list

    # Function: Tranpose Dictionary. From https://github.com/Valdecy/pyDecision
    def transpose_dict(self, rank_count_dict):
        transposed_dict = {}
        list_length     = len(next(iter(rank_count_dict.values())))
        for i in range(list_length):
            transposed_dict[i+1] = [values[i] for values in rank_count_dict.values()]
        return transposed_dict

    # Function: Plot Ranks. Adapted From https://github.com/Valdecy/pyDecision
    def plot_rank_freq(self, size_x = 8, size_y = 10):
        flag_1             = 0
        ranks              = self.ranks_matrix.T
        alternative_labels = [f'a{i+1}' for i in range(ranks.shape[0])]
        rank_count_dict    = {i+1: [0]*ranks.shape[0] for i in range(0, ranks.shape[0])}
        for i in range(0, ranks.shape[0]):
            for j in range(0, ranks.shape[1]):
                rank = int(ranks[i, j])
                rank_count_dict[i+1][rank-1] = rank_count_dict[i+1][rank-1] + 1
        rank_count_dict = self.transpose_dict(rank_count_dict)
        fig, ax         = plt.subplots(figsize = (size_x, size_y))
        try:
          cmap   = colormaps.get_cmap('tab20')
          colors = [cmap(i) for i in np.linspace(0, 1, ranks.shape[0])]
        except:
          colors = plt.cm.get_cmap('tab20', ranks.shape[0])
          flag_1 = 1
        bottom = np.zeros(len(alternative_labels))
        for rank, counts in rank_count_dict.items():
            if (flag_1 == 0):
              bars = ax.barh(alternative_labels, counts, left = bottom, color = colors[rank-1])
            else:
              bars = ax.barh(alternative_labels, counts, left = bottom, color = colors(rank-1))
            bottom = bottom + counts
            for rect, c in zip(bars, counts):
                if (c > 0):
                    width = rect.get_width()
                    ax.text(width/2 + rect.get_x(), rect.get_y() + rect.get_height() / 2, f"r{rank} ({c})", ha = 'center', va = 'center', color = 'black')
        ax.invert_yaxis()
        ax.xaxis.set_major_locator(MaxNLocator(integer = True))
        ax.tick_params(axis = 'y', which = 'both', pad = 25)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Alternative')
        ax.set_title('Rank Frequency per Alternative')
        plt.show()
        return

    # Function: Normalized Weights Box Plot
    def wm_boxplot(self, size_x = 15, size_y = 7):
        plt.figure(figsize = (size_x, size_y))
        df_melted = self.df_w.melt(var_name = 'Columns', value_name = 'Values')
        sns.boxplot(x = 'Columns', y = 'Values', data = df_melted, palette = 'Set3', hue = 'Columns', dodge = False)
        plt.xlabel('Columns')
        plt.ylabel('Values')
        plt.legend([], [], frameon = False)
        plt.show()
        
    # Function: Topsis Box Plot
    def topsis_boxplot(self, size_x = 15, size_y = 7):
        plt.figure(figsize = (size_x, size_y))
        df_melted = self.df_p.melt(var_name = 'Columns', value_name = 'Values')
        sns.boxplot(x = 'Columns', y = 'Values', data = df_melted, palette = 'Set3', hue = 'Columns', dodge = False)
        plt.xlabel('Columns')
        plt.ylabel('Values')
        plt.legend([], [], frameon = False)
        plt.show()

    # Function: EC TOPSIS
    def run(self):
        X                    = np.copy(self.data).astype(float)
        min_indices          = np.where(np.array(self.ctype) == 'min')[0]
        X[:, min_indices]    = 1.0 / X[:, min_indices]
        self.critic_weights  = self.critic_method()
        self.entropy_weights = self.entropy_method()
        self.ranks_matrix    = []
        self.wnorm_matrix    = []
        self.ts_matrix       = []
        self.sol             = []
        lower_upper_pairs    = []
        for i in range(len(self.critic_weights)):
            all_weights = [self.entropy_weights[i], self.critic_weights[i]]
            if (self.cset):
                for custom_set in self.cset:
                    total = sum(custom_set)
                    normalized_set = [x/total for x in custom_set] if total else custom_set
                    if (i < len(custom_set)):
                        all_weights.append(normalized_set[i])
            lower = min(all_weights)
            lower = max(1e-10, lower)
            upper = max(all_weights)
            lower_upper_pairs.append((lower, upper))
        weights_data = []
        weights_data.append(['Entropy'] + [self.entropy_weights[i]  for i in range(len(self.entropy_weights))])
        weights_data.append(['Critic']  + [self.critic_weights[i] for i in range(len(self.critic_weights))])
        if (self.cset):
            count = 1
            for custom_set in self.cset:
                total          = sum(custom_set)
                normalized_set = [x/total for x in custom_set] if total else custom_set
                weights_data.append(['Custom Weights ' + str(count)] + normalized_set)
                count          = count + 1
        lower_weights   = ['Lower'] + [lower for lower, upper in lower_upper_pairs]
        upper_weights   = ['Upper'] + [upper for lower, upper in lower_upper_pairs]
        weights_data.append(lower_weights)
        weights_data.append(upper_weights)
        columns         = ['Weight Name'] + ['g'+str(i+1) for i in range(len(self.critic_weights))]
        self.weights_df = pd.DataFrame(weights_data, columns = columns)
        self.weights_df.set_index('Weight Name', inplace = True)
        for _ in range(self.iter):
            random_weights   = np.array([random.uniform(lower, upper) for lower, upper in lower_upper_pairs])
            self.wnorm_matrix.append(random_weights)
            ts_result        = self.topsis_method(random_weights)
            self.ts_matrix.append(ts_result)
            ranks            = np.argsort(ts_result)[::-1]
            ranks            = self.generate_rank_array(ts_result, ranks)
            self.ranks_matrix.append(ranks)
        self.wnorm_matrix = np.array(self.wnorm_matrix)
        self.ranks_matrix = np.array(self.ranks_matrix)
        self.ts_matrix    = np.array(self.ts_matrix)
        self.sol_m        = self.find_column_modes(self.ranks_matrix)
        ts_sum            = np.sum(self.ts_matrix, axis = 0)
        ts_rank           = np.argsort(ts_sum)[::-1]
        ts_rank           = self.generate_rank_array(ts_sum, ts_rank)
        self.sol          = [ [item] for item in ts_rank]
        self.df_w         = pd.DataFrame(self.wnorm_matrix, columns = [f'g{i+1}' for i in range(self.wnorm_matrix.shape[1])], index = [f'Iteration {i+1}' for i in range(self.wnorm_matrix.shape[0])])
        self.df_r         = pd.DataFrame(self.ranks_matrix, columns = [f'a{i+1}' for i in range(self.ranks_matrix.shape[1])], index = [f'Iteration {i+1}' for i in range(self.ranks_matrix.shape[0])])
        self.df_p         = pd.DataFrame(self.ts_matrix, columns = [f'a{i+1}' for i in range(self.ts_matrix.shape[1])],       index = [f'Iteration {i+1}' for i in range(self.ts_matrix.shape[0])])
        return

###############################################################################
