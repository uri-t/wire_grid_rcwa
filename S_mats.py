import numpy as np

class S_mats:
   def __init__(self, S11, S12, S21, S22):
       self.S11 = S11
       self.S12 = S12
       self.S21 = S21
       self.S22 = S22

   
       
   def star(mat1, mat2):
      n = np.shape(mat1.S11)[1]
       
      I_mat = np.eye(n)
       
      row1_mat = mat1.S12 @ np.linalg.inv(I_mat - mat2.S11 @ mat1.S22)
      row2_mat = mat2.S21 @ np.linalg.inv(I_mat - mat1.S22 @ mat2.S11)
       
      S11 = mat1.S11 + row1_mat @ mat2.S11 @ mat1.S21
      S12 = row1_mat @ mat2.S12
      S21 = row2_mat @ mat1.S21
      S22 = mat2.S22 + row2_mat @ mat1.S22 @ mat2.S12

      return S_mats(S11 = S11, S12 = S12, S21 = S21, S22 = S22)
