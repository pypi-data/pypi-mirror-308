import numpy as np
import sherbystats as sherby

def dtw_multi(Z_):

    # Multivarié et Multiples séries    

    # Number of batches
    count = 0
    for element in Z_: count += 1
    #print('Number of batches:',count)
    
    # Number of variables
    nb = np.size(Z_[0],1)
    #print('Number of variables:',nb)
    
    
    for i in range(count):
        ref = Z_[0]
        other = Z_[i]
        distance, path = sherby.dtw(ref[:,0],other[:,0])
        path = np.array(path)
        # print('#######')
        # print('i=',i)
        for j in range(1,count):
            other = Z_[j]
            # print('j=',j)
            if j < i:
                ref_w = []
                for k in range(nb):
                    r = ref[:,k][path[:,0]]
                    ref_w.append(r)
                ref_w = (np.array(ref_w))       
                Z_[0] = ref_w.T        
        
                other_w = []
                for k in range(nb):
                    r = other[:,k][path[:,0]]
                    other_w.append(r)
                other_w = (np.array(other_w))       
                Z_[j] = other_w.T 
                
                
    
            elif j == i :
    
                ref_w = []
                for k in range(nb):
                    r = ref[:,k][path[:,0]]
                    ref_w.append(r)
                ref_w = (np.array(ref_w))       
                Z_[0] = ref_w.T  
                
                other_w = []
                for k in range(nb):
                    r = other[:,k][path[:,1]]
                    other_w.append(r)
                other_w = (np.array(other_w))       
                Z_[j] = other_w.T 
    
    
    
                
            else: # do nothing
                Z_[j] = Z_[j]

    return Z_