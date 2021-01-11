import numpy as np

# LSB TO THE RIGHT
# Trail 1 from the original paper
trail_og1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
         [0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,3],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
         [0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,3],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
         [0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,3]]

# Trail 2 from original paper
trail_og2= [[0,0,0,0,0,0,0,0,0,0,0,0,7,0,7,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10],
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 8, 8],
            [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3]]


# LSB TO THE LEFT
# Trail 1 from the Differential cryptanalysis one
trail_diff1 = np.zeros((5,16), dtype=np.int8).tolist()
trail_diff1[0][0] = 4
trail_diff1[0][3] = 4
trail_diff1[1][0] = 9
trail_diff1[1][8] = 9
trail_diff1[2][8] = 1
trail_diff1[2][10] = 1
trail_diff1[3][2] = 5
trail_diff1[3][14] = 5
trail_diff1[4][0] = 4
trail_diff1[4][3] = 4

# Trail 2 from the Differential cryptanalysis one
trail_diff2 = np.zeros((15,16), dtype=np.int8).tolist()
trail_diff2[0][2] = 7
trail_diff2[0][14] = 7
trail_diff2[1][0] = 4
trail_diff2[1][3] = 4
trail_diff2[2][0] = 9
trail_diff2[2][8] = 9
trail_diff2[3][8] = 1
trail_diff2[3][10] = 1
trail_diff2[4][2] = 5
trail_diff2[4][14] = 5
trail_diff2[5][0] = 4
trail_diff2[5][3] = 4
trail_diff2[6][0] = 9
trail_diff2[6][8] = 9
trail_diff2[7][8] = 1
trail_diff2[7][10] = 1
trail_diff2[8][2] = 5
trail_diff2[8][14] = 5
trail_diff2[9][0] = 4
trail_diff2[9][3] = 4
trail_diff2[10][0] = 9
trail_diff2[10][8] = 9
trail_diff2[11][8] = 1
trail_diff2[11][10] = 1
trail_diff2[12][2] = 5
trail_diff2[12][14] = 5
trail_diff2[13][0] = 4
trail_diff2[13][3] = 4
trail_diff2[14][0] = 9
trail_diff2[14][8] = 9


# Trail 1 for GIFT, table 5 of the paper
trail_gift1 = [[0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,1,0],
               [0,0,0,0, 0,0,0,10, 0,0,0,0, 0,0,0,10],
               [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,1],
               [0,0,0,10, 0,0,0,0, 0,0,0,10, 0,0,0,0],
               [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,1,0]]

trail_gift2 = [[0,12,0,0, 0,0,0,0, 0,0,6,0, 0,0,0,0],
               [0,0,0,0, 0,0,0,0, 0,0,0,0, 4,0,2,0]]
