import numpy as np
from portpy.photon.data_explorer import DataExplorer
from portpy.photon.influence_matrix import InfluenceMatrix
import json
from copy import deepcopy

class Arcs:
    """
    A class representing beams_dict.

    - **Attributes** ::

        :param arcs_dict: arcs_dict dictionary that contains information about arcs in the format of dict
        dict: {'arcs':
                   'ID': list(int),
                   'gantry_angle': list(float),
                   'collimator_angle': list(float) }
                  }

        :type arcs_dict: dict

    - **Methods** ::

        :get_gantry_angle(beam_id: Optional(int, List[int]):
            Get gantry angle in degrees
        :get_collimator_angle(beam_id):
            Get collimator angle in degrees

    """

    def __init__(self, inf_matrix: InfluenceMatrix, file_name: str = None, data: DataExplorer = None, arcs_dict: dict = None):
        """

        :param file_name: json file containing arcs information
        :data: object of DataExplorer class
        :arcs_dict: dictionary containing arcs information

        """
        if file_name is not None:
            self.arcs_dict = self.load_json(file_name)
        if arcs_dict is not None:
            self.arcs_dict = arcs_dict
        if data is not None:
            metadata = data.load_metadata()
            self.arcs_dict = metadata['arcs']
        self._inf_matrix = inf_matrix
        self.preprocess()

    def load_json(self, arcs_json_file):
        # store in arcs dictionary
        f = open(arcs_json_file)
        arcs_dict = json.load(f)
        f.close()
        return arcs_dict

    def get_max_cols(self):
        max_cols = 0
        arcs = self.arcs_dict['arcs']
        for a, arc in enumerate(arcs):
            for b, beam in enumerate(arc['vmat_opt']):
                max_cols = np.maximum(beam['reduced_2d_grid'].shape[1], max_cols)
        return max_cols

    def preprocess(self):
        arcs_dict = self.arcs_dict
        inf_matrix = self._inf_matrix
        all_cp_ids = inf_matrix.get_all_beam_ids()

        for i, arc in enumerate((arcs_dict['arcs'])):
            cp_ids = arc["control_point_ids"]
            ind_access = [all_cp_ids.index(cp_id) for cp_id in cp_ids]
            beams_list = [deepcopy(inf_matrix.beamlets_dict[ind]) for ind in ind_access]
            arc['vmat_opt'] = beams_list

    def get_initial_leaf_pos(self, initial_leaf_pos='BEV'):
        arcs_dict = self.arcs_dict
        """
        Initialize leaf positions for the scp
        """

        for i, arc in enumerate((arcs_dict['arcs'])):
            beams_list = arc['vmat_opt']
            for j, beam in enumerate(beams_list):
                reduced_2d_grid = self._inf_matrix.get_bev_2d_grid(beam_id=beam['beam_id'])
                reduced_2d_grid = reduced_2d_grid[~np.all(reduced_2d_grid == -1, axis=1), :]  # remove rows which are not in BEV
                beam['reduced_2d_grid'] = reduced_2d_grid
                beam['num_rows'] = reduced_2d_grid.shape[0]
                beam['start_leaf_pair'] = np.amax(beam['MLC_leaf_idx'][0])
                beam['end_leaf_pair'] = np.amin(beam['MLC_leaf_idx'][0])
                beam['num_cols'] = beam['reduced_2d_grid'].shape[1]
                beam['start_beamlet_idx'] = np.unique(np.sort(reduced_2d_grid[reduced_2d_grid >= 0]))[0]
                beam['end_beamlet_idx'] = np.amax(reduced_2d_grid)
                beam['leaf_pos_bev'] = []
                beam['leaf_pos_left'] = []
                beam['leaf_pos_right'] = []
                beam['leaf_pos_f'] = []
                beam['leaf_pos_b'] = []
                for _, row in enumerate(beam['reduced_2d_grid']):
                    if len(row) > 0:
                        if initial_leaf_pos == 'BEV':
                            left_pos, right_pos = np.argwhere(row >= 0)[0][0] - 1, np.argwhere(row >= 0)[-1][0] + 1

                            beam['leaf_pos_bev'].append([left_pos, right_pos])
                            beam['leaf_pos_left'].append(left_pos)
                            beam['leaf_pos_right'].append(right_pos)
                            beam['leaf_pos_f'].append([left_pos, right_pos])
                            beam['leaf_pos_b'].append([left_pos, right_pos])
            arc['num_beams'] = len(arc['vmat_opt'])
            arc['start_beamlet_idx'] = arc['vmat_opt'][0]['start_beamlet_idx']
            arc['end_beamlet_idx'] = arc['vmat_opt'][-1]['end_beamlet_idx']
            arc['total_rows'] = np.sum([arc['vmat_opt'][i]['num_rows'] for i in range(len(arc['vmat_opt']))])
            arc['max_rows'] = np.amax([arc['vmat_opt'][i]['num_rows'] for i in range(len(arc['vmat_opt']))])
            arc['max_cols'] = np.amax([arc['vmat_opt'][i]['num_cols'] for i in range(len(arc['vmat_opt']))])
            arc['start_leaf_pair'] = np.amax(
                [arc['vmat_opt'][i]['start_leaf_pair'] for i in range(len(arc['vmat_opt']))])
            arc['end_leaf_pair'] = np.amin([arc['vmat_opt'][i]['end_leaf_pair'] for i in range(len(arc['vmat_opt']))])

    def gen_interior_and_boundary_beamlets(self, forward_backward: int = 1, step_size_f: int = 8, step_size_b: int = 8):
        """
        Create interior and boundary beamlets based upon step_size and forward backward

        """
        arcs_dict = self.arcs_dict
        for a, arc in enumerate(arcs_dict['arcs']):
            vmat = arc['vmat_opt']
            num_beams = arc['num_beams']

            for b in range(num_beams):
                bound_ind_l = []
                bound_ind_r = []
                int_ind = []

                num_rows = vmat[b]['num_rows']
                num_cols = vmat[b]['num_cols']
                map_ = vmat[b]['reduced_2d_grid']
                bev = vmat[b]['leaf_pos_bev']
                leaf_pos_l = vmat[b]['leaf_pos_left']
                leaf_pos_r = vmat[b]['leaf_pos_right']

                for r in range(num_rows):
                    # moving the left/right leaves forward
                    row = map_[r, :]
                    new_leaf_pos_l = min(leaf_pos_l[r] + step_size_f * forward_backward, leaf_pos_r[r] - 1)
                    new_leaf_pos_r = max(leaf_pos_r[r] - step_size_f * forward_backward, leaf_pos_l[r] + 1)

                    # collision check
                    count = 0
                    while new_leaf_pos_l >= new_leaf_pos_r:
                        if count % 2 == 0:
                            new_leaf_pos_l -= 1
                        else:
                            new_leaf_pos_r += 1
                        count += 1

                    # create boundary indices
                    if leaf_pos_l[r] + 1 <= new_leaf_pos_l:
                        bound_ind_l.append(list(map_[r, leaf_pos_l[r] + 1:new_leaf_pos_l + 1]))
                        # bound_ind_l.append(list(map_[r, leaf_pos_l[r]:new_leaf_pos_l]))
                    else:
                        bound_ind_l.append([])

                    if new_leaf_pos_r <= leaf_pos_r[r] - 1:
                        bound_ind_r.append(list(map_[r, new_leaf_pos_r:leaf_pos_r[r]]))
                    else:
                        bound_ind_r.append([])

                    new_leaf_pos_l = max(leaf_pos_l[r] - step_size_b * (1 - forward_backward), -1)
                    # new_leaf_pos_l = max(leaf_pos_l[r] - step_size_b * (1 - forward_backward), 0)
                    new_leaf_pos_r = min(leaf_pos_r[r] + step_size_b * (1 - forward_backward), num_cols)

                    # beam eye view check
                    new_leaf_pos_l = max(new_leaf_pos_l, bev[r][0])
                    new_leaf_pos_r = min(new_leaf_pos_r, bev[r][1])

                    if new_leaf_pos_l + 1 <= leaf_pos_l[r]:
                        if not bound_ind_l[r]:
                            bound_ind_l[r] = list(map_[r, new_leaf_pos_l + 1:leaf_pos_l[r] + 1])
                        else:
                            bound_ind_l[r].extend(map_[r, new_leaf_pos_l + 1:leaf_pos_l[r] + 1])

                    if leaf_pos_r[r] <= new_leaf_pos_r - 1:
                        if not bound_ind_r[r]:
                            bound_ind_r[r] = list(map_[r, leaf_pos_r[r]:new_leaf_pos_r])
                        else:
                            bound_ind_r[r].extend(map_[r, leaf_pos_r[r]:new_leaf_pos_r])

                    # ind = ~np.isin(map_[r, :][map_[r, :] >= 0], np.union1d(bound_ind_l[r], bound_ind_r[r]))
                    # if any(ind):
                    #     int_ind.extend(map_[r, :][map_[r, :] >= 0][ind])
                    if bound_ind_l[r] and bound_ind_r[r]:
                        if not bound_ind_l[r][-1] + 1 == bound_ind_r[r][0]:
                            min_col = np.where(row == bound_ind_l[r][-1])[0][0] + 1
                            max_col = np.where(row == bound_ind_r[r][0])[0][0]
                            int_ind.extend(map_[r, min_col:max_col])
                    elif bound_ind_l[r]:
                        if not bound_ind_l[r][-1] + 1 == leaf_pos_r[r]:
                            min_col = np.where(row == bound_ind_l[r][-1])[0][0] + 1
                            int_ind.extend(map_[r, min_col:leaf_pos_r[r]])
                    elif bound_ind_r[r]:
                        if not leaf_pos_l[r] + 1 == bound_ind_r[r][0]:
                            max_col = np.where(row == bound_ind_r[r][0])[0][0]
                            int_ind.extend(map_[r, leaf_pos_l[r] + 1: max_col])
                    else:
                        if not leaf_pos_l[r] + 1 == leaf_pos_r[r]:
                            int_ind.extend(map_[r, leaf_pos_l[r] + 1: leaf_pos_r[r]])
                    # if not int_ind:
                    #     int_ind = []
                vmat[b]['bound_ind_left'] = bound_ind_l
                vmat[b]['bound_ind_right'] = bound_ind_r
                vmat[b]['int_ind'] = int_ind

    def calc_actual_from_intermediate_sol(self, sol: dict):

        int_v = sol['int_v']
        bound_v_l = sol['bound_v_l']
        bound_v_r = sol['bound_v_r']
        arcs = self.arcs_dict['arcs']

        beam_so_far = 0
        beamlet_so_far = 0
        count = 0
        w_beamlet = []
        # calculate intermediate solution for interior and boundary beamlets
        for a, arc in enumerate(arcs):
            num_beams = arc['num_beams']
            num_beamlets = arc['end_beamlet_idx'] - arc['start_beamlet_idx'] + 1
            w_beamlet.append(np.zeros(num_beamlets))

            for b, beam in enumerate(arc['vmat_opt']):
                beam['bound_v_l'] = []
                beam['bound_v_r'] = []
                beam['int_v'] = int_v[beam_so_far + b]

                if beam['int_ind']:
                    w_beamlet[a][np.array(beam['int_ind']) - beamlet_so_far] = beam['int_v']

                for r in range(beam['num_rows']):
                    beam['bound_v_l'].append(bound_v_l[count])
                    if beam['bound_ind_left'][r]:
                        w_beamlet[a][np.array(beam['bound_ind_left'][r]) - beamlet_so_far] = beam['bound_v_l'][r]

                    beam['bound_v_r'].append(bound_v_r[count])
                    if beam['bound_ind_right'][r]:
                        w_beamlet[a][np.array(beam['bound_ind_right'][r]) - beamlet_so_far] = beam['bound_v_r'][r]
                    count += 1

            beam_so_far += num_beams
            beamlet_so_far += num_beamlets
            arcs[a]['w_beamlet'] = w_beamlet[a]
        self.calculate_beamlet_value()
        self.intermediate_to_actual()
        # self.update_beamlets_weights()  # first and 2nd beam weights adjustment
        self._get_leaf_pos_in_beamlet(sol=sol)

    def update_leaf_pos(self, forward_backward: int, update_reference_leaf_pos: bool = True):
        if update_reference_leaf_pos:
            self._update_reference_leaf_pos()

        for arc in self.arcs_dict['arcs']:

            for beam in arc['vmat_opt']:
                for r in range(beam['num_rows']):
                    beam['leaf_pos_left'][r] = beam['leaf_pos_f'][r][0] * forward_backward + beam['leaf_pos_b'][r][
                        0] * (1 - forward_backward)
                    beam['leaf_pos_right'][r] = beam['leaf_pos_f'][r][1] * forward_backward + beam['leaf_pos_b'][r][
                        1] * (1 - forward_backward)

    def update_best_solution(self):
        arcs = self.arcs_dict['arcs']
        for a, arc in enumerate(arcs):
            for b, beam in enumerate(arc['vmat_opt']):
                beam['best_beam_weight'] = beam['int_v']
                beam['best_leaf_position_in_cm'] = beam['cont_leaf_pos_in_beamlet']*self._inf_matrix.beamlet_width_mm/10
            arc['best_w_beamlet_act'] = arc['w_beamlet_act']

    def calculate_beamlet_value(self):
        # calculates the beamlet values between (0-1)
        arcs = self.arcs_dict['arcs']
        num_beamlets_so_far = 0

        for a, arc in enumerate(arcs):
            w_beamlet = arc['w_beamlet']
            num_beamlets = arc['end_beamlet_idx'] - arc['start_beamlet_idx'] + 1

            for b, beam in enumerate(arc['vmat_opt']):
                beam['intermediate_sol'] = np.zeros_like(beam['reduced_2d_grid'], dtype=float)

                for i in range(beam['start_beamlet_idx'], beam['end_beamlet_idx'] + 1):
                    row, col = np.where(beam['reduced_2d_grid'] == i)
                    if beam['int_v'] > 0:
                        beam['intermediate_sol'][row, col] = min(1, w_beamlet[i - num_beamlets_so_far] / beam['int_v'])
                    else:
                        beam['intermediate_sol'][row, col] = 0

            num_beamlets_so_far += num_beamlets

        return arcs

    def calculate_dose(self, inf_matrix: InfluenceMatrix, sol: dict, vmat_params: dict, best_plan: bool = False):
        A = inf_matrix.A
        arcs = self.arcs_dict['arcs']
        adj1 = vmat_params['second_beam_adj']
        adj0 = vmat_params['first_beam_adj']
        # adj2 = vmat_params['last_beam_adj']

        if best_plan:
            sol['best_act_dose_v'] = np.zeros(A.shape[0])
        else:
            sol['act_dose_v'] = np.zeros(A.shape[0])
            sol['int_dose_v'] = np.zeros(A.shape[0])
            sol['optimal_intensity'] = np.zeros(A.shape[1])

        beamlet_so_far = 0
        for arc in arcs:
            from_ = arc['start_beamlet_idx']
            to_ = arc['end_beamlet_idx']

            num_beamlets = to_ - from_ + 1
            adjust_beamlets_weight = np.ones(num_beamlets)

            # adjust 1st beam
            from_0 = arc['vmat_opt'][0]['start_beamlet_idx']
            to_0 = arc['vmat_opt'][0]['end_beamlet_idx']
            adjust_beamlets_weight[from_0 - beamlet_so_far: to_0 - beamlet_so_far + 1] = adj0

            # adjust beamlets weight of 2nd beam
            from_1 = arc['vmat_opt'][1]['start_beamlet_idx']
            to_1 = arc['vmat_opt'][1]['end_beamlet_idx']

            adjust_beamlets_weight[from_1-beamlet_so_far: to_1-beamlet_so_far + 1] = adj1
            if best_plan:
                sol['best_act_dose_v'] += A[:, from_:to_ + 1] @ (arc['best_w_beamlet_act'] * adjust_beamlets_weight)
            else:
                sol['act_dose_v'] += A[:, from_:to_ + 1] @ (arc['w_beamlet_act']*adjust_beamlets_weight)
                sol['int_dose_v'] += A[:, from_:to_ + 1] @ (arc['w_beamlet']*adjust_beamlets_weight)
                sol['optimal_intensity'][from_:to_+1] = arc['w_beamlet_act']*adjust_beamlets_weight
            beamlet_so_far = beamlet_so_far + num_beamlets

        return sol

    def intermediate_to_actual(self):
        arcs = self.arcs_dict['arcs']
        beamlet_so_far = 0
        # Convert intermediate solution to actual feasible solution
        for a, arc in enumerate(arcs):
            num_beams = arc['num_beams']
            num_beamlets = arc['end_beamlet_idx'] - arc['start_beamlet_idx'] + 1
            w_beamlet_act = np.zeros(num_beamlets)

            for b, beam in enumerate(arc['vmat_opt']):
                num_rows = beam['num_rows']
                num_cols = beam['num_cols']
                reduced_2d_grid = beam['reduced_2d_grid']
                int_sol = beam['intermediate_sol']
                act_solution = np.zeros((num_rows, num_cols))

                for r in range(num_rows):
                    row = int_sol[r, :]
                    fractional_indices = (row > 0.0) & (row < 1.0)
                    signal = True
                    if np.sum(fractional_indices) <= 1:
                        act_solution[r, :] = row
                        signal = False
                    elif np.sum(fractional_indices) == 2:
                        col = np.where(fractional_indices)[0]
                        if col[1] - col[0] > 1:
                            act_solution[r, :] = row
                            signal = False

                    if signal:
                        act_solution[r, :] = row
                        if beam['bound_ind_left'][r]:
                            bound_ind = beam['bound_ind_left'][r]
                            col = np.where(np.isin(reduced_2d_grid[r, :], bound_ind))[0]
                            sum_boundary = np.sum(row[col])
                            count = 0
                            while np.floor(sum_boundary) >= 1:
                                c = col[-1] - count
                                act_solution[r, c] = 1
                                sum_boundary -= 1
                                count += 1
                            if sum_boundary > 0:
                                act_solution[r, col[-1] - count] = sum_boundary
                            if col[0] <= col[-1] - count - 1:
                                act_solution[r, col[0]: col[-1] - count] = 0
                        if beam['bound_ind_right'][r]:
                            bound_ind = beam['bound_ind_right'][r]
                            col = np.where(np.isin(reduced_2d_grid[r, :], bound_ind))[0]
                            sum_boundary = np.sum(row[col])
                            count = 0
                            while np.floor(sum_boundary) >= 1:
                                c = col[0] + count
                                act_solution[r, c] = 1
                                sum_boundary -= 1
                                count += 1
                            if sum_boundary > 0:
                                act_solution[r, col[0] + count] = sum_boundary
                            if col[0] + count + 1 <= col[-1]:
                                act_solution[r, col[0] + count + 1: col[-1]+1] = 0
                    for c in range(num_cols):
                        if reduced_2d_grid[r, c] > 0:
                            w_beamlet_act[reduced_2d_grid[r, c] - beamlet_so_far] = act_solution[r, c] * beam['int_v']

                beam['actual_sol'] = act_solution

            arc['w_beamlet_act'] = w_beamlet_act
            beamlet_so_far = beamlet_so_far + num_beamlets

    def _update_reference_leaf_pos(self):
        arcs = self.arcs_dict['arcs']
        for arc in arcs:

            for b, beam in enumerate(arc['vmat_opt']):
                int_sol = beam['intermediate_sol']
                reduced_2d_grid = beam['reduced_2d_grid']

                for r in range(beam['num_rows']):
                    if beam['bound_ind_left'][r]:
                        bound_ind = beam['bound_ind_left'][r]
                        col = np.where(np.isin(reduced_2d_grid[r, :], bound_ind))[0]
                        beam['leaf_pos_b'][r][0] = max(col) - int(sum(int_sol[r, col]))
                        beam['leaf_pos_f'][r][0] = max(col) - int(np.ceil(sum(int_sol[r, col])))
                    else:
                        beam['leaf_pos_b'][r][0] = beam['leaf_pos_left'][r]
                        beam['leaf_pos_f'][r][0] = beam['leaf_pos_left'][r]

                    if beam['bound_ind_right'][r]:
                        bound_ind = beam['bound_ind_right'][r]
                        col = np.where(np.isin(reduced_2d_grid[r, :], bound_ind))[0]
                        beam['leaf_pos_b'][r][1] = min(col) + int(sum(int_sol[r, col]))
                        beam['leaf_pos_f'][r][1] = min(col) + int(np.ceil(sum(int_sol[r, col])))
                    else:
                        beam['leaf_pos_b'][r][1] = beam['leaf_pos_right'][r]
                        beam['leaf_pos_f'][r][1] = beam['leaf_pos_right'][r]

    def _get_leaf_pos_in_beamlet(self, sol):
        arcs = self.arcs_dict['arcs']
        leaf_pos_mu_l = sol['leaf_pos_mu_l']
        leaf_pos_mu_r = sol['leaf_pos_mu_r']
        count = 0
        beam_so_far = 0
        for a, arc in enumerate(arcs):
            for b, beam in enumerate(arc['vmat_opt']):
                num_rows = beam['num_rows']
                beam_mu = sol['int_v'][beam_so_far + b]
                beam['cont_leaf_pos_in_beamlet'] = np.zeros((num_rows, 2))
                for r in range(num_rows):
                    beam['cont_leaf_pos_in_beamlet'][r, 0] = leaf_pos_mu_l[count] / (beam_mu + 0.000000000001)
                    beam['cont_leaf_pos_in_beamlet'][r, 1] = leaf_pos_mu_r[count] / (beam_mu + 0.000000000001)
                    count = count + 1
            beam_so_far += arc['num_beams']
