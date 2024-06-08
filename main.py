import pandas as pd
import matplotlib.pyplot as plt

# wget -qO dataset.csv https://surfdrive.surf.nl/files/index.php/s/vxOY3pFjSnP5KoQ/download
df = pd.read_csv('dataset.csv', index_col=0)
# Modify the dataset to add a missing education for the gang member 'Greg'
df.at['Greg', 'HS'] = 1
df.at['HS', 'Greg'] = 1

excitation = {col: df.index[df[col] == 1].to_list() for col in df.columns}

# Dataset column block sizes: instance nodes, gangs, ages, educations,
# marital statuses, occupations, names
column_block_sizes = [27, 2, 3, 3, 3, 3, 27]
inhibition_circular_lists = []
block_start_index = 0
for block_size in column_block_sizes:
    new_circular_list = list(
        df.columns[block_start_index + 1:block_start_index + block_size + 1])
    if len(new_circular_list) != block_size:
        new_circular_list.append(df.columns[-1])
    new_circular_list[-1] = df.columns[block_start_index]
    inhibition_circular_lists += new_circular_list
    block_start_index += block_size

inhibition = dict(zip(df.columns, inhibition_circular_lists))


class IACModel:
    def __init__(self, excitation_adj: dict, inhibition_circ: dict,
                 probe_list: list, p: float = 0.2,
                 E: float = 0.05, I: float = 0.03, M: float = 1.0,
                 m: float = -0.2, D: float = 0.05, R: float = -0.1) -> None:
        if len(probe_list) == 0:
            raise ValueError('The probe list may not be empty.')
        if len(excitation_adj) != len(inhibition_circ):
            raise ValueError('The number of nodes in the inhibition circular '
                             'dictionary must be equal to the number of nodes '
                             'in the excitation adjacency dictionary.')
        if len(excitation_adj) == 0:
            raise ValueError('The model may not be empty.')

        self.excitation_constant = E
        self.inhibition_constant = I
        self.maximum_activation = M
        self.minimum_activation = m
        self.decay = D
        self.resting_value = R
        self.probe_weight = p

        self.excitation_adj = excitation_adj
        self.inhibition_circ = inhibition_circ
        self.activations = {key: m for key in excitation_adj.keys()}  # val < 0
        self.probe_list = probe_list

    def update_activations(self) -> None:
        new_activations = {}
        for node, activation in self.activations.items():
            excitation_sum = sum(self.activations[neighbour]
                                 for neighbour in self.excitation_adj[node]
                                 if self.activations[neighbour] >= 0)

            inhibition_sum = 0
            current_node = self.inhibition_circ[node]
            while current_node != node:
                neighbour_activation = self.activations[current_node]
                if neighbour_activation >= 0:
                    inhibition_sum += neighbour_activation
                current_node = self.inhibition_circ[current_node]

            probe = self.probe_weight if node in self.probe_list else 0

            input = (probe + self.excitation_constant * excitation_sum
                     - self.inhibition_constant * inhibition_sum)

            if input >= 0:
                effect = (self.maximum_activation - activation) * input
            else:
                effect = (activation - self.minimum_activation) * input

            new_activations[node] = (activation + effect - self.decay
                                     * (activation - self.resting_value))
        self.activations = new_activations

    def run(self, steps: int = 500) -> None:
        for _ in range(steps):
            self.update_activations()


# Example probe, as also performed in the original paper
def plot_model_outcome(activations_dict: dict, title: str) -> None:
    fig, ax = plt.subplots()
    ax.bar(activations_dict.keys(), activations_dict.values())
    ax.set(xlabel='Node', ylabel='Activation', title=title)
    plt.xticks(rotation=90)
    plt.show()


jets_model = IACModel(excitation, inhibition, ['Jets'], I=0.04)
jets_model.run()
activations = {key: value for key, value in jets_model.activations.items()
               if key in df.columns[27:]}
plot_model_outcome(activations, 'Property Nodes Activation for Jets Probe')
